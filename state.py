from enum import Enum
from copy import deepcopy
from board import Color

from features import win_move_king, capture_king, draw_check


class Player(Enum):
    MAX = 1
    MIN = 0


class State:

    def __init__(self, board, move, value, color, player, alpha, beta, draw_fifo):
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

        ck = capture_king(self.board, self.color)
        if ck != 0:
            self.value = ck
            self.evaluated = True

        wmk = win_move_king(self.board, self.color)
        if wmk != 0:
            self.value = wmk
            self.evaluated = True

        if draw_check(self.board, self.color, draw_fifo):
            self.value = 0
            self.evaluated = True

        # Set state's draw_fifo
        self.draw_fifo = draw_fifo
        if len(self.draw_fifo) == 3:
            self.draw_fifo.pop(0)
        self.draw_fifo.append(self.board.coords_color)

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
            deepcopy(self.draw_fifo),
        )

    @staticmethod
    def do_move(self, move):
        new_board = deepcopy(self.board)
        new_board.move_piece(move)
        return new_board
