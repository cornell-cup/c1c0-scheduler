from concurrent import futures

import grpc

from . import protocols_pb2, protocols_pb2_grpc, config
from .system import System


system: System = config.system


class Scheduler(protocols_pb2_grpc.SchedulerServicer):
    # noinspection PyUnresolvedReferences
    def SysCommand(self, request, context):
        # system.get_functionality()['start_module'](request.recipient)
        return protocols_pb2.SysResponse(
            response=f'Module has been started! {request.recipient}')

    def SysCommandStream(self, request, context):
        i = 0
        while True:
            yield protocols_pb2.SysResponse(
                response=f'Sending {i}'
            )
            i += 1


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    protocols_pb2_grpc.add_SchedulerServicer_to_server(Scheduler(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    # Initialize robot's services
    # system = config.init_c1c0()

    # Start serving
    serve()
