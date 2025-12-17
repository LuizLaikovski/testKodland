import random
from pgzero.actor import Actor
from config import WIDTH, HEIGHT
from sprite_diamond import DIAMOND_SPRITES

DEFAULT_DIAMOND_SPEED = 200
ANIMATION_INTERVAL = 0.8
class Diamond:
    def __init__(self, speed=DEFAULT_DIAMOND_SPEED):
        self.speed = speed
        self.actor = None
        self.active = False
        self.waiting = False

        self.spawn_timer = 0.5

        self.animation_timer = ANIMATION_INTERVAL
        self.animation_index = 0

        self.spawn()

    def spawn(self):
        self.animation_index = 0
        sprite = DIAMOND_SPRITES[self.animation_index]
        self.actor = Actor(sprite)
        self.actor.x = random.randint(20, WIDTH - 20)
        self.actor.y = -self.actor.height

        self.active = True
        self.waiting = False
        self.animation_timer = 0.5


    def collect(self):
        """Called when the player collects the diamond"""
        self.active = False
        self.waiting = True

    def update(self, dt):
        if self.active:
            # Movement
            self.actor.y += self.speed * dt

            # Animation
            self.animation_timer -= dt
            if self.animation_timer <= 0:
                self.animation_timer = 0.5
                self.animation_index = (self.animation_index + 1) % len(DIAMOND_SPRITES)
                self.actor.image = DIAMOND_SPRITES[self.animation_index]

            # Out of screen
            if self.actor.top > HEIGHT:
                self.collect()

        elif self.waiting:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                self.spawn()

    @property
    def get_speed(self):
        return self.speed

    def draw(self):
        if self.active:
            self.actor.draw()
