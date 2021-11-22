from c1c0_scheduler import client

if __name__ == '__main__':
    client = client.Client('Testing Client')
    print(client.start_submodule('path-planning'))
    i = 0
    for datum in client.get_data('terabee1'):
        print(f'Got "{i}th piece of data {datum}"')
        i += 1
    # Lol, for comparison
    # for i in range(2**64):
    #     print(f'Got fake datum: "{i}"')



