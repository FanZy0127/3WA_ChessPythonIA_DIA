import sys
import pygame
from consts.consts import *
from src.build.piece import *
from src.build.move import Move
from src.build.square import Square
from src.build.chess_game import Chess


class Run:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('3WA_DIA : Baptiste HARAMBOURE IA Chess Project')
        self.chess_game = Chess()

    @staticmethod
    def display_screen_behavior(game, screen):
        game.display_background(screen)
        game.display_last_move(screen)
        game.display_moves(screen)
        game.display_pieces(screen)
        game.display_hovered_square(screen)

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

                        if piece.color == game.next_player:
                            board.calculate_allowed_moves(piece, clicked_row, clicked_column)
                            dragger.save_base_position(event.pos)
                            dragger.drag_piece(piece)
                            self.display_screen_behavior(game, screen)

                # Check the mouse motion event
                elif event.type == pygame.MOUSEMOTION:
                    row = event.pos[1] // SQUARE_SIZE
                    column = event.pos[0] // SQUARE_SIZE
                    game.set_hover_square(row, column)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        # Necessary code to avoid flickering of all pieces while dragging one
                        # Also avoid the dragged piece to be followed by ghosts(?) pieces of the same kind
                        self.display_screen_behavior(game, screen)

                        dragger.update_blit(screen)

                # Check the mouse release event
                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        released_row = dragger.mouse_y // SQUARE_SIZE
                        released_column = dragger.mouse_x // SQUARE_SIZE

                        base_square = Square(dragger.base_row, dragger.base_column)
                        final_square = Square(released_row, released_column)
                        move = Move(base_square, final_square)

                        if board.validate_move(dragger.piece, move):
                            board.apply_move_on_screen(dragger.piece, move)
                            # Method allowing the prise en passant if the pawn just moved, else it isn't allowed
                            board.set_prise_en_passant(dragger.piece)

                            if final_square.row == 0 or final_square.row == 7:
                                if isinstance(dragger.piece, Pawn):
                                    game.board.promote_pawn(dragger.piece)

                            self.display_screen_behavior(game, screen)
                            game.next_turn()

                    dragger.undo_drag_piece()

                # Check when a key is pressed on keyboard
                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_r:
                        game.restart()
                        game = self.chess_game
                        dragger = self.chess_game.dragger
                        board = self.chess_game.board

                    # Check when the game is closed with Esc
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                # Check when the game is closed
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


run = Run()
run.infinite_run_loop()
