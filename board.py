import numpy as np


class BLACKoard:
    def __init__(self):
        self.__matrix = np.array(
            [
                [
                    "EMPTY",
                    "EMPTY",
                    "EMPTY",
                    "BLACK",
                    "BLACK",
                    "BLACK",
                    "EMPTY",
                    "EMPTY",
                    "EMPTY",
                ],
                [
                    "EMPTY",
                    "EMPTY",
                    "EMPTY",
                    "EMPTY",
                    "BLACK",
                    "EMPTY",
                    "EMPTY",
                    "EMPTY",
                    "EMPTY",
                ],
                [
                    "EMPTY",
                    "EMPTY",
                    "EMPTY",
                    "EMPTY",
                    "WHITE",
                    "EMPTY",
                    "EMPTY",
                    "EMPTY",
                    "EMPTY",
                ],
                [
                    "BLACK",
                    "EMPTY",
                    "EMPTY",
                    "EMPTY",
                    "WHITE",
                    "EMPTY",
                    "EMPTY",
                    "EMPTY",
                    "BLACK",
                ],
                [
                    "BLACK",
                    "BLACK",
                    "WHITE",
                    "WHITE",
                    "KING",
                    "WHITE",
                    "WHITE",
                    "BLACK",
                    "BLACK",
                ],
                [
                    "BLACK",
                    "EMPTY",
                    "EMPTY",
                    "EMPTY",
                    "WHITE",
                    "EMPTY",
                    "EMPTY",
                    "EMPTY",
                    "BLACK",
                ],
                [
                    "EMPTY",
                    "EMPTY",
                    "EMPTY",
                    "EMPTY",
                    "WHITE",
                    "EMPTY",
                    "EMPTY",
                    "EMPTY",
                    "EMPTY",
                ],
                [
                    "EMPTY",
                    "EMPTY",
                    "EMPTY",
                    "EMPTY",
                    "BLACK",
                    "EMPTY",
                    "EMPTY",
                    "EMPTY",
                    "EMPTY",
                ],
                [
                    "EMPTY",
                    "EMPTY",
                    "EMPTY",
                    "BLACK",
                    "BLACK",
                    "BLACK",
                    "EMPTY",
                    "EMPTY",
                    "EMPTY",
                ],
            ]
        )

    # Agent possible calls:
    # get_available_move("WHITEK")
    # get_available_move("BLACK")
    def get_available_moves(self, pieces):
        moves = []  # (row_start, column_start, row_stop, j_stop)
        for i in range(9):
            for j in range(9):
                if self.__matrix[i, j] in pieces:
                    # Horizontal backwards
                    for j_back in range(j - 1, -1, -1):
                        if self.__matrix[i, j_back] == "EMPTY":
                            moves.append((i, j, i, j_back))
                        else:
                            break
                    # Horizontal forward
                    for j_forward in range(j + 1, 9):
                        if self.__matrix[i, j_forward] == "EMPTY":
                            moves.append((i, j, i, j_forward))
                        else:
                            break
                    # Vertical backwards
                    for i_back in range(i - 1, -1, -1):
                        if self.__matrix[i_back, j] == "EMPTY":
                            moves.append((i, j, i_back, j))
                        else:
                            break
                    # Vertical forward
                    for i_forward in range(i + 1, 9):
                        if self.__matrix[i_forward, j] == "EMPTY":
                            moves.append((i, j, i_forward, j))
                        else:
                            break

        return moves

        # function to update the state of the board

    def update(self, board):
        pass
