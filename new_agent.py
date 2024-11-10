import copy
import time
from enum import Enum

from agent import Agent

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

class NewAgent(Agent):
    def __init__(self, gateway, timeout, color, board):
        self.gateway = gateway
        self.gateway.set_agent(self)
        self.color = color
        self.board = board
        self.timeout = timeout

        # sends and receives messages
        while True:
            current_state, turn = gateway.get_state()
            if turn == self.color:
                self.board.update(current_state)

                # Define depth, timeout percentage
                start_time = time.time()
                move, n_nodes = self.alphabeta_it(
                    time_limit = time.time() + self.timeout * 0.95, 
                    depth = 10)
                elapsed_time = time.time() - start_time

                print(f"Explored nodes: {n_nodes}")
                # print(f"Time elapsed: {elapsed_time}")
                # print(f"Avg n_nodes/sec: {int(n_nodes/elapsed_time)}")

                conv_move = self.convert_move(move)
                self.gateway.send_state(conv_move)

    def alphabeta_it(self, time_limit, depth):
        root_state = State(self.board, None, float('-inf'), self.color, Player.MAX, float('-inf'), float('inf'))
        L = [root_state]

        n_nodes = 0
        state = root_state

        while not root_state.evaluated:

            if state.evaluated:
                del L[-1]
                parent = L[-1]
                n_nodes += 1

                if parent.player == Player.MAX:
                    if state.value > parent.value:
                        parent.value = state.value
                        parent.best_move = state.move
                    if parent.value >= parent.beta:
                        parent.evaluated = True
                        continue
                    parent.alpha = max(parent.alpha, parent.value)
                else: 
                    if state.value < parent.value:
                        parent.value = state.value
                        parent.best_move = state.move
                    if parent.value <= parent.alpha:
                        parent.evaluated = True
                        continue
                    parent.beta = min(parent.beta, parent.value)

                next_state = parent.next_state()
                if next_state != parent:
                    L.append(next_state)
                else:
                    parent.evaluated = True

            elif len(L) == depth+1 or time.time() >= time_limit:
                state.value = self.eval(state.board)
                state.evaluated = True

            else:
                next_state = state.next_state()
                if next_state != state:
                    L.append(next_state)

            state = L[-1]

        return root_state.best_move, n_nodes
