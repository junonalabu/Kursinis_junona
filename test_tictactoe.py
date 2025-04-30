import unittest
from unittest.mock import patch, mock_open
from io import StringIO

from game import Board, HumanPlayer, ComputerPlayer, TicTacToeGame, GameSymbol


class TestTicTacToe(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.reset()
        self.player1 = HumanPlayer("Test1", GameSymbol.X.value)
        self.player2 = ComputerPlayer("Computer", GameSymbol.O.value)

    def test_board_reset(self):
        self.board._cells = ['X'] * 9
        self.board.reset()
        self.assertEqual(self.board._cells, [' '] * 9)

    def test_is_position_empty(self):
        self.assertTrue(self.board.is_position_empty(0))
        self.board.update_cell(0, 'X')
        self.assertFalse(self.board.is_position_empty(0))

    def test_board_is_full(self):
        self.board._cells = ['X', 'O', 'X', 'X', 'O', 'O', 'O', 'X', 'X']
        self.assertTrue(self.board.is_full())

    def test_update_cell_bounds(self):
        self.board.update_cell(0, 'X')
        self.assertEqual(self.board._cells[0], 'X')

    @patch('builtins.input', return_value='1')
    def test_human_player_move_valid(self, mock_input):
        position = self.player1.make_move(self.board)
        self.assertEqual(position, 0)

    def test_computer_player_move(self):
        position = self.player2.make_move(self.board)
        self.assertIn(position, range(9))
        self.assertTrue(self.board.is_position_empty(position))

    def test_check_winner_horizontal(self):
        self.board._cells = ['X', 'X', 'X'] + [' '] * 6
        self.assertEqual(self.board.check_winner(), 'X')

    def test_check_winner_vertical(self):
        self.board._cells = ['O', ' ', ' '] * 3
        self.board._cells[0] = self.board._cells[3] = self.board._cells[6] = 'O'
        self.assertEqual(self.board.check_winner(), 'O')

    def test_check_winner_diagonal(self):
        self.board._cells = ['X', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X']
        self.assertEqual(self.board.check_winner(), 'X')
        self.board._cells = [' ', ' ', 'O', ' ', 'O', ' ', 'O', ' ', ' ']
        self.assertEqual(self.board.check_winner(), 'O')

    def test_check_no_winner(self):
        self.board._cells = ['X', 'O', 'X', 'X', 'O', 'O', 'O', 'X', 'X']
        self.assertIsNone(self.board.check_winner())

    def test_switch_player(self):
        game = TicTacToeGame(self.player1, self.player2)
        self.assertEqual(game.get_current_player(), self.player1)
        game.switch_player()
        self.assertEqual(game.get_current_player(), self.player2)

    @patch('builtins.open', new_callable=mock_open, read_data='Test1 (X) laimėjo!\n')
    def test_previous_game_result_display(self, mock_file):
        player1 = HumanPlayer("Test1", GameSymbol.X.value)
        player2 = HumanPlayer("Test2", GameSymbol.O.value)
        game = TicTacToeGame(player1, player2)
        with patch('builtins.input', return_value='n'), patch('sys.stdout', new=StringIO()) as fake_out:
            with patch.object(Board, 'is_full', return_value=True), patch.object(Board, 'check_winner', return_value=None):
                game.play()
            self.assertIn("Praeito žaidimo rezultatas:", fake_out.getvalue())


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
