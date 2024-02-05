import pygame


move_speed = 7
gravity = 0.4
jump_speed = 10
class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,right_ani,left_ani,hp):
        pygame.sprite.Sprite.__init__(self)
        self.resp_x =x
        self.resp_y =y

        self.right_m = right_ani

        self.correlation = (self.right_m[0].get_size()[0] / self.right_m[0].get_size()[1])
        self.image_height = 100
        self.image_width = round(self.image_height * self.correlation)

        self.right_m = [pygame.transform.scale(i, (self.image_width, self.image_height)) for i in self.right_m]

        self.left_m = left_ani
        self.left_m = [pygame.transform.scale(i, (self.image_width, self.image_height)) for i in self.left_m]

        self.image = self.right_m[0]

        self.hp = hp

        self.anim_count = 0

        self.prev_move ='R'

        self.rect = self.image.get_rect()
        self.xvel = 0
        self.yvel = 0
        self.rect.x = x
        self.rect.y = y
        self.onground = False

    def update(self,left,right,up,platforms):
        if left:
            self.xvel = - move_speed

            if self.anim_count + 1 > 60:
                self.anim_count = 0
            self.image = self.left_m[self.anim_count // 15]
            self.prev_move = 'L'
            self.anim_count += 1
        if right:
            self.xvel = move_speed

            if self.anim_count + 1 > 60:
                self.anim_count = 0
            self.image = self.right_m[self.anim_count // 15]
            self.prev_move = 'R'
            self.anim_count += 1
        if up and self.onground:
            self.yvel -= jump_speed

        if not(left or right):
            self.xvel= 0

        if not(self.onground):
            self.yvel += gravity

        self.onground = False
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)


    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onground = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает


