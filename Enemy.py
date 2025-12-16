import random
from pgzero.actor import Actor
from config import *

class EnemyFly:
    def __init__(self, sprite_idle_list, sprite_walk_list_right, sprite_walk_list_left, start_pos, territory_limits, 
                speed=2, fly_height=HEIGHT // 2):
        self.sprite_idle_list = sprite_idle_list
        self.sprite_walk_list_right = sprite_walk_list_right
        self.sprite_walk_list_left = sprite_walk_list_left
        self.actor = Actor(sprite_idle_list[0], start_pos)
        self.x_min, self.x_max = territory_limits
        self.speed = speed
        self.direction = random.choice(["left", "right"])
        
        # animação
        self.walk_index = 0
        self.walk_timer = 0
        self.WALK_SPEED = 8  # troca sprite a cada 8 frames
        self.fly_height = fly_height

    def update(self, enemies_list=None):
        """Move horizontalmente dentro do território e anima a sprite"""
        # Movimento horizontal
        if self.direction == "right":
            self.actor.x += self.speed
            if self.actor.x >= self.x_max:
                self.actor.x = self.x_max
                self.direction = "left"
        else:
            self.actor.x -= self.speed
            if self.actor.x <= self.x_min:
                self.actor.x = self.x_min
                self.direction = "right"

        # Mantém altura fixa (metade da tela)
        self.actor.y = self.fly_height

        # Animação de voo
        self.walk_timer += 1
        if self.walk_timer >= self.WALK_SPEED:
            self.walk_timer = 0
            self.walk_index = (self.walk_index + 1) % len(self.sprite_walk_list_left or self.sprite_walk_list_right)
            if self.direction == "right":
                self.actor.image = self.sprite_walk_list_right[self.walk_index]
            else:
                self.actor.image = self.sprite_walk_list_left[self.walk_index]

        # Casa haja colisão trocar de direção
        if enemies_list:
            for other in enemies_list:
                if other != self and self.actor.colliderect(other.actor):
                    self.direction = "left" if self.direction == "right" else "right"





    def is_moving(self):
        """Retorna True se o inimigo está se movendo."""
        return self.speed != 0

    def draw(self):
        """Desenha o inimigo na tela."""
        self.actor.draw()

    def set_position(self, x, y):
        """Define a posição do inimigo."""
        self.actor.x = x
        self.actor.y = y

    def get_rect(self):
        """Retorna o retângulo do inimigo (útil para colisão)."""
        return self.actor.rect