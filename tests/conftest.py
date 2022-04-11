from pytest import fixture
from src.gomoku.gomoku import Gomoku
from src.gomoku.structures import SequencesInfo


@fixture(scope='function')
def mini_gomoku():
    yield Gomoku(size=7)

@fixture(scope='function')
def normal_gomoku():
    yield Gomoku(size=19)

@fixture(scope='function')
def seq_info():
    yield SequencesInfo()
