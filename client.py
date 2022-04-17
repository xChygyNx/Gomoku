import socket
import os
import dotenv
import json
import time


RESOURCES = os.path.join(os.getcwd(), "resources", "methods")

messages = {
    'msg1': {
        'a': 1,
        'b': 2,
        'c': 3,
    },
    'msg2': {
        'message': 'a' * 10000
    },
    'msg3': {
        'title': 'end_game',
        'message': 'White Player Win'
    }
}


if __name__ == '__main__':
    dotenv.load_dotenv()
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((socket.gethostbyname('127.0.0.1'), int(os.environ['PORT'])))
    try:
        for file in sorted(os.listdir(f'{RESOURCES}')):
            with open(os.path.join(RESOURCES, file), 'r') as f:
                data = json.loads(f.read())
                print(f'Dumps {json.dumps(data)}')
                connection.send(json.dumps(data).encode('utf8'))
                response = connection.recv(1024).decode('utf8')
                print(response)
            time.sleep(3)
    except Exception:
        pass
    finally:
        connection.close()
