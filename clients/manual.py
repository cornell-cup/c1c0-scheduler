import sys; path: str = sys.argv[1]; sys.path.insert(0, path) # Modifying Python Path

from scheduler.config import * # Configuration
from scheduler.client import Client # Client
from scheduler.util import Message # Utilities

if __name__ == '__main__':
    # Initializing client
    client: Client = Client('manual')
    client.connect()

    while True:
        # Getting command from user
        ctype: str = input('Enter command tag: ')
        if (ctype == 'exit' or ctype == 'quit'): break
        cdata: str = input('Enter command data: ')

        # Sending message to server
        response: Message = client.communicate(ctype, cdata)

    # Closing client
    client.close()
    print('Program terminated.')
