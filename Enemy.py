import random
import pygame
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

    def update(self, enemies_list):
        """Move horizontalmente dentro do território e anima a sprite"""
        # Movimento horizontal
        half_w = self.actor.width // 2
        # Determine limites efetivos (território restrito e borda da tela)
        left_limit = max(self.x_min if self.x_min is not None else -float('inf'), half_w)
        right_limit = min(self.x_max if self.x_max is not None else float('inf'), current_width - half_w)

        if self.direction == "right":
            new_x = self.actor.x + self.speed
            # Se alcançou o limite direito (território ou tela), ajusta e inverte
            if new_x >= right_limit:
                self.actor.x = right_limit
                self.direction = "left"
            else:
                self.actor.x = new_x
        else:
            new_x = self.actor.x - self.speed
            # Se alcançou o limite esquerdo (território ou tela), ajusta e inverte
            if new_x <= left_limit:
                self.actor.x = left_limit
                self.direction = "right"
            else:
                self.actor.x = new_x

        # Mantém altura fixa (metade da tela)
        self.actor.y = self.fly_height

        # Colisão entre inimigos voadores
        for other in enemies_list:
            if other != self and isinstance(other, EnemyFly) and self.actor.colliderect(other.actor):
                # Trocar de direção
                self.direction = "left" if self.direction == "right" else "right"
                # Afastar um pouco para evitar colisão contínua
                if self.direction == "right":
                    self.actor.x += 1
                else:
                    self.actor.x -= 1
                break # Sai do loop de colisão após a primeira colisão

        # Animação de voo
        self.walk_timer += 1
        if self.walk_timer >= self.WALK_SPEED:
            self.walk_timer = 0
            self.walk_index = (self.walk_index + 1) % len(self.sprite_walk_list_left or self.sprite_walk_list_right)
            if self.direction == "right":
                self.actor.image = self.sprite_walk_list_right[self.walk_index]
            else:
                self.actor.image = self.sprite_walk_list_left[self.walk_index]


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

    def getSpeed():
        return self.speed

    def get_rect(self):
        """Retorna o retângulo do inimigo (útil para colisão)."""
        # Construir um pygame.Rect a partir do Actor (x,y são o centro)
        try:
            w = int(self.actor.width)
            h = int(self.actor.height)
            left = int(self.actor.x - w / 2)
            top = int(self.actor.y - h / 2)
            rect = pygame.Rect(left, top, w, h)
            # Reduzir largura e altura para diminuir a 'hitbox' (30% width, 20% height)
            shrink_w = int(rect.width * 0.30)
            shrink_h = int(rect.height * 0.20)
            rect.inflate_ip(-shrink_w, -shrink_h)
            return rect
        except Exception:
            # Fallback: criar retângulo básico sem shrink
            try:
                w = int(getattr(self.actor, 'width', 0) or 0)
                h = int(getattr(self.actor, 'height', 0) or 0)
                left = int(getattr(self.actor, 'x', 0) - w / 2)
                top = int(getattr(self.actor, 'y', 0) - h / 2)
                return pygame.Rect(left, top, w, h)
            except Exception:
                return None