from concurrent.futures import ThreadPoolExecutor

import asyncio
from typing import Coroutine, Any

import grpc

from . import protocols_pb2, protocols_pb2_grpc, config
from .config import DEBUG, MAX_WORKERS
from .system import System, DataProvider

system: System = config.system


class Scheduler(protocols_pb2_grpc.SchedulerServicer):
    """
    The server object that exposes the System's functionality.
    """
    # noinspection PyUnresolvedReferences
    async def SysCommand(self, request, context):
        """
        Takes a request and context and returns the result dependent on the
        command (cmd) embedded in the request.
        """
        if DEBUG:
            print('SysCommand called:')
            print(f'cmd:{request.cmd}\n'
                  f'sender: {request.sender}\n'
                  f'recipient: {request.recipient}\n'
                  f'data: {request.data}\n')

        return protocols_pb2.SysResponse(
            response=str(system.get_functionality()[request.cmd](
                request.sender, request.recipient, *request.data)))

    async def SysCommandStream(self, request, context):
        """
        Takes a request and context and yields the result dependent on the
        command (cmd) embedded in the request.
        """
        refresh_rate = request.refresh_rate
        # This command is only compatible with streaming threads
        data_obj: DataProvider = system.get_functionality()[request.cmd](
            request.sender, request.recipient, *request.data)
        print(f'refresh_rate={refresh_rate}')
        if not getattr(data_obj, 'is_data_provider'):
            raise RuntimeError('Stream requested of non-stream functionality.')
        while True:
            print('Server response lock acquire')
            with data_obj.new_data:
                print('Server response lock acquired')
                yield protocols_pb2.SysResponse(response=str(data_obj.data))
                data_obj.new_data.wait(refresh_rate)


async def serve():
    """
    Serves the server.
    """
    server = grpc.aio.server(ThreadPoolExecutor(max_workers=MAX_WORKERS))
    protocols_pb2_grpc.add_SchedulerServicer_to_server(Scheduler(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    await server.wait_for_termination()


def setup_and_serve() -> Coroutine[Any, Any, None]:
    global system
    # Initialize robot's services
    system = config.init_default()
    print(f'C1C0 System has been initialized!')
    print(f'Functionality:\n{system.get_functionality()}')
    print(f'Workers:\n{system.get_workers()}')
    # Start serving
    return serve()


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait([setup_and_serve()]))
    asyncio.run(setup_and_serve())


if __name__ == '__main__':
    asyncio.run(setup_and_serve())
