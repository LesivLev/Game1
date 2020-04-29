# 1 - подключить библиотеки
# 2 - создать глобальные перменные
# 3 - создать окно игры

import pygame
import random

# ширина, высота, фпс (частота кадров), основные цвета
WIDTH = 400
HEIGHT = 500
FPS = 60

# цвета задаются по RGB (КЗС) от 0 до 255
# Черный - 0 цветов
# Белый - все цвета
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# настройка игрового окна

pygame.init() # создание игры
pygame.mixer.init() # создание (подключение) звуков
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # создание экрана
pygame.display.set_caption("World of Tanks") # определяем название игры
clock = pygame.time.Clock()

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
        self.speedx = 0 # скокрость передвижения спрайта по оси X
        self.speedy = 0
        
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

class Zombie(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # Определяем переменную как спрайт
        self.image = pygame.Surface((20, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        if(random.randint(0, 2)==0):
            self.rect.centerx == 10
        else:
            self.rect.centerx == HEIGHT-10
        self.rect.centery =random.randint(0, WIDTH-9)
        self.speedx = 0  
        self.speedy = 0

        

# Создать группы спрайтов, чтобы работx`ать с ними со всеми одновременно
all_sprites = pygame.sprite.Group()
player = Player() # создаем переменную player класса Player
all_sprites.add(player) # добавляем игрока в группу всех спрайтов
for i in range (0, 3):
    zombie = Zombie()
    all_sprites.add(zombie)
# Игровой цикл
# 1 - проверить, что цикл работает на правильной частоте обновления кадров
# 2 - обработка ввода
# 3 - обновление данных
# 4 - вывод изменений на экран

run = True # переменная, которая отвечает за запуск игрового цикла
while run:
    clock.tick(FPS) # проверка пункта 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    all_sprites.update()

    screen.fill(BLACK) # заполнение экрана цветом
    all_sprites.draw(screen) # вносим изменения спрайтов на экран
    pygame.display.flip() # обновление экран (отображение нового кадра)

pygame.quit()