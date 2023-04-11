"""
Scheduling API for C1C0

Rewritten 4/10/23 by Chris De Jesus

Purposes of the API:

"""
import socket
import re

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Iterable, Tuple

from c1c0_scheduler import config, exceptions

# class ProcessType(Enum):
#     """
#     The various modules being worked on by the CUP team, this is the scheduler's internal lookup table for module names.
#     """
#     CHATBOT = 'chatbot'
#     PATH_PLANNING = 'path-planning'
#     OBJECT_DETECTION = 'object-detection'
#     FACIAL_RECOGNITION = 'facial-recognition'



def gen_msg(mod: str, *args: 'Iterable[str]') -> str:
    """
    Generates msgs sent over socket
    """
    return config.CHAR_SEP.join('%s'*(len(args)+1)).format(mod, *args) + config.MSG_SEP


def decode_msg(msg):
    return list(re.findall(config.MSG_REGEX, msg)[0])

class Client:
    """
    The universal C1C0 client, allowing the modules to communicate runtime info back to the scheduler.
    """
    encoding = 'utf-8'
    RECV_SIZE = 32

    def __init__(self, process_name: str, host: 'Optional[str]', port: 'Optional[int]'):
        """
        Parameter: process_type
        Invariant: process_type is a string in ["path-planning", "object-detection", "locomotion"]
        """
        self.sock = socket.socket(config.AF, config.SOCK_TYPE)

        self.process_name: str = process_name
        self.host = config.HOST if host is None else host
        self.port = config.PORT if port is None else port
        self.connected = False

    def communicate(self, *payload):
        try:
            self.sock.send(gen_msg(self.process_name, *payload).encode(self.encoding))
            resp = self.sock.recv(64).decode(self.encoding)
            # print(resp)
        except socket.error:
            raise exceptions.DisconnectedClient(self.process_name)
        return resp


    def _echo_check(self, val, n=config.CONNECTION_RETRIES):
        """
        Notifies the scheduler of a status change with the expectation it will be echoed.

        See server equivalent [not yet implemented]
        """
        resp = self.communicate(decode_msg(resp))
        try:
            sender, datum, *opt = decode_msg(resp)
            return sender == self.process_name and datum == val
        except ValueError as e:
            raise exceptions.DisconnectedClient() from e

    def connect(self, host_port: 'Tuple[str, int]' = None):
        """
        Connects the client to the server on the host/port combination given by
        (self.host, self.port).
        """
        host_port = (self.host, self.port) if host_port is None else host_port
        self.host, self.port = host_port
        
        # connect
        try:
            self.sock.connect(host_port)
        except socket.error as e:
            raise exceptions.DisconnectedClient(self.process_name) from e

        attempt = 0
        while not self.connected:
            if self._echo_check('initialized'):
                break
            attempt += 1
        self.connected = True

    def close(self):
        if not self._echo_check('disconnected'):
            raise exceptions.DisconnectedClient(self.process_name)
        self.sock.close()
        # print("closed connection")
    
    

