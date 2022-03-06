from c1c0_scheduler import client
import multiprocessing
import time


iterations = {i: 0 for i in range(10)}
clients = [client.Client('Testing Client {i}') for i in range(10)]
with clients[0] as client__:
    client__.start_submodule('path_planning')
client_pool = multiprocessing.Pool()


def collect_data(idx):
    # print(idx)
    with clients[idx] as client_:
        # print(f'{idx}: calling get_data')
        res = client_.get_data(f'terabee1')
        return res
        # print(f'{idx}: get_data called, got {res} iterations={iterations}')


if __name__ == '__main__':

    while True:
        start = time.time()
        client_pool = multiprocessing.Pool(10)
        futures = [client_pool.apply_async(collect_data, [i]) for i in range(10)]
        [f.get(5.0) for f in futures]
        client_pool.terminate()
        # print(f'iterations={iterations}')
        # print(f'sum(iterations)={sum(iterations)}')
