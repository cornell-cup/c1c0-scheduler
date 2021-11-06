"""
Scheduling API for C1C0

March 19, 2021

Purposes of the API:

"""
# import multserver
import socket

from ..config import DEFAULT_HOST, DEFAULT_PORT, ENCODING, extract_process_type, PType


class Client(object):
    def __init__(self, process_type: PType):
        """
        Parameter: process_type
        Invariant: process_type is a string in ["path-planning", "object-detection", "locomotion"]
        """

        self.handshake_complete = False
        self.client_socket = socket.socket()
        self.process_type = extract_process_type(process_type)

    def handshake(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        """
        Invoked to initialize the connection to the socket server.

        PARAMETERS
        --------
        host
            The IP address of the host socket the module wishes to connect to. Default: "127.0.0.1"
        port
            The port of the host socket the module wishes to connect to. Default: 1233
        """
        print('Waiting for connection...')
        try:
            self.client_socket.connect((host, port))
            print(f"Connection to {host}:{port} successful!")
        except socket.error as e:
            print(str(e))

        response_ = self.client_socket.recv(32)
        while not self.handshake_complete:
            # TODO: handshake timeout mechanism
            self.client_socket.send(f"I am {self.process_type}".encode(ENCODING))
            response_ = self.client_socket.recv(32)
            response = response_.decode(ENCODING)
            # print("I am a genius")
            if response == self.process_type + " is recognized":
                print(response)
                self.handshake_complete = True

    def communicate(self, request):
        if self.handshake_complete:
            self.client_socket.sendall(request.encode(ENCODING))
            response_ = self.client_socket.recv(32)
            response = response_.decode(ENCODING)
            print(response)
            return response

    def close(self):
        self.communicate("kill")
        self.client_socket.close()
        print("closed connection")
