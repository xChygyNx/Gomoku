import os

import dotenv
import socket
import json


if __name__ == '__main__':
    dotenv.load_dotenv()
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    print(socket.gethostname())
    print(socket.gethostbyname('localhost'))
    conn.bind((socket.gethostbyname('localhost'), int(os.environ['PORT'])))
    conn.listen(0)

    connection, address = conn.accept()
    connection.send('Get me data\n'.encode('utf-8'))

    while True:
        data = connection.recv(1024).decode("utf8")

        if data:
            break
    print(type(data))
    data = json.loads(data)
    print(type(data))
    print(data)
    print('Thanks')
    # launch something