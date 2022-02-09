from c1c0_scheduler import client
import multiprocessing
import time


iterations = [0]*10

def collect_data():
    i = 0
    for datum in client.get_data('terabee1'):
        # print(f'Got "{i}th piece of data {datum}"')
        i += 1


if __name__ == '__main__':
    clients = [client.Client('Testing Client {i}') for i in range(10)]
    [client.start_submodule('path-planning') for client in clients]

    client_pool = multiprocessing.Pool(10)

    while True:
        client_pool.apply_async(collect_data)
        time.sleep(1)
        client_pool.terminate()
