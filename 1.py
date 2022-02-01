import os
import sys
import pygame
from Level1 import Level


level_map = [
    'XXXXXXXXXXXXXXXXXXXXXXX',
    'X         XXX         X',
    'X   C      E      C   X',
    'X  XXXX         XXXX  X',
    'X                     X',
    'X         XXX         X',
    'X        XXXXX        X',
    'X P                   X',
    'XXXX   XXX   XXX   XXXX',
    'X                     X',
    'X         XXX    C    X',
    'X    C          XXX   X',
    'X   XXX   XXX X XXX   X',
    'XXXXXXXXXXXXXXXXXXXXXXX'
]


title_size = 64
screen_width = len(level_map[0]) * title_size
screen_height = len(level_map) * title_size

pygame.init()
size = screen_width, screen_height
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 60

level = Level(level_map, screen)

all_sprites = pygame.sprite.Group()
score = 0

running = True
while running:
        # внутри игрового цикла ещё один цикл
        # приема и обработки сообщений
    for event in pygame.event.get():
            # при закрытии окна
        if event.type == pygame.QUIT:
            running = False

        # отрисовка и изменение свойств объектов
        # ...

        # обновление экрана
    screen.fill('navy')
    running, score = level.run()

    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
