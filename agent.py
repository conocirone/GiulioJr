import time
import copy

from features import piece_score, king_safety, win_move_king, capture_king, king_distance
from state import State, Player

class Agent:
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
                
                """"
                  move = self.alphabeta_it(
                    time_limit = time.time() + self.timeout * 0.95, 
                    depth = 10)
                """""
              
                
                move = self.iterative_deepening(time.time() + self.timeout * 0.95)


                print(f"Move {move}, piece score: {piece_score(self.do_move(board, move), self.color)}")

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
        
    
    def iterative_deepening(self, time_limit):
        depth = 1
        best_move = None
        while time.time() < time_limit:
            
            move  = self.alphabeta_it(
                time_limit = time_limit, 
                depth = depth)
            
            if move is not None:
                best_move = move
                # print("Best move: ", best_move, "depth: ", depth)
                depth += 1

        if best_move is None:
            best_move = self.board.get_available_moves(self.color)[0] 
        return best_move

    def alphabeta_it(self, time_limit, depth):
        root_state = State(self.board, None, float('-inf'), self.color, Player.MAX, float('-inf'), float('inf'))
        L = [root_state]

        state = root_state

        while not root_state.evaluated:

            if state.evaluated:
                del L[-1]
                parent = L[-1]

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

            elif len(L) == depth+1:
                state.value = self.eval(state.board)
                state.evaluated = True

            elif time.time() >= time_limit:
                break

            else:
                next_state = state.next_state()
                if next_state != state:
                    L.append(next_state)

            state = L[-1]

        return root_state.best_move

    def do_move(self, state, move):
        new_board = copy.deepcopy(state)
        new_board.move_piece(move)
        return new_board

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
