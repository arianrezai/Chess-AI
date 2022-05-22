"""
Chess Program Evaluation: Contains the function that evaluates the performance levels given different depth options

"""
import numpy as np
import chess
from core import chess_engine
from utils.tui import play_chess
import timeit


# the Minimax chess AI with different depth options plays against a greedy chess AI 
def main():
    # game outcomes and performance are each stored in a dictionary
    runtime = {}
    wins = {}
    # each version of the mini max algorithm (white) plays three games against the greedy next move algorithm (black)
    for depth in range(1,7):
        runtime[depth] = []
        wins[depth] = 0
        for _ in range(3):
            board = chess.Board()
            move_generator = chess_engine.MoveGenerator(depth)
            start = timeit.default_timer()
            player1_won = play_chess(board, white=move_generator.mini_max_ab_pruning,
                                black=move_generator.greedy_best_move)
            stop = timeit.default_timer()
            time = round(stop - start,2)
            wins[depth] += int(0 if player1_won is None else player1_won)
            runtime[depth].append(time)
    
    # print results
    print("\n\nRuntime in seconds for each game:")
    print(runtime)
    print("\n\nAverage runtime in seconds for each depth option:")
    runtime_avg = {x : round(np.mean(y),3) for x,y in runtime.items()}
    print(runtime_avg)
    print("\n\nNumber of games won by the minimax algorithm for each depth option:")
    print(wins)

    # 4 moves ahead ensures a good trade-off between looking ahead and running time

if __name__ == '__main__':
    main()

