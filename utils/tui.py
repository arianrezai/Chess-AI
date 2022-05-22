"""
Chess TUI: This file contains a play option without GUI to allow autoplay in performace_evaluation.py

"""
import chess

def play_chess(board, white, black):
    while True:
        # check if the game is over
        outcome = board.outcome()
        if outcome is None:
            # generate and push a move to the board
            if board.turn == chess.WHITE:
                move = white(board)
                board.push(move)
            else:
                move = black(board)
                board.push(move)
        # return the winner
        else:
            return outcome.winner 
