import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image,(40,40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
