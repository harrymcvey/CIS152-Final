import pygame
from constants import BLACK, ROWS, COLS, RED, WHITE, SQUARE_SIZE
from piece import Piece

# Initialize the game board
class GameBoard:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()

    # Draw alternating black and white squares on the game board
    def draw_squares(self, win):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = WHITE
                else:
                    color = BLACK
                pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Evaluate the board by comparing piece counts and kings
    def evaluate_board(self):
        return self.white_left - self.red_left + (self.white_kings * 1.5 - self.red_kings * 1.5)

    # Get all pieces on the board of a specific color
    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    # Move a piece to a new location and check if it becomes a king
    def move_piece(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move_piece(row, col)
        if (row == ROWS - 1 or row == 0):
            aKing = piece.check_king()
            if aKing == False:
                piece.make_king()
                if piece.color == WHITE:
                    self.white_kings += 1
                else:
                    self.red_kings += 1

    # Return the piece at a specified location on the board
    def get_piece(self, row, col):
        return self.board[row][col]

    # Create the first setup of the board with pieces in starting positions
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    # Draw the board, including squares and pieces
    def draw_board(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw_piece(win)

    # Remove specified pieces from the board
    def remove_piece(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    # Determine if there is a winner based on the remaining pieces
    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        else:
            return None

    # Calculate all valid moves for a specified piece based on its position and color
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self.traverse(row - 1, max(row - 3, -1), -1, piece.color, 'left', left))
            moves.update(self.traverse(row - 1, max(row - 3, -1), -1, piece.color, 'right', right))

        if piece.color == WHITE or piece.king:
            moves.update(self.traverse(row + 1, min(row + 3, ROWS), 1, piece.color, 'left', left))
            moves.update(self.traverse(row + 1, min(row + 3, ROWS), 1, piece.color, 'right', right))

        return moves

# A helper method to traverse the board diagonally for possible moves and jumps
    def traverse(self, start, stop, step, color, direction, col, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if col < 0 or col >= COLS:
                break

            current = self.board[r][col]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, col)] = last + skipped
                else:
                    moves[(r, col)] = last

                if last:
                    new_col_left = col - 1 if direction == 'left' else col + 1
                    new_col_right = col + 1 if direction == 'left' else col - 1
                    new_row = max(r - 3, 0) if step == -1 else min(r + 3, ROWS)
                    moves.update(
                        self.traverse(r + step, new_row, step, color, direction, new_col_left, skipped=last))
                    moves.update(
                        self.traverse(r + step, new_row, step, color, direction, new_col_right, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            col += (-1 if direction == 'left' else 1)
        return moves
