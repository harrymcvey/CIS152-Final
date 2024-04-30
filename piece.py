import pygame
from constants import GRAY, SQUARE_SIZE, CROWN

class Piece:
    PADDING = 20 # Space between the piece and the edge of the square
    OUTLINE = 2 # Thickness of the piece's outline

    # Constructor to initialize a piece with position and color, state (not king), and calculate its screen coordinates
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calculate_pos()

    # Calculate the screen position of a piece based on its row and column
    def calculate_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    # Check if the piece is a king
    def check_king(self):
        return self.king == True

    # Mark the piece as a king
    def make_king(self):
        self.king = True

    # Draw the piece on the board, add a crown image if it is made a king
    def draw_piece(self, win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, GRAY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))

    # Move the piece to a new location and recalculate its position
    def move_piece(self, row, col):
        self.row = row
        self.col = col
        self.calculate_pos()

    def __repr__(self):
        return str(self.color)
