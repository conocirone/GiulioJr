from collections import defaultdict


class Board:
    def __init__(self):
        self.color_coords = defaultdict(set)  # BLACK|WHITE|KING -> {(i,j), ...}
        self.coords_color = {}  # (i,j) -> BLACK|WHITE|KING
        self.__coords_noenter = { # TODO: make static
            (3, 0): "L",  # left citadels
            (4, 0): "LC",
            (5, 0): "L",
            (4, 1): "L",
            (3, 8): "R",  # right citades
            (4, 8): "RC",
            (5, 8): "R",
            (4, 7): "R",
            (0, 3): "U",  # upper citadels
            (0, 4): "UC",
            (0, 5): "U",
            (1, 4): "U",
            (8, 3): "D",  # lower citadels
            (8, 4): "DC",
            (8, 5): "D",
            (7, 4): "D",
            (4, 4): "T",  # throne
        }

    def get_available_moves(self, color):
        if color == "WHITE":
            pieces = ("WHITE", "KING")
        else:
            pieces = ("BLACK",)

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
        return moves

    # Updates board state
    def update(self, board):
        self.color_coords = defaultdict(
            set
        )  # BLACK|WHITE|KING -> {(i,j), ...} (str   -> set(tuple))
        self.coords_color = {}  # (i,j) -> BLACK|WHITE|KING        (tuple -> str       )
        for i in range(9):
            for j in range(9):
                if board[i][j] != "EMPTY":
                    self.color_coords[board[i][j]].add((i, j))

        self.coords_color = {
            coord: color
            for color, coords in self.color_coords.items()
            for coord in coords
        }

    # Checks if move is valid
    def is_valid(self, start_coords, stop_coords):
        start_noenter, stop_noenter = self.__coords_noenter.get(
            start_coords, None
        ), self.__coords_noenter.get(stop_coords, None)
        if start_noenter == None:  # checker outside of citadel/throne
            return stop_noenter == None  # moves to a non-citadel/non-throne -> True
        elif (
            stop_noenter != None
        ):  # checker in citadel/throne (wants to move in citadel)
            return (
                start_noenter[0] == stop_noenter[0]
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

        if color == "WHITE":
            color = "WHITEKING"
        else:
            color = "BLACK"
            
        # check right
        right_square = self.coords_color.get((stop_row, stop_col + 1), "EMPTY")
        if right_square not in color and right_square not in "EMPTY":
            right_right_square = self.coords_color.get((stop_row, stop_col + 2), "EMPTY")
            if right_right_square in "EMPTY":
                # right_right_square is not checker, reassigned right_right to possible citadel
                right_right_square = self.__coords_noenter.get(
                    (stop_row, stop_col + 2), "EMPTY"
                )
            if right_right_square in color or (
                right_right_square not in "EMPTY" and len(right_right_square) == 1
            ):
                del self.coords_color[(stop_row, stop_col + 1)]
                self.color_coords[right_square].remove((stop_row, stop_col + 1))

        # check left
        left_square = self.coords_color.get((stop_row, stop_col - 1), "EMPTY")
        if left_square not in color and left_square not in "EMPTY":
            left_left_square = self.coords_color.get((stop_row, stop_col - 2), "EMPTY")
            if left_left_square in "EMPTY":
                # left_left_square is not checker, reassigned left_left to possible citadel
                left_left_square = self.__coords_noenter.get(
                    (stop_row, stop_col - 2), "EMPTY"
                )

            if left_left_square in color or (
                left_left_square not in "EMPTY" and len(left_left_square) == 1
            ):
                del self.coords_color[(stop_row, stop_col - 1)]
                self.color_coords[left_square].remove((stop_row, stop_col - 1))

        # check top
        top_square = self.coords_color.get((stop_row - 1, stop_col), "EMPTY")
        if top_square not in color and top_square not in "EMPTY":
            top_top_square = self.coords_color.get((stop_row - 2, stop_col), "EMPTY")
            if top_top_square in "EMPTY":
                # top_top_square is not a checker, reassigned top_top to possible citadel
                top_top_square = self.__coords_noenter.get(
                    (stop_row - 2, stop_col), "EMPTY"
                )

            if top_top_square in color or (
                top_top_square not in "EMPTY" and len(top_top_square) == 1
            ):
                del self.coords_color[(stop_row - 1, stop_col)]
                self.color_coords[top_square].remove((stop_row - 1, stop_col))

        # check do
        down_square = self.coords_color.get((stop_row + 1, stop_col), "EMPTY")
        if down_square not in color and down_square not in "EMPTY":
            down_down_square = self.coords_color.get((stop_row + 2, stop_col), "EMPTY")
            if down_down_square in "EMPTY":
                # down_down_square is not checker, reassigned down_down to possible citadel
                down_down_square = self.__coords_noenter.get(
                    (stop_row + 2, stop_col), "EMPTY"
                )

            if down_down_square in color or (
                down_down_square not in "EMPTY" and len(down_down_square) == 1
            ):
                del self.coords_color[(stop_row + 1, stop_col)]
                self.color_coords[down_square].remove((stop_row + 1, stop_col))

    def get_king_coords(self):
        # Returns king position tuple
        temp = self.color_coords["KING"].copy()
        try:
            return temp.pop()
        except KeyError:
            return None
