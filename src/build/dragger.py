import pygame
from src.consts.consts import *


class Dragger:

    def __init__(self):
        self.mouse_x = 0
        self.mouse_y = 0
        self.base_row = 0
        self.base_column = 0
        self.piece = None
        self.dragging = False

    def update_mouse(self, position):
        self.mouse_x, self.mouse_y = position  # (x_coordinate, y_coordinate)

    def save_base_position(self, position):
        self.base_column = position[0] // SQUARE_SIZE
        self.base_row = position[1] // SQUARE_SIZE

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False

    def update_blit(self, surface):
        # Image_path
        self.piece.set_image(size=128)
        image_path = self.piece.image

        # Image
        image = pygame.image.load(image_path)

        # Rectangle
        image_center = (self.mouse_x, self.mouse_y)
        self.piece.texture_rectangle = image.get_rect(center=image_center)

        # Blit
        surface.blit(image, self.piece.texture_rectangle)
