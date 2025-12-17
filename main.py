import pgzero
from pgzero.builtins import Actor, keyboard, mouse, music, sounds
from sprites_person import *
from sprites_bg import *
from config import *
from Enemy import EnemyFly
from EnemySlug import EnemySlug
from sprites_fly import *
from sprites_slug import *
from Diamond import Diamond
from Difficulty import Difficulty
from pygame import Rect
import game_state as _game_state

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

# UI: botão padrão
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 60

def make_button_rect(centerx, centery, w=BUTTON_WIDTH, h=BUTTON_HEIGHT):
    return Rect(int(centerx - w//2), int(centery - h//2), int(w), int(h))

def menu_buttons_layout():
    cx = current_width // 2
    return [
        { 'id': 'start', 'label': 'INICIAR', 'rect': make_button_rect(cx, 350) },
        { 'id': 'options', 'label': 'OPÇÕES', 'rect': make_button_rect(cx, 430) },
        { 'id': 'quit', 'label': 'SAIR', 'rect': make_button_rect(cx, 510) },
    ]

def options_buttons_layout():
    cx = current_width // 2
    return [
        { 'id': 'music', 'label': lambda: f"MÚSICA: {'ON' if music_on else 'OFF'}", 'rect': make_button_rect(cx, 350) },
        { 'id': 'sound', 'label': lambda: f"SONS: {'ON' if sound_on else 'OFF'}", 'rect': make_button_rect(cx, 430) },
        { 'id': 'back', 'label': 'VOLTAR', 'rect': make_button_rect(cx, 550, w=200, h=50) },
    ]

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
if music_on:
    try:
        music.play('musicbackground')
        music.set_volume(0.4)
    except Exception:
        pass

# FUNÇÕES DE DESENHO

# Desenha o menu principal
def draw_menu():
    screen.draw.text("MEU JOGO", center=(current_width//2, 150), fontsize=80)
    for btn in menu_buttons_layout():
        rect = btn['rect']
        # fundo do botão
        try:
            screen.draw.filled_rect(rect, (30, 30, 30))
        except Exception:
            screen.draw.filled_rect(rect, 'black')
        # borda
        screen.draw.rect(rect, 'white')
        # label
        label = btn['label']
        screen.draw.text(label, center=rect.center, fontsize=50)

# Desenha a tela de opções
def draw_options():
    screen.draw.text("OPÇÕES", center=(current_width//2, 150), fontsize=80)
    for btn in options_buttons_layout():
        rect = btn['rect']
        screen.draw.filled_rect(rect, (30, 30, 30))
        screen.draw.rect(rect, 'white')
        label = btn['label']() if callable(btn['label']) else btn['label']
        screen.draw.text(label, center=rect.center, fontsize=50)

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
    global game_state, velocity_y, current_lifes
    game_state = "game"
    _game_state.game_state = "game"
    velocity_y = 0
    current_lifes = MAX_LIFES
    person.x, person.y = 100, 0
    if music_on:
        try:
            music.play('musicbackground')
        except Exception:
            pass

def restart_game():
    """Reinicia o jogo após o Game Over."""
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
    global game_state, music_on, sound_on
    x, y = pos
    if game_state == "menu":
        for btn in menu_buttons_layout():
            if btn['rect'].collidepoint((x, y)):
                if btn['id'] == 'start':
                    start_game()
                elif btn['id'] == 'options':
                    game_state = 'options'
                    _game_state.game_state = 'options'
                elif btn['id'] == 'quit':
                    quit()
                return

    elif game_state == 'options':
        for btn in options_buttons_layout():
            if btn['rect'].collidepoint((x, y)):
                if btn['id'] == 'music':
                    music_on = not music_on
                    _game_state.music_on = music_on
                    if music_on:
                        try:
                            music.play('musicbackground')
                        except Exception:
                            pass
                    else:
                        try:
                            music.stop()
                        except Exception:
                            pass
                elif btn['id'] == 'sound':
                    sound_on = not sound_on
                    _game_state.sound_on = sound_on
                elif btn['id'] == 'back':
                    game_state = 'menu'
                    _game_state.game_state = 'menu'
                return

    elif game_state == 'game' and current_lifes <= 0:
        restart_game()
        game_state = 'menu'
        _game_state.game_state = 'menu'

# FUNÇÕES PRINCIPAIS DO PGZERO
def draw():
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

    if _game_state.game_state != 'game':
        return

    # update diamond
    try:
        if _game_state.diamond:
            _game_state.diamond.update(dt)
    except Exception:
        pass

    # Se o jogador estiver morto, pular atualizações
    try:
        if current_lifes <= 0:
            return
    except Exception:
        pass

    moving = False
    direction = None

    # Idle (parado) se não estiver se movendo
    if (not keyboard.d and not keyboard.a and not keyboard.w) or (keyboard.space and not keyboard.s):
        if _game_state.person:
            _game_state.person.image = SPRITE_NORMAL

    # Movimento horizontal
    if keyboard.d and _game_state.person:
        _game_state.person.x += 8
        moving = True
        direction = 'right'
    if keyboard.a and _game_state.person:
        _game_state.person.x -= 8
        moving = True
        direction = 'left'

    # Limitar jogador à tela
    if _game_state.person:
        _game_state.person.x = max(0, min(_game_state.person.x, current_width - 50))
        _game_state.person.y = max(0, min(_game_state.person.y, current_height - 100))

    # Pulo
    if keyboard.space and on_ground:
        velocity_y = -18
        globals()['on_ground'] = False

    # Gravidade
    globals()['velocity_y'] += gravity
    if _game_state.person:
        _game_state.person.y += velocity_y

    # Atualizar inimigos
    for e in _game_state.enemies:
        if isinstance(e, EnemySlug):
            e.update()
        else:
            e.update(enemies_list=_game_state.enemies)
        if hasattr(e, 'actor'):
            # keep enemies vertically inside screen; slug may leave horizontally
            if isinstance(e, EnemySlug):
                e.actor.y = max(0, min(e.actor.y, current_height - 100))
            else:
                e.actor.x = max(0, min(e.actor.x, current_width - 50))
                e.actor.y = max(0, min(e.actor.y, current_height - 100))

    # Colisão com o chão (jogador)
    globals()['on_ground'] = False
    for g in _game_state.grounds:
        try:
            if _game_state.person.colliderect(g) and velocity_y >= 0:
                _game_state.person.bottom = g.top
                globals()['velocity_y'] = 0
                globals()['on_ground'] = True
        except Exception:
            pass

    # Coleta de diamante
    try:
        if _game_state.diamond and _game_state.diamond.active and _game_state.person.colliderect(_game_state.diamond.actor):
            score += 1
            _game_state.diamond.collect()

            new_difficulty = score // 10
            if new_difficulty > difficulty:
                diff_increase = new_difficulty - difficulty
                globals()['difficulty'] = new_difficulty

                # aumentar velocidade do diamante uma vez por nível
                try:
                    _game_state.diamond.speed += 17 * diff_increase
                except Exception:
                    pass

                # aumentar velocidade dos inimigos
                for ee in _game_state.enemies:
                    if hasattr(ee, 'speed'):
                        ee.speed += 0.5 * diff_increase
    except Exception:
        pass

    # Colisão com inimigos (dano)
    for e in _game_state.enemies:
        rect = None
        if hasattr(e, 'get_rect'):
            try:
                rect = e.get_rect()
            except Exception:
                rect = None
        target = rect if rect is not None else (e.actor if hasattr(e, 'actor') else None)
        try:
            if target is not None and _game_state.person.colliderect(target) and invencible == 0:
                globals()['current_lifes'] -= 1
                globals()['invencible'] = 60
                globals()['hurt_timer'] = TEMPO_HURT
                if _game_state.person:
                    _game_state.person.image = SPRITE_HURT
                if sound_on:
                    try:
                        print("SOM")
                        sounds.eep.play()
                    except Exception:
                        pass
        except Exception:
            pass

    # Atualizar sprite de pulo
    if not on_ground and hurt_timer == 0:
        if direction == 'right' and 'jumpingsprite' in globals():
            _game_state.person.image = jumpingsprite
        elif direction == 'left' and 'jumpingsprite_left' in globals():
            _game_state.person.image = jumpingsprite_left
        globals()['walk_timer'] = 0

    # Animação de caminhada
    elif (keyboard.d or keyboard.a) and on_ground and hurt_timer == 0:
        globals()['walk_timer'] += 1
        if walk_timer >= WALK_SPEED:
            globals()['walk_timer'] = 0
            # ciclo seguro usando as listas de sprites disponíveis
            try:
                globals()['walk_index'] = (walk_index + 1) % len(walk_sprites_person_right)
                if direction == 'right':
                    _game_state.person.image = walk_sprites_person_right[walk_index]
                else:
                    _game_state.person.image = walk_sprites_person_left[walk_index]
            except Exception:
                pass

    # Idle (parado)
    elif hurt_timer == 0:
        _game_state.person.image = SPRITE_NORMAL
        globals()['walk_index'] = 0
        globals()['walk_timer'] = 0

    # Invencibilidade
    if invencible > 0:
        globals()['invencible'] -= 1

    # Timer de dano
    if hurt_timer > 0:
        globals()['hurt_timer'] -= 1
        if hurt_timer == 0:
            _game_state.person.image = SPRITE_NORMAL
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