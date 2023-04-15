import sys
import logging
import threading
import socket
import subprocess
from contextlib import contextmanager
import time

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Callable, Tuple, Union, Mapping, List, MutableMapping

from c1c0_scheduler import exceptions, config, utils

logger = logging.getLogger(__name__)
logger.setLevel(config.LOG_LEVEL)
logger.addHandler(config.STREAM_HANDLER)


# Remove this line when we can, this is a hold-over from years ago from Locomotion.
sys.path.append('~/Desktop/c1c0-modules/c1c0-movement/c1c0-movement/Locomotion') #Relative to THIS directory (multithreading)

# Robo "APIs"
# import locomotion_API
# import arm_API
# from xboxcontrol_API import xboxcontroller
# import HeadRotation_XBox_API as headrotation

class System:
    debug = config.DEBUG

    def __init__(self, name):
        self._name = name

    @property
    def name(self) -> str:
        """
        The name of this system.
        """
        return self._name
    
    @name.setter
    def name(self, name_) -> None:
        """
        A property in case we need to do anything else when we set name.

        PARAMETERS
        ----------
        name_
            Set's the client's name to `name_`.
        """
        self._name = name_



def default_read(subsystem: 'Subsystem', *args, **kwargs):
    """
    
    """
    print(f'Server waiting for data from: {subsystem.name}')
    # Example usage
    print(subsystem.name)
    data = subsystem.communicate(send=False, recv=True)
    while data:
        mod_name, *payload = data
        print(f' Server subsystem {subsystem.name} received the msg: {[mod_name, *payload]}')
        if mod_name != subsystem.name:
            logger.warning(f'Received data for another module.')
        if not payload:
            continue
        
        # temp
        subsystem.buffer += config.MSG_SEP + config.PAYLOAD_SEP.join(payload)
        data = subsystem.communicate(send=False, recv=True)

class Subsystem(System):

    # CLASS-INSTANCE FUNCTIONALIY
    # #############################

    encoding = config.ENCODING
    buffer_size = config.BUFFER_SIZE
    modules_data = config.SUBSYSTEMS
    debug = config.DEBUG
    timeout = config.CONNECTION_THREAD_TIMEOUT
    conn_retries = config.CONNECTION_RETRIES

    @classmethod
    def _accept(cls: 'Subsystem', *args, **kwargs):
        print(f'accept got {args}, {kwargs}')
        """
        Accepts new connections in accordance to system expectations
        """
        while True:
            sock, addr = cls.server_socket.accept()
            resp = sock.recv(cls.buffer_size).decode(cls.encoding)
            try:
                mod, *payload = utils.decode_msg(resp)
            except ValueError:
                logger.error(f'Accepted a socket but received no data. sock={sock} addr={addr}')
            cls.headless_clients.update({
                mod: {
                'sock': sock,
                'addr': addr,
                'init_payload': payload
                }
            })

    @classmethod
    @contextmanager
    def ctx(cls):
        """
        Initialized the threaded client listener thread, which is responsible for accepting new connections.
        """
        cls.server_socket.listen()
        cls.server_thread.start()
        try:
            yield
        finally:
            cls.server_socket.shutdown(socket.SHUT_RDWR)
            cls.server_thread.join(cls.timeout)
            cls.server_socket.close()

    server_socket: 'socket.socket' = utils.create_server((config.HOST, config.PORT))
    server_thread: 'threading.Thread'
    headless_clients: 'MutableMapping[str, Mapping[str, Union[socket.socket, str, bytes, List[str]]]]' = {}

    # INSTANCE FUNCTIONALITY
    # ##############################

    def __init__(self, name: str, read_func: 'Callable' = default_read, 
                 host=config.HOST, port=config.PORT, *args, **kwargs):
        """
        PARAMETERS
        ----------
        
        name
            The name of this subsystem, used both to identify and display.

        read_func
            The method used to collect data from the socket. This is passed as the target to the client-thread.

        host
            The host IP for the socket server.
        
        port
            The host port for the socket server.
        
        args
            Additional args to be passed to the thread-client.
        
        kwargs
            Additional kwargs to be passed to the thread-client.

        """
        super().__init__(name)
        self.host, self.port = host, port
        self.args, self.kwargs = args, kwargs
        self.connected = False
        self.buffer = ''
        
        self.read_func: 'Callable' = read_func
        self.data_thread = None
        self.process_handle = None
        
        self.mod_data : 'Optional[Mapping[str, Mapping[str, Union[socket.socket, str, bytes, List[str]]]]]' = None
        self.sock: 'Optional[socket.socket]' = None
        self.addr: 'Optional[Union[str, bytes]]' = None

            
    def reconnect(self, force: bool = False):
        """
        Reconnects the current thread and renotifies the scheduler of the reconnection.

        PRECONDITIONS
        -------------
        Within `Subsystem.ctx`, and that a single instance with this `name` was created.

        PARAMETERS
        ----------
        force
            Forces the client to reconnect

        RAISES
        ------
        exceptions.DisconnectedClient(name)
            Raised when unable to find a connection in Subsystem.headless_clients.

        """
        if self.connected and not force:
            logger.warning(f'{self.name} attempted to reconnect while connected.'
                           f'Continuing without reconnecting, please set force=True to force a reconnect.')
            return
        
        counter = 0
        try:
            while not self.headless_clients or self.name not in self.headless_clients:
                print(f'current headless clients: {self.headless_clients}')
                if counter > self.conn_retries:
                    logger.error(f'Failed to establish connections for {self.name}, no incoming connections!')
                    raise exceptions.DisconnectedClient(self.name)
                logger.info(f'Waiting for headless clients to connect to...')
                time.sleep(self.timeout)
                counter += 1
        except Exception as e:
            print('Got unexpected error:', type(e))
            logger.error(e)
            raise exceptions.DisconnectedClient(self.name) from e
        
        # NOTE: Dictionary method calls (that are atomic operations) are thread-safe.
        self.mod_data = self.headless_clients.pop(self.name)
        self.sock, self.addr = self.mod_data['sock'], self.mod_data['addr']
        self.data_thread = threading.Thread(target=self.read_func, args=(self, *self.args), kwargs=self.kwargs, daemon=True)
        logger.debug(f'Got init_payload={self.mod_data["init_payload"]} from {self.name}')
        
        # self.sock, self.addr = self.server_socket.accept()
        msg = utils.gen_msg(self.name, 'initialized').encode(self.encoding)
        print(f'Sending {msg} to client.')
        self.sock.send(msg)
        self.connected = True

    def start(self, force_reconnect:bool = False):
        """
        Starts the `Subsystem` instance, starting the process and listener thread.
        
        PRECONDITIONS
        -------------

        """

        # NOTE: We are not using subprocess.Popen.communicate as pipes a unidirectional.
        # TODO: Remove `shell=True` when possible, it is considered insecure.
    
        # Start process
        self.process_handle = subprocess.Popen(config.SUBSYSTEMS[self.name]['cmd'], shell=True)
        logger.info(f'{self.name} process started.')

        if not self.connected or force_reconnect:
            self.reconnect()

        # Setup socket connection
        self.data_thread.start()
        logger.info(f'{self.name} client-thread started.')

    def stop(self, close_sig=None, force=True):
        """
        Stops the indicated subsystem, cleaning up some used resources.

        close_sig
            The data communicated to the process just before shutting it down.
            None by default.
        """
        # NOTE: The objects that need closing are:
        # - self.process_handle
        # - self.sock
        # - self.conn_thread

        # Notify process of imminent demise.
        stdout, stderr = None, None
        try:
            if force:
                logger.info(f'Forcely stopping {self.name}.')
                self.process_handle.kill()
            stdout, stderr = self.process_handle.communicate(input=close_sig, timeout=self.timeout)
            logger.info(f'{self.name} gracefully stopping, client-thread outputted: {stdout}')
            if stderr:
                logger.error(f'{self.name} raised errors: {stderr}')
        except subprocess.TimeoutExpired:
            # Force kill
            logger.warning(f'Timeout expired while attempting to gracefully close {self.name}. Killing it.')
            self.process_handle.kill()
            stdout_, stderr_ = self.process_handle.communicate()
            # Attempt to salvage output (we do not currently use these, but nice to have)
            stdout = stdout_ if stdout is None else stdout
            stderr = stderr_ if stderr is None else stderr
            logger.info(f'{self.name} killed violently, client-thread outputted: {stdout}')
            if stderr:
                logger.error(f'{self.name} raised errors: {stderr}')
        
        self.sock.shutdown(socket.SHUT_RDWR)
        # NOTE: We don't close the socket client in case we want to start() again.
        self.data_thread.join(timeout=self.timeout)

        logger.debug(f'{self.name} stopped.')

    def __enter__(self):
        self.start()

    def __exit__(self, *exc_data):
        self.stop()
        self.sock.close()



    def communicate(self, *payload, send:bool = True, recv:bool = False):
        """
        Scheduler side communication with the subsystem (module).

        PARAMETERS
        ----------
        recv
            Whether a response is expected from the socket.
        payload
            The data sent to the module.
        """
        # TODO: Refactor to use sock.recv_into
        try:
            if send:
                self.sock.send(utils.gen_msg(self.name, *payload).encode(self.encoding))
            if recv:
                data = self.sock.recv(self.buffer_size)
                print(data)
                return utils.decode_msg(self.sock.recv(self.buffer_size, ).decode(self.encoding))
            # print(resp)
        except socket.error:
            raise exceptions.DisconnectedClient(self.name)


Subsystem.server_thread = threading.Thread(target=Subsystem._accept, daemon=False)

# Used for chatbot and other locally bound systems
# class HierarchalControlSystem(System):
# Temporary demo fix
class HierarchicalControlSystem(Subsystem):
    """
    A system that has higher priority than other subsystems.
    Individual instances form a hierarchical control system.
    """

    control_mutex = threading.Lock()
    groups = []
    holding_group = None

    modules_data = config.CONTROL_SYSTEMS

    # def __init__(self, name, group = 0, timeout = 1.0):
    # temp
    def __init__(self, name, group = 0, timeout = 1.0, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self._group = group
        self.timeout = timeout
        HierarchicalControlSystem.groups.append(self)
    
    @property
    def group(self):
        return self._group
    
    @group.setter
    def group(self, group_):
        self._group = group_
    
    def __enter__(self):
        # temp demo fix
        super().__enter__()

        self.control_mutex.acquire(True, )
        HierarchicalControlSystem.holding_group = self.group
    
    def __exit__(self, *exc_data):
        # temp demo fix
        super().__exit__(*exc_data)

        self.control_mutex.release()


def spawn_subsystem():
    return Subsystem()

def default_control_read(control_sys: HierarchicalControlSystem, *args, **kwargs):
    print(f'Server waiting for data from: {control_sys.name}')
    # Example usage
    mod_name, *payload = control_sys.communicate(send=False, recv=True)
    print(f' Server subsystem {control_sys.name} received the msg: {[mod_name, *payload]}')
    if mod_name != control_sys.name:
        logger.warning(f'Received data for another module.')
    if not payload:
        return
    
    try:
        cmd, *payload = payload

    except ValueError:
        return

