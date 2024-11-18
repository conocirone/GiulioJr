from collections import defaultdict
from enum import IntEnum


class Citadels(IntEnum):
    L = 10
    LC = 11

    R = 20
    RC = 21

    U = 30
    UC = 31

    D = 40
    DC = 41

    T = 50


class Color(IntEnum):
    WHITE = 0
    BLACK = 1
    KING = 2
    EMPTY = 3


class Board:
    coords_noenter = {
        (3, 0): Citadels.L,  # left citadels
        (4, 0): Citadels.LC,
        (5, 0): Citadels.L,
        (4, 1): Citadels.L,
        (3, 8): Citadels.R,  # right citadels
        (4, 8): Citadels.RC,
        (5, 8): Citadels.R,
        (4, 7): Citadels.R,
        (0, 3): Citadels.U,  # upper citadels
        (0, 4): Citadels.UC,
        (0, 5): Citadels.U,
        (1, 4): Citadels.U,
        (8, 3): Citadels.D,  # lower citadels
        (8, 4): Citadels.DC,
        (8, 5): Citadels.D,
        (7, 4): Citadels.D,
        (4, 4): Citadels.T,  # throne
    }

    history_table = {Color.WHITE: {}, Color.BLACK: {}}  # {COLOR: {move: value}}

    def __init__(self):
        self.color_coords = defaultdict(set)  # BLACK|WHITE|KING -> {(i,j), ...}
        self.coords_color = {}  # (i,j) -> BLACK|WHITE|KING

    def get_available_moves(self, color):
        if color == Color.WHITE:
            pieces = (Color.KING, Color.WHITE)
        else:
            pieces = (Color.BLACK,)

        # for move, value in  self.history_table[color].items():
        #     from_move = (move[0], move[1])

        #     if color == 'WHITE' and (from_move in self.color_coords['KING'] or :

        moves = []
        for piece in pieces:
            coords = self.color_coords[piece]
            for i, j in coords:
                # Horizontal backwards
                for j_back in range(j - 1, -1, -1):
                    if self.coords_color.get(
                        (i, j_back), None
                    ) is None and self.is_valid(
                        (i, j), (i, j_back)
                    ):  # before calling function, check if destination coord is empty
                        moves.append((i, j, i, j_back))
                    else:
                        break
                # Horizontal forward
                for j_forward in range(j + 1, 9):
                    if self.coords_color.get(
                        (i, j_forward), None
                    ) is None and self.is_valid((i, j), (i, j_forward)):
                        moves.append((i, j, i, j_forward))
                    else:
                        break
                # Vertical backwards
                for i_back in range(i - 1, -1, -1):
                    if self.coords_color.get(
                        (i_back, j), None
                    ) is None and self.is_valid((i, j), (i_back, j)):
                        moves.append((i, j, i_back, j))
                    else:
                        break
                # Vertical forward
                for i_forward in range(i + 1, 9):
                    if self.coords_color.get(
                        (i_forward, j), None
                    ) is None and self.is_valid((i, j), (i_forward, j)):
                        moves.append((i, j, i_forward, j))
                    else:
                        break

        heuristic_moves = []

        i = 0
        while i < len(moves):
            move = moves[i]
            if move in self.history_table[color]:
                heuristic_moves.append((move, self.history_table[color][move]))
                del moves[i]
            else:
                i += 1

        heuristic_moves.sort(key=lambda x: x[1], reverse=True)
        sorted_moves = [move[0] for move in heuristic_moves] + moves

        return sorted_moves

    # Updates board state
    def update(self, board):
        self.color_coords = defaultdict(
            set
        )  # BLACK|WHITE|KING -> {(i,j), ...} (str   -> set(tuple))
        self.coords_color = {}  # (i,j) -> BLACK|WHITE|KING        (tuple -> str       )
        for i in range(9):
            for j in range(9):
                if board[i][j] == "WHITE":
                    self.color_coords[Color.WHITE].add((i, j))
                elif board[i][j] == "BLACK":
                    self.color_coords[Color.BLACK].add((i, j))
                elif board[i][j] == "KING":
                    self.color_coords[Color.KING].add((i, j))

        self.coords_color = {
            coord: color
            for color, coords in self.color_coords.items()
            for coord in coords
        }

    # Checks if move is valid
    def is_valid(self, start_coords, stop_coords):
        start_noenter, stop_noenter = self.coords_noenter.get(
            start_coords, None
        ), self.coords_noenter.get(stop_coords, None)
        if start_noenter is None:  # checker outside of citadel/throne
            return stop_noenter is None  # moves to a non-citadel/non-throne -> True
        elif (
            stop_noenter != None
        ):  # checker in citadel/throne (wants to move in citadel)
            return (
                start_noenter == stop_noenter or abs(start_noenter - stop_noenter) == 1
            )  # moves in its own citadel (can't be throne) -> True
        return True  # checker moves from citadel/throne to a non-citadel/non-throne

    def move_piece(self, move):
        stop_row, stop_col = move[2], move[3]
        # start updating __coords_color
        color = self.coords_color[(stop_row, stop_col)] = self.coords_color[
            (move[0], move[1])
        ]

        # update __color_coords
        self.color_coords[color].remove((move[0], move[1]))
        self.color_coords[color].add((stop_row, stop_col))

        # end updating __coords_color
        del self.coords_color[(move[0], move[1])]

        if color != Color.BLACK:
            color = Color.WHITE

        self.check_capture(color, stop_row, stop_col, 0, 1)  # Right capture
        self.check_capture(color, stop_row, stop_col, 0, -1)  # Left capture
        self.check_capture(color, stop_row, stop_col, -1, 0)  # Top capture
        self.check_capture(color, stop_row, stop_col, 1, 0)  # Down capture

    def check_capture(self, color, stop_row, stop_col, inc_row, inc_col):
        # Check and capture pieces
        next_coords = (stop_row + inc_row, stop_col + inc_col)
        next_next_coords = (stop_row + (inc_row * 2), stop_col + (inc_col * 2))
        next_square = self.coords_color.get(next_coords, Color.EMPTY)

        if (
            color == Color.BLACK
            and next_square == Color.KING
            and next_coords in ((4, 4), (5, 4), (4, 5), (4, 3), (3, 4))
        ):
            if next_coords == (4, 4):  # king on throne
                required_for_capture = 4
            else:
                required_for_capture = 3

            close_blacks = 0
            if (
                self.coords_color.get((next_coords[0] - 1, next_coords[1]), None)
                == Color.BLACK
            ):  # Up square check
                close_blacks += 1
            if (
                self.coords_color.get((next_coords[0] + 1, next_coords[1]), None)
                == Color.BLACK
            ):  # Down square check
                close_blacks += 1
            if (
                self.coords_color.get((next_coords[0], next_coords[1] - 1), None)
                == Color.BLACK
            ):  # Left square check
                close_blacks += 1
            if (
                self.coords_color.get((next_coords[0], next_coords[1] + 1), None)
                == Color.BLACK
            ):  # Right square check
                close_blacks += 1
            if required_for_capture - close_blacks == 0:
                del self.coords_color[next_coords]
                self.color_coords[next_square].remove(next_coords)

        # color in Color.WHITE, Color.BLACK
        # next_square in Color.WHITE, Color.BLACK, Color.KING, Color.EMPTY
        elif next_square != Color.EMPTY and color == 1 - (next_square % 2):
            next_next_square = self.coords_noenter.get(
                next_next_coords, self.coords_color.get(next_next_coords, Color.EMPTY)
            )  # will be a citadel, pawn or empty
            if next_next_square == color or next_next_square in (
                Citadels.L,
                Citadels.R,
                Citadels.D,
                Citadels.U,
                Citadels.T,
            ):
                if next_square == Color.KING and (0 in next_coords or 8 in next_coords):
                    return  # Removes problem of king being captured after escape
                else:
                    del self.coords_color[next_coords]
                    self.color_coords[next_square].remove(next_coords)

    def get_king_coords(self):
        # Returns king position tuple
        temp = self.color_coords[Color.KING].copy()
        try:
            return temp.pop()
        except KeyError:
            return None
