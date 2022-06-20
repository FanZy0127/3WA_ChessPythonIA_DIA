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

    def infinite_run_loop(self):
        game = self.chess_game
        screen = self.screen

        while True:
            game.display_background(screen)
            game.display_pieces(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


run = Run()
run.infinite_run_loop()
