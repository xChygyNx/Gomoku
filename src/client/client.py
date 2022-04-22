import socket
import os
import dotenv
import json
import time
import logging
import typing as t

from src.gomoku.gomoku import Gomoku


RESOURCES = os.path.join(os.getcwd(), "resources", "methods")

dotenv.load_dotenv()

logger = logging.getLogger(__name__)

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


class Client:
    def __init__(self):
        self._connection = None
        self.address = None
        self.gomoku: Gomoku = None

    @property
    def connection(self):
        if self._connection is not None:
            return self._connection
        self._connection = (socket.AF_INET, socket.SOCK_STREAM)
        return self._connection

    def connect_to_server(self) -> None:
        self.connection.connect((socket.gethostbyname(os.environ['HOST']), int(os.environ['PORT'])))

    def send_data(self, data: str, encode: str = os.environ['RECEIVE_ENCODING']) -> None:
        self.connection.send(data.encode(encode))
        logger.info(f'Client send:\n {json.loads(data)}')

    def receive_response(self, batch_size: int = int(os.environ['RECEIVE_BATCH_SIZE']),
                         decode: str = os.environ['RECEIVE_ENCODING']) -> str:
        response = self.connection.recv(batch_size).decode(decode)
        logger.info(f'Client receive:\n {json.loads(response)}')
        return response



if __name__ == '__main__':
    client = Client()
    client.connect_to_server()
    try:
        for file in sorted(os.listdir(f'{RESOURCES}')):
            with open(os.path.join(RESOURCES, file), 'r') as f:
                data = f.read()
                client.send_data(data)
                response = client.receive_response()
            time.sleep(3)
    except Exception:
        pass
    finally:
        client.connection.close()
