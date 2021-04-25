"""
Handling the AI moves.
"""
import random

piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3

knight_scores = [[1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 2, 2, 2, 2, 2, 2, 1],
                 [1, 2, 3, 3, 3, 3, 2, 1],
                 [1, 2, 3, 4, 4, 3, 2, 1],
                 [1, 2, 3, 4, 4, 3, 2, 1],
                 [1, 2, 3, 3, 3, 3, 2, 1],
                 [1, 2, 2, 2, 2, 2, 2, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1]]

bishop_scores = [[4, 3, 2, 1, 1, 2, 3, 4],
                 [3, 4, 3, 2, 2, 3, 4, 3],
                 [2, 3, 4, 3, 3, 4, 3, 2],
                 [1, 2, 3, 4, 4, 3, 2, 1],
                 [1, 2, 3, 4, 4, 3, 2, 1],
                 [2, 3, 4, 3, 3, 4, 3, 2],
                 [3, 4, 3, 2, 2, 3, 4, 3],
                 [4, 3, 2, 1, 1, 2, 3, 4],]

queen_scores = [[1, 1, 1, 3, 1, 1, 1, 1],
                [1, 2, 3, 3, 3, 1, 1, 1],
                [1, 4, 3, 3, 3, 4, 2, 1],
                [1, 2, 3, 3, 3, 2, 2, 1],
                [1, 2, 3, 3, 3, 2, 2, 1],
                [1, 4, 3, 3, 3, 4, 2, 1],
                [1, 1, 2, 3, 3, 1, 1, 1],
                [1, 1, 1, 3, 1, 1, 1, 1],]

rook_scores = [[4, 3, 4, 4, 4, 4, 3, 4],
               [4, 4, 4, 4, 4, 4, 4, 4],
               [1, 1, 2, 3, 3, 2, 1, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 1, 2, 2, 2, 2, 1, 1],
               [4, 4, 4, 4, 4, 4, 4, 4],
               [4, 3, 4, 4, 4, 4, 3, 4],]

white_pawn_scores = [[8, 8, 8, 8, 8, 8, 8, 8],
                     [8, 8, 8, 8, 8, 8, 8, 8],
                     [5, 6, 6, 7, 7, 6, 6, 5],
                     [2, 3, 3, 5, 5, 3, 3, 2],
                     [1, 2, 3, 4, 4, 3, 2, 1],
                     [1, 1, 2, 3, 3, 2, 1, 1],
                     [1, 1, 1, 0, 0, 1, 1, 1],
                     [0, 0, 0, 0, 0, 0, 0, 0],]

black_pawn_scores = [[0, 0, 0, 0, 0, 0, 0, 0],
                     [1, 1, 1, 0, 0, 1, 1, 1],
                     [1, 1, 2, 3, 3, 2, 1, 1],
                     [1, 2, 3, 4, 4, 3, 2, 1],
                     [2, 3, 3, 5, 5, 3, 3, 2],
                     [5, 6, 6, 7, 7, 6, 6, 5],
                     [8, 8, 8, 8, 8, 8, 8, 8],
                     [8, 8, 8, 8, 8, 8, 8, 8],]

piece_position_scores = {'N': knight_scores, 'Q': queen_scores, 'B': bishop_scores, 'R': rook_scores, 'bp': black_pawn_scores, 'wp': white_pawn_scores}


# finds and returns a valid move
def findRandomMove(valid_moves):
    return random.choice(valid_moves)


# Helper method to make the first recursive call
# Not used in program as better algorithm written
def findBestMoveMinMax(game_state, valid_moves):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    findMoveMinMax(game_state, valid_moves, DEPTH, game_state.white_to_move)
    return next_move


# Min max recursive algorithm to find best move
def findMoveMinMax(game_state, valid_moves, depth, white_to_move):
    global next_move
    if depth == 0:
        return scoreBoard(game_state)
    if white_to_move:
        max_score = -CHECKMATE
        for move in valid_moves:
            game_state.makeMove(move)
            next_moves = game_state.getValidMoves()
            score = findMoveMinMax(game_state, next_moves, depth - 1, False)
            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    next_move = move
            game_state.undoMove()
        return max_score
    else:
        min_score = CHECKMATE
        for move in valid_moves:
            game_state.makeMove(move)
            next_moves = game_state.getValidMoves()
            score = findMoveMinMax(game_state, next_moves, depth - 1, True)
            if score < min_score:
                min_score = score
                if depth == DEPTH:
                    next_move = move
            game_state.undoMove()
        return min_score


# Helper method to make the first recursive call
# Not used in program as better algorithm written
def findBestMoveNegaMax(game_state, valid_moves):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    findMoveNegaMax(game_state, valid_moves, DEPTH, 1 if game_state.white_to_move else -1)
    return next_move


# Nega max recursive algorithm to find best move
def findMoveNegaMax(game_state, valid_moves, depth, turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * scoreBoard(game_state)

    max_score = -CHECKMATE
    for move in valid_moves:
        game_state.makeMove(move)
        next_moves = game_state.getValidMoves()
        score = -findMoveNegaMax(game_state, next_moves, depth - 1, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        game_state.undoMove()
    return max_score


# hepler method to make first recursive call
# Nega max algorithm with alpha beta pruning to decrease computation time
def findBestMoveNegaMaxAlphaBeta(game_state, valid_moves):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    findMoveNegaMaxAlphaBeta(game_state, valid_moves, DEPTH, -CHECKMATE, CHECKMATE, 1 if game_state.white_to_move else -1)
    return next_move

#
def findMoveNegaMaxAlphaBeta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * scoreBoard(game_state)

    max_score = -CHECKMATE
    for move in valid_moves:
        game_state.makeMove(move)
        next_moves = game_state.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        game_state.undoMove()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score


# Score the board. A positive score is good for white, a negative score is good for black
def scoreBoard(game_state):
    if game_state.checkmate:
        if game_state.white_to_move:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif game_state.stalemate:
        return STALEMATE

    score = 0
    for row in range(len(game_state.board)):
        for col in range(len(game_state.board[row])):
            square = game_state.board[row][col]
            if square != '--':
                piece_position_score = 0
                if square[1] != 'K':
                    if square[1] == 'p':
                        piece_position_score = piece_position_scores[square][row][col]
                    else:
                        piece_position_score = piece_position_scores[square[1]][row][col]

                if square[0] == 'w':
                    score += piece_score[square[1]] + piece_position_score * 0.1
                elif square[0] == 'b':
                    score -= piece_score[square[1]] + piece_position_score * 0.1
    return score
