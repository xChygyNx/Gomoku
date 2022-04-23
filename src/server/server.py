import os
import typing as t
import dotenv
import socket
import json
from src.gomoku import Gomoku


dotenv.load_dotenv()


class Server:
    def __init__(self):
        self._socket = None
        self.connection = None
        self.address = None
        self.gomoku: Gomoku = None

    @property
    def socket(self):
        if self._socket is not None:
            return self._socket
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((socket.gethostbyname('localhost'), int(os.environ['PORT'])))
        return self._socket

    def accept_connection(self):
        self.socket.listen(0)
        self.connection, self.address = self.socket.accept()

    def get_data(self) -> t.Generator:
        while True:
            data = self.connection.recv(int(os.environ['SERVER_BATCH_SIZE'])).decode(os.environ['SERVER_ENCODING'])
            data = json.loads(data)
            if data.get('title') == 'start':
                self.gomoku = Gomoku(**data.get('message'))
                self.connection.send('ok'.encode(os.environ['SERVER_ENCODING']))
            elif data.get('title') == 'end_game':
                self.connection.send(json.dumps(data.get('message')).encode(os.environ['SERVER_ENCODING']))
                break
            else:
                self.connection.send('ok'.encode(os.environ['SERVER_ENCODING']))
                method = self.gomoku.__getattribute__(data.get('title'))
                method(**data.get('message'))
                yield data

    def listen_connection(self):
        for message in self.get_data():
            print(message)
            print()
        self.connection.close()



if __name__ == '__main__':
    server = Server()
    server.accept_connection()
    server.listen_connection()
    print('Thanks')
    # launch something