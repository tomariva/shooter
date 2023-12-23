from pygame import *
from random import randint
from time import time as timer

win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')

#clock = time.Clock()
#FPS = 60

font.init()
font2 = font.SysFont('Arial', 36)
font1 = font.SysFont('Arial', 80)
lose = font1.render('You lose!', True, (255, 0, 0))
win = font1.render('You win!', True, (0, 255, 50))

score = 0
lost = 0
life = 3
amount_fire = 5


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def resert(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()

        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 5:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= win_height:
            self.rect.x = randint(0, win_width-80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
    
ship = Player('rocket.png',  5, win_height - 100, 80, 100, 15)

monsters = sprite.Group()
bullets = sprite.Group()

for i in range(1, 6):
    monster = Enemy('ufo.png', randint(0,win_width-80), 0, 110, 75, randint(1, 7))
    monsters.add(monster)

asteroids = sprite.Group()

for i in range(1, 3):
    asteroid = Enemy('asteroid.png', randint(0, win_width), 0, 110, 75, randint(5, 7))
    asteroids.add(asteroid)

rel_time = False
num_fire = 0

run = True
finish = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    amount_fire -=1
                    fire_sound.play()
                    ship.fire()

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(background, (0, 0))

        text = font2.render('Счёт:' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        text_bullet = font2.render('Осталось пуль:' + str(amount_fire), 1, (255, 255, 255))
        window.blit(text_bullet, (10, 80))
        
        ship.update()
        ship.resert()

        bullets.update()
        bullets.draw(window)

        monsters.update()
        monsters.draw(window)

        asteroids.update()
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload_time = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload_time, (160, 460))

            else:
                num_fire = 0
                amount_fire = 5
                rel_time = False

        if sprite.spritecollide(ship, monsters, True):
            life -= 1

        if sprite.spritecollide(ship, asteroids, True):
            life -= 1

        if sprite.groupcollide(bullets, monsters, True, True):
            monster = Enemy('ufo.png', randint(0,win_width-80), 0, 110, 75, randint(1, 7))
            monsters.add(monster)
            score += 1

        if score >= 10:
            finish = True
            window.blit(win, (200, 200))

        if lost > 6:
            finish = True
            window.blit(lose, (200, 200))

        if life < 1:
            finish = True
            window.blit(lose, (200, 200))

        if life == 3:
            life_color = (0, 255, 0)
        if life == 2:
            life_color = (150, 120, 0)
        if life == 1:
            life_color = (255, 0, 0)
        
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))

        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        life = 3
        amount_fire = 5
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()

        time.delay(2000)
        for i in range(1, 6):
            monster = Enemy('ufo.png', randint(0,win_width-80), 0, 110, 75, randint(1, 7))
            monsters.add(monster)

        for i in range(1, 3):
            asteroid = Enemy('asteroid.png', randint(0, win_width), 0, 110, 75, randint(5, 7))
            asteroids.add(asteroid)

    time.delay(60)