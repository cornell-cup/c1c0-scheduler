import zmq # Standard Python Imports

from scheduler.config import * # Configurations
from scheduler.utils import Message, printc # Utilities

from typing import Optional, Tuple # Type Hinting

class Server:
    """
    The universal C1C0 server, allowing REP scripts to communicate with REQ scripts.
    """

    def __init__(self: any, port: Optional[int] = None) -> 'Server':
        """
        Initializes a server instance for the given port.

        @param port: An optional int representing the port to connect to.
        @return: A Client instance with fields set as specified.
        """

        # Initializing fields
        self.port: int    = PORT if port is None else port
        self.status: bool = False

        # Debug printing
        if (DEBUG): printc(f'PORT: {self.port}', INF_COLOR)

    def start(self: any, port: Optional[int] = None) -> bool:
        """
        Starts the server on the given port.

        @param port: An optional int representing the port to connect to.
        @return: Whether or not the server successfully started.
        """

        # Updating host/port if necessary
        if (port is not None): self.port = port

        try:
            # Initializing ZMQ Connection
            context = zmq.Context()
            self.sock = context.socket(zmq.REP)
            self.sock.bind(f'tcp://*:{self.port}')
            return True

        except zmq.error.ZMQError as err:
            # Error occurred, returning false
            if (DEBUG): printc(f'ZMQ Error: {err}', ERR_COLOR)
            return False

    def stop(self: any) -> None:
        """
        Stops the server's ZMQ connection.
        """

        # Closing connection
        self.sock.close()

    def receive(self: any) -> Message:
        """
        Receives a message from the client and returns its.

        @return: The message from the client.
        """

        # Receiving message from client
        message: Message = Message.decode(self.sock.recv_string())
        if (DEBUG and message.show()): printc(f'[{message}]', RCV_COLOR)
        return message

    def send(self: any, message: Message) -> None:
        """
        Sends a message to the client with the given name, tag, and data.

        @param message: A Message instance representing the message to be sent.
        """

        # Sending message to client
        if (DEBUG and message.show()): printc(f'[{message}]', SNT_COLOR)
        self.sock.send_string(str(message))
