import socket
import logging
import sys

# UNIVERSAL SCHEDULER DEVELOPMENT/PRODUCTION MODE SWITCH
DEBUG = True

HOST = '127.0.0.1'
PORT = 1233
ENCODING = 'utf-8'

AF = socket.AF_INET
SOCK_TYPE = socket.SOCK_STREAM
BUFFER_SIZE = 1024

CONNECTION_RETRIES = 10
IGNORE_NONFATAL = DEBUG

FILE_HANDLER = logging.FileHandler('output.log', encoding=ENCODING)
STREAM_HANDLER = logging.StreamHandler(sys.stdout if DEBUG else sys.stderr)

MODULES = {
    'chatbot': {
    },
    'path-planning': {
    },
    'object-detection': {
    },
    'path-planning': {
    
    }
}

CHAR_SEP = ':'
MSG_SEP = ';'
MSG_REGEX = f'(\w+){CHAR_SEP}([\w\d]+){MSG_SEP}'
MSG_FMT = f'%s{CHAR_SEP}%s{MSG_SEP}'

# As scary as this looks, all it does is remove them from the config namespace.
del socket
del logging
del sys