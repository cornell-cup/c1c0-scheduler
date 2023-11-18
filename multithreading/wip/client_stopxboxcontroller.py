import client

if __name__ == "__main__":
    global scheduler
    scheduler = client.Client("stop-xboxcontroller")
    scheduler.handshake()
