import numpy as np


class Board:
    def __init__(self):
        self.__matrix = None

    # Agent possible calls:
    # get_available_move("WHITEKING")
    # get_available_move("BLACK")
    def get_available_moves(self, pieces):
        moves = []  # (row_start, column_start, row_stop, j_stop)
        for i in range(9):
            for j in range(9):
                if self.__matrix[i, j] in pieces:
                    # Horizontal backwards
                    for j_back in range(j - 1, -1, -1):
                        if self.__matrix[i, j_back] == "EMPTY" and self.is_valid(
                            i, j, i, j_back
                        ):
                            moves.append((i, j, i, j_back))
                        else:
                            break
                    # Horizontal forward
                    for j_forward in range(j + 1, 9):
                        if self.__matrix[i, j_forward] == "EMPTY" and self.is_valid(
                            i, j, i, j_forward
                        ):
                            moves.append((i, j, i, j_forward))
                        else:
                            break
                    # Vertical backwards
                    for i_back in range(i - 1, -1, -1):
                        if self.__matrix[i_back, j] == "EMPTY" and self.is_valid(
                            i, j, i_back, j
                        ):
                            moves.append((i, j, i_back, j))
                        else:
                            break
                    # Vertical forward
                    for i_forward in range(i + 1, 9):
                        if self.__matrix[i_forward, j] == "EMPTY" and self.is_valid(
                            i, j, i_forward, j
                        ):
                            moves.append((i, j, i_forward, j))
                        else:
                            break
        return moves

    # function to update the state of the board
    def update(self, board):
        self.__matrix = np.array(board)
        print(self.__matrix)

    def is_valid(self, row_start, column_start, row_stop, column_stop):
        # cittadels + throne
        citadels = (
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
        if (row_stop, column_stop) in citadels:
            if (row_start, column_start) in citadels:
                return True
            else:
                return False
        else:
            return True
