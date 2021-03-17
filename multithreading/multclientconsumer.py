import socket

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
while(not handshakeComplete):
    ClientSocket.send(str.encode("I am Producer"))
    ResponseSocket = ClientSocket.recv(1024)
    Response = ResponseSocket.decode('utf-8')
    print(Response)
    if (Response == "Producer is recognized"):
            handshakeComplete = True
while handshakeComplete:
    Input = input('Say Something: ')
    ClientSocket.send(str.encode(Input))
    ResponseSocket = ClientSocket.recv(1024)
    Response = ResponseSocket.decode('utf-8')
    print(Response)

ClientSocket.close()

