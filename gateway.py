import json
import socket
import struct


class Gateway:
    def __init__(self, color, name, timeout, server_ip):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.color = color
        self.name = name
        self.timeout = timeout
        self.server_ip = server_ip

        # Connection
        if self.color == "WHITE":
            # Connect the socket to the port where the server is listening
            server_address = (self.server_ip, 5800)
        elif self.color == "BLACK":
            # Connect the socket to the port where the server is listening
            server_address = (self.server_ip, 5801)
        else:
            raise ConnectionError("Player must be WHITE or BLACK!")

        self.socket.connect(server_address)

        # Send the player's name to the server
        self.socket.send(struct.pack(">i", len(self.name)))
        self.socket.send(self.name.encode())

    def get_state(self):
        len_bytes = struct.unpack(">i", self.__recvall(4))[0]
        current_state_server_bytes = self.socket.recv(len_bytes)

        # Converting byte into json
        json_current_state_server = json.loads(current_state_server_bytes)

        board, turn = self.read_msg(json_current_state_server)

        if not turn in ("WHITEWIN", "BLACKWIN", "DRAW"):
            return board
        else:
            self.socket.close()
            print("chiusa la connessione")

    def send_state(self, move):
        start_pos, end_pos = move
        turn = self.color

        move_msg = {"from": move[0], "to": move[1], "turn": turn}
        self.socket.send(struct.pack(">i", len(move)))
        self.socket.send(move.encode())

    def __recvall(self, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = b""
        while len(data) < n:
            packet = self.socket.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    def __del__(self):
        self.socket.close()

    def set_agent(self, agent):
        self.agent = agent

    def read_msg(self, json_msg):
        msg = list(json_msg.items())
        board, turn = msg[0], msg[1]

        return board, turn
