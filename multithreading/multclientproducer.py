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
while True:
    #Input = input('Say Something: ')
    Response = ""
    while(Response != "Producer is recognized"):
        ClientSocket.send(str.encode("I am Producer"))
        ResponseSocket = ClientSocket.recv(1024)
        Response = ResponseSocket.decode('utf-8')
        print(Response)
    while True:
        Input = input('Say Something: ')
        ClientSocket.send(str.encode(Input))
        ResponseSocket = ClientSocket.recv(1024)
        Response = ResponseSocket.decode('utf-8')
        print(Response)

ClientSocket.close()

