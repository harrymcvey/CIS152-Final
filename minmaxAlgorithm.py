from copy import deepcopy

RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Determine the best move using the minimax algorithm
def minimax_algorithm(position, depth, max_player, game):
    if depth == 0 or position.winner() != None:
        return position.evaluate_board(), position

    if max_player:
        maxEval = float("-100")
        best_move = None
        # For maximizing player, explore possible moves and choose one with the maximum evaluation
        for move in get_all_moves(position, WHITE, game):
            evaluation = minimax_algorithm(move, depth - 1, True, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move

        return maxEval, best_move

    else:
        minEval = float("100")
        best_move = None
        # For minimizing player, explore possible opponent moves and choose one with the minimum evaluation
        for move in get_all_moves(position, RED, game):
            evaluation = minimax_algorithm(move, depth - 1, False, game)[0]
            minEval = max(minEval, evaluation)
            if minEval == evaluation:
                best_move = move

        return minEval, best_move

# Simulate a move on the board, applying the effect of the move and remove skipped pieces
def simulate_move(piece, move, board, game, skip):
    board.move_piece(piece, move[0], move[1])
    if skip:
        board.remove_piece(skip)

    return board

# Generate possible moves for a given color from the current board state
def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        # Get valid moves for the current piece
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            # Create a deep copy of the board and simulate the move
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)

    return moves
