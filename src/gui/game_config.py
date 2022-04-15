
BOARD_SIZE = {"19 x 19": 19, "15 x 15": 15}


class GameConfig:

    def __init__(self, mode, difficult, board_size, first_move):
        self._mode = mode
        self._difficult = difficult
        self._board_size = BOARD_SIZE[board_size]
        self._first_move = first_move

    @staticmethod
    def create(mode, difficult, board_size, first_move):
        return GameConfig(mode, difficult, board_size, first_move)

    def get_board_size(self):
        return self._board_size

    def get_mode(self):
        return self._mode

    def get_difficult(self):
        return self._difficult

    def get_first_move(self):
        return self._first_move

    def __str__(self):
        return f"Mode: {str(self._mode)}\nDifficult: {str(self._difficult)}\n" + \
               f"Board size: {str(self._board_size)}\nFirst move: {str(self._first_move)}\n"
