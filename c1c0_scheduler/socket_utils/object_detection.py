import socket


BUFFER_SIZE = 32


def from_chatbot(socket_: socket.socket):
    response = socket_.recv(BUFFER_SIZE)
    # Trim "C_S_O(%s)"
    response = response[6:-1]
    # We have the object! .. surrounded by the guard "Obj(%s)"
    return response[4:-1]
