import socket

ENCODING = 'UTF-8'


def to_object_detection(socket_, obj):
    socket_.send(f'C_S_O(Obj({obj}))'.encode(ENCODING))


def to_path_planning(socket_: socket.socket, coords_dir, dist=None):
    if dist is None:
        socket_.send(f'C_S_P(Coords({str(coords_dir)}))'.encode(ENCODING))
    else:
        socket_.send(f'C_S_P(A({coords_dir}),{dist})'.encode(ENCODING))


def to_facial_recognition(socket_):
    pass
