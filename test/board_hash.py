from collections import defaultdict
from random import randint

class BoardHash:
    def __init__(self):
        self.__color_coords = defaultdict(set)
        self.__coords_color = {}
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

    def get_available_moves(self, pieces):
        moves = []
        for piece in pieces:
            coords = self.__color_coords[piece]
            for i, j in coords:
                # Horizontal backwards
                for j_back in range(j - 1, -1, -1):
                    if self.__coords_color.get((i, j_back), None) == None and self.is_valid((i, j), (i, j_back)):
                        moves.append((i, j, i, j_back))
                    else:
                        break
                # Horizontal forward
                for j_forward in range(j + 1, 9):
                    if self.__coords_color.get((i, j_forward), None) == None and self.is_valid((i, j), (i, j_forward)):
                        moves.append((i, j, i, j_forward))
                    else:
                        break
                # Vertical backwards
                for i_back in range(i - 1, -1, -1):
                    if self.__coords_color.get((i_back, j), None) == None and self.is_valid((i, j), (i_back, j)):
                        moves.append((i, j, i_back, j))
                    else:
                        break
                # Vertical forward
                for i_forward in range(i + 1, 9):
                    if self.__coords_color.get((i_forward, j), None) == None and self.is_valid((i, j), (i_forward, j)):
                        moves.append((i, j, i_forward, j))
                    else:
                        break
        return moves

    # Test move
    def random_move(self, moves):
        start_i, start_j, end_i, end_j = moves[randint(0,len(moves)-1)]

        # swap
        color = self.__coords_color[(end_i, end_j)] = self.__coords_color[(start_i, start_j)]

        self.__color_coords[color].remove((start_i, start_j))
        self.__color_coords[color].add((end_i, end_j))
        # self.__color_coords[color] ^= {(start_i, start_j), (end_i, end_j)}

        del self.__coords_color[(start_i, start_j)]

    def update(self, board):
        self.__color_coords = defaultdict(set)
        self.__coords_color = {}
        for i in range(9):
            for j in range(9):
                if board[i][j] != 'EMPTY':
                    self.__color_coords[board[i][j]].add((i,j))

        self.__coords_color = {coord:color for color,coords in self.__color_coords.items() for coord in coords}

    def is_valid(self, start_coords, stop_coords):
        start_noenter, stop_noenter = self.__coords_noenter.get(start_coords, None), self.__coords_noenter.get(stop_coords, None)
        if start_noenter == None:                   # checker outside of citadel/throne
            return stop_noenter == None                 # moves to a non-citadel/throne -> True
        elif stop_noenter != None:                  # checker in citadel/throne (wants to move in citadel)
            return start_noenter == stop_noenter        # moves in its own citadel (can't be throne) -> True
        return True                                 # checker moves from citadel/throne to a non-citadel/throne
