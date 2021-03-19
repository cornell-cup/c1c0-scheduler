"""
Scheduling API for C1C0

March 19, 2021

Purposes of the API:

"""
import multserver
import socket

class Client(object):

    def __init__(process_type):
        """
        Parameter: process_type
        Invariant: process_type is a string in [path-planning", "object-detection", "locomotion"]
        """
        server_connect(process_type)

    def server_connect(client):
        ClientSocket = socket.socket()
        host = '127.0.0.1'
        port = 1233

        print('Waiting for connection')
        try:
            ClientSocket.connect((host, port))
        except socket.error as e:
            print(str(e))

        Response = ClientSocket.recv(1024)
        handshakeComplete = False
        while (not handshakeComplete):
            ClientSocket.send(str.encode("I am "+ client))
            ResponseSocket = ClientSocket.recv(1024)
            Response = ResponseSocket.decode('utf-8')
            print(Response)
            if (Response == client + " is recognized"):
                handshakeComplete = True
        while handshakeComplete:
            Input = input('Say Something: ')
            ClientSocket.send(str.encode(Input))
            ResponseSocket = ClientSocket.recv(1024)
            Response = ResponseSocket.decode('utf-8')
            print(Response)
            #Response to close socket
            if(Response == "Close"):
                handshakeComplete = False
        ClientSocket.close()
    
    def close_socket():

