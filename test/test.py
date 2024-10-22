from random import randint
from board_hash import BoardHash
from board import Board
from time import time

colors = ('EMPTY', 'BLACK', 'WHITE', 'KING')

def test_get_available_moves(board, times):
    total_time = 0
    for _ in range(times):
        board_from_server = [[colors[randint(0, 3)] for _ in range(9)] for _ in range(9)]
        board.update(board_from_server)

        start_time = time()
        board.get_available_moves(('BLACK',))
        board.get_available_moves(('WHITE', 'KING'))
        total_time += time() - start_time
    return total_time

def test_random_move(board, times):
    total_time = 0
    for _ in range(times):
        board_from_server = [[colors[randint(0, 3)] for _ in range(9)] for _ in range(9)]
        board.update(board_from_server)

        moves = board.get_available_moves(('BLACK',))

        start_time = time()
        board.random_move(moves)
        total_time += time() - start_time

    return total_time

def test_update(board, times):
    total_time = 0
    for _ in range(times):
        board_from_server = [[colors[randint(0, 3)] for _ in range(9)] for _ in range(9)]

        start_time = time()
        board.update(board_from_server)
        total_time += time() - start_time
    return total_time


board_from_server = [[colors[randint(0, 3)] for _ in range(9)] for _ in range(9)]
board_hash = BoardHash()
board_matrix = Board()

times = 10000

print(f"board_matrix.get_available_moves: {test_get_available_moves(board_matrix, times)}")
print(f"board_hash.get_available_moves:   {test_get_available_moves(board_hash, times)}")

print(f"board_matrix.random_move: {test_random_move(board_matrix, times)}")
print(f"board_hash.random_move:   {test_random_move(board_hash, times)}")

print(f"board_matrix.update: {test_update(board_matrix, times)}")
print(f"board_hash.update:   {test_update(board_hash, times)}")
