import socket


def generate_data(seed_):
    return_list = []
    for i in range(10):
        return_list.append(i + 10 * seed_)
    return return_list


client_socket = socket.socket()
host = '127.0.0.1'
port = 1233

print('Waiting for connection')
try:
    client_socket.connect((host, port))
except socket.error as e:
    print(str(e))

Response = client_socket.recv(1024)
handshakeComplete = False
while not handshakeComplete:
    client_socket.send(str.encode("I am Producer"))
    ResponseSocket = client_socket.recv(1024)
    Response = ResponseSocket.decode('utf-8')
    print(Response)
    if Response == "Producer is recognized":
        handshakeComplete = True
print("---------------------------------------------------")
for seed in range(10):
    client_socket.send(str.encode(str(generate_data(seed))))
    ResponseSocket = client_socket.recv(1024)
    Response = ResponseSocket.decode('utf-8')
    print(Response)
client_socket.send(str.encode("Done sending data"))
ResponseSocket = client_socket.recv(1024)
client_socket.close()
