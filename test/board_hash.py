from collections import defaultdict
from random import randint

class BoardHash:
    def __init__(self):
        self.color_coords = {}
        self.coords_color = {}

    def get_available_moves(self, pieces):
        moves = []
        for piece in pieces:
            coords = self.color_coords[piece]
            for i, j in coords:
                # Horizontal backwards
                for j_back in range(j - 1, -1, -1):
                    if self.coords_color.get((i, j_back), None) == None and self.is_valid((i, j), (i, j_back)):
                        moves.append((i, j, i, j_back))
                    else:
                        break
                # Horizontal forward
                for j_forward in range(j + 1, 9):
                    if self.coords_color.get((i, j_forward), None) == None and self.is_valid((i, j), (i, j_forward)):
                        moves.append((i, j, i, j_forward))
                    else:
                        break
                # Vertical backwards
                for i_back in range(i - 1, -1, -1):
                    if self.coords_color.get((i_back, j), None) == None and self.is_valid((i, j), (i_back, j)):
                        moves.append((i, j, i_back, j))
                    else:
                        break
                # Vertical forward
                for i_forward in range(i + 1, 9):
                    if self.coords_color.get((i_forward, j), None) == None and self.is_valid((i, j), (i_forward, j)):
                        moves.append((i, j, i_forward, j))
                    else:
                        break
        return moves

    # Test move
    def random_move(self, moves):
        start_i, start_j, end_i, end_j = moves[randint(0,len(moves)-1)]

        # swap
        color = self.coords_color[(end_i, end_j)] = self.coords_color[(start_i, start_j)]

        self.color_coords[color].remove((start_i, start_j))
        self.color_coords[color].add((end_i, end_j))
        # self.color_coords[color] ^= {(start_i, start_j), (end_i, end_j)}

        del self.coords_color[(start_i, start_j)]

    def update(self, board):
        self.color_coords = defaultdict(set)
        for i in range(9):
            for j in range(9):
                if board[i][j] != 'EMPTY':
                    self.color_coords[board[i][j]].add((i,j))

        self.coords_color = {coord:color for color,coords in self.color_coords.items() for coord in coords}

    def is_valid(self, coords_beg, coords_end):
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
        if coords_end in citadels:
            if coords_beg in citadels:
                return True
            else:
                return False
        else:
            return True
        # return (not (coords_end in citadels)) or (coords_beg in citadels)
