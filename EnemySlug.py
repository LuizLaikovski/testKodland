import random
from pygame import Rect
from pgzero.actor import Actor

class EnemySlug:
    def __init__(self, position_start, sprite_idle_list, sprite_walk_list_right, sprite_walk_list_left):
        self.direction = random.choice(["left", "right"])
        self.sprite_idle_list = sprite_idle_list
        self.sprite_walk_list_right = sprite_walk_list_right
        self.sprite_walk_list_left = sprite_walk_list_left
        self.actor = Actor(sprite_idle_list[0], position_start)
        
        # Configurações de movimento
        self.speed = 2  # Velocidade de movimento horizontal
        self.velocity_y = 0  # Velocidade vertical para gravidade
        self.on_ground = False
        
        # Configurações de respawn
        self.respawn_timer = 0
        self.respawn_delay = 4.6 * 60  # 4.6 segundos em frames (60 FPS)
        self.is_offscreen = False
        self.visible = True  # Controlar visibilidade manualmente
        self.offscreen_side = None  # 'left' or 'right' quando fora da tela
        self.last_leave_direction = None  # direção quando saiu (left/right)
        
        # Animação
        self.walk_index = 0
        self.walk_timer = 0
        self.walk_speed = 10  # Velocidade da animação de caminhada
        
        # Gravidade
        self.gravity = 1
        
        # Configurações de tela (serão atualizadas)
        self.screen_width = 800
        self.screen_height = 600

        # Ajustar posição vertical inicial para ficar sobre o chão
        self.place_on_ground()

    def update(self, grounds=None, enemies_list=None):
        """Atualiza a posição e estado da lesma"""
        # Atualizar tamanho da tela (sempre atualizar para desenhar corretamente enquanto offscreen)
        try:
            from config import current_width, current_height, GROUND_Y
            self.screen_width = current_width
            self.screen_height = current_height
        except:
            GROUND_Y = None

        from config import GROUND_Y, GRASS_SIZE
        self.place_on_ground(GROUND_Y, GRASS_SIZE)


        # Se está fora da tela, contar tempo para respawn
        if self.is_offscreen:
            self.respawn_timer += 1
            if self.respawn_timer >= self.respawn_delay:
                # 40% de chance de reaparecer no lado OPPOSTO ao qual saiu
                if self.offscreen_side is None:
                    # retorno: escolha aleatória
                    respawn_side = random.choice(["left", "right"])
                else:
                    if random.random() < 0.4:
                        # reaparece no lado oposto
                        respawn_side = "right" if self.offscreen_side == "left" else "left"
                    else:
                        # reaparece no mesmo lado
                        respawn_side = self.offscreen_side

                # Posicionar fora da tela no lado escolhido e colocar direção para entrar na tela
                if respawn_side == "right":
                    self.actor.x = self.screen_width + self.actor.width
                    self.direction = "left"
                else:
                    self.actor.x = -self.actor.width
                    self.direction = "right"

                # Ajustar Y se possível
                if GROUND_Y is not None:
                    self.place_on_ground()

                # Resetar estados
                self.is_offscreen = False
                self.respawn_timer = 0
                self.visible = True
                self.offscreen_side = None
            return
        
        # Movimento horizontal baseado na direção
        if self.direction == "right":
            self.actor.x += self.speed
            self.animate_walk("right")
        else:
            self.actor.x -= self.speed
            self.animate_walk("left")
        
        # A lesma terrestre não usa gravidade nem colisão com o chão,
        # pois deve se mover horizontalmente no chão.
        # A posição Y será definida no respawn para GROUND_Y.
        pass
        
        # Verificar se saiu da tela
        self.check_offscreen()
        
        # Atualizar animação
        self.update_animation()



    def check_offscreen(self):
        """Verifica se a lesma saiu da tela"""
        # Se saiu completamente da tela pela esquerda ou direita
        if self.actor.x < -self.actor.width:
            # saiu pela esquerda: marcar offscreen e NÃO desenhar na borda
            self.is_offscreen = True
            self.visible = False
            self.offscreen_side = "left"
        elif self.actor.x > self.screen_width + self.actor.width:
            # saiu pela direita: marcar offscreen e NÃO desenhar na borda
            self.is_offscreen = True
            self.visible = False
            self.offscreen_side = "right"

    def respawn(self):
        """Faz a lesma reaparecer do lado oposto e com direção aleatória."""
        
        # Escolher lado de reaparecimento aleatoriamente
        side = random.choice(["left", "right"])
        
        if side == "right":
            # Reaparecer à direita, movendo-se para a esquerda
            self.actor.x = self.screen_width + self.actor.width
            self.direction = "left"
        else:
            # Reaparecer à esquerda, movendo-se para a direita
            self.actor.x = -self.actor.width
            self.direction = "right"
        
        # Posicionar sobre o chão corretamente
        self.place_on_ground()
        
        # Resetar estados
        self.is_offscreen = False
        self.respawn_timer = 0
        self.visible = True  # Tornar visível novamente
        self.velocity_y = 0

    def animate_walk(self, direction):
        """Anima o movimento da lesma"""
        self.walk_timer += 1
        if self.walk_timer >= self.walk_speed:
            self.walk_timer = 0
            if direction == "right":
                if self.walk_index >= len(self.sprite_walk_list_right):
                    self.walk_index = 0
                self.actor.image = self.sprite_walk_list_right[self.walk_index]
                self.walk_index = (self.walk_index + 1) % len(self.sprite_walk_list_right)
            else:
                if self.walk_index >= len(self.sprite_walk_list_left):
                    self.walk_index = 0
                self.actor.image = self.sprite_walk_list_left[self.walk_index]
                self.walk_index = (self.walk_index + 1) % len(self.sprite_walk_list_left)

    def update_animation(self):
        """Atualiza a animação quando parado"""
        if not self.direction:  # Se não está se movendo
            idle_frame = self.walk_index % len(self.sprite_idle_list)
            self.actor.image = self.sprite_idle_list[idle_frame]

    def get_rect(self):
        """Retorna um pygame.Rect reduzido (hitbox) para a lesma.

        Reduz a largura e altura em 30% para diminuir o alcance de dano.
        """
        try:
            w = int(self.actor.width)
            h = int(self.actor.height)
            left = int(self.actor.x - w / 2)
            top = int(self.actor.y - h / 2)
            rect = Rect(left, top, w, h)
            shrink_w = int(rect.width * 0.30)
            shrink_h = int(rect.height * 0.30)
            rect.inflate_ip(-shrink_w, -shrink_h)
            return rect
        except Exception:
            try:
                w = int(getattr(self.actor, 'width', 0) or 0)
                h = int(getattr(self.actor, 'height', 0) or 0)
                left = int(getattr(self.actor, 'x', 0) - w / 2)
                top = int(getattr(self.actor, 'y', 0) - h / 2)
                return Rect(left, top, w, h)
            except Exception:
                return None
        

    def place_on_ground(self, ground_y=None, grass_size=None):
        """Posiciona o actor de forma que sua base (bottom) fique sobre o topo da grama.

        Calcula: ground_top = GROUND_Y - GRASS_SIZE/2
        e define actor.y = ground_top - actor.height/2
        """
        try:
            # Preferir parâmetros fornecidos, senão tentar importar de config
            if ground_y is None or grass_size is None:
                from config import GROUND_Y, GRASS_SIZE
                if ground_y is None:
                    ground_y = GROUND_Y
                if grass_size is None:
                    grass_size = GRASS_SIZE

            # ground_y é o center Y do tile de grama; seu topo fica em ground_y - grass_size/2
            ground_top = ground_y - (grass_size / 2)
            h = float(getattr(self.actor, 'height', 0) or 0)
            # definir center Y do actor para que sua bottom == ground_top
            self.actor.y = int(ground_top - (h / 2))
        except Exception:
            # retorno: não fazer nada
            pass

    def getSpeed():
        return self.speed

    def draw(self):
        """Desenha a lesma se estiver visível"""
        # Se está offscreen, desenhar uma representação na borda correspondente
        if self.is_offscreen and self.visible and self.offscreen_side is not None:
            # salvar x original
            orig_x = self.actor.x
            if self.offscreen_side == "left":
                render_x = self.actor.width // 2
            else:
                render_x = self.screen_width - (self.actor.width // 2)
            self.actor.x = render_x
            self.actor.draw()
            self.actor.x = orig_x
        elif not self.is_offscreen and self.visible:
            self.actor.draw()