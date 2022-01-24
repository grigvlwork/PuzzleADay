import pygame

class SpriteRotate(pygame.sprite.Sprite):

    def __init__(self, imageName, origin, pivot):
        super().__init__() 
        self.image = pygame.image.load(imageName)
        self.original_image = self.image
        self.rect = self.image.get_rect(topleft = (origin[0]-pivot[0], origin[1]-pivot[1]))
        self.origin = origin
        self.pivot = pivot
        self.angle = 0

    def update(self):
        image_rect = self.original_image.get_rect(topleft = (self.origin[0] - self.pivot[0], self.origin[1]-self.pivot[1]))
        offset_center_to_pivot = pygame.math.Vector2(self.origin) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-self.angle)
        rotated_image_center = (self.origin[0] - rotated_offset.x, self.origin[1] - rotated_offset.y)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center = rotated_image_center)
  
pygame.init()
size = (400,400)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

cannon = SpriteRotate('cannon.png', (200, 200), (33.5, 120))
cannon_mount = SpriteRotate('cannon_mount.png', (200, 200), (43, 16))
all_sprites = pygame.sprite.Group([cannon, cannon_mount])
angle_range = [-90, 0]
angle_step = -1

frame = 0
done = False
while not done:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    all_sprites.update()
    screen.fill((64, 128, 255))
    pygame.draw.rect(screen, (127, 127, 127), (0, 250, 400, 150))
    all_sprites.draw(screen)
    pygame.display.flip()
    frame += 1
    cannon.angle += angle_step
    if not angle_range[0] < cannon.angle < angle_range[1]:
        angle_step *= -1
    
pygame.quit()
exit()
