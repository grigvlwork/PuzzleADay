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

def rotate_matrix_right(a):
    rows = len(a)
    cols = len(a[0])
    b = [[0] * rows for i in range(cols)]
    for i in range(rows):
        for j in range(cols):
            b[j][rows - i] = a[i][j]
    return b

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
        for sprite in self.arr_sprites:
            sprite.load()
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
        pygame.draw.rect(screen, pygame.Color(245, 198, 144), (540, 0, 1080, 540))
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
        self.dx = 0
        self.dy = 0
        self.number = number
        self.images = [pixelimage]
        self.rotate_right_dict = {0: 0}
        self.rotate_left_dict = {0: 0}
        self.mirror_dict = {0: 0}
        self.current_state = 1
        self.matrix = []
        self.is_current = False
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.current_state = 0

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            if self.in_matrix(args[0].pos[0], args[0].pos[1]):
                self.is_current = not self.is_current
            if self.is_current:
                self.dx = self.rect.x - args[0].pos[0]
                self.dy = self.rect.y - args[0].pos[1]
            if self.is_current and args[0].button == 5:
                self.rotate_right()
            if self.is_current and args[0].button == 4:
                self.rotate_left()
        if self.is_current and event.type == pygame.MOUSEMOTION:
            self.rect.x = event.pos[0] + self.dx
            self.rect.y = event.pos[1] + self.dy
        if self.is_current and event.type == pygame.KEYDOWN:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_SPACE]:
                self.mirror()
            if pressed[pygame.K_ESCAPE]:
                self.is_current = False

    def in_matrix(self, x, y):
        i = (x - self.rect.x) // 60
        j = (y - self.rect.y) // 60
        return self.matrix[i][j] == 1


    def rotate_right(self):
        self.current_state = self.rotate_right_dict[self.current_state]
        self.image = self.images[self.current_state]
        self.rect = self.image.get_rect()
        self.rect.x = event.pos[0] + self.dx
        self.rect.y = event.pos[1] + self.dy

    def rotate_left(self):
        self.current_state = self.rotate_left_dict[self.current_state]
        self.image = self.images[self.current_state]
        self.rect = self.image.get_rect()
        self.rect.x = event.pos[0] + self.dx
        self.rect.y = event.pos[1] + self.dy

    def mirror(self):
        self.current_state = self.mirror_dict[self.current_state]
        curr_rect = self.rect
        self.image = self.images[self.current_state]
        self.rect = self.image.get_rect()
        self.rect.x = curr_rect.x
        self.rect.y = curr_rect.y
        self.is_current = False

    def load(self):
        pass


class LBigPiece(Piece):
    image = load_image('L-bigt.png')

    def __init__(self, x, y, *group):
        super().__init__(x, y, 1, group)
        self.images = [LBigPiece.image]
        self.rect = self.images[0].get_rect()
        self.rect.x, self.rect.y = x, y
        self.matrix = [[1, 0, 0],
                       [1, 0, 0],
                       [1, 1, 1]]
        self.visible = 1

    def load(self):
        list_pics = ['L-bigt90.png', 'L-bigt180.png', 'L-bigt270.png']
        for pic in list_pics:
            self.images.append(load_image(pic))
        self.rotate_right_dict = {0: 1, 1: 2, 2: 3, 3: 0}
        self.rotate_left_dict = {0: 3, 1: 0, 2: 1, 3: 2}
        self.mirror_dict = {0: 2, 1: 3, 2: 0, 3: 1}



class CPiece(Piece):
    image = load_image('Ct.png')

    def __init__(self, x, y, *group):
        super().__init__(x, y, 2, group)
        self.images = [CPiece.image]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.matrix = [[1, 1],
                       [1, 0],
                       [1, 1]]
        self.visible = 1

    def load(self):
        list_pics = ['Ct90.png', 'Ct180.png', 'Ct270.png']
        for pic in list_pics:
            self.images.append(load_image(pic))
        self.rotate_right_dict = {0: 1, 1: 2, 2: 3, 3: 0}
        self.rotate_left_dict = {0: 3, 1: 0, 2: 1, 3: 2}
        self.mirror_dict = {0: 2, 1: 3, 2: 0, 3: 1}


class LSmallPiece(Piece):
    image = load_image('L-smallt.png')

    def __init__(self, x, y, *group):
        super().__init__(x, y, 3, group)
        self.images = [LSmallPiece.image]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.matrix = [[1, 0],
                       [1, 0],
                       [1, 0],
                       [1, 1]]
        self.visible = 1

    def load(self):
        list_pics = ['L-smallt90.png', 'L-smallt180.png', 'L-smallt270.png',
                     'L-smalltmirrv.png', 'L-smalltmirrv90.png', 'L-smalltmirrv180.png', 'L-smalltmirrv270.png']
        for pic in list_pics:
            self.images.append(load_image(pic))
        self.rotate_right_dict = {0: 1, 1: 2, 2: 3, 3: 0, 4: 5, 5: 6, 6: 7, 7: 4}
        self.rotate_left_dict = {0: 3, 1: 0, 2: 1, 3: 2, 4: 7, 5: 4, 6: 5, 7: 6}
        self.mirror_dict = {0: 4, 1: 5, 2: 6, 3: 7, 4: 0, 5: 1, 6: 2, 7: 3}


class OPiece(Piece):
    image = load_image('Ot.png')

    def __init__(self, x, y, *group):
        super().__init__(x, y, 4, group)
        self.images = [OPiece.image]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.matrix = [[1, 1],
                       [1, 1],
                       [1, 1]]
        self.visible = 1

    def load(self):
        list_pics = ['Ot90.png']
        for pic in list_pics:
            self.images.append(load_image(pic))
        self.rotate_right_dict = {0: 1, 1: 0}
        self.rotate_left_dict = {0: 1, 1: 0}
        self.mirror_dict = {0: 0, 1: 1}


class PPiece(Piece):
    image = load_image('Pt.png')

    def __init__(self, x, y, *group):
        super().__init__(x, y, 5, group)
        self.images = [PPiece.image]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.matrix = [[1, 1],
                       [1, 1],
                       [1, 0]]
        self.visible = 1

    def load(self):
        list_pics = ['Pt90.png', 'Pt180.png', 'Pt270.png',
                     'Ptmirrv.png', 'Ptmirrv90.png', 'Ptmirrv180.png', 'Ptmirrv270.png']
        for pic in list_pics:
            self.images.append(load_image(pic))
        self.rotate_right_dict = {0: 1, 1: 2, 2: 3, 3: 0, 4: 5, 5: 6, 6: 7, 7: 4}
        self.rotate_left_dict = {0: 3, 1: 0, 2: 1, 3: 2, 4: 7, 5: 4, 6: 5, 7: 6}
        self.mirror_dict = {0: 4, 1: 5, 2: 6, 3: 7, 4: 0, 5: 1, 6: 2, 7: 3}


class TPiece(Piece):
    image = load_image('Tt.png')

    def __init__(self, x, y, *group):
        super().__init__(x, y, 6, group)
        self.images = [TPiece.image]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.matrix = [[1, 0],
                       [1, 0],
                       [1, 1],
                       [1, 0]]
        self.visible = 1

    def load(self):
        list_pics = ['Tt90.png', 'Tt180.png', 'Tt270.png',
                     'Ttmirrv.png', 'Ttmirrv90.png', 'Ttmirrv180.png', 'Ttmirrv270.png']
        for pic in list_pics:
            self.images.append(load_image(pic))
        self.rotate_right_dict = {0: 1, 1: 2, 2: 3, 3: 0, 4: 5, 5: 6, 6: 7, 7: 4}
        self.rotate_left_dict = {0: 3, 1: 0, 2: 1, 3: 2, 4: 7, 5: 4, 6: 5, 7: 6}
        self.mirror_dict = {0: 4, 1: 5, 2: 6, 3: 7, 4: 0, 5: 1, 6: 2, 7: 3}


class ZBigPiece(Piece):
    image = load_image('Z-bigt.png')

    def __init__(self, x, y, *group):
        super().__init__(x, y, 7, group)
        self.images = [ZBigPiece.image]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.matrix = [[1, 1, 0],
                       [0, 1, 0],
                       [0, 1, 1]]
        self.visible = 1

    def load(self):
        list_pics = ['Z-bigt90.png', 'Z-bigtmirrv.png', 'Z-bigtmirrv90.png']
        for pic in list_pics:
            self.images.append(load_image(pic))
        self.rotate_right_dict = {0: 1, 1: 0, 2: 3, 3: 2}
        self.rotate_left_dict = {0: 1, 1: 0, 2: 3, 3: 2}
        self.mirror_dict = {0: 2, 1: 3, 2: 0, 3: 1}


class ZSmallPiece(Piece):
    image = load_image('Z-smallt.png')

    def __init__(self, x, y, *group):
        super().__init__(x, y, 8, group)
        self.images = [ZSmallPiece.image]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.matrix = [[1, 0],
                       [1, 0],
                       [1, 1],
                       [0, 1]]
        self.visible = 1

    def load(self):
        list_pics = ['Z-smallt90.png', 'Z-smallt180.png', 'Z-smallt270.png',
                     'Z-smalltmirrv.png', 'Z-smalltmirrv90.png', 'Z-smalltmirrv180.png', 'Z-smalltmirrv270.png']
        for pic in list_pics:
            self.images.append(load_image(pic))
        self.rotate_right_dict = {0: 1, 1: 2, 2: 3, 3: 0, 4: 5, 5: 6, 6: 7, 7: 4}
        self.rotate_left_dict = {0: 3, 1: 0, 2: 1, 3: 2, 4: 7, 5: 4, 6: 5, 7: 6}
        self.mirror_dict = {0: 4, 1: 5, 2: 6, 3: 7, 4: 0, 5: 1, 6: 2, 7: 3}


board = Board()
board.new()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.sprites.update(event)
        if event.type == pygame.MOUSEMOTION:
            board.sprites.update(event)
        if event.type == pygame.KEYDOWN:
            board.sprites.update(event)
    board.draw()
    board.sprites.draw(screen)
    pygame.display.flip()
