import unittest
from features import *


class TestFeatures(unittest.TestCase):

    def test_piece_score(self):
        b = Board()
        b.color_coords[Color.WHITE] = {
            (4, 2),
            (4, 3),
            (2, 4),
            (2, 3),
            (2, 5),
            (2, 6),
            (4, 5),
            (4, 6),
        }
        b.color_coords[Color.BLACK] = {
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
        self.assertEqual(piece_score(b, Color.WHITE), 0)
        self.assertEqual(piece_score(b, Color.BLACK), 0)

        b.color_coords[Color.WHITE] = {(4, 2), (4, 3), (2, 4), (2, 3)}
        # Unbalanced state
        self.assertEqual(piece_score(b, Color.WHITE), -0.5)
        self.assertEqual(piece_score(b, Color.BLACK), 0.5)

    def test_king_safety(self):
        b = Board()
        b.color_coords[Color.KING] = {(4, 4)}

        # King on throne, no close blacks
        self.assertEqual(king_safety(b, Color.WHITE), 1)
        self.assertEqual(king_safety(b, Color.BLACK), -1)

        b.color_coords[Color.BLACK] = {(4, 3)}
        b.coords_color[(4, 3)] = Color.BLACK
        # King on throne, 1 close black
        self.assertEqual(king_safety(b, Color.WHITE), 0.5)
        self.assertEqual(king_safety(b, Color.BLACK), -0.5)

        b.color_coords[Color.BLACK] = {(4, 3), (4, 5)}
        b.coords_color[(4, 5)] = Color.BLACK
        # King on throne, 2 close blacks
        self.assertEqual(king_safety(b, Color.WHITE), 0)
        self.assertEqual(king_safety(b, Color.BLACK), 0)

        b.color_coords[Color.BLACK] = {(4, 3), (4, 5), (3, 4)}
        b.coords_color[(3, 4)] = Color.BLACK
        # King on throne, 3 close blacks
        self.assertEqual(king_safety(b, Color.WHITE), -0.5)
        self.assertEqual(king_safety(b, Color.BLACK), 0.5)

        b.color_coords[Color.KING] = {(5, 4)}
        # King next to throne, no close blacks
        self.assertEqual(king_safety(b, Color.WHITE), 0.5)
        self.assertEqual(king_safety(b, Color.BLACK), -0.5)

        b.color_coords[Color.BLACK] = {(4, 3), (4, 5), (3, 4), (5, 3)}
        b.coords_color[(5, 3)] = Color.BLACK
        # King next to throne, 1 close black
        self.assertEqual(king_safety(b, Color.WHITE), 0)
        self.assertEqual(king_safety(b, Color.BLACK), 0)

        b.color_coords[Color.BLACK] = {(4, 3), (4, 5), (3, 4), (5, 3), (5, 5)}
        b.coords_color[(5, 5)] = Color.BLACK
        # King next to throne, 2 close blacks
        self.assertEqual(king_safety(b, Color.WHITE), -0.5)
        self.assertEqual(king_safety(b, Color.BLACK), 0.5)

        b.color_coords[Color.KING] = {(7, 7)}
        # King in the open, no close blacks
        self.assertEqual(king_safety(b, Color.WHITE), 0)
        self.assertEqual(king_safety(b, Color.BLACK), 0)

        b.color_coords[Color.KING] = {(5, 6)}
        # King in the open, 1 close black
        self.assertEqual(king_safety(b, Color.WHITE), -0.5)
        self.assertEqual(king_safety(b, Color.BLACK), 0.5)

        b.color_coords[Color.KING] = {(4, 6)}
        # King in the open, 1 close black and 1 citadel
        self.assertEqual(king_safety(b, Color.WHITE), -1)
        self.assertEqual(king_safety(b, Color.BLACK), 1)

        b.color_coords[Color.KING] = {(3, 3)}
        # King in the open, 2 close blacks but no capture
        self.assertEqual(king_safety(b, Color.WHITE), -1)
        self.assertEqual(king_safety(b, Color.BLACK), 1)

        b.color_coords[Color.KING] = {(6, 4)}
        # King in the open, 1 citadel
        self.assertEqual(king_safety(b, Color.WHITE), -0.5)
        self.assertEqual(king_safety(b, Color.BLACK), 0.5)

        b.color_coords[Color.KING] = {(7, 5)}
        # King in the open, 2 citadels
        self.assertEqual(king_safety(b, Color.WHITE), -1)
        self.assertEqual(king_safety(b, Color.BLACK), 1)

    def test_capture_king(self):
        b = Board()
        self.assertEqual(capture_king(b, Color.WHITE), float("-inf"))
        self.assertEqual(capture_king(b, Color.BLACK), float("inf"))

    def test_king_free_road(self):
        b = Board()
        b.color_coords[Color.KING] = {(4, 2)}
        # King in empty col
        self.assertEqual(king_free_road(b, Color.WHITE), 100)
        self.assertEqual(king_free_road(b, Color.BLACK), -100)

        b.color_coords[Color.KING] = {(2, 4)}
        # King in empty row
        self.assertEqual(king_free_road(b, Color.WHITE), 100)
        self.assertEqual(king_free_road(b, Color.BLACK), -100)
        
    def test_win_move_king(self):
        b = Board()
        # King on boarder
        b.color_coords[Color.KING] = {(3, 0)}
        self.assertEqual(win_move_king(b, Color.WHITE), float("inf"))
        self.assertEqual(win_move_king(b, Color.BLACK), float("-inf"))

        b.color_coords[Color.KING] = {(0, 5)}
        self.assertEqual(win_move_king(b, Color.WHITE), float("inf"))
        self.assertEqual(win_move_king(b, Color.BLACK), float("-inf"))

    def test_king_distance(self):
        b = Board()
        b.color_coords[Color.KING] = {(3, 3)}
        b.color_coords[Color.BLACK] = {(6, 6)}
        b.coords_color[(6, 6)] = Color.BLACK
        # Free quadrant
        self.assertEqual(king_distance(b, Color.WHITE), -((1.5 - 0.25) / 7.25 * 2 - 1))
        self.assertEqual(king_distance(b, Color.BLACK), ((1.5 - 0.25) / 7.25 * 2 - 1))

        b.color_coords[Color.BLACK] = {(6, 6), (2, 1), (1, 2)}
        b.coords_color[(2, 1)] = Color.BLACK
        b.coords_color[(1, 2)] = Color.BLACK
        # 1 black in quadrant with king
        self.assertEqual(king_distance(b, Color.WHITE), -((2 - 0.25) / 7.25 * 2 - 1))
        self.assertEqual(king_distance(b, Color.BLACK), ((2 - 0.25) / 7.25 * 2 - 1))


if __name__ == "main":
    unittest.main()
