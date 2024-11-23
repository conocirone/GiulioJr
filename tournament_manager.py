# import os
from multiprocessing import cpu_count
import subprocess
import time
from threading import Semaphore, Thread
import pandas as pd

server_port = 10000
timeout = 1
threads = []
results = pd.DataFrame(
    columns=[
        "piece_score",
        "king_safety",
        "king_distance",
        "WHITE_WIN",
        "WHITE_LOSE",
        "BLACK_WIN",
        "BLACK_LOSE",
        "DRAW",
    ]
)
port_offset = 0
# Semaphore for updating results
results_semaphore = Semaphore(1)
# Semaphore for matching: allocate a match for each free cpu
cpu_semaphore = Semaphore(cpu_count())


def start_results(server_port, white_args, black_args, timeout):
    global results
    cpu_semaphore.acquire()

    print(f"Matching WHITE:{white_args} against BLACK:{black_args}")
    # List of processes to manage
    processes = []

    # Create a SERVER subprocess (suppress stderr and stdout)
    processes.append(
        subprocess.Popen(
            f"java -jar server.jar -p {server_port}",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    )
    time.sleep(1)

    # Create WHITE agent subprocess (suppress stderr and stdout)
    processes.append(
        subprocess.Popen(
            f"""python main.py \
                --team WHITE \
                --name white \
                --ip localhost \
                --timeout {timeout} \
                --port {server_port} \
                --weights {white_args['piece_score']} \
                          {white_args['king_safety']} \
                          {white_args['king_distance']}""",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    )
    # Create a BLACK subprocess (suppress stderr and stdout)
    processes.append(
        subprocess.Popen(
            f"""python main.py \
                --team BLACK \
                --name black \
                --ip localhost \
                --timeout {timeout} \
                --port {server_port+1} \
                --weights {black_args['piece_score']} \
                          {black_args['king_safety']} \
                          {black_args['king_distance']}""",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    )

    # Array containing return values of each subprocess:
    # Only the winning agent will return 0, other processes will return 1
    exit_codes = [p.wait() for p in processes]

    results_semaphore.acquire()
    white_args_df = pd.DataFrame(white_args, index=[hash(tuple(white_args.values()))])
    black_args_df = pd.DataFrame(black_args, index=[hash(tuple(black_args.values()))])
    if exit_codes[1] == 0:
        # WHITE wins
        if (
            not white_args_df.isin(
                results[["piece_score", "king_safety", "king_distance"]]
            )
            .any()
            .any()
        ):
            results = pd.concat([results, white_args_df])
            results.loc[white_args_df.index, "WHITE_WIN"] = 1
            results.loc[white_args_df.index, "WHITE_LOSE"] = 0
            results.loc[white_args_df.index, "BLACK_WIN"] = 0
            results.loc[white_args_df.index, "BLACK_LOSE"] = 0
            results.loc[white_args_df.index, "DRAW"] = 0
        else:
            results.loc[white_args_df.index, "WHITE_WIN"] = (
                results.loc[white_args_df.index, "WHITE_WIN"] + 1
            )

        # BLACK loses
        if (
            not black_args_df.isin(
                results[["piece_score", "king_safety", "king_distance"]]
            )
            .any()
            .any()
        ):
            results = pd.concat([results, black_args_df])
            results.loc[black_args_df.index, "WHITE_WIN"] = 0
            results.loc[black_args_df.index, "WHITE_LOSE"] = 0
            results.loc[black_args_df.index, "BLACK_WIN"] = 0
            results.loc[black_args_df.index, "BLACK_LOSE"] = 1
            results.loc[black_args_df.index, "DRAW"] = 0
        else:
            results.loc[black_args_df.index, "BLACK_LOSE"] = (
                results.loc[black_args_df.index, "BLACK_LOSE"] + 1
            )

    elif exit_codes[2] == 0:
        # BLACK wins
        if (
            not black_args_df.isin(
                results[["piece_score", "king_safety", "king_distance"]]
            )
            .any()
            .any()
        ):
            results = pd.concat([results, black_args_df])
            results.loc[black_args_df.index, "WHITE_WIN"] = 0
            results.loc[black_args_df.index, "WHITE_LOSE"] = 0
            results.loc[black_args_df.index, "BLACK_WIN"] = 1
            results.loc[black_args_df.index, "BLACK_LOSE"] = 0
            results.loc[black_args_df.index, "DRAW"] = 0
        else:
            results.loc[black_args_df.index, "BLACK_WIN"] = (
                results.loc[black_args_df.index, "BLACK_WIN"] + 1
            )
        # WHITE loses
        if (
            not white_args_df.isin(
                results[["piece_score", "king_safety", "king_distance"]]
            )
            .any()
            .any()
        ):
            results = pd.concat([results, white_args_df])
            results.loc[white_args_df.index, "WHITE_WIN"] = 0
            results.loc[white_args_df.index, "WHITE_LOSE"] = 1
            results.loc[white_args_df.index, "BLACK_WIN"] = 0
            results.loc[white_args_df.index, "BLACK_LOSE"] = 0
            results.loc[white_args_df.index, "DRAW"] = 0
        else:
            results.loc[white_args_df.index, "WHITE_LOSE"] = (
                results.loc[white_args_df.index, "WHITE_LOSE"] + 1
            )
    else:
        # DRAW
        if (
            not white_args_df.isin(
                results[["piece_score", "king_safety", "king_distance"]]
            )
            .any()
            .any()
        ):
            results = pd.concat([results, white_args_df])
            results.loc[white_args_df.index, "WHITE_WIN"] = 0
            results.loc[white_args_df.index, "WHITE_LOSE"] = 0
            results.loc[white_args_df.index, "BLACK_WIN"] = 0
            results.loc[white_args_df.index, "BLACK_LOSE"] = 0
            results.loc[white_args_df.index, "DRAW"] = 1
        else:
            results.loc[white_args_df.index, "DRAW"] = (
                results.loc[white_args_df.index, "DRAW"] + 1
            )
        if (
            not black_args_df.isin(
                results[["piece_score", "king_safety", "king_distance"]]
            )
            .any()
            .any()
        ):
            results = pd.concat([results, black_args_df])
            results.loc[black_args_df.index, "WHITE_WIN"] = 0
            results.loc[black_args_df.index, "WHITE_LOSE"] = 0
            results.loc[black_args_df.index, "BLACK_WIN"] = 0
            results.loc[black_args_df.index, "BLACK_LOSE"] = 0
            results.loc[black_args_df.index, "DRAW"] = 1
        else:
            results.loc[black_args_df.index, "DRAW"] = (
                results.loc[black_args_df.index, "DRAW"] + 1
            )

    results_semaphore.release()

    cpu_semaphore.release()


# Generate all possible parameter combination
def get_all_weights_combos(weight_list_size, high):
    if weight_list_size == 1:
        return [[high]]
    res = []
    for i in range(1, high):
        for weight_combo in get_all_weights_combos(weight_list_size - 1, high - i):
            res.append([i] + weight_combo)
    return res


weight_combos = get_all_weights_combos(3, 10)


for i in range(len(weight_combos)):
    combo1 = weight_combos[i]
    for j in range(i + 1, len(weight_combos)):
        combo2 = weight_combos[j]
        # WHITE: combo1, BLACK: combo_2
        t1 = Thread(
            target=start_results,
            args=(
                server_port + port_offset,
                {
                    "piece_score": combo1[0],
                    "king_safety": combo1[1],
                    "king_distance": combo1[2],
                },
                {
                    "piece_score": combo2[0],
                    "king_safety": combo2[1],
                    "king_distance": combo2[2],
                },
                timeout,
            ),
        )
        # WHITE: combo2, BLACK: combo_1
        t2 = Thread(
            target=start_results,
            args=(
                server_port + port_offset + 2,
                {
                    "piece_score": combo2[0],
                    "king_safety": combo2[1],
                    "king_distance": combo2[2],
                },
                {
                    "piece_score": combo1[0],
                    "king_safety": combo1[1],
                    "king_distance": combo1[2],
                },
                timeout,
            ),
        )
        # increase port for the next match (10 for good measure)
        port_offset += 10
        # start matches
        t1.start()
        t2.start()
        # keep track of threads
        threads.append(t1)
        threads.append(t2)

for t in threads:
    t.join()

results.to_csv("results.csv")
