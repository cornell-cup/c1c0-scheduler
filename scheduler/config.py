DEBUG: bool   = True # Universal Scheduler Development/Production Mode Switch.
ATTEMPTS: int = 10 # Number of times to attempt a connection before giving up.

HOST: str     = 'localhost' # Either '127.0.0.1' or '192.168.4.127'.
PORT: int     = 5555 # Choose whatever you want, but make sure it's not in use.
ENCODING: str = 'utf-8' # Encoding to use for all data sent/received.

DATA_SEP: str     = ': ' # Separator between metadata and data.
TAG_SEP: str      = '_' # Separator between name and tag.
DEFAULT_RESP: str = 'null' # Default response to send if no response is found.
