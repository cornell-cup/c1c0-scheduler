import subprocess


def run_protos():
    print()
    cmd = '''
    python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/protocols.proto
    '''
    print('\nRan protos successfully\n' if not subprocess.run(
        cmd, shell=True).returncode else 'Failed to run protos')


def correct_grpc_module():
    with open('protocols_pb2_grpc.py', 'r+') as f:
        lines = []
        for line in f.readlines():
            if line.startswith('import protocols_pb2 as protocols__pb2'):
                line = f'from . {line}'
            lines.append(line)
        f.seek(0)
        f.writelines(lines)
        f.truncate()
    print('\nFinished correcting grpc module.\n')


if __name__ == '__main__':
    run_protos()
    correct_grpc_module()
