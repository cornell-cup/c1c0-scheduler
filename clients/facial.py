import sys; path: str = sys.argv[1]; sys.path.insert(0, path) # Modifying Python Path
import time

from scheduler.config import * # Configuration
from scheduler.client import Client as SClient # Client
from scheduler.util import Message # Utilities
from client.client import Client as FClient # Importing The Client/Task Manager

STALL: int = 3 # Time To Wait For New Task

if __name__ == '__main__':
    # Creating clients
    facial_client: FClient = FClient(load=False, disp=False, prnt=True)
    scheduler_client: SClient = SClient('facial')
    scheduler_client.connect()

    while True:
        # Asking ZMQ For Next Task
        time.sleep(STALL)
        response1: Message = scheduler_client.communicate('get', 'null')

        # Getting The Task
        split: list[str] = response1.data.split(' ')
        command, args = split[0], split[1:]
        if (command == 'null'): continue

        # Running The Task
        try:
            task = facial_client.interpret_task(command)
            names = task(args)
        except:
            names = []

        # Sending The Result Back To ZMQ
        response2: Message = scheduler_client.communicate('put', str(names))
