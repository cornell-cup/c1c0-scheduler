from concurrent import futures

import grpc

from . import protocols_pb2, protocols_pb2_grpc, config
from .system import System


system: System = config.system
# DEBUG = False
DEBUG = True


class Scheduler(protocols_pb2_grpc.SchedulerServicer):
    # noinspection PyUnresolvedReferences
    def SysCommand(self, request, context):
        # system.get_functionality()['start_module'](request.recipient)
        if DEBUG:
            print('SysCommand called:')
            print(f'cmd:{request.cmd}\n'
                  f'sender: {request.sender}\n'
                  f'recipient: {request.recipient}\n'
                  f'data: {request.data}\n')
        # response = None
        # try:
        #     response = protocols_pb2.SysResponse(
        #     response=str(system.get_functionality()[request.cmd](
        #         request.sender, request.recipient, *request.data)))
        # except Exception as e:
        #     print(e)
        #     raise e
        # return response
        return protocols_pb2.SysResponse(
            response=str(system.get_functionality()[request.cmd](
                request.sender, request.recipient, *request.data)))

    def SysCommandStream(self, request, context):
        while True:
            yield protocols_pb2.SysResponse(
                response=str(system.get_functionality()[request.cmd](
                    request.sender, request.recipient, *request.data)))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    protocols_pb2_grpc.add_SchedulerServicer_to_server(Scheduler(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


def setup_and_serve():
    global system
    # Initialize robot's services
    system = config.init_c1c0()
    print(f'C1C0 System has been initialized!')
    print(f'Functionality:\n{system.get_functionality()}')
    print(f'Workers:\n{system.get_workers()}')
    # Start serving
    serve()


if __name__ == '__main__':
    setup_and_serve()
