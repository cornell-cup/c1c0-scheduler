import grpc

from . import protocols_pb2, protocols_pb2_grpc


class Client:
    def __init__(self, module_name):
        self.module_name = module_name
        self.channel = grpc.insecure_channel('localhost:50051')

    def close(self):
        self.channel.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def start_submodule(self, module, *args):
        kwargs = {
            'sender': self.module_name,
            'cmd': 'start_subsystem',
            'recipient': module
        }
        if args:
            kwargs['data'] = ', '.join(args)
        stub = protocols_pb2_grpc.SchedulerStub(self.channel)
        return stub.SysCommand(protocols_pb2.SysRequest(**kwargs))

    def get_data(self, data_id, *args):
        kwargs = {
            'sender': self.module_name,
            'cmd': 'get_data',
            'recipient': data_id,
            'refresh_rate': 0
        }
        if args:
            kwargs['data'] = ', '.join(args)
        stub = protocols_pb2_grpc.SchedulerStub(self.channel)
        for datum in stub.SysCommandStream(protocols_pb2.SysRequestStream(
                **kwargs)):
            yield datum
