#!../venv/bin/python3
import subprocess


def run_protos():
    """
    Runs the bash command to compile the proto files.
    """
    print()
    cmd = '''
    python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/protocols.proto
    '''
    print('\nRan protos successfully\n' if not subprocess.run(
        cmd, shell=True).returncode else 'Failed to run protos')


def correct_grpc_module():
    """
    Opens and edits the generated files to relatively import each other.
    """
    with open('protocols_pb2_grpc.py', 'r+') as f:
        lines = []
        for line in f.readlines():
            if line.startswith('import protocols_pb2 as protocols__pb2'):
                line = f'try:\n    from . {line}except ImportError:\n    from c1c0_scheduler {line}'
            lines.append(line)
        f.seek(0)
        f.writelines(lines)
        f.truncate()
    print('\nFinished correcting grpc module.\n')


if __name__ == '__main__':
    run_protos()
    correct_grpc_module()
