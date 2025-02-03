from abc import ABC
import pygame
import random


class FallingObject(pygame.sprite.Sprite, ABC):
    miss_s = ""
    catch_s = ""

    def __init__(self, screen, sprite, player, speed_mp, text_dict, score, miss_s = None, catch_s = None):
        super(FallingObject, self).__init__()
        self.to_destroy = False
        self.screen = screen
        self.speed = 3 * speed_mp
        self.player = player
        self.score = score
        self.text_dict = text_dict
        
        # Звуки
        if miss_s:
            self.miss_s = miss_s
        if catch_s:
            self.catch_s = catch_s

        self.surf = pygame.image.load(sprite).convert()
        self.surf = pygame.transform.scale(self.surf, (64, 64))
        
        self.x = random.randint(0, screen.get_width() - 64)
        self.y = -10

        self.rect = pygame.Rect(self.x, self.y, 64, 64)

    def update(self):
        self.y += self.speed
        self.rect.y = self.y

        # Проверка коллизии
        if self.rect.colliderect(self.player.rect):
            self.on_collide()
            self.to_destroy = True
        
        if self.y >= self.screen.get_height() - 64:
            self.on_miss()
            self.to_destroy = True

    def on_collide(self):
        """Событие при столкновении игрока с объектом подкласса этого родителя"""
        if self.catch_s:
            pygame.mixer.Sound(self.catch_s).play()

    def on_miss(self):
        """Событие при столкновении объекта с границей"""
        if self.miss_s:
            pygame.mixer.Sound(self.miss_s).play()

    def draw(self):
        self.screen.blit(self.surf, (self.x, self.y))

    def init_score(self, positive: bool = True):
        fnt = pygame.font.SysFont('Console', 30)

        if positive:
            text = fnt.render(f'+{self.score}', False, (50, 205, 50))
        else:
            text = fnt.render(f'-1♥', False, (220, 20, 60))
        
        self.text_dict[text] = [100, self.x, self.y]