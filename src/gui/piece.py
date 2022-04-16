import json


class Piece:

    def __init__(self, piece, pos, color):
        self._piece = piece
        self._pos = pos
        self._color = color

    def get_pos(self):
        return self._pos

    def get_color(self):
        return self._color

    def get_piece(self):
        return self._piece

    def __eq__(self, other):
        if isinstance(other, str):
            return self.get_pos() == other
        return self.get_pos() == other.get_pos()

    def __str__(self):
        return f"{self._pos}: {self._color}"

    def to_json(self):
        return json.dumps(self.__dict__())

    def __dict__(self):
        return {
            "position": self._pos,
            "color": self._color
        }
