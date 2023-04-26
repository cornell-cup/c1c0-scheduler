import socket
import logging
import sys

# UNIVERSAL SCHEDULER DEVELOPMENT/PRODUCTION MODE SWITCH
DEBUG = True

HOST = '127.0.0.1'
# HOST = '192.168.4.127'
PORT = 1233
ENCODING = 'utf-8'

AF = socket.AF_INET
SOCK_KIND = socket.SOCK_STREAM
BUFFER_SIZE = 1024

CONNECTION_RETRIES = 3
CONNECTION_THREAD_TIMEOUT = 2.0
IGNORE_NONFATAL = DEBUG

FILE_HANDLER = logging.FileHandler('output.log', encoding=ENCODING)
STREAM_HANDLER = logging.StreamHandler(sys.stdout if DEBUG else sys.stderr)
LOG_LEVEL = logging.DEBUG if DEBUG else logging.WARNING

# TODO: Refactor to be of type Mapping[str, str] if no other data is needed
#  See server.Subsystem.start for usage.
SUBSYSTEMS = {
    'facial-recognition': {
        # Temp
        'cmd': 'venv/bin/python client_test.py --mod="facial-recognition"'
    },
    'path-planning': {
        'cmd': 'venv/bin/python client_test.py --mod="path-planning"'
    },
    'object-detection': {
        'cmd': 'venv/bin/python client_test.py --mod="object-detection"'
    },
}

CONTROL_SYSTEMS = {
    'chatbot': {

    },
    'xbox-controller': {

    }
}

PAYLOAD_SEP = ':'
MSG_SEP = ';'
MSG_PLACEHOLDER = '{}'
MSG_REGEX = f'([\w-]+){PAYLOAD_SEP}([\w\d]+){MSG_SEP}'
# MSG_FMT = f'%s{CHAR_SEP}%s{MSG_SEP}'

# As scary as this looks, all it does is remove them from the config namespace.
del socket
del logging
del sys
