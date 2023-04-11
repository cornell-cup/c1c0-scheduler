import sys
import logging
import threading
import socket
import subprocess
from contextlib import contextmanager
import time

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Callable

from c1c0_scheduler.client import gen_msg, decode_msg
from c1c0_scheduler import exceptions, config

logger = logging.getLogger(__name__)


# Remove this line when we can, this is a hold-over from years ago from Locomotion.
sys.path.append('~/Desktop/c1c0-modules/c1c0-movement/c1c0-movement/Locomotion') #Relative to THIS directory (multithreading)

# Robo "APIs"
# import locomotion_API
# import arm_API
# from xboxcontrol_API import xboxcontroller
# import HeadRotation_XBox_API as headrotation

# NOTE: To ECEs
# The original had too many issues (if you would like I could compile a list!)
# As a result, I had already been working a (second) rewrite using the same systems the old version used,
# which means it should hopefully not take too much time to get used to. I will be writing up detailed
# documentation over the coming days, but this should hopefully solve a lot of problems we have been
# having.



class ThreadedSocket(threading.Thread):
    """
    The primary ThreadedClient to be used BY the scheduler (as opposed to by the modules)
    """
    ENCODING = config.ENCODING
    BUFFER_SIZE = config.BUFFER_SIZE
    MODULES = config.MODULES

    clients = {}
    server_socket: 'socket.socket' = socket.create_server((config.HOST, config.PORT))
    
    new_conn = threading.Condition()

    def __init__(self, name: str, processor: 'Optional[Callable]' = None,
                 autoconnect: bool = False, host=config.HOST, port=config.PORT, *args, **kwargs):
        self._name = name
        self.processor: 'Optional[Callable]' = lambda *_, **__: None if processor is None else processor
        self.host, self.port = host, port
        self.args, self.kwargs = args, kwargs
        self.connected = False
        self.buffer = ''

        super().__init__(*args, **kwargs)
        if autoconnect:
            self.reconnect()


    def run(self):
        """
        Starts the thread. Reads data from the socket into the buffer to bring it into scheduler context.
        """

        # Ensure connected
        if not self.connected:
            raise exceptions.DisconnectedClient(self.name)
        # Read data into synced buffer
        data = self.sock.recv(self.BUFFER_SIZE).decode(self.ENCODING)
        print(f'Received: `{data}`.')

        self.buffer = self.processor(data)

    
    @property
    def name(self):
        """
        The name of this data stream.
        """
        return self._name
    
    @name.setter
    def name(self, name_):
        """
        A property in case we need to do anything else when we set name.

        PARAMETERS
        ----------
        name_
            Set's the client's name to `name_`.
        """
        self._name = name_


    @classmethod
    def _accept(cls: 'ThreadedSocket'):
        """
        Accepts new connections in accordance to system expectations
        """
        while True:
            sock, addr = cls.server_socket.accept()
            resp = sock.recv(cls.BUFFER_SIZE).decode(cls.ENCODING)
            mod, *payload = decode_msg(resp)
            
            

    
    @classmethod
    @contextmanager
    def ctx(cls):
        """
        Initialized the threaded client listener thread, which is responsible for accepting new connections.
        """
        cls.server_socket.listen()
        try:
            yield
        finally:
            cls.server_socket.close()

    def communicate(self, *payload):
        try:
            self.sock.send(gen_msg(self.name, *payload).encode(config.ENCODING))
            resp = self.sock.recv(64).decode(config.ENCODING)
            # print(resp)
        except socket.error:
            raise exceptions.DisconnectedClient(self.name)
        return resp

    def reconnect(self, force: bool = False):
        """
        Reconnects the current thread and renotifies the scheduler of the reconnection.

        PARAMETERS
        ----------
        force
            Forces the client to reconnect

        """
        if self.connected and not force:
            # log anomaly
            return
        self.sock, self.addr = ThreadedSocket.server_socket.accept()
        self.sock.send(gen_msg(self.name, 'connected').encode(ThreadedSocket.ENCODING))
        with ThreadedSocket.meta_mutex:
            ThreadedSocket.clients_connected += 1
print('Waiting for a Connection..')

# testing
# def send_external_msg(mod, *args):
#     with socket.socket(AF, SOCK_TYPE) as sock:
#         sock.connect((HOST, PORT))
#         msg = gen_sock_msg(mod, *args)
#         print(f'Main sending: `{msg}`')
#         sock.sendall(msg.encode(ENCODING))


class Subsystem:
    def __init__(self, name, mod_data):
        self._name = name
        self.client = ThreadedSocket(name)
        self.process_handle = subprocess.Popen(mod_data['cmd'], shell=True)

    def start(self, force=False):
        # NOTE: We are not using subprocess.Popen.communicate as pipes a unidirectional.
        self.client.reconnect(force=force)

    def stop(self):
        self.client.cl
        self.process_handle.communicate()

    def __enter__(self):
        self.start()

    def __exit__(self, *exc_data):
        self.stop()

    def communicate(self, *payload):
        pass

with ThreadedSocket.ctx():
    # Created facial client
    chatbot = ThreadedSocket('chatbot', print, start=True)
    facial_client = ThreadedSocket('facial-recognition', print, start=True)
    obj_client = ThreadedSocket('object-detection', print, start=True)
    path_client = ThreadedSocket('path-planning', print, start=True)

    # testing
    # send_external_msg('facial_detection')
    # send_external_msg('obj_client')
    # send_external_msg('path_planning')

    time.sleep(2)

