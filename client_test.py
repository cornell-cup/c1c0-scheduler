from c1c0_scheduler import client
import time

if __name__ == '__main__':
    client = client.Client('Testing Client')
    print(client.start_submodule('path-planning'))
    for datum in client.get_data('some_data_id'):
        print(f'Got datum: "{datum}"')



