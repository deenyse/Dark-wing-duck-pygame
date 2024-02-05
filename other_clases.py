import pygame
class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,hp,move_range):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/enemies/orange_1.png')
        self.correlation = (self.image.get_size()[0] / self.image.get_size()[1])
        self.image_height = 100
        self.image_width = round(self.image_height * self.correlation)
        self.image = pygame.transform.scale(self.image, (self.image_width, self.image_height))

        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.bottom = y
        self.hp = hp

        self.anim_count = 0

        self.right = False
        self.left = True

        self.speed = 2

        self.shooting = False

        self.move_time = 0
        self.move_range = move_range

    def updating(self):
        if self.move_time < self.move_range and self.left:
            self.rect.x -= self.speed
            if self.move_time % 50 == 0:
                self.shooting = True
            else:
                self.shooting = False
        elif self.move_time < self.move_range and self.right:
            self.rect.x += self.speed
            if self.move_time % 50 == 0:
                self.shooting = True
            else:
                self.shooting = False
        else:
            self.left,self.right = self.right, self.left
            self.move_time = 0
        self.move_time +=1

class bullet_type(pygame.sprite.Sprite):
    def __init__(self, x, y, filename, fly_side, damage,pers):
        pygame.sprite.Sprite.__init__(self)
        self.image_r = pygame.image.load(filename).convert_alpha()
        self.image_r = pygame.transform.rotate(self.image_r, -90)
        self.image_width = 27
        self.correlation = (self.image_r.get_size()[1] / self.image_r.get_size()[0])
        self.image_height = round(self.image_width * self.correlation)
        self.image_r = pygame.transform.scale(self.image_r, (self.image_width, self.image_height))
        self.image_l = pygame.transform.flip(self.image_r, True, False)

        self.image = self.image_r

        self.damage = damage

        self.side = fly_side

        self.rect = self.image_r.get_rect(center=(x+30*self.side - 10, y))
        self.pers = pers
    def fly(self):
        self.rect.x+= 9*self.side


