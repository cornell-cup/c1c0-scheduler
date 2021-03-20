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
        Invariant: process_type is a string in ["path-planning", "object-detection", "locomotion"]

        Attribute: process_type
        Invariant: process_type is a string in ["path-planning", "object-detection", "locomotion"]
        """
        process_type = process_type
        handshakeComplete = False
        ClientSocket = socket.socket()


    def handshake():
        host = '127.0.0.1'
        port = 1233

        print('Waiting for connection')
        try:
            ClientSocket.connect((host, port))
        except socket.error as e:
            print(str(e))

        Response = ClientSocket.recv(1024)
        while (not handshakeComplete):
            ClientSocket.send(str.encode("I am "+ process_type))
            ResponseSocket = ClientSocket.recv(1024)
            Response = ResponseSocket.decode('utf-8')
            print(Response)
            if (Response == process_type + " is recognized"):
                handshakeComplete = True

    def communicate(request):
        if handshakeComplete:
            ClientSocket.send(str.encode(request))
            ResponseSocket = ClientSocket.recv(1024)
            Response = ResponseSocket.decode('utf-8')
            return Response

    def close():
        ClientSocket.close()
    
    

