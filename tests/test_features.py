import unittest
from features import *


class TestFeatures(unittest.TestCase):

    def test_piece_score(self):
        b = Board()
        b.color_coords["WHITE"] = {
            (4, 2),
            (4, 3),
            (2, 4),
            (2, 3),
            (2, 5),
            (2, 6),
            (4, 5),
            (4, 6),
        }
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

        # Even state
        self.assertEqual(piece_score(b, "WHITE"), 0)
        self.assertEqual(piece_score(b, "BLACK"), 0)

        b.color_coords["WHITE"] = {(4, 2), (4, 3), (2, 4), (2, 3)}
        # Unbalanced state
        self.assertEqual(piece_score(b, "WHITE"), -0.5)
        self.assertEqual(piece_score(b, "BLACK"), 0.5)

    def test_king_safety(self):
        b = Board()
        b.color_coords["KING"] = {(4, 4)}

        # King on throne, no close blacks
        self.assertEqual(king_safety(b, "WHITE"), 1)
        self.assertEqual(king_safety(b, "BLACK"), -1)

        b.color_coords["BLACK"] = {(4, 3)}
        b.coords_color[(4, 3)] = "BLACK"
        # King on throne, 1 close black
        self.assertEqual(king_safety(b, "WHITE"), 0.5)
        self.assertEqual(king_safety(b, "BLACK"), -0.5)

        b.color_coords["BLACK"] = {(4, 3), (4, 5)}
        b.coords_color[(4, 5)] = "BLACK"
        # King on throne, 2 close blacks
        self.assertEqual(king_safety(b, "WHITE"), 0)
        self.assertEqual(king_safety(b, "BLACK"), 0)

        b.color_coords["BLACK"] = {(4, 3), (4, 5), (3, 4)}
        b.coords_color[(3, 4)] = "BLACK"
        # King on throne, 3 close blacks
        self.assertEqual(king_safety(b, "WHITE"), -0.5)
        self.assertEqual(king_safety(b, "BLACK"), 0.5)

        b.color_coords["KING"] = {(5, 4)}
        # King next to throne, no close blacks
        self.assertEqual(king_safety(b, "WHITE"), 0.5)
        self.assertEqual(king_safety(b, "BLACK"), -0.5)

        b.color_coords["BLACK"] = {(4, 3), (4, 5), (3, 4), (5, 3)}
        b.coords_color[(5, 3)] = "BLACK"
        # King next to throne, 1 close black
        self.assertEqual(king_safety(b, "WHITE"), 0)
        self.assertEqual(king_safety(b, "BLACK"), 0)

        b.color_coords["BLACK"] = {(4, 3), (4, 5), (3, 4), (5, 3), (5, 5)}
        b.coords_color[(5, 5)] = "BLACK"
        # King next to throne, 2 close blacks
        self.assertEqual(king_safety(b, "WHITE"), -0.5)
        self.assertEqual(king_safety(b, "BLACK"), 0.5)

        b.color_coords["KING"] = {(7, 7)}
        # King in the open, no close blacks
        self.assertEqual(king_safety(b, "WHITE"), 0)
        self.assertEqual(king_safety(b, "BLACK"), 0)

        b.color_coords["KING"] = {(5, 6)}
        # King in the open, 1 close black
        self.assertEqual(king_safety(b, "WHITE"), -0.5)
        self.assertEqual(king_safety(b, "BLACK"), 0.5)

        b.color_coords["KING"] = {(4, 6)}
        # King in the open, 1 close black and 1 citadel
        self.assertEqual(king_safety(b, "WHITE"), -1)
        self.assertEqual(king_safety(b, "BLACK"), 1)

        b.color_coords["KING"] = {(3, 3)}
        # King in the open, 2 close blacks but no capture
        self.assertEqual(king_safety(b, "WHITE"), -1)
        self.assertEqual(king_safety(b, "BLACK"), 1)

        b.color_coords["KING"] = {(6, 4)}
        # King in the open, 1 citadel
        self.assertEqual(king_safety(b, "WHITE"), -0.5)
        self.assertEqual(king_safety(b, "BLACK"), 0.5)

        b.color_coords["KING"] = {(7, 5)}
        # King in the open, 2 citadels
        self.assertEqual(king_safety(b, "WHITE"), -1)
        self.assertEqual(king_safety(b, "BLACK"), 1)

    def test_capture_king(self):
        b = Board()
        self.assertEqual(capture_king(b, "WHITE"), float("-inf"))
        self.assertEqual(capture_king(b, "BLACK"), float("inf"))

    def test_win_move_king(self):
        b = Board()
        b.color_coords["KING"] = {(4, 2)}
        # King in empty col
        self.assertEqual(win_move_king(b, "WHITE"), float("inf"))
        self.assertEqual(win_move_king(b, "BLACK"), float("-inf"))

        b.color_coords["KING"] = {(2, 4)}
        # King in empty row
        self.assertEqual(win_move_king(b, "WHITE"), float("inf"))
        self.assertEqual(win_move_king(b, "BLACK"), float("-inf"))

        # King on boarder
        b.color_coords["KING"] = {(3, 0)}
        self.assertEqual(win_move_king(b, "WHITE"), float("inf"))
        self.assertEqual(win_move_king(b, "BLACK"), float("-inf"))

        b.color_coords["KING"] = {(0, 5)}
        self.assertEqual(win_move_king(b, "WHITE"), float("inf"))
        self.assertEqual(win_move_king(b, "BLACK"), float("-inf"))


if __name__ == "main":
    unittest.main()
