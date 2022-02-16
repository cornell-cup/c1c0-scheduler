from c1c0_scheduler import client
import multiprocessing
import time


iterations = [0]*10
clients = [client.Client('Testing Client {i}') for i in range(10)]
[client.start_submodule('path-planning') for client in clients]
client_pool = multiprocessing.Pool(10)


def collect_data(idx):
    clients[idx].get_data(f'terabee{idx+1}')
    iterations[idx] += 1


if __name__ == '__main__':

    while True:
        start = time.time()
        client_pool = multiprocessing.Pool(10)
        client_pool.apply_async(collect_data)
        client_pool.map()
        time.sleep(1)
        client_pool.terminate()
        print(f'iterations={iterations}')
        print(f'sum(iterations)={sum(iterations)}')
