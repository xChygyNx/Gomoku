from pytest import fixture
from src.store.gomoku import Gomoku


@fixture(scope='function')
def mini_gomoku():
    yield Gomoku(size=7)
