from pygame import *
init()
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play(-1)
volume = 0.2
mixer.music.set_volume(volume)
kick = mixer.Sound('kick.ogg')
money = mixer.Sound('money.ogg')
font = font.SysFont('Arial', 70)


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.width = width
        self.rect.height = height
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, x, y, width, height, speed):
        super().__init__(player_image, x, y, width, height)
        self.speed = speed

    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < window_size[1] - self.rect.height:
            self.rect.y += self.speed
        if keys_pressed[K_d] and self.rect.x < window_size[0] - self.rect.width:
            self.rect.x += self.speed
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed

class Enemy(GameSprite):
    def __init__(self, player_image, x, y, width, height, speed):
        super().__init__(player_image, x, y, width, height)
        self.speed = speed
        self.direction = 'left'

    def update(self):
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

        if self.rect.x <= 493:
            self.direction = 'right'
        elif self.rect.x >= window_size[0] - self.rect.width:
            self.direction = 'left'

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height, ):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y


    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

walls = sprite.Group()
walls.add(Wall(75, 255, 137, 197, 19, 19, 341))
walls.add(Wall(75, 255, 137, 148, 437, 341, 19))
walls.add(Wall(75, 255, 137, 293, 19, 19, 341))
walls.add(Wall(75, 255, 137, 293, 341, 93, 19))
walls.add(Wall(75, 255, 137, 472, 232, 19, 293))
walls.add(Wall(75, 255, 137, 472, 0, 19, 131))
walls.add(Wall(75, 255, 137, 399, 217, 93, 19))

player = Player('hero.png', 45, 432, 65, 65, 5)
enemy = Enemy('cyborg.png', 625, 311, 65, 65, 1)
treasure = GameSprite('treasure.png', 579, 432, 50, 50)

window_size = (700, 500)
run = True
finish = False

window = display.set_mode(window_size)
display.set_caption('Лабиринт')
background = transform.scale(image.load('background.jpg'), window_size)

clock = time.Clock()
FPS = 60

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_KP_PLUS:
                if volume < 1.5:
                    volume += 0.1
            if e.key == K_KP_MINUS:
                if volume > 0:
                    volume -= 0.1

    if not finish:
        window.blit(background, (0, 0))
        walls.draw(window)
        player.reset()
        enemy.reset()
        treasure.reset()
        if sprite.collide_rect(player, treasure):
            finish = True
            money.play()
            win = font.render('YOU WIN', True, (255, 215, 0))
            window.blit(win, (window_size[0] // 2 - 100, window_size[1] // 2 - 37))
            mixer.music.pause()
        if sprite.collide_rect(player, enemy) or sprite.spritecollide(player, walls, False):
            finish = True
            kick.play()
            win = font.render('YOU LOSE', True, (255, 25, 25))
            window.blit(win, (window_size[0] // 2 - 100, window_size[1] // 2 - 37))        
            mixer.music.pause()
        player.update()
        enemy.update()
    else:
        time.delay(750)
        mixer.music.unpause()
        player.rect.x = 45
        player.rect.y = 432
        finish = False
    mixer.music.set_volume(volume)
    clock.tick(FPS)
    display.flip()
    