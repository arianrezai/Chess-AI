import chess
import chess.polyglot 
import random
import pygame 
from core.chess_heuristics import Heuristics


class MoveGenerator:
    def __init__(self, depth = 4):
        self.CHECKMATE = 1000
        self.STALEMATE = 0
        self.DEPTH = depth  # Result of the tests in performance_evaluation.py
        self.QUIT = False
        self.heuristics = Heuristics()
        self.transposition = {}

    def random_move(self, board):
        moves = list(board.legal_moves)
        return random.choice(moves)

    def greedy_best_move(self, board):
        white = board.turn == chess.WHITE
        legal_moves = list(board.legal_moves)
        turn_multiplier = 1 if board.turn == chess.WHITE else -1
        max_score = -self.CHECKMATE
        best_move = None

        for player_move in legal_moves:
            board.push(player_move)  # make the move in order to evaluate it
            if board.is_checkmate():
                score = self.CHECKMATE
            elif board.is_stalemate():
                score = self.STALEMATE
            else:
                score = turn_multiplier * self.heuristics.pieces_score_heuristic(board, white)
            if score > max_score:
                max_score = score
                best_move = player_move
            board.pop()  # undo the move

        if best_move is None:
            return self.random_move(board)

        return best_move

    def mini_max_ab_pruning(self, board):

        best_move = [None]
        # stating if white or black is playing for max/min
        white = board.turn == chess.WHITE
        maximize = True

        self.find_mini_max_move(board, self.DEPTH, maximize, white, -10000, 10000, best_move)
        if self.QUIT is True:
            return False

        if best_move[0] is None:
            best_move[0] = self.random_move(board)

        return best_move[0]

    def find_mini_max_move(self, board, depth, maximize, white, alpha, beta, best_move):
        
        # allow the user to close the game
        try:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    self.QUIT = True
            if self.QUIT is True:
                return 0
        except Exception:
            pass

        # legal moves are ordered so that moves that capture a piece are listed first
        legal_moves = list(board.legal_moves)
        legal_moves.sort( key= lambda m: 0 if board.piece_at(m.to_square) else 1)
        
        # check for 'terminal node' and max depth
        if depth == 0 or len(legal_moves) == 0:  
            score = self.heuristics.full_board_evaluation_heuristic(board, white)
            return score
        
        # transposition table, return score if the position was already reached at same or higher depth 
        hash = chess.polyglot.zobrist_hash(board)
        if hash in self.transposition and self.transposition.get(hash)[1] >= depth:
            score = self.transposition.get(hash)[0]
            return score
        
        if maximize:
            max_score = -10000
            for move in legal_moves:
                board.push(move)
                score = self.find_mini_max_move(board, depth - 1, False, white, alpha, beta, best_move)
                if score > max_score:
                    max_score = score
                    # set the best move
                    if depth == self.DEPTH:
                        best_move[0] = move
                # pruning - update alpha
                if max_score > alpha:
                    alpha = max_score
                # pruning - skip branch if move is better than best move opponent will allow
                if max_score >= beta:
                    board.pop()
                    break
                board.pop()
            self.transposition.update({hash : [max_score, depth]})
            return max_score

        else:
            min_score = 10000
            for move in legal_moves:
                board.push(move)
                score = self.find_mini_max_move(board, depth - 1, True, white, alpha, beta, best_move)
                if score < min_score:
                    min_score = score
                # pruning - update beta
                if min_score < beta:
                    beta = min_score
                # pruning - skip branch if worse than the worst score we are willing to accept
                if min_score <= alpha:
                    board.pop()
                    break
                board.pop()
            self.transposition.update({hash : [min_score, depth]})
            return min_score

