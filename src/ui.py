import pygame
pygame.font.init()

menu_font = pygame.font.SysFont('Console', 32)
title_font = pygame.font.SysFont('Console', 48)

TITLE = title_font.render(f'YOUR FRUIT CATCHER', False, (220, 20, 60))
PAUSE_PRESS_SPACE_TEXT = menu_font.render(f'НАЖМИТЕ ПРОБЕЛ ЧТОБЫ ПРОДОЛЖИТЬ', False, (255, 255, 255))
PAUSE_TEXT = menu_font.render(f'ИГРА НА ПАУЗЕ', False, (255, 255, 255))

START_BUTTON = menu_font.render(f'НАЖМИТЕ ЧТОБЫ НАЧАТЬ', False, (255, 191, 0))
CHOICE_HERO_BUTTON_RAW = 'ВЫБРАТЬ ИКОНКУ ИГРОКА'
CHOICE_FOOD_BUTTON_RAW = 'ВЫБРАТЬ ИКОНКУ ФРУКТА'