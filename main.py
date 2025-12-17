import pgzero
from pgzero.builtins import Actor, keyboard, mouse, music
from sprites_person import *
from sprites_bg import *
from config import *
from Enemy import EnemyFly
from EnemySlug import EnemySlug
from sprites_fly import *
from sprites_slug import *
from Diamond import Diamond
from Difficulty import Difficulty
import logic

# Configurações do Jogo
game_state = "menu"
music_on = True
sound_on = True
difficulty = Difficulty(difficultyInitial=1)

current_lifes = MAX_LIFES
invencible = 0
hurt_timer = 0

velocity_y = 0
enemy_velocity_y = 0
on_ground = False
enemy_on_ground = False

walk_index = 0
walk_timer = 0

# Listas de elementos do jogo
person = Actor(SPRITE_NORMAL, (100, 0))
hearts = []
backgrounds = []
grounds = []
enemies = []
score = 0
difficulty = 0  # dificuldade atual (aumenta a cada 10 pontos)

# Função para recriar todos os elementos gráficos com base no tamanho atual
def rebuild_game_elements():
    global backgrounds, grounds, hearts
    
    # Limpar listas
    backgrounds.clear()
    grounds.clear()
    hearts.clear()
    
    # Recriar fundo
    for x in range(0, current_width + BG_SIZE, BG_SIZE):
        for y in range(0, current_height + BG_SIZE, BG_SIZE):
            bg = Actor(bg_cloud)
            bg.x = x + BG_SIZE // 2
            bg.y = y + BG_SIZE // 2
            backgrounds.append(bg)
    
    # Recriar chão
    # Linha de cima - grama
    for x in range(0, current_width + GRASS_SIZE, GRASS_SIZE):
        grass = Actor(ground_grass)
        grass.x = x + GRASS_SIZE // 2
        grass.y = GROUND_Y
        grounds.append(grass)
    
    # Linha de baixo - terra/pedra
    for x in range(0, current_width + GRASS_SIZE, GRASS_SIZE):
        stone = Actor(ground_earth)
        stone.x = x + GRASS_SIZE // 2
        stone.y = SECOND_GROUND_Y
        grounds.append(stone)
    
    # Recriar HUD de vidas
    for i in range(MAX_LIFES):
        heart = Actor('hud_heartfull')
        heart.x = HUD_MARGIN_X + i * HEART_SPACING
        heart.y = HUD_MARGIN_Y
        hearts.append(heart)

# ADICIONAR OS INIMIGOS
enemies.append(EnemyFly(
    sprite_idle_list=[fly_stop],
    sprite_walk_list_right=fly_enemy_right,
    sprite_walk_list_left=fly_enemy_left,
    start_pos=(200, HEIGHT // 2),
    territory_limits=(50, min(350, WIDTH - 50)),
    speed=2
))

enemies.append(EnemyFly(
    sprite_idle_list=[fly_stop],
    sprite_walk_list_right=fly_enemy_right,
    sprite_walk_list_left=fly_enemy_left,
    start_pos=(500, HEIGHT // 2),
    territory_limits=(50, WIDTH - 50),
    speed=2
))

enemies.append(EnemySlug(
    position_start=(600, GROUND_Y), # Inicia no chão
    sprite_idle_list=slug_idle,
    sprite_walk_list_right=slug_walk_right,
    sprite_walk_list_left=slug_walk_left
))

diamond = Diamond()

# Construir elementos iniciais
rebuild_game_elements()

# Expor os objetos principais para `game_state` para que módulos separados possam operar sobre os mesmos dados
import game_state as _game_state
_game_state.person = person
_game_state.hearts = hearts
_game_state.backgrounds = backgrounds
_game_state.grounds = grounds
_game_state.enemies = enemies
_game_state.score = score
_game_state.difficulty = difficulty
_game_state.diamond = diamond

# Música de fundo
music.play('musicbackground')
music.set_volume(0.4)

# FUNÇÕES DE DESENHO

# Desenha o menu principal
def draw_menu():
    screen.draw.text("MEU JOGO", center=(current_width//2, 150), fontsize=80)
    screen.draw.text("INICIAR", center=(current_width//2, 350), fontsize=50)
    screen.draw.text("OPÇÕES", center=(current_width//2, 430), fontsize=50)
    screen.draw.text("SAIR", center=(current_width//2, 510), fontsize=50)

# Desenha a tela de opções
def draw_options():
    screen.draw.text("OPÇÕES", center=(current_width//2, 150), fontsize=80)
    screen.draw.text(f"MÚSICA: {'ON' if music_on else 'OFF'}",
                     center=(current_width//2, 350), fontsize=50)
    screen.draw.text(f"SONS: {'ON' if sound_on else 'OFF'}",
                     center=(current_width//2, 430), fontsize=50)
    screen.draw.text("VOLTAR", center=(current_width//2, 550), fontsize=40)

# Desenha o HUD de vidas (só os corações restantes)
def draw_hud():
    for i in range(current_lifes):
        hearts[i].draw()

# Desenha o jogo em execução
def draw_game():
    for bg in backgrounds:
        bg.draw()
    for g in grounds:
        g.draw()
    for e in enemies:
        e.draw()
    
    # desenhar score usando sprites para cada dígito (hud_0..hud_9)
    draw_score_images(score, topleft=(960, 30))
    diamond.draw()
    person.draw()
    draw_hud()


def increase_difficulty(amount):
    """Increase difficulty by `amount`: raise enemy speeds.

    This function iterates current enemies and increases their `speed`.
    It avoids increasing speeds for enemies that don't have `speed` attribute.
    """
    if amount <= 0:
        return
    for e in enemies:
        try:
            # aumente a velocidade base do inimigo
            if hasattr(e, 'speed'):
                # opcional: limitar velocidade máxima
                max_speed = 12
                e.speed = min(max_speed, e.speed + amount)
        except Exception:
            pass


def draw_score_images(value, topleft=(20, 60), digit_spacing=2):
    """Desenha o score usando imagens `hud_0`..`hud_9`.

    `topright` é a tupla (x, y) onde o lado direito do número será posicionado.
    Os dígitos são desenhados da direita para a esquerda.
    """
    try:
        x_right, y_top = topleft
        s = str(int(value)) if value is not None else '0'
    except Exception:
        x_right, y_top = 20, 60
        s = '0'

    # desenhar pelo menos um dígito
    if s == '':
        s = '0'

    cur_x = x_right
    # percorre os dígitos da direita para a esquerda
    for ch in reversed(s):
        img_name = f'hud_{ch}'
        try:
            d = Actor(img_name)
        except Exception:
            # se a imagem não existir, pular (evita crash)
            continue
        # posiciona o dígito com seu canto superior-direito em (cur_x, y_top)
        d.topleft = (cur_x - d.width, y_top)
        d.draw()
        # mover cursor para a esquerda para o próximo dígito
        cur_x -= (d.width + digit_spacing)

# Desenha a tela de Game Over
def draw_game_over():
    screen.fill((0, 0, 0))
    screen.draw.text("GAME OVER", center=(current_width//2, current_height//2 - 50), fontsize=100, color="red")
    screen.draw.text("Clique para voltar ao menu", center=(current_width//2, current_height//2 + 50), fontsize=40, color="white")

# FUNÇÕES DE INÍCIO E REINÍCIO
def start_game():
    """Inicia o jogo a partir do menu."""
    # delegar para o módulo logic
    try:
        logic.start_game()
    except Exception:
        # retorno: manter comportamento mínimo existente
        global game_state, velocity_y, current_lifes
        game_state = "game"
        velocity_y = 0
        current_lifes = MAX_LIFES
        person.x, person.y = 100, 0
        if music_on:
            music.play('musicbackground')

def restart_game():
    """Reinicia o jogo após o Game Over."""
    try:
        logic.restart_game()
    except Exception:
        # retorno: comportamento anterior
        global current_lifes, velocity_y, invencible, hurt_timer
        current_lifes = MAX_LIFES
        velocity_y = 0
        invencible = 0
        hurt_timer = 0
        person.x, person.y = 100, 0
        for e in enemies:
            if hasattr(e, 'actor'):
                e.actor.x, e.actor.y = 500, 0

# FUNÇÃO DE CLIQUE DO MOUSE
def on_mouse_down(pos):
    try:
        logic.on_mouse_down(pos)
    except Exception:
        # retorno: comportamento anterior
        global game_state, music_on, sound_on
        x, y = pos
        if game_state == "menu":
            if 330 < y < 380:
                start_game()
            elif 410 < y < 460:
                game_state = "options"
            elif 490 < y < 540:
                quit()

        elif game_state == "options":
            if 330 < y < 380:
                music_on = not music_on
                if music_on:
                    music.play('musicbackground')
                    pass
                else:
                    music.stop()
                if sound_on:
                    sounds.eep.set_volume(0)
            elif 410 < y < 460:
                sound_on = not sound_on
            elif 530 < y < 580:
                game_state = "menu"

        elif game_state == "game" and current_lifes <= 0:
            restart_game()
            game_state = "menu"

# FUNÇÕES PRINCIPAIS DO PGZERO
def draw():
    # delegar desenho para o módulo logic
    try:
        logic.draw()
    except Exception:
        # retorno: manter comportamento simples de desenho anterior
        screen.clear()
        if game_state == "menu":
            draw_menu()
        elif game_state == "options":
            draw_options()
        elif game_state == "game":
            if current_lifes > 0:
                draw_game()
            else:
                draw_game_over()

def update(dt):
    global invencible, hurt_timer, walk_index, walk_timer, current_lifes, velocity_y, enemy_velocity_y
    global on_ground, enemy_on_ground, score, difficulty
    # delegar para o módulo logic
    try:
        logic.update(dt)
    except Exception:
        # retorno: sem operação
        return
# Função especial do pgzero para detectar mudanças de tamanho
def on_resize(width, height):
    try:
        logic.on_resize(width, height)
    except Exception:
        # retorno: comportamento de redimensionamento padrão
        global current_width, current_height
        current_width = width
        current_height = height
        update_screen_size(width, height)
        rebuild_game_elements()
        for e in enemies:
            if hasattr(e, 'territory_limits'):
                left, right = e.territory_limits
                right = min(right, current_width - 50)
                e.territory_limits = (left, right)