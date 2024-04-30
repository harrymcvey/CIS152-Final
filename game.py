import pygame
from constants import RED, WHITE, GREEN, SQUARE_SIZE
from board import GameBoard

class Game:
    # Initialize the game with a window, game board, and set the initial turn to RED
    def __init__(self, win):
        self.win = win
        self.selected = None
        self.board = GameBoard()
        self.turn = RED
        self.valid_moves = {}

    # Draw the game window, including the board and valid moves, and update the display
    def update_display(self):
        self.board.draw_board(self.win)
        self.draw_valid_moves()
        pygame.display.update()

    # Reset the game to its initial state
    def reset_game(self):
        self.selected = None
        self.board = GameBoard()
        self.turn = RED
        self.valid_moves = {}

    # Return the winner of the game
    def winner(self):
        return self.board.winner()

    # Select a piece or a valid move spot; select action based on game state and turn
    def select(self, row, col):
        piece = self.board.get_piece(row, col)
        if piece and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        elif self.selected and (row, col) in self.valid_moves:
            self.move(row, col)
            return True
        return False

    # Move the selected piece to the new location and handle any captured pieces
    def move(self, row, col):
        self.board.move_piece(self.selected, row, col)
        skipped = self.valid_moves.get((row, col))
        if skipped:
            self.board.remove_piece(skipped)
        self.change_turn()

    # Highlight valid moves on the board for the selected piece
    def draw_valid_moves(self):
        for move in self.valid_moves:
            row, col = move
            pygame.draw.circle(self.win, GREEN, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    # Switch turns between RED and WHITE
    def change_turn(self):
        self.valid_moves = {}
        self.turn = WHITE if self.turn == RED else RED

    # Algorithm makes a move and switch turns
    def algorithm_move(self, board):
        self.board = board
        self.change_turn()

    # Return the current state of the game board
    def get_board(self):
        return self.board
