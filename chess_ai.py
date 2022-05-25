import chess
from core import chess_engine
from utils.gui import play_chess


def main():
    # create a chess board object
    board = chess.Board()
    # play white against minimax algorithm with a depth of 4 moves
    move_generator = chess_engine.MoveGenerator() 
    play_chess(board, black=move_generator.mini_max_ab_pruning)

if __name__ == '__main__':
    main()
