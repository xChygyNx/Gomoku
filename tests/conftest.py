from pytest import fixture
from src.gomoku.gomoku import Gomoku
from src.gomoku.structures import SequencesInfo


@fixture(scope='function')
def mini_gomoku():
    yield Gomoku(board_size=7, mode='PvP')


@fixture(scope='function')
def normal_gomoku():
    yield Gomoku(board_size=19, mode='PvP')


@fixture(scope='function')
def seq_info():
    yield SequencesInfo()
