from .abstract_falling import FallingObject
import pygame


class Food(FallingObject):
    miss_s = "assets/sounds/miss.wav"
    catch_s = "assets/sounds/catch.wav"

    def on_collide(self):
        super().on_collide()
        self.player.score += self.score
        self.init_score()
    
    def on_miss(self):
        super().on_miss()
        self.player.hp -= 1
        self.init_score(False)