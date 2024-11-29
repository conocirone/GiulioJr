from weight_combinations import get_all_weights_combos
from match import init_match
import pandas as pd

# Tournament settings
server_port = 10000
port_offset = 0
timeout = 60

# Generate all possible parameter combination
weight_combos = get_all_weights_combos(3, 10)

# List of threads, each thread starts a match
threads = []
# Results of each match: tuple(weight_combination) -> list(match stats), can be None
results = {}
for i in range(len(weight_combos)):
    combo1 = weight_combos[i]
    for j in range(i + 1, len(weight_combos)):
        combo2 = weight_combos[j]
        init_match(combo1, combo2, server_port, port_offset    , timeout, results, threads)
        init_match(combo2, combo1, server_port, port_offset + 2, timeout, results, threads)
        port_offset += 10

for t in threads:
    t.join()

if type(results) == dict:
    results_df = pd.DataFrame(list(results.values()), columns = [
        "piece_score",
        "king_safety",
        "king_distance",
        "WHITE_WIN",
        "WHITE_LOSE",
        "BLACK_WIN",
        "BLACK_LOSE",
        "WHITE_DRAW",
        "BLACK_DRAW",
    ])
    results_df.to_csv("results.csv")
