"""
Chess Heuristics : Contains the chess heuristics used to score the chess positions in chess_engine.py

"""

import chess
global best_move

# generate a matrix associated to the board, which will be used to assess scores
class MakeMatrix:

    def __init__(self):
        self.board_mat = []

    def convert_to_matrix(self, board):
        board_str = board.epd()
        rows = board_str.split(" ", 1)[0].split("/")
        for row in rows:
            board_row = []
            for cell in row:
                if cell.isdigit():
                    for i in range(0, int(cell)):
                        board_row.append('--')
                else:
                    if cell.islower():  # black
                        board_row.append(("b", cell))
                    else:  # white
                        board_row.append(("w", cell.lower()))
            self.board_mat.append(board_row)
        return self.board_mat


# heuristic rules that associates a score to each board disposition 
class Heuristics:
    def __init__(self):
        self.CHECKMATE = 1000
        self.STALEMATE = 0
        self.piece_score = {"k": 0, "q": 10, "r": 5, "b": 3, "n": 3, "p": 1}
        self.mobility_piece_score = {"k": 4, "q": 10, "r": 5, "b": 3, "n": 3, "p": 1}

    """
    Heuristic #1
    
    scores boards based on piece value set in self.piece_score:
    
        1. each piece is worth +points if it is yours, and -points if it is your opponents
        2. special case for checkmate (+/- 1000 points)
        3. special case for stalemate (0 points)
    """
    def pieces_score_heuristic(self, board, white):
        # case 1: return +1000 if it is checkmate and we win
        if board.is_checkmate() and (white and board.turn == chess.BLACK or
                                     not white and board.turn == chess.WHITE):
            return self.CHECKMATE

        # case 2: return -1000 if it is checkmate and we lose
        if board.is_checkmate() and (not white and board.turn == chess.BLACK or
                                     white and board.turn == chess.WHITE):
            return -self.CHECKMATE

        # case 3: return 0 if it is a stalemate
        if board.is_stalemate():
            return self.STALEMATE

        # case 4: otherwise return the board score
        return self.score_material(board, white)

    def score_material(self, board, white):
        chess_board = MakeMatrix().convert_to_matrix(board)
        score = 0
        count_black = 0
        count_white = 0
        for row in chess_board:
            for cell in row:
                color = cell[0]
                piece_type = cell[1]
                if color == "w":
                    count_white += 1
                    score += self.piece_score[piece_type]
                elif color == "b":
                    count_black += 1
                    score -= self.piece_score[piece_type]
        # invert the score if we are playing black
        if white is False:
            score = -score
        return score

    """
    Heuristic #2

    adds to heuristic #1:
    
        1. scores boards based on number of pieces
        2. scores boards based on control of center squares
        3. scores boards based on diagonal control
        
    """


    # function to score board based on control of diagonals
    def control_diagonals(self, board, white):
        # This procedure determines if diagonals are controlled by bishops or queen

        # Define figures capable of controlling the diagonals
        diagonal_figures = ["b", "q"]

        # set initial heuristic to zero
        diagonal_heuristics = 0

        # Convert board
        chess_board = MakeMatrix().convert_to_matrix(board)

        # Define diagonals
        black_diagonal = [chess_board[1][1], chess_board[2][2], chess_board[3][3], chess_board[4][4],
                          chess_board[5][5], chess_board[6][6], chess_board[7][7], chess_board[0][0]]

        white_diagonal = [chess_board[0][7], chess_board[1][6], chess_board[2][5], chess_board[3][4],
                          chess_board[4][3], chess_board[5][2], chess_board[6][1], chess_board[7][0]]

        for cell in black_diagonal:
            for figure in diagonal_figures:
                if figure == cell[1]:
                    if (cell[0] == "w" and white) or (cell[0] == "b" and not white):
                        diagonal_heuristics += 3
        for cell in white_diagonal:
            for figure in diagonal_figures:
                if figure == cell[1]:
                    if (cell[0] == "w" and white) or (cell[0] == "b" and not white):
                        diagonal_heuristics += 3

        return diagonal_heuristics

    # function to score board based on control of center squares
    def control_center(self, board, white):
        # This procedure will give heuristic points for control of central squares

        # Convert board
        chess_board = MakeMatrix().convert_to_matrix(board)

        # define central squares: e4, e5, d4, d5
        central_squares = [chess_board[4][4], chess_board[4][5], chess_board[5][4], chess_board[5][5]]

        # Define squares can be used to control central squares by pawns
        white_pawn_squares = [chess_board[3][3], chess_board[4][3], chess_board[5][3], chess_board[6][3],
                              chess_board[4][3], chess_board[4][4], chess_board[4][5], chess_board[4][6]]

        black_pawn_squares = [chess_board[3][6], chess_board[4][6], chess_board[5][6], chess_board[6][6],
                              chess_board[3][5], chess_board[4][5], chess_board[5][5], chess_board[5][6]]

        # Define squares can be used to control central squares by knights
        knight_squares = [chess_board[3][2], chess_board[4][2], chess_board[5][2], chess_board[6][2],
                          chess_board[2][3], chess_board[3][3], chess_board[6][3], chess_board[7][3],
                          chess_board[2][4], chess_board[7][4], chess_board[2][5], chess_board[7][5],
                          chess_board[2][6], chess_board[3][6], chess_board[6][6], chess_board[7][6],
                          chess_board[3][7], chess_board[4][7], chess_board[5][7], chess_board[6][7]]

        # Set control center heuristics to 0
        ccHeuristic = 0

        # Give points for each piece in central square (pawn or knight)
        for square in central_squares:
            if square[1] == "p":
                ccHeuristic += 1
            elif square[1] == "n":
                ccHeuristic += 2
            elif square[1] == "b":
                ccHeuristic += 2
            elif square[1] == "r":
                ccHeuristic += 2
            elif square[1] == "q":
                ccHeuristic += 3
            elif square[1] == "k":
                ccHeuristic += 2

        # Give points for white pawns in controlling positions
        if white:
            for square in white_pawn_squares:
                if square == "p":
                    ccHeuristic += 1

        # Give points for black pawns in controlling positions
        if not white:
            for square in black_pawn_squares:
                if square == "p":
                    ccHeuristic += 1

        # Give points for knights controlling central squares
        for square in knight_squares:
            if square == "n":
                ccHeuristic += 2

        return ccHeuristic

    def full_board_evaluation_heuristic(self, board, white):
        # generate the initial score based on pieces score
        score = self.pieces_score_heuristic(board, white)
        # complement with additional heuristics rescaled by a costant to assess their relative impact
        score += self.control_diagonals(board, white) / 5
        score += self.control_center(board, white) / 4
        return score


