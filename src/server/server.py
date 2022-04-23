import os
import random
import typing as t
import dotenv
import socket
import json
from src.gomoku import Gomoku
import time


dotenv.load_dotenv()

MOVES = []


def fill_moves(size):
    MOVES.clear()
    for r in range(size):
        for c in range(size):
            MOVES.append(chr(97 + c) + str(r + 1))


def get_random_move():
    pos = random.choice(MOVES)
    MOVES.remove(pos)
    return pos


def remove_move(move):
    MOVES.remove(move)


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
            if not data:
                break
            data = json.loads(data)
            if data.get('method') == 'start':
                self.gomoku = Gomoku(**data.get('arguments'))
                self.connection.send('ok'.encode(os.environ['SERVER_ENCODING']))

                # генерация тестовых данных
                fill_moves(int(data["arguments"]["board_size"]) + 1)
            elif data.get('method') == 'end_game':
                break
            else:
                self.connection.send('ok'.encode(os.environ['SERVER_ENCODING']))
                if data.get('method') in dir(self.gomoku):
                    method = self.gomoku.__getattribute__(data.get('method'))
                    method(**data.get('arguments'))

                    # отправляем рандомный неповторяющийся ответ
                    time.sleep(0.5)
                    remove_move(data["arguments"]["position"])
                    answer = {
                        "method": "make_turn",
                        "arguments": {"position": get_random_move(), "color": "white"}
                    }
                    arguments = json.dumps(answer)
                    self.connection.send(arguments.encode(os.environ['SERVER_ENCODING']))
                else:
                    print(f"Unresolved method {data.get('method')}")
                yield data

    def listen_connection(self):
        for message in self.get_data():
            if message:
                print(message)
                print()
        self.connection.close()


if __name__ == '__main__':
    while True:
        server = Server()
        server.accept_connection()
        server.listen_connection()
        print('Thanks')
