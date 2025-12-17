from pgzero.actor import Actor
from sprite_diamond import spriteDiamond
from config import WIDTH, HEIGHT
import random

class Diamond:
    def __init__(self, speed=200):
        self.speed = speed
        self.actor = None
        self.active = False
        self.waiting = False
        self.spawn_timer = 0.5

        self.spawn()

    def spawn(self):
        self.actor = Actor(spriteDiamond)
        self.actor.x = random.randint(20, WIDTH - 20)
        self.actor.y = -self.actor.height
        self.active = True
        self.waiting = False

    def collect(self):
        """Chamado quando o player pega o diamante"""
        self.active = False
        self.waiting = True
        self.spawn_timer = 0.5

    def update(self, dt):
        if self.active:
            self.actor.y += self.speed * dt

            if self.actor.top > HEIGHT:
                self.collect()

        elif self.waiting:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                self.spawn()

    def getSpeed():
        return self.speed

    def draw(self):
        if self.active:
            self.actor.draw()

    