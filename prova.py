import random

zobrist_table =  [[[random.getrandbits(64)] * 2 for _ in range(9)] for _ in range(9)] 
print(zobrist_table[1][0][0])
print(random.getrandbits(64))