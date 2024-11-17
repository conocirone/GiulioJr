import unittest
from board import Board


class TestBoard(unittest.TestCase):
    def test_get_available_moves(self):
        # Initial state
        b = Board()
        b.color_coords["WHITE"] = {
            (4, 2),
            (4, 3),
            (2, 4),
            (3, 4),
            (5, 4),
            (6, 4),
            (4, 5),
            (4, 6),
        }
        for c in b.color_coords["WHITE"]:
            b.coords_color[c] = "WHITE"
        b.color_coords["BLACK"] = {
            (3, 0),
            (4, 0),
            (5, 0),
            (4, 1),
            (0, 3),
            (0, 4),
            (0, 5),
            (1, 4),
            (7, 4),
            (8, 3),
            (8, 4),
            (8, 5),
            (4, 7),
            (3, 8),
            (4, 8),
            (5, 8),
        }
        for c in b.color_coords["BLACK"]:
            b.coords_color[c] = "BLACK"
        b.color_coords["KING"] = {(4, 4)}
        b.coords_color[(4, 4)] = "KING"

        moves_white = b.get_available_moves("WHITE")
        self.assertEqual(len(moves_white), 56)
        self.assertEqual(
            len(set(moves_white)), len(moves_white)
        )  # Duplicate move check

        moves_black = b.get_available_moves("BLACK")
        self.assertEqual(len(moves_black), 80)
        self.assertEqual(
            len(set(moves_white)), len(moves_white)
        )  # Duplicate move check

        # Checking killer moves
        b = Board()
        b.color_coords["KING"] = {(2, 4)}
        b.coords_color[(2, 4)] = "KING"
        b.color_coords["BLACK"] = {(2, 3), (1, 5)}
        b.coords_color[(2, 3)] = "BLACK"
        b.coords_color[(1, 5)] = "BLACK"

        moves_white = b.get_available_moves("WHITE")
        self.assertTrue((2, 4, 2, 8) in moves_white)  # king escape
        self.assertTrue((2, 4, 3, 4) in moves_white)  # king moves to empty row
        self.assertEqual(len(moves_white), 5)

        moves_black = b.get_available_moves("BLACK")
        self.assertTrue((1, 5, 2, 5) in moves_black)  # black captures king
        self.assertEqual(len(moves_black), 18)
