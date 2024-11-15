from collections import defaultdict


class Board:
    __coords_noenter = { # TODO: make static
        (3, 0): "L",  # left citadels
        (4, 0): "LC",
        (5, 0): "L",
        (4, 1): "L",
        (3, 8): "R",  # right citadels
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

    history_table = {'WHITE':{}, 'BLACK':{}} # {COLOR: {move: value}}

    def __init__(self):
        self.color_coords = defaultdict(set)  # BLACK|WHITE|KING -> {(i,j), ...}
        self.coords_color = {}  # (i,j) -> BLACK|WHITE|KING

    def get_available_moves(self, color):
        if color == "WHITE":
            pieces = ("KING", "WHITE")
        else:
            pieces = ("BLACK",)
        
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

        if color == "WHITE" or color == "KING":
            color = "WHITEKING"
        else:
            color = "BLACK"
        
        self.check_capture(color, stop_row, stop_col, 0, 1)  # Right capture
        self.check_capture(color, stop_row, stop_col, 0, -1)  # Left capture
        self.check_capture(color, stop_row, stop_col, -1, 0)  # Top capture
        self.check_capture(color, stop_row, stop_col, 1, 0)  # Down capture
        
    
    def check_capture(self, color, stop_row, stop_col, inc_row, inc_col):
        # Check and capture pieces
        next_coords = (stop_row + inc_row, stop_col + inc_col)
        next_next_coords = (stop_row + (inc_row * 2), stop_col + (inc_col*2))
        next_square = self.coords_color.get(next_coords, "EMPTY")

        if color == 'BLACK' and next_square == 'KING' and 4 in next_coords:
            required_for_capture = 2
            if next_coords == (4,4): # king on throne
                required_for_capture = 4
            else:
                required_for_capture = 3
            
            close_blacks = 0
            if (
                self.coords_color.get((next_coords[0] - 1, next_coords[1]), None)
                == "BLACK"
            ):  # Up square check
                close_blacks += 1
            if (
                self.coords_color.get((next_coords[0] + 1, next_coords[1]), None)
                == "BLACK"
            ):  # Down square check
                close_blacks += 1
            if (
                self.coords_color.get((next_coords[0], next_coords[1] - 1), None)
                == "BLACK"
            ):  # Left square check
                close_blacks += 1
            if (
                self.coords_color.get((next_coords[0], next_coords[1] + 1), None)
                == "BLACK"
            ):  # Right square check
                close_blacks += 1
            if required_for_capture - close_blacks == 0:
                del self.coords_color[next_coords]
                self.color_coords[next_square].remove(next_coords)
                

        elif next_square not in color and next_square not in "EMPTY":
            next_next_square = self.coords_color.get(next_next_coords, "EMPTY")
            if next_next_square in "EMPTY":
                # next_next_square is not checker, reassigned next_next to possible citadel
                next_next_square = self.__coords_noenter.get(next_next_coords, "EMPTY")
            if next_next_square in color or (
                next_next_square not in "EMPTY" and len(next_next_square) == 1
            ):
                del self.coords_color[next_coords]
                self.color_coords[next_square].remove(next_coords)


    def get_king_coords(self):
        # Returns king position tuple
        temp = self.color_coords["KING"].copy()
        try:
            return temp.pop()
        except KeyError:
            return None
