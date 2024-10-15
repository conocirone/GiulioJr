import random


class Agent:
    def __init__(self, gateway, timeout, color, board):
        self.gateway = gateway
        self.gateway.set_agent(self)
        self.color = color
        self.board = board

        # sends and receives messages
        while True:
            current_state, turn = gateway.get_state()
            if turn == self.color:
                self.board.update(current_state)
                if self.color == "WHITE":
                    moves = self.board.get_available_moves(["WHITE", "KING"])
                else:
                    moves = self.board.get_available_moves(["BLACK"])

                random_move = random.choice(moves)
                conv_move = self.convert_move(random_move)
                self.gateway.send_state(conv_move)

    def convert_move(self, move):
        return chr(move[1] + 97) + str(move[0] + 1), chr(move[3] + 97) + str(
            move[2] + 1
        )
