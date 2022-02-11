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
while (not handshakeComplete):
    ClientSocket.send(str.encode("I am Chatbot"))
    ResponseSocket = ClientSocket.recv(1024)
    Response = ResponseSocket.decode('utf-8')
    print(Response)
    if (Response == "Chatbot is recognized"):
        handshakeComplete = True
        print("Handshake is completed")
while handshakeComplete:
    Input = input('Say Something: ')
    ClientSocket.send(str.encode(Input))
    ResponseSocket = ClientSocket.recv(1024)
    Response = ResponseSocket.decode('utf-8')
    print(Response)

ClientSocket.close()
