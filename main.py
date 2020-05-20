# 1 - подключить библиотеки
# 2 - создать глобальные перменные
# 3 - создать окно игры

import pygame
import random
import math

# ширина, высота, фпс (частота кадров), основные цвета
WIDTH = 800
HEIGHT = 700
FPS = 60

# цвета задаются по RGB (КЗС) от 0 до 255
# Черный - 0 цветов
# Белый - все цвета
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (255, 0, 255)
VP = 25


# настройка игрового окна

pygame.init() # создание игры
pygame.mixer.init() # создание (подключение) звуков
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # создание экрана
pygame.display.set_caption("Zombe in swamP") # определяем название игры
clock = pygame.time.Clock()

def draw_shield_bar(surf, x, y, pct, colour):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, colour, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def levelup(level):
    zombie.speed += level//4
    bullet.speed -= level//2

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # Определяем переменную как спрайт
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect() # Берем прямоугольник, который отвечает за спрайт
        # у rect есть centerx, centery - центр по оси X прямоугльника и центр по оси Y прямоугольника
        # у rect есть left, right, top, bottom - левая граница, правая граница, верхняя граница, нижняя граница
        # у rect есть x, y - координата по оси X и по оси Y
        self.rect.centery = HEIGHT / 2
        self.rect.centerx = WIDTH / 2
        self.hp = 100
        self.speedx = 0 # скокрость передвижения спрайта по оси X
        self.speedy = 0
        self.score = 0
        
    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5 
        if keystate[pygame.K_DOWN]:
            self.speedy = 5
        if keystate[pygame.K_UP]:
            self.speedy = -5

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def hit(self):
        self.hp -= 1


class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # Определяем переменную как спрайт
        self.image = pygame.Surface((20, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        tmp = random.randint(0, 4) 
        if(tmp == 0):
            self.rect.centery = 10
            self.rect.centerx = random.randint(0, WIDTH)
        elif(tmp == 1):
            self.rect.centery = HEIGHT-10
            self.rect.centerx = random.randint(0, WIDTH)
        elif(tmp == 2):
            self.rect.centery = random.randint(0, HEIGHT)
            self.rect.centerx = 10
        elif(tmp == 3):
            self.rect.centery = random.randint(0, HEIGHT)
            self.rect.centerx = WIDTH-10
        self.speedx = 0  
        self.speedy = 0
        self.hp = 20
        self.speed = 1

    def Hp(self):
        self.hp -= 10

    def update(self, text=""):
        if text == "regen":
            self.regenerate()
            return
        self.speedx = 0
        self.speedy = 0

        if(player.rect.x > self.rect.x):
            self.speedx = self.speed
        if(player.rect.x < self.rect.x):
            self.speedx = -self.speed
        if(player.rect.x == self.rect.x):
            self.speedx = 0
        if(player.rect.y > self.rect.y):
            self.speedy = self.speed
        if(player.rect.y < self.rect.y):
            self.speedy = -self.speed
        if(player.rect.y == self.rect.y):
            self.speedy = 0
        
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def regenerate(self):
        # Обновить координаты, восполнить жизни
        tmp = random.randint(0, 4) 
        if(tmp == 0):
            self.rect.centery = -10
            self.rect.centerx = random.randint(-10, WIDTH + 10)
        elif(tmp == 1):
            self.rect.centery = HEIGHT+10
            self.rect.centerx = random.randint(-10, WIDTH + 10)
        elif(tmp == 2):
            self.rect.centery = random.randint(-10, HEIGHT + 10)
            self.rect.centerx = -10
        elif(tmp == 3):
            self.rect.centery = random.randint(-10, HEIGHT + 10)
            self.rect.centerx = WIDTH+10
        self.hp = 20

class Bullet(pygame.sprite.Sprite):
    def __init__(self, zombie):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = player.rect.centerx
        self.rect.centery = player.rect.centery
        self.speedx = 0
        self.speedy = 0
        self.speed = 7

    def next_zombie(self):
        curr = 1000000
        answer = None
        for zombie in all_zombies:
            tmp = math.fabs(self.rect.centerx - zombie.rect.centerx) + math.fabs(self.rect.centery - zombie.rect.centery)
            if tmp < curr:
                answer = zombie
                curr = tmp
        return answer
        # a = math.fabs(self.rect.centerx - zombie1.rect.centerx) + math.fabs(self.rect.centery - zombie1.rect.centery)
        # b = math.fabs(self.rect.centerx - zombie2.rect.centerx) + math.fabs(self.rect.centery - zombie2.rect.centery)
        # c = math.fabs(self.rect.centerx - zombie3.rect.centerx) + math.fabs(self.rect.centery - zombie3.rect.centery)


        # if min(a, b, c) == c:
        #     return zombie3
        # if min(a, b, c) == b:
        #     return zombie2
        # if min(a, b, c) == a:
        #     return zombie1

    def update(self):
        self.zombie = self.next_zombie()
        if(self.zombie.rect.centerx > self.rect.x):
            self.speedx = self.speed
        if(self.zombie.rect.centerx < self.rect.x):
            self.speedx = -self.speed
        if(self.zombie.rect.centerx == self.rect.x):
            self.speedx = 0
        if(self.zombie.rect.centery > self.rect.y):
            self.speedy = self.speed
        if(self.zombie.rect.centery < self.rect.y):
            self.speedy = -self.speed
        if(self.zombie.rect.centery == self.rect.y):
            self.speedy = 0
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
     
class Wall(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 200))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH//8
        self.rect.centery = HEIGHT//2

#     def update(self):
        


class Dog(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # Определяем переменную как спрайт
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = 340
        self.rect.centery = 340

    def update(self):
        self.speedx = 0
        self.speedy = 0

        if(zombie.rect.x > self.rect.x):
            self.speedx = 3
        if(zombie.rect.x < self.rect.x):
            self.speedx = -3
        if(zombie.rect.x == self.rect.x):
            self.speedx = 0
        if(zombie.rect.y > self.rect.y):
            self.speedy = 3
        if(zombie.rect.y < self.rect.y):
            self.speedy = -3
        if(zombie.rect.y == self.rect.y):
            self.speedy = 0
        
        self.rect.x += self.speedx
        self.rect.y += self.speedy

# Создать группы спрайтов, чтобы работать с ними со всеми одновременно
all_sprites = pygame.sprite.Group()
all_zombies = pygame.sprite.Group()
player = Player() # создаем переменную player класса Player
#dog =  Dog()
# bullet = Bullet()
#coin = Coin()
#all_sprites.add(coin)
# all_sprites.add(bullet)
#all_sprites.add(dog)
all_sprites.add(player) # добавляем игрока в группу всех спрайтов
wall = Wall()
all_sprites.add(wall)
for i in range(0, 3):
    zombie = Zombie()
    all_sprites.add(zombie)
    all_zombies.add(zombie)

isBulletActive = False

# Игровй цикл
# 1 - проверить, что цикл работает на правильной частоте обновления кадров
# 2 - обработка ввода
# 3 - обновление данных
# 4 - вывод изменений на экран

run = True # переменная, которая отвечает за запуск игрового dикла
bullet = None
killedZombie = 0
ifLevelup = False
level = 0
while run:
    clock.tick(FPS) # проверка пункта 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_SPACE]:
        if isBulletActive == False:
            isBulletActive = True
            bullet = Bullet(all_zombies.sprites()[0])
            all_sprites.add(bullet)
            player.score -= 1

    hits = pygame.sprite.spritecollide(player, all_zombies, False)
    for hit in hits:
        player.hit()
        if(player.hp <= 0):
            run = False

    if isBulletActive:
        hits = pygame.sprite.spritecollide(bullet, all_zombies, False)
        for zombie in hits:
            bullet.remove(all_sprites)
            # удалить спрайт пули
            isBulletActive = False
            zombie.Hp()
            player.score += 2
            if zombie.hp == 0:
                if ifLevelup == False:
                    zombie.regenerate()
                    killedZombie += 1
                    player.score += 10
                else:
                    killedZombie += 1
                    zombie.remove(all_sprites)
                    zombie.remove(all_zombies)
                # zombie.remove(all_sprites, all_zombies)
                # zombie = Zombie()
                # all_sprites.add(zombie)
                # all_zombies.add(zombie)

    if (zombie.rect.centerx >= 0 and zombie.rect.centery >= 0) or (zombie.rect.centerx <= WIDTH and zombie.rect.centery >= 0) or (zombie.rect.centerx >= 0 and zombie.rect.centery <= HEIGHT) or (zombie.rect.centerx <= WIDTH and zombie.rect.centery <= HEIGHT):
        killedZombie -= 0

    if player.score >= 100:
        ifLevelup = True
        if killedZombie >= 3:
            level += 1
            killedZombie == 0
            ifLevelup = False
            player.hp = 100
            player.score = 0 
            all_zombies.update("regen") 
            levelup(level)
        else:
            player.score = 100

    all_sprites.update()
    all_zombies.update() # надо понять почему эта строка не нужна

    screen.fill(BLACK) # заполнение экрана цветом
    all_sprites.draw(screen) # вносим изменения спрайтов на экран
    draw_shield_bar(screen, 5, 5, player.hp, GREEN)
    draw_shield_bar(screen, WIDTH - 60, 5, killedZombie * 25, PURPLE)
    draw_shield_bar(screen, 295, 5, player.score, YELLOW)
    draw_shield_bar(screen, 175, 5, level * 10, BLUE)
    pygame.display.flip() # обновление экран (отображение нового кадра)

pygame.quit()

# TODO: добавить время между регенарацией зомби
# TODO: выровнять баланс скоростей
# TODO: сделать шире поле
# TODO: добавить препятствия
# TODO: находить и выбирать при создании пули ближайшего зомби

# git add *
# git commit 
# git push