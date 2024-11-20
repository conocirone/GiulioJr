import time
import copy


from board import Board
from features import (
    piece_score,
    king_safety,
    win_move_king,
    capture_king,
    king_distance,
)
from state import State, Player
import random


class Agent:
    def __init__(self, gateway, timeout, color, board):
        self.gateway = gateway
        self.gateway.set_agent(self)
        self.color = color
        self.board = board
        self.timeout = timeout
        #initialize with random values
        self.transposition_table = {}
        self.transposition_table_size = 2**22
        self.nodes = 0
        self.cache_hits = 0

        # sends and receives messages
        while True:
            current_state, turn = gateway.get_state()
            if turn == self.color.name:
                self.board.update(current_state)

                # Define depth, timeout percentage
                move = self.iterative_deepening(time.time() + self.timeout * 0.95)

                conv_move = self.convert_move(move)
                self.gateway.send_state(conv_move)

    def convert_move(self, move):
        """converts move indexes from integers to board format (letter-number)

        Args:
            move (tuple): (row_start, column_start, row_stop, column_stop)

        Returns:
            tuple: (starting_position, ending_position)
        """
        return chr(move[1] + 97) + str(move[0] + 1), chr(move[3] + 97) + str(
            move[2] + 1
        )
    

    def put_in_transposition_table(self, key, search_depth, move, value, color, flag):
        if len(self.transposition_table) >= self.transposition_table_size:
            print("transposition table full")
            self.transposition_table.popitem()
        if (key, color) in self.transposition_table.keys():
            if self.transposition_table[(key, color)][0] < search_depth:
                print("overwriting entry")
                self.transposition_table[(key, color)] = [search_depth, move, value, flag]
        

    def get_from_tansposition_table(self, key, search_depth, alpha, beta, color):
        if (key, color) in self.transposition_table.keys():
            t_entry = self.transposition_table[(key, color)]
            self.cache_hits += 1
            if t_entry[0] >= search_depth:
                if t_entry[3] == "EXACT":
                    return t_entry[2]
                elif t_entry[3] == "ALPHA" and t_entry[2] <= alpha:
                    return alpha
                elif t_entry[3] == "BETA" and t_entry[2] >= beta:
                    return beta
        return None
                
    
    def iterative_deepening(self, time_limit):
        depth = 1
        best_move = None
        while time.time() < time_limit:
            move, value = self.alphabeta_it(time_limit=time_limit, depth=depth)
            if move is not None:
                best_move = move
                depth += 1
                print(f"{self.color.name}: depth: {depth}, value: {value}")
                
        if best_move is None:
            best_move = self.board.get_available_moves(self.color)[0]
        
        print(f'Number of explored nodes: {self.nodes}')
        print(f'Number of cache hits: {self.cache_hits}')
        return best_move

    def alphabeta_it(self, time_limit, depth):
        root_state = State(
            self.board,
            None,
            float("-inf"),
            self.color,
            Player.MAX,
            float("-inf"),
            float("inf"),
        )
        L = [root_state]
        
        while not root_state.evaluated:
            
            state = L[-1]
            
            
            if state.evaluated:
                del L[-1]
                parent = L[-1]

                if parent.player == Player.MAX:
                    if state.value > parent.value:
                        parent.value = state.value
                        parent.best_move = state.move
                    parent.alpha = max(parent.alpha, parent.value)
                    if parent.alpha >= parent.beta:
                        #beta cut-off
                        Board.history_table[parent.color][parent.best_move] = (
                            Board.history_table[parent.color].get(parent.best_move, 0)
                            + 2 ** (depth - len(L) - 1)
                        )
                        parent.evaluated = True
                        self.put_in_transposition_table(parent.__hash__(), (len(L) - 1), parent.move, parent.value, parent.color, "BETA")
                        continue
                else:
                    if state.value < parent.value:
                        parent.value = state.value
                        parent.best_move = state.move
                    parent.beta = min(parent.beta, parent.value)
                    if parent.alpha >= parent.beta:
                        #alpha cut-off
                        Board.history_table[parent.color][parent.best_move] = (
                            Board.history_table[parent.color].get(parent.best_move, 0)
                            + 2 ** (depth - len(L) - 1)
                        )
                        parent.evaluated = True
                        self.put_in_transposition_table(parent.__hash__(), (len(L) - 1), parent.move, parent.value, parent.color, "ALPHA")
                        continue

                next_state = parent.next_state()
                if next_state != parent:
                    L.append(next_state)
                else:
                    parent.evaluated = True
                    Board.history_table[parent.color][parent.best_move] = (
                        Board.history_table[parent.color].get(parent.best_move, 0)
                        + 2 ** (depth - len(L) - 1)
                    )
                    self.put_in_transposition_table(parent.__hash__(), (len(L) - 1), parent.move, parent.value, parent.color, "EXACT")

            elif len(L) == depth + 1:
                state.value = self.eval(state.board)
                self.put_in_transposition_table(state.__hash__(), len(L) - 1, state.move, state.value, state.color, "EXACT")
                state.evaluated = True
                self.nodes += 1
                

            elif time.time() >= time_limit:
                return None, None

            else:
                next_state = state.next_state()
                if next_state != state:
                    L.append(next_state)
            
            
            state_key = state.__hash__()  
            corresponding_entry = self.get_from_tansposition_table(state_key, depth, state.alpha, state.beta, state.color)
            if corresponding_entry is not None:
               state.evaluated = True
               state.value = corresponding_entry
            
        return root_state.best_move, root_state.value

    def eval(self, state):
        # Killer moves check
        ck = capture_king(state, self.color)
        if ck != 0:
            return ck

        wmk = win_move_king(state, self.color)
        if wmk != 0:
            return wmk

        # Feature linear combination
        s = 0
        s += 0.3 * piece_score(state, self.color)
        s += 0.1 * king_safety(state, self.color)
        s += 0.6 * king_distance(state, self.color)
        # other features
        return s
