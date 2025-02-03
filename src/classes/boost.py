from .food import Food
from abc import ABC


class Boost(Food, ABC):
    sprite = ""
    score = 500
    catch_s = "assets/sounds/boost.wav"
    # Атрибута miss_s нет, т.к. пропуск не наказывается

    def __init__(self, screen, player, speed_mp, text_list):
        super().__init__(screen, self.sprite, player, speed_mp, text_list, self.score)

    def on_collide(self):
        super().on_collide()

    def on_miss(self):
        # Пропуск бустов не будет наказываться
        ...


class SpeedBoost(Boost):
    sprite = "assets/images/boosts/speed.png"

    def on_collide(self):
        super().on_collide()
        if self.player.speed < 30:
            self.player.speed += 1


class HPBoost(Boost):
    sprite = "assets/images/boosts/hp.png"

    def on_collide(self):
        super().on_collide()
        self.player.hp += 1


class DeHPBoost(Boost):
    sprite = "assets/images/boosts/dehp.png"
    score = 750

    # Трейд жизни на очки
    def on_collide(self):
        super().on_collide()
        self.player.hp -= 1


class PointsBoost(Boost):
    sprite = "assets/images/boosts/morepoints.png"
    score = 1000


boosts = [SpeedBoost, HPBoost, DeHPBoost, PointsBoost]