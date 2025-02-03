import pygame
import tkinter.filedialog as fl
from pygame.locals import (
    K_d,
    K_a,
    K_LEFT,
    K_RIGHT,
)


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, sprite):
        super(Player, self).__init__()
        self.screen = screen
        self.speed = 5
        self.hp = 3
        self.score = 0
        
        self.surf = pygame.image.load(sprite).convert()
        self.surf = pygame.transform.scale(self.surf, (64, 64))

        self.x = x
        self.y = y

        self.rect = pygame.Rect(self.x, self.y, 64, 64)

    def update(self, pressed_keys):
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            if self.x > 0:
                self.x -= self.speed
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            if self.x < self.screen.get_width() - 64:
                self.x += self.speed

        self.rect.x = self.x

    def draw(self):
        self.screen.blit(self.surf, (self.x, self.y))