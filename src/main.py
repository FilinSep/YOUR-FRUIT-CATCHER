import pygame
import tkinter.filedialog as fl
from pygame.locals import (
    K_ESCAPE,
    MOUSEBUTTONDOWN,
    KEYDOWN,
    QUIT,
    K_r,
    K_SPACE,
)
import random
import json

from classes.player import Player
from classes.food import Food
from classes .boost import Boost, boosts
from constants import *
from ui import *

pygame.init()
pygame.display.set_caption("YOUR FRUIT CATCHER")
pygame.font.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
running = True
game = False
paused = False

falling_speed_mp = 1
spawn_mp = 1
objects: list[Food, Boost] = []
text_dict = {}
player = None

CHOICE_HERO_BUTTON = None
CHOICE_FOOD_BUTTON = None

hero_sprite = "assets/images/hero.png"
food_sprite = "assets/images/strawberry.png"

# Счетчики
ticks = {
    "spawn": 0,
    "mp": 0,
    "boost": 0
}


def check_ticks(key, value):
    if ticks[key] >= value:
        ticks[key] = 0
        return True
    
    return False


def update_ticks():
    for key in ticks.keys():
        ticks[key] += 1


def get_score():
    """Получить счет из json"""
    with open("data.json", "r") as j:
       return json.loads(j.read())["best_score"]


def save_score(score):
    """Сохранить счет в json"""
    bscore = get_score()

    if not bscore:
        bscore = -1

    if score > bscore:
        with open("data.json", "w") as j:
            j.write(json.dumps({"best_score": score}))


def clear_game():
    global player, text_dict, objects, falling_speed_mp, spawn_mp, ticks, game
    
    player = Player(screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/1.2, hero_sprite)
    text_dict = {}
    objects = []

    for key in ticks.keys():
        ticks[key] = 0

    falling_speed_mp = 1
    spawn_mp = 1


def button_handler(button):
    global game, hero_sprite, food_sprite

    if button is START_BUTTON:
        clear_game()
        game = True

    elif button is CHOICE_HERO_BUTTON:
        hero_sprite = fl.askopenfilename(title="Выберите иконку героя", filetypes=[('PNG','*.png'), 
                             ('JPEG','*.jpg')])
        if not hero_sprite:
            hero_sprite = "assets/images/hero.png"
            
    elif button is CHOICE_FOOD_BUTTON:
        food_sprite = fl.askopenfilename(title="Выберите иконку фрукта", filetypes=[('PNG','*.png'), 
                                    ('JPEG','*.jpg')])
        if not food_sprite:
            food_sprite = "assets/images/strawberry.png"

# Инициализация данных
save_score(0)

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            
            # Выход в меню -> Из игры
            if event.key == K_ESCAPE:
                if game:
                    clear_game()
                    game = False
                else:
                    running = False
            
            # Пауза
            if event.key == K_SPACE:
                if game:
                    paused = not paused

            elif event.key == K_r:
                # Перезапуск игры на клавишу R
                if game:
                    clear_game()
                    game = False
            
        elif event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse = pygame.mouse.get_pos()

                # События нажатия кнопок
                if mouse[0] in range(200, 600) and mouse[1] in range(300, 330):
                    button_handler(CHOICE_HERO_BUTTON)
                elif mouse[0] in range(200, 600) and mouse[1] in range(350, 380):
                    button_handler(CHOICE_FOOD_BUTTON)
                elif mouse[0] in range(200, 600) and mouse[1] in range(400, 430):
                    button_handler(START_BUTTON)

    if paused:
        screen.fill((0, 0, 0))
        screen.blit(TITLE, (140, 100))
        screen.blit(PAUSE_TEXT, (260, 200))
        screen.blit(PAUSE_PRESS_SPACE_TEXT, (100, 230))
        
        pygame.display.flip()
        continue

    if game:
        update_ticks()
        screen.fill((0, 0, 0))

        # События, связанные с тиками
        if check_ticks("spawn", 180 // spawn_mp):
            objects.append(Food(screen, food_sprite, player, falling_speed_mp, text_dict, 100))
        if check_ticks("mp", 500):
            spawn_mp += .1
            spawn_mp = round(spawn_mp, 1)
            falling_speed_mp += .05
            falling_speed_mp = round(falling_speed_mp, 2)
        if check_ticks("boost", 720):
            objects.append(random.choice(boosts)(screen, player, falling_speed_mp, text_dict))

        for ob in objects:
            ob.update()
            if ob.to_destroy:
                ob.kill()
                objects.remove(ob)
                continue

            ob.draw()

        player.update(pygame.key.get_pressed())
        player.draw()

        trm = []
        for text in text_dict.keys():
            t = text_dict[text]
            screen.blit(text, (t[1], t[2]))
            text_dict[text] = [t[0] - 1, t[1], t[2]]

            if text_dict[text][0] == 0:
                trm.append(text)

        for text in trm:
            text_dict.pop(text)

        # Показатели в левом верхнем углу
        fnt = pygame.font.SysFont('Console', 32)
        # Счёт
        score_text = fnt.render(f'{player.score}', False, (255, 255, 255))
        # Здоровье
        hp_text = fnt.render(f'{player.hp}♥', False, (220, 20, 60))
        
        screen.blit(score_text, (5, 5))
        screen.blit(hp_text, (5, 35))

        # Подсказка
        fnt = pygame.font.SysFont('Console', 16)
        space_text = fnt.render(f'нажмите пробел для паузы', False, (255, 255, 255))
        screen.blit(space_text, (280, 5))

        if player.hp <= 0:
            save_score(player.score)
            game = False

    else:
        screen.fill((0, 0, 0))
        fnt = pygame.font.SysFont('Console', 32)
        text = fnt.render(f'НАИЛУЧШИЙ СЧЕТ: {get_score()}', False, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3))

        CHOICE_HERO_BUTTON = menu_font.render(CHOICE_HERO_BUTTON_RAW, False, (255, 255, 255))
        CHOICE_FOOD_BUTTON = menu_font.render(CHOICE_FOOD_BUTTON_RAW, False, (255, 255, 255))

        # Смена цветов взависимости от выбранных иконок
        if hero_sprite != "assets/images/hero.png":
            CHOICE_HERO_BUTTON = menu_font.render(CHOICE_HERO_BUTTON_RAW, False, (50, 205, 50))
        if food_sprite != "assets/images/strawberry.png":
            CHOICE_FOOD_BUTTON = menu_font.render(CHOICE_FOOD_BUTTON_RAW, False, (50, 205, 50))

        # Расстановка элементов меню
        screen.blit(TITLE, (150, 100))
        screen.blit(START_BUTTON, (SCREEN_WIDTH // 4, 400))
        screen.blit(CHOICE_HERO_BUTTON, (SCREEN_WIDTH // 4, 300))
        screen.blit(CHOICE_FOOD_BUTTON, (SCREEN_WIDTH // 4, 350))

    pygame.display.flip()
    clock.tick(FPS)
        