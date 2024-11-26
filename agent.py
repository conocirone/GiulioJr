import time
import copy


from board import Board
from features import (
    piece_score,
    king_safety,
    king_distance,
    king_free_road,
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
        self.draw_fifo = []
        #initialize with random values
        self.transposition_table = {}
        self.transposition_table_size = 2**16
        self.nodes = 0
        self.cache_hits = 0
        
        # sends and receives messages
        while True:
            current_state, turn = gateway.get_state()
            if turn == self.color.name:
                self.board.update(current_state)

                # Update draw_fifo
                if len(self.draw_fifo) == 4:
                    self.draw_fifo.pop(0)
                self.draw_fifo.append(self.board.color_coords)

                # Define depth, timeout percentage
                move = self.iterative_deepening(time.time() + self.timeout * 0.95)

                conv_move = self.convert_move(move)
                self.gateway.send_state(conv_move)

                # Updating draw FIFO
                chosen_board = copy.deepcopy(self.board)
                chosen_board.move_piece(move)
                if len(self.draw_fifo) == 4:
                    self.draw_fifo.pop(0)
                self.draw_fifo.append(chosen_board.color_coords)

                print("Waiting opponent:\n")

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
    

    def put_in_transposition_table(self, key, search_depth, move, value, flag):
        if len(self.transposition_table) >= self.transposition_table_size:
            self.transposition_table.popitem()
        if key in self.transposition_table.keys():
            if self.transposition_table[key][0] < search_depth:
                self.transposition_table[key] = [search_depth, move, value, flag]
        else:
            self.transposition_table[key] = [search_depth, move, value, flag]
        

    def get_from_tansposition_table(self, key, search_depth, alpha, beta):
        if key in self.transposition_table.keys():
            t_entry = self.transposition_table[key]
            self.cache_hits += 1
            if t_entry[0] >= search_depth:
                if t_entry[3] == "EXACT":
                    return t_entry[1], t_entry[2]
                elif t_entry[3] == "ALPHA" and t_entry[2] <= alpha:
                    return t_entry[1], alpha
                elif t_entry[3] == "BETA" and t_entry[2] >= beta:
                    return t_entry[1], beta
        return None, None
                
    
    def iterative_deepening(self, time_limit):
        depth = 1
        best_move = None
        max_depth = 100
        while time.time() < time_limit and depth <= max_depth:
            move, value = self.alphabeta_it(time_limit=time_limit, depth=depth)
            if move is not None:
                best_move = move
                print(f"{self.color.name}: depth: {depth}, value: {value}, nodes: {self.nodes}, cache_hits: {self.cache_hits}, move: {self.convert_move(best_move)}")
                depth += 1
                
            
        if best_move is None:
            best_move = self.board.get_available_moves(self.color)[0]
            
        self.nodes = 0  
        self.cache_hits = 0
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
            self.draw_fifo,
            self.color
        )
        L = [root_state]
        
        while not root_state.evaluated:
            
            state = L[-1]
            
            if not state.evaluated:
                state_key = state.__hash__()  
                t_move, t_value = self.get_from_tansposition_table(state_key, depth - (len(L) - 1), state.alpha, state.beta)
                if t_move is not None and t_value is not None:
                    state.evaluated = True
                    state.value = t_value
                    state.best_move = t_move
                    if state is root_state:
                        break
            
            if state.evaluated:
                del L[-1]
                parent = L[-1]

                if parent.player == Player.MAX:
                    if state.value > parent.value:
                        parent.value = state.value
                        parent.best_move = state.move
                    parent.alpha = max(parent.alpha, parent.value)
                    if parent.alpha >= parent.beta:
                        Board.history_table[parent.color.value][parent.best_move] = (
                            Board.history_table[parent.color.value].get(parent.best_move, 0)
                            + 2 ** depth - (len(L) - 1)
                        )
                        parent.evaluated = True
                        self.put_in_transposition_table(parent.__hash__(), depth - (len(L) - 1), parent.best_move, parent.value, "BETA")
                        continue
                else:
                    if state.value < parent.value:
                        parent.value = state.value
                        parent.best_move = state.move
                    parent.beta = min(parent.beta, parent.value)
                    if parent.alpha >= parent.beta:
                        Board.history_table[parent.color.value][parent.best_move] = (
                            Board.history_table[parent.color.value].get(parent.best_move, 0)
                            + 2 ** depth - (len(L) - 1)
                        )
                        parent.evaluated = True
                        self.put_in_transposition_table(parent.__hash__(), depth - (len(L) - 1), parent.best_move, parent.value, "ALPHA")
                        continue

                next_state = parent.next_state()
                if next_state != parent:
                    L.append(next_state)
                else:
                    Board.history_table[parent.color.value][parent.best_move] = (
                        Board.history_table[parent.color.value].get(parent.best_move, 0)
                        + 2 ** depth - (len(L) - 1)
                    )
                    parent.evaluated = True
                    self.put_in_transposition_table(parent.__hash__(), depth - (len(L) - 1), parent.best_move, parent.value, "EXACT")

            elif len(L) == depth + 1:
                state.value = self.eval(state.board)
                state.evaluated = True
                self.nodes += 1
                

            elif time.time() >= time_limit:
                return None, None

            else:
                next_state = state.next_state()
                if next_state != state:
                    L.append(next_state)
            
        return root_state.best_move, root_state.value

    def eval(self, state):
        kfr = king_free_road(state, self.color)
        if kfr != 0:
            return kfr

        # Feature linear combination
        s = 0
        s += 0.3 * piece_score(state, self.color)
        s += 0.1 * king_safety(state, self.color)
        s += 0.6 * king_distance(state, self.color)
        # other features
        return s
