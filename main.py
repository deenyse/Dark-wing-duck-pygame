import pygame
from player import Player
from platforms import Platform
from other_clases import Enemy, bullet_type

size = (1200,800)
W = size[0]
H = size[1]
sc = pygame.display.set_mode(size)

is_dead = False
enemies = []

walk_right_hero=[pygame.image.load('walk_gif/black_'+i+'.png')for i in ['1','2','3','4']]
walk_left_hero = [pygame.transform.flip(i,1,0) for i in walk_right_hero]

main_hero = Player(90,620,walk_right_hero,walk_left_hero,100)
left = right = up = False


level = [
    "                                                                                                                                                                                                                    ",
    "                                                                                                                                                                                                                    ",
    "                                                                                                                                                                                                                    ",
    "                                                                                                                                                                                                                    ",
    "                                                                                                                                                                                            b                       ",
    "                                                                                                                                                                                          ---                       ",
    "                                                                                                                                                                                                                    ",
    "                                                                                                                                                                                                       b            ",
    "                                                                                                                                                                                     -                 <============",
    "                                                                                                                                    -                                                -                    i       i ",
    "                                                                                                                                    -            t                                   -        y           i       i ",
    "                                                                                                                                    ----------------                                 -----------          i       i ",
    "                                                                                                                                                                                                          i       i ",
    "                                                   b                                                                                                                                                      i       i ",
    "                                                ----                                                                                                       b                                         --   i       i ",
    "                                                                                                                                                           ----              ---                          i       i ",
    "                                                                       <=========>                                                                                                                        i       i ",
    "                                         ---                            i       i                                             <======================>                               <================>   i       i ",
    " b                                                          ----        i       i                               ----              i               i                  ----             i              i    i       i ",
    " <======>                      <======>                     -           i      <===>                            -                 i               i                                   i              i    i       i ",
    "  i    i                 --     i    i                                  i       i  i           ---                              r i               i                                   i              i    i       i ",
    "  i    i              e         i    i                                  i       i <===>                  ---            <==========>              i                                   i              i    i       i ",
    "  i    i     <========>         i    i                                  i       i  i i                                   i        i               i                                   i              i    i       i ",
    "  i    i       i    i           i    i                                  i      <===========>                             i        i               i                                   i              i    i       i ",
    "  i    i       i    i           i    i                                  i       i         i                              i        i               i                                   i              i    i       i ",
    "  i    i       i    i           i    i                                  i       i         i                              i        i               i                                   i              i    i       i "]

sprite_group = pygame.sprite.Group()
sprite_group.add(main_hero)
platformes_list = []
x=y=0
for row in level:  # вся строка
    for col in row:  # каждый символ
        if col == "-":
            pl = Platform(x,y,'images/metal_const.png')
            sprite_group.add(pl)
            platformes_list.append(pl)
        elif col == 'i':
            pl = Platform(x, y, 'images/stolb.png')
            sprite_group.add(pl)
            platformes_list.append(pl)
        elif col == '<':
            pl = Platform(x, y, 'images/pl_left.png')
            sprite_group.add(pl)
            platformes_list.append(pl)
        elif col == '=':
            pl = Platform(x, y, 'images/pl_mid.png')
            sprite_group.add(pl)
            platformes_list.append(pl)
        elif col == '>':
            pl = Platform(x, y, 'images/pl_right.png')
            sprite_group.add(pl)
            platformes_list.append(pl)
        elif col == 'b':
            pl = Platform(x, y, 'images/barrel.png')
            sprite_group.add(pl)
            platformes_list.append(pl)
        elif col == 'e':
            en = Enemy(x+40,y+40,100,140)
            sprite_group.add(en)
            enemies.append(en)
        elif col == 'r':
            en = Enemy(x+40,y+40,100,100)
            sprite_group.add(en)
            enemies.append(en)
        elif col == 't':
            en = Enemy(x+40,y+40,100,200)
            sprite_group.add(en)
            enemies.append(en)
        elif col == 'y':
            en = Enemy(x+40,y+40,100,90)
            sprite_group.add(en)
            enemies.append(en)
        x += 40  # блоки платформы ставятся на ширине блоков
    y += 40  # то же самое и с высотой
    x = 0

total_level_width = len(level[0])*40
total_level_height = len(level)*40

def enemies_update():
    for enemy in enemies:
        enemy.updating()
        if enemy.shooting:
            if enemy.left:
                bully = bullet_type(enemy.rect.center[0], enemy.rect.center[1], 'images/bullet.png', -1, 10, 'enem')
                bullets.append(bully)
                sprite_group.add(bully)
            elif enemy.right:
                bully = bullet_type(enemy.rect.center[0], enemy.rect.center[1], 'images/bullet.png', 1, 10, 'enem')
                bullets.append(bully)
                sprite_group.add(bully)

def bullet_fly():
    for bullet in bullets:
        if damage_enemies(bullet) or bullet.rect.centerx < 0 or bullet.rect.centerx > total_level_width or bullet.rect.collidelist(platformes_list)>=0 or damage_hero(bullet):
            bullet.kill()
            bullets.pop(bullets.index(bullet))

        else:
            bullet.fly()

def is_dieing():
    global is_dead
    if main_hero.rect.top > total_level_height:
        is_dead = True


def damage_enemies(bullet):
    for enemy in enemies:
        if enemy.rect.collidepoint(bullet.rect.center) and bullet.pers == 'hero':
            enemy.hp-=bullet.damage
            if enemy.hp<=0:
                enemy.kill()
                enemies.pop(enemies.index((enemy)))
            return True

def damage_hero(bullet):
    global is_dead
    if main_hero.rect.collidepoint(bullet.rect.center) and bullet.pers != 'hero':
        main_hero.hp -= bullet.damage
        if main_hero.hp <= 0:
            is_dead = True

class Camera:
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_func(camera, target_rect):
    l = -target_rect.x + size[0]/2
    t = -target_rect.y + size[1]/2
    w,h = camera.width , camera.height


    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width  - size[0]), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - size[1]), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return pygame.Rect(l, t, w, h)



camera = Camera(camera_func, total_level_width,total_level_height)

clock = pygame.time.Clock()

bg = pygame.image.load('wp.jpg')
bg = pygame.transform.scale(bg,size)

bullets = []

repeat = True

while repeat:
    clock.tick(60)
    if not(is_dead):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                repeat = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left = True
                if event.key == pygame.K_RIGHT:
                    right = True
                if event.key == pygame.K_UP:
                    up = True
                if event.key == pygame.K_SPACE:
                    if main_hero.prev_move=='R':
                        bully = bullet_type(main_hero.rect.center[0], main_hero.rect.center[1], 'images/bullet.png', 1,17,'hero')
                        bullets.append(bully)
                        sprite_group.add(bully)
                    else:
                        bully = bullet_type(main_hero.rect.center[0], main_hero.rect.center[1], 'images/bullet.png', -1,17,'hero')
                        bullets.append(bully)
                        sprite_group.add(bully)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left = False
                if event.key == pygame.K_RIGHT:
                    right = False
                if event.key == pygame.K_UP:
                    up = False
        is_dieing()
        bullet_fly()
        sc.blit(bg,(0,0))
        enemies_update()
        main_hero.update(left,right,up,platformes_list)
        camera.update(main_hero)
        for e in sprite_group:
            sc.blit(e.image, camera.apply(e))
        pygame.display.update()
    else:
        sc.fill((0,0,0))
        sc.blit(pygame.image.load('dead.png').convert_alpha(),(0,0))
        pygame.display.update()

pygame.quit()