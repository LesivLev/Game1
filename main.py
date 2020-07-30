# 1 - подключить библиотеки
# 2 - создать глобальные перменные
# 3 - создать окно игры

from os import path

import pygame

# ширина, высота, фпс (частота кадров), основные цвета
from bullet import Bullet
from const import WIDTH, HEIGHT, FPS, GREEN, BLUE, YELLOW, BLACK, WHITE, PURPLE
from player import Player
from wall import Wall
from zombie import Zombie

# цвета задаются по RGB (КЗС) от 0 до 255
# Черный - 0 цветов
# Белый - все цвета

# настройка игрового окна

pygame.init()  # создание игры
pygame.mixer.init()  # создание (подключение) звуков
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # создание экрана
pygame.display.set_caption("Zombe in swamP")  # определяем название игры
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
all_zombies = pygame.sprite.Group()
all_walls = pygame.sprite.Group()
player = Player()  # создаем переменную player класса Player
wall = Wall()
zombie = Zombie()
isBulletActive = False
isWallshdPlayer = False
zombie1 = Zombie()
run = True  # переменная, которая отвечает за запуск игрового dикла
bullet = None
killedZombie = 0
ifLevelup = False
level = 0


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
    zombie.speed += level // 4
    bullet.speed -= level // 2


background = pygame.image.load(path.join(path.dirname(__file__), 'background.jpg'))
background_rect = background.get_rect()

font_name = pygame.font.match_font('comicsansms')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def show_start_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Zombie", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, " Нажмите пробел для прыжка, и C для приседания", 18, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Нажми любую клавишу для старта", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    i = 0
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type != keystate[pygame.K_ESCAPE]:
                waiting = False
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type != keystate[pygame.K_ESCAPE]:
                waiting = False


# Создать группы спрайтов, чтобы работать с ними со всеми одновременно
# dog =  Dog()
# bullet = Bullet()
# coin = Coin()
# all_sprites.add(coin)
# all_sprites.add(bullet)
# all_sprites.add(dog)
all_sprites.add(player)  # добавляем игрока в группу всех спрайтов
all_sprites.add(wall)
for i in range(0, 1):
    all_sprites.add(zombie)
    all_zombies.add(zombie)
all_walls.add(wall)

# Игровй цикл
# 1 - проверить, что цикл работает на правильной частоте обновления кадров
# 2 - обработка ввода
# 3 - обновление данных
# 4 - вывод изменений на экран

isStopped = False
while run:
    if isStopped:
        show_start_screen()
        isStopped = False

    clock.tick(FPS)  # проверка пункта 1
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

    if keystate[pygame.K_ESCAPE]:
        isStopped = True

    hits = pygame.sprite.spritecollide(player, all_zombies, False)
    for hit in hits:
        player.hit()
        if (player.hp <= 0):
            run = False

    hits = pygame.sprite.spritecollide(player, all_walls, False)
    for hit in hits:
        player.hitwall(wall, keystate)

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

    if (zombie.rect.centerx >= 0 and zombie.rect.centery >= 0) or (
            zombie.rect.centerx <= WIDTH and zombie.rect.centery >= 0) or (
            zombie.rect.centerx >= 0 and zombie.rect.centery <= HEIGHT) or (
            zombie.rect.centerx <= WIDTH and zombie.rect.centery <= HEIGHT):
        if (zombie1 == zombie):
            killedZombie -= 1
            zombie1 = zombie

    if player.score >= 100:
        ifLevelup = True
        if killedZombie >= 3:
            level += 1
            killedZombie == 0
            ifLevelup = False
            player.hp = 100
            player.score = 0
            all_zombies.update(player, "regen")
            levelup(level)
        else:
            player.score = 100

    # all_sprites.update()
    all_zombies.update(player)
    all_walls.update()
    player.update(keystate)

    screen.fill(BLACK)  # заполнение экрана цветом
    all_sprites.draw(screen)  # вносим изменения спрайтов на экран
    draw_shield_bar(screen, 5, 5, player.hp, GREEN)
    draw_shield_bar(screen, WIDTH - 60, 5, killedZombie * 25, PURPLE)
    draw_shield_bar(screen, 295, 5, player.score, YELLOW)
    draw_shield_bar(screen, 175, 5, level * 10, BLUE)
    pygame.display.flip()  # обновление экран (отображение нового кадра)

pygame.quit()

# TODO: добавить время между регенарацией зомби
# TODO: выровнять баланс скоростей
# TODO: сделать шире поле
# TODO: добавить препятствия
# TODO: находить и выбирать при создании пули ближайшего зомби
# TODO: cт

# git add *
# git commit 
# git push
