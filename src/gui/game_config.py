EASY = 0
MEDIUM = 1
HARD = 2
PVE_MODE = 0
PVP_MODE = 0


class GameConfig:

    def __init__(self):
        self._mode = PVE_MODE
        self._difficult = EASY

    def pvp_mode(self):
        self._mode = PVP_MODE
        return self

    def pve_mode(self):
        self._mode = PVE_MODE
        return self

    def get_mode(self):
        return self._mode

    def easy(self):
        self._difficult = EASY
        return self

    def medium(self):
        self._difficult = MEDIUM
        return self

    def hard(self):
        self._difficult = HARD
        return self

    def get_difficult(self):
        return self._difficult
