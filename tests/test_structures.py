from unittest.mock import patch, MagicMock

class TestSequencesInfo:
    @patch('src.gomoku.gomoku.Gomoku.check_horizontal')
    @patch('src.gomoku.gomoku.Gomoku.check_vertical')
    @patch('src.gomoku.gomoku.Gomoku.check_diagonal_1')
    @patch('src.gomoku.gomoku.Gomoku.check_horizontal_2')
    def test_horizontal_white_win(self,
                            check_diagonal2_mock: MagicMock,
                            check_diagonal1_mock: MagicMock,
                            check_vertical_mock: MagicMock,
                            check_horizontal_mock: MagicMock,
                            normal_gomoku):
        normal_gomoku.make_turn(x=5, y=5, color=Color.WHITE)
        normal_gomoku.make_turn(x=5, y=6, color=Color.WHITE)
        normal_gomoku.make_turn(x=5, y=7, color=Color.WHITE)
        normal_gomoku.make_turn(x=5, y=8, color=Color.WHITE)
        normal_gomoku.make_turn(x=5, y=9, color=Color.WHITE)
        normal_gomoku.check_state()
        assert check_horizontal_mock.called
        assert check_horizontal_mock.call_count == 1
        assert not check_vertical_mock.called
        assert not check_diagonal1_mock.called
        assert not check_diagonal2_mock.called



