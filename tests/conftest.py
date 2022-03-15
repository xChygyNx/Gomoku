from pytest import fixture
from src.store.gomoku import Gomoku


@fixture(scope='function')
def new_gomoku():
    yield Gomoku()
