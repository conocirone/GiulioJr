import random
import math
import time

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
                moves = self.board.get_available_moves(self.color)
                # Random agent
                random_move = random.choice(moves)

                conv_move = self.convert_move(random_move)
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
    
    
    def alphabeta(state, depth, alpha, beta, maximazingPlayer, time_limit):
        if depth == 0 and time.time() >= time_limit:
            value = eval(state)
            #put this value into a transposition table
            return value
        
        oppositeColor = ''
        if self.color == "WHITE":
            oppositeColor = "BLACK"
        else: 
            oppositeColor = "WHITE"
        
                
        if(maximazingPlayer):
            bestValue = float('-inf')
            for move in state.get_available_moves(oppositeColor):
                s = do_move(state, move)
                value = alphabeta(s, depth - 1, alpha, beta, False)
                bestValue = max(bestValue, value)
                alpha = max(alpha, bestValue)
                if bestValue >= beta:
                    return bestValue, move
            return bestValue, move
        else:
            bestValue = float('inf')
            for move in state.get_available_moves(oppositeColor):
                s = do_move(state, move)
                value = alphabeta(s, depth - 1, alpha, beta, True)
                bestValue = min(bestValue, value)
                beta = min(beta, bestValue)
                if bestValue <= alpha:
                    return bestValue, move
            return bestValue, move        
        
    def do_move(self, state, move):
        new_board = state.copy()
        new_board.move_piece(move)
        return new_board
        

            
        