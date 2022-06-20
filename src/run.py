import pygame
import sys
from consts.consts import *
from build.chess_game import Chess


class Run:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('3WA_DIA : Baptiste HARAMBOURE IA Chess Project')
        self.chess_game = Chess()

    @staticmethod
    def display_screen_behavior(game, screen):
        game.display_background(screen)
        game.display_pieces(screen)

    def infinite_run_loop(self):
        game = self.chess_game
        screen = self.screen
        dragger = self.chess_game.dragger
        board = self.chess_game.board

        while True:
            self.display_screen_behavior(game, screen)

            # Condition avoiding pieces to flicker when dragged
            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                # Check the mouse click event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    clicked_row = dragger.mouse_y // SQUARE_SIZE
                    clicked_column = dragger.mouse_x // SQUARE_SIZE

                    # Check if the clicked square has a piece on it
                    if board.squares[clicked_row][clicked_column].has_piece():
                        piece = board.squares[clicked_row][clicked_column].piece
                        dragger.save_base_position(event.pos)
                        dragger.drag_piece(piece)

                # Check the mouse motion event
                elif event.type == pygame.MOUSEMOTION:

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        # Necessary code to avoid flickering of all pieces while dragging one
                        # Also avoid the dragged piece to be followed by ghosts(?) pieces of the same kind
                        self.display_screen_behavior(game, screen)

                        dragger.update_blit(screen)

                # Check the mouse release event
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragger.undrag_piece()

                # Check when the game is closed
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


run = Run()
run.infinite_run_loop()
