import numpy as np
from random import randint

class Board:
    def __init__(self):
        self.__matrix = np.ndarray((9,9))
        # camps + throne
        self.__coords_noenter = { 
            (3, 0):'L', # left citadels
            (4, 0):'L',
            (5, 0):'L',
            (4, 1):'L', 

            (3, 8):'R', # right citades
            (4, 8):'R',
            (5, 8):'R',
            (4, 7):'R', 

            (0, 3):'U', # upper citadels
            (0, 4):'U',
            (0, 5):'U',
            (1, 4):'U',

            (8, 3):'D', # lower citadels
            (8, 4):'D',
            (8, 5):'D',
            (7, 4):'D',

            (4, 4):'T'  # throne
        }

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
                        if self.__matrix[i, j_back] == "EMPTY" and self.is_valid((i, j), (i, j_back)):
                            moves.append((i, j, i, j_back))
                        else:
                            break
                    # Horizontal forward
                    for j_forward in range(j + 1, 9):
                        if self.__matrix[i, j_forward] == "EMPTY" and self.is_valid((i, j), (i, j_forward)):
                            moves.append((i, j, i, j_forward))
                        else:
                            break
                    # Vertical backwards
                    for i_back in range(i - 1, -1, -1):
                        if self.__matrix[i_back, j] == "EMPTY" and self.is_valid((i, j), (i_back, j)):
                            moves.append((i, j, i_back, j))
                        else:
                            break
                    # Vertical forward
                    for i_forward in range(i + 1, 9):
                        if self.__matrix[i_forward, j] == "EMPTY" and self.is_valid((i, j), (i_forward, j)):
                            moves.append((i, j, i_forward, j))
                        else:
                            break
        return moves

    def random_move(self, moves):
        start_i, start_j, end_i, end_j = moves[randint(0,len(moves)-1)]
        # swap
        self.__matrix[end_i, end_j], self.__matrix[start_i, start_j] = self.__matrix[start_i, start_j], self.__matrix[end_i, end_j]

    # function to update the state of the board
    def update(self, board):
        self.__matrix = np.array(board)

    def is_valid(self, start_coords, stop_coords):
        start_noenter, stop_noenter = self.__coords_noenter.get(start_coords, None), self.__coords_noenter.get(stop_coords, None)
        if start_noenter == None:                   # checker outside of citadel/throne
            return stop_noenter == None                 # moves to a non-citadel/non-throne -> True
        elif stop_noenter != None:                  # checker in citadel/throne (wants to move in citadel)
            return start_noenter == stop_noenter        # moves in its own citadel (can't be throne) -> True
        return True                                 # checker moves from citadel/throne to a non-citadel/non-throne

