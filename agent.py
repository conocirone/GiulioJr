import random
import time
import copy

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
                _ , move = self.alphabeta(self.board, depth=10, alpha=float("-inf"), beta=float("inf"), maximazingPlayer=True, time_limit=time.time() + self.timeout * 0.95) 
                
                
                """
                moves = self.board.get_available_moves(self.color)
                # Random agent
                random_move = random.choice(moves)
                """
                conv_move = self.convert_move(move)
                self.gateway.send_state(conv_move)

    def convert_move(self, move):
        """converts move indexes from integers to board format (letter-number)

        Args:
            move (tuple): (row_start, column_start, row_stop, column_stop)

        Returns:
            tuple: (starting_position, ending_position)
        """
        return chr(move[1] + 97) + str(move[0] + 1), chr(move[3] + 97) + str(move[2] + 1
        )
    
    
    def alphabeta(self, state, depth, alpha, beta, maximazingPlayer, time_limit):
        print(f"board: {state}")
        
        if depth == 0 or time.time() >= time_limit:
            value = self.eval(state)
            return value, None
        
        if self.color == "WHITE":
            oppositeColor = "BLACK"
        else: 
            oppositeColor = "WHITE"
        
        bestMove = None
        if maximazingPlayer:
            bestValue = float('-inf')
            available_moves = state.get_available_moves(self.color)
            print(f"Av moves max: {available_moves}")
            for move in available_moves: # TODO: Order moves
                s = self.do_move(state, move)
                value, _ = self.alphabeta(s, depth - 1, alpha, beta, False, time_limit)
                if value > bestValue:
                    bestValue = value
                    bestMove = move
                    alpha = max(alpha, bestValue)
                if bestValue >= beta:
                    break
            return bestValue, bestMove 
        else:
            bestValue = float('inf')
            available_moves = state.get_available_moves(oppositeColor)
            print(f"Av moves min: {available_moves}")
            for move in available_moves:
                s = self.do_move(state, move)
                value, _ = self.alphabeta(s, depth - 1, alpha, beta, True, time_limit)
                if value < bestValue:
                    bestValue = value
                    bestMove = move
                    beta = min(beta, bestValue)
                if bestValue <= alpha:
                    break
            return bestValue, bestMove 
        
    def do_move(self, state, move):
        new_board = copy.deepcopy(state)
        new_board.move_piece(move)
        return new_board
    
    def eval(self, state):
        # TODO: implement
        return random.randint(-5, 5)
        

            
        