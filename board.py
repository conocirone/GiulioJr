import numpy as np


class Board:
    def __init__(self):
        self.__matrix = None

    def get_available_moves(self, color):
        if color == "WHITE":
            pieces = ["WHITE", "KING"]
        else:
            pieces = ["BLACK"]

        moves = []  # (row_start, column_start, row_stop, column_stop)
        for i in range(9):
            for j in range(9):
                if self.__matrix[i, j] in pieces:
                    # Horizontal backwards
                    for j_back in range(j - 1, -1, -1):
                        if self.is_valid(i, j, i, j_back):
                            moves.append((i, j, i, j_back))
                        else:
                            break
                    # Horizontal forward
                    for j_forward in range(j + 1, 9):
                        if self.is_valid(i, j, i, j_forward):
                            moves.append((i, j, i, j_forward))
                        else:
                            break
                    # Vertical backwards
                    for i_back in range(i - 1, -1, -1):
                        if self.is_valid(i, j, i_back, j):
                            moves.append((i, j, i_back, j))
                        else:
                            break
                    # Vertical forward
                    for i_forward in range(i + 1, 9):
                        if self.is_valid(i, j, i_forward, j):
                            moves.append((i, j, i_forward, j))
                        else:
                            break
        return moves

    # Updates board state
    def update(self, board):
        self.__matrix = np.array(board)

    # Checks if move is valid
    def is_valid(self, row_start, column_start, row_stop, column_stop):
        if self.__matrix[row_stop, column_stop] != "EMPTY":
            return False

        # camps + throne
        non_enter_cells = (
            (0, 3),
            (0, 4),
            (0, 5),
            (1, 4),
            (3, 0),
            (4, 0),
            (5, 0),
            (4, 1),
            (8, 3),
            (8, 4),
            (8, 5),
            (7, 4),
            (3, 8),
            (4, 8),
            (5, 8),
            (4, 7),
            (4, 4),
        )
        if (row_stop, column_stop) in non_enter_cells:
            if (row_start, column_start) in non_enter_cells:  # Black checker exception
                return True
            else:
                return False
        else:
            return True

    def move_piece(self, move):
        piece =  self.__matrix[move[0], move[1]]
        self.__matrix[move[0], move[1]] = "EMPTY" 
        self.__matrix[move[2], move[3]] = piece