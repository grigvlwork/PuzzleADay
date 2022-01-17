import os

import pygame
import sys

#
# myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
# ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
from pygame.sprite import AbstractGroup

pygame.init()
size = width, height = (1080, 540)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Puzzle-A-Day")
icon = pygame.image.load('images/icon.jpg')
pygame.display.set_icon(icon)
fps = 60


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if colorkey == -1:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    image = image.convert_alpha()
    return image


pixelimage = load_image('pix1.png')

class Board:
    def __init__(self):
        self.field = []
        self.sprites = pygame.sprite.Group()
        self.l_big_piece = LBigPiece(550, 350, self.sprites)
        self.c_piece = CPiece(620, 270, self.sprites)
        self.l_small_piece = LSmallPiece(550, 20, self.sprites)
        self.o_piece = OPiece(620, 10, self.sprites)
        self.p_piece = PPiece(760, 10, self.sprites)
        self.t_piece = TPiece(760, 280, self.sprites)
        self.z_big_piece = ZBigPiece(890, 10, self.sprites)
        self.z_small_piece = ZSmallPiece(900, 280, self.sprites)
        self.arr_sprites = [self.l_big_piece, self.c_piece, self.l_small_piece, self.o_piece,
                            self.p_piece, self.t_piece, self.z_big_piece, self.z_small_piece]
        self.current_piece = None

    def set_current_piece(self, number):
        for sprite in self.arr_sprites:
            if sprite.is_current:
                self.current_piece = sprite.number

    def new(self):
        self.field = [[-1, -1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, 0, 0, 0, 0, 0, 0, -1, -1],
                      [-1, 0, 0, 0, 0, 0, 0, -1, -1],
                      [-1, 0, 0, 0, 0, 0, 0, 0, -1],
                      [-1, 0, 0, 0, 0, 0, 0, 0, -1],
                      [-1, 0, 0, 0, 0, 0, 0, 0, -1],
                      [-1, 0, 0, 0, 0, 0, 0, 0, -1],
                      [-1, 0, 0, 0, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1, -1]]

    def draw(self):
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        m = iter(months)
        border_color = pygame.Color(135, 83, 24)
        pygame.draw.rect(screen, pygame.Color(245, 198, 144), (0, 0, 540, 540))
        pygame.draw.rect(screen, border_color, (1, 1, 537, 537), 2)
        font = pygame.font.Font(None, 33)
        num = iter(range(1, 32))
        for i in range(2):
            for j in range(6):
                pygame.draw.rect(screen, border_color, (60 + j * 60, 60 + i * 60, 60, 60), 2)
                text = font.render(next(m), 1, border_color)
                text_x = 60 + j * 60 + 10
                text_y = 60 + i * 60 + 20
                screen.blit(text, (text_x, text_y))
        for i in range(2, 6):
            for j in range(7):
                pygame.draw.rect(screen, border_color, (60 + j * 60, 60 + i * 60, 60, 60), 2)
                text = font.render(str(next(num)), 1, border_color)
                text_x = 60 + j * 60 + 18
                text_y = 60 + i * 60 + 20
                screen.blit(text, (text_x, text_y))
        for j in range(3):
            pygame.draw.rect(screen, border_color, (60 + j * 60, 420, 60, 60), 2)
            text = font.render(str(next(num)), 1, border_color)
            text_x = 60 + j * 60 + 18
            screen.blit(text, (text_x, 440))


class Piece(pygame.sprite.Sprite):
    def __init__(self, x, y, number, *group, image=None):
        super().__init__(*group)
        self.x = x
        self.y = y
        self.number = number
        self.image = image
        self.matrix = []
        self.is_current = False
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            self.is_current = not self.is_current
        if self.is_current and event.type == pygame.MOUSEMOTION:
            self.rect.x = event.pos[0]
            self.rect.y = event.pos[1]



class LBigPiece(Piece):
    image = load_image('L-bigt.png')

    def __init__(self, x, y, *group):
        super().__init__(x, y, 1, group)
        self.image = LBigPiece.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.matrix = [[1, 0, 0],
                       [1, 0, 0],
                       [1, 1, 1]]
        self.visible = 1

class CPiece(Piece):
    image = load_image('Ct.png')

    def __init__(self, x, y, *group):
        super().__init__(x, y, 2, group)
        self.image = CPiece.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.matrix = [[1, 1],
                       [1, 0],
                       [1, 1]]
        self.visible = 1

class LSmallPiece(Piece):
    image = load_image('L-smallt.png')

    def __init__(self, x, y, *group):
        super().__init__(x, y, 3, group)
        self.image = LSmallPiece.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.matrix = [[1, 0],
                       [1, 0],
                       [1, 0],
                       [1, 1]]
        self.visible = 1

class OPiece(Piece):
    image = load_image('Ot.png')

    def __init__(self, x, y, *group):
        super().__init__(x, y, 4, group)
        self.image = OPiece.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.matrix = [[1, 1],
                       [1, 1],
                       [1, 1]]
        self.visible = 1

class PPiece(Piece):
    image = load_image('Pt.png')

    def __init__(self, x, y, *group):
        super().__init__(x, y, 5, group)
        self.image = PPiece.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.matrix = [[1, 1],
                       [1, 1],
                       [1, 0]]
        self.visible = 1

class TPiece(Piece):
    image = load_image('Tt.png')

    def __init__(self, x, y, *group):
        super().__init__(x, y, 6, group)
        self.image = TPiece.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.matrix = [[1, 0],
                       [1, 0],
                       [1, 1],
                       [1, 0]]
        self.visible = 1

class ZBigPiece(Piece):
    image = load_image('Z-bigt.png')

    def __init__(self, x, y, *group):
        super().__init__(x, y, 7, group)
        self.image = ZBigPiece.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.matrix = [[1, 1, 0],
                       [0, 1, 0],
                       [0, 1, 1]]
        self.visible = 1

class ZSmallPiece(Piece):
    image = load_image('Z-smallt.png')

    def __init__(self, x, y, *group):
        super().__init__(x, y, 8, group)
        self.image = ZSmallPiece.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.matrix = [[1, 0],
                       [1, 0],
                       [1, 1],
                       [0, 1]]
        self.visible = 1

board = Board()
board.new()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.sprites.update(event)
    board.draw()
    board.sprites.draw(screen)
    pygame.display.flip()
