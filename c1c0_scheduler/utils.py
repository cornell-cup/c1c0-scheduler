import sys
import re
import socket

from c1c0_scheduler import config

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Iterable

def gen_msg(mod: str, *args: 'Iterable[str]') -> str:
    """
    Generates msgs to be sent over the socket for the scheduler.
    """
    return config.CHAR_SEP.join(
        [config.MSG_PLACEHOLDER]*(len(args)+1)
    ).format(mod, *args) + config.MSG_SEP


def decode_msg(msg) -> 'Iterable[str]':
    """
    Decodes messages that were sent over a socket for the scheduler.
    """
    try:
        return list(re.findall(config.MSG_REGEX, msg)[0])
    except IndexError:
        return list()

# For pre-python3.8
try:
    major, minor, micro, releaselevel, serial = sys.version_info
    if major==3 and minor>=8:
        from socket import create_server
    else:
        raise ValueError
except ValueError:
    def create_server(address, family=config.AF, kind=config.SOCK_KIND) -> socket.socket:
        
        major, minor, micro, releaselevel, serial = sys.version_info
        if major==3 and minor>=8:
            sock = socket.create_server(family, kind, reuse_port=True)
        else:
            sock = socket.socket(family, kind)
            # See: https://stackoverflow.com/questions/44387712/python-sockets-how-to-shut-down-the-server
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(address)
        return sock
