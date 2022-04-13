class BlackPlayerWinException(Exception):
    def __init__(self):
        super().__init__('Black Player Win')


class WhitePlayerWinException(Exception):
    def __init__(self):
        super().__init__('White Player Win')
