import zmq # Standard Python Imports

from scheduler.config import * # Configurations
from scheduler.util import Message # Utilities

from typing import Optional # Type Hinting

class Client:
    """
    The universal C1C0 client, allowing REQ scripts to communicate with REP scripts.
    """

    def __init__(self: any, name: str, host: Optional[str] = None, port: Optional[int] = None) -> 'Client':
        """
        Initializes a client instance for the given host/port combination.

        @param name: A string representing the unique identifier of the client.
        @param host: An optional string representing the host to connect to.
        @param port: An optional int representing the port to connect to.
        @return: A Client instance with fields set as specified.
        """

        # Initializing fields
        self.name: str       = name
        self.host: str       = HOST if host is None else host
        self.port: int       = PORT if port is None else port
        self.connected: bool = False

        # Debug printing
        if (DEBUG): print(f'NAME: {self.name}, HOST: {self.host}, PORT: {self.port}')

    def connect(self: any, host: Optional[str] = None, port: Optional[int] = None) -> bool:
        """
        Connects the client to the server at the given host/port combination.

        @param host: An optional string representing the host to connect to.
        @param port: An optional int representing the port to connect to.
        @return: Whether or not the client successfully connected to the server.
        """

        # Updating host/port if necessary
        if (host is not None): self.host = host
        if (port is not None): self.port = port

        # Initializing ZMQ Connection
        try:
            context: any = zmq.Context()
            self.sock: any = context.socket(zmq.REQ)
            self.sock.connect(f'tcp://{self.host}:{self.port}')

        except zmq.error.ZMQError as err:
            if (DEBUG): print(f'ZMQ Error: {err}')
            return False

        # Checking connection
        attempt: int = 0
        while not self.connected and attempt < ATTEMPTS:
            if (self.check('connected')): self.connected = True
            attempt += 1

        # Returning connection status
        if (DEBUG): print(f'CONNECTED: {self.connected}, ATTEMPTS: {attempt}')
        return self.connected

    def close(self: any) -> None:
        """
        Closes the client's ZMQ connection to the server.
        """

        # Sending disconnect message and closing connection
        sent: bool = self.check('disconnected')
        self.connected = False; self.sock.close()
        if (DEBUG): print(f'CONNECTED: {self.connected}, SENT: {sent}')

    def check(self: any, data: str) -> bool:
        """
        Checks the client's connection to the server.

        @param data: A string representing the data to send to the server.
        @return: Whether or not the client successfully connected to the server.
        """

        try:
            # Sending message to server
            message: Message = Message(self.name, 'check', data)
            self.sock.send_string(str(message))
            if (DEBUG): print(f'MESSAGE: {message}')

            # Receiving response from server
            response: Message = Message.decode(self.sock.recv_string())
            if (DEBUG): print(f'RESPONSE: {response}')
            return response == message

        except:
            # Returning false if an error occurred
            return False

    def communicate(self: any, tag: str, data: str) -> Message:
        """
        Communicates the given message to scheduler and returns the response.

        @param tag: A string representing the tag of the message.
        @param data: A string representing the data to send to the server.
        @return: The response from the server.
        """

        try:
            # Sending message to server
            message: Message = Message(self.name, tag, data)
            self.sock.send_string(str(message))
            if (DEBUG): print(f'MESSAGE: {message}')

            # Receiving response from server
            response: Message = Message.decode(self.sock.recv_string())
            if (DEBUG): print(f'RESPONSE: {response}')
            return response

        except:
            # Returning an empty string if an error occurred
            return ''
