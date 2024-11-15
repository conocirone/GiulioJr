from enum import Enum
import copy

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
        self.move = move
        self.best_move = None
        self.available_moves_iterator = iter(self.board.get_available_moves(self.color))
        self.evaluated = False

    def next_state(self):
        try:
            move = next(self.available_moves_iterator)
        except StopIteration:
            return self

        if self.player == Player.MAX:
            child_value = float('inf')
            child_player = Player.MIN
        else:
            child_value = float('-inf')
            child_player = Player.MAX

        if self.color == 'WHITE':
            child_color = 'BLACK'
        else:
            child_color = 'WHITE'
        return State(self.do_move(move), move, child_value, child_color, child_player, self.alpha, self.beta)

    def do_move(self, move):
        new_board = copy.deepcopy(self.board)
        new_board.move_piece(move)
        return new_board
    
    def __repr__(self):
        if self.player == Player.MAX:
            return f"MAX|alpha:{self.alpha}|beta:{self.beta}|value:{self.value}"
        return f"MIN|alpha:{self.alpha}|beta:{self.beta}|value:{self.value}"
