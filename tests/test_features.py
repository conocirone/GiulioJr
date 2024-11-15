import unittest
from features import *


class TestFeatures(unittest.TestCase):

    def test_piece_score(self):
        b = Board()
        b.color_coords["KING"] = {(4, 4)}
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


if __name__ == "main":
    unittest.main()
