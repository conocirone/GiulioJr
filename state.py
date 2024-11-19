from enum import Enum
import copy
from board import Color
from operator import xor


class Player(Enum):
    MAX = 1
    MIN = 0


class State:

    def __init__(self, board, move, value, color, player, alpha, beta):
        self.board = board
        self.value = value
        self.color = color
        self.player = player
        self.alpha = alpha
        self.beta = beta
        self.move = move  # from: move[0], move[1], to move[1], move[2]
        self.best_move = None
        self.available_moves_iterator = iter(self.board.get_available_moves(self.color))
        self.evaluated = False
    
    def __hash__(self):
        return xor(hash(frozenset(self.board.color_coords[Color.WHITE])), hash(frozenset(self.board.color_coords[Color.BLACK])))
        
    def next_state(self):
        try:
            next_move = next(self.available_moves_iterator)
        except StopIteration:
            return self

        if self.player == Player.MAX:
            child_value = float("inf")
            child_player = Player.MIN
        else:
            child_value = float("-inf")
            child_player = Player.MAX

        if self.color == Color.WHITE:
            child_color = Color.BLACK
        else:
            child_color = Color.WHITE

        return State(
            self.do_move(next_move),
            next_move,
            child_value,
            child_color,
            child_player,
            self.alpha,
            self.beta,
        )

    def do_move(self, move):
        new_board = copy.deepcopy(self.board)
        new_board.move_piece(move)
        return new_board
