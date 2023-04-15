import time
from argparse import ArgumentParser

from c1c0_scheduler.client import Client

parser = ArgumentParser()

parser.add_argument('-m', '--mod', action='store', type=str)

args, unknown_args = parser.parse_known_args()

name = args.mod

client = Client(name)
print(f'{name}.timeout={client.sock.gettimeout()}')
client.connect()

time.sleep(10)