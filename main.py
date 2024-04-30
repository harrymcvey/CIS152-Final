import pygame
from constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from game import Game
from minmaxAlgorithm import minimax_algorithm

# Set up the game window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

# Takes the mouse position as input and returns the corresponding row and column index on the game board
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

# Main game loop
def main_game():
    run = True
    clock = pygame.time.Clock()
    game = Game(WINDOW)

    while run:

        # Execute algorithm move if it's not players turn
        if game.turn == WHITE:
            value, new_board = minimax_algorithm(game.get_board(), 3, WHITE, game)
            game.algorithm_move(new_board)

        # Print the winner and end the game
        if game.winner() is not None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # End the game loop if the window is closed
                run = False

            # Handle mouse clicks for selecting or moving pieces
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        # Update game display
        game.update_display()

    pygame.quit()

main_game()
