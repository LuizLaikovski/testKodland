import pgzero
from pgzero.builtins import Actor, keyboard, mouse, music
from sprites_person import *
from sprites_bg import *
from config import *
from Enemy import EnemyFly
from EnemySlug import EnemySlug
from sprites_fly import *
from sprites_slug import *

# Configurações do Jogo
game_state = "menu"
music_on = True
sound_on = True

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

# ADICIONAR UM INIMIGO PARA O PERSONAGEM DESVIAR
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

# Construir elementos iniciais
rebuild_game_elements()

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
    person.draw()
    draw_hud()

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
    velocity_y = 0
    current_lifes = MAX_LIFES
    person.x, person.y = 100, 0
    if music_on:
        music.play('musicbackground')

def restart_game():
    """Reinicia o jogo após o Game Over."""
    global current_lifes, velocity_y, invencible, hurt_timer
    current_lifes = MAX_LIFES
    velocity_y = 0
    invencible = 0
    hurt_timer = 0
    person.x, person.y = 100, 0
    for e in enemies:
        # Corrigido: usar e.actor para EnemyFly e EnemySlug
        if hasattr(e, 'actor'):
            e.actor.x, e.actor.y = 500, 0

# FUNÇÃO DE CLIQUE DO MOUSE
def on_mouse_down(pos):
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

def update():
    global invencible, hurt_timer, walk_index, walk_timer, current_lifes, velocity_y, enemy_velocity_y
    global on_ground, enemy_on_ground
    
    if game_state != "game":
        return

    # Se morreu, não atualiza mais o jogo
    if current_lifes <= 0:
        return

    moving = False
    direction = None

    # Idle se não estiver se movendo
    if not keyboard.d and not keyboard.a and not keyboard.w or keyboard.space and not keyboard.s:
        person.image = SPRITE_NORMAL

    # Movimento horizontal
    if keyboard.d:
        person.x += 8
        moving = True
        direction = 'right'
    if keyboard.a:
        person.x -= 8
        moving = True
        direction = 'left'

    # Limitar personagem aos limites da tela
    person.x = max(0, min(person.x, current_width - 50))
    person.y = max(0, min(person.y, current_height - 100))

    # Pulo
    if keyboard.space and on_ground:
        velocity_y = -22
        on_ground = False

    # Gravidade
    velocity_y += gravity
    person.y += velocity_y

    # Atualizar inimigos - APENAS UMA VEZ!
    for e in enemies:
        if isinstance(e, EnemySlug):
            e.update() # A lesma terrestre não precisa mais de grounds
        else:
            e.update(enemies_list=enemies) # Passar a lista completa para colisão entre voadores
        
        # Limitar inimigos aos limites da tela
        if hasattr(e, 'actor'):
            # Não forçar a lesma a permanecer dentro da tela — ela pode sair para reaparecer
            if isinstance(e, EnemySlug):
                e.actor.y = max(0, min(e.actor.y, current_height - 100))
            else:
                e.actor.x = max(0, min(e.actor.x, current_width - 50))
                e.actor.y = max(0, min(e.actor.y, current_height - 100))

    # Colisão com chão (personagem)
    on_ground = False
    for g in grounds:
        if person.colliderect(g) and velocity_y >= 0:
            person.bottom = g.top
            velocity_y = 0
            on_ground = True

    # Colisão com inimigo (dano)
    for e in enemies:
        # Use a custom collision rect if the enemy exposes one (reduces fly damage range)
        target = e.get_rect() if hasattr(e, 'get_rect') else e.actor
        if person.colliderect(target) and invencible == 0:
            current_lifes -= 1
            invencible = 60
            hurt_timer = TEMPO_HURT
            person.image = SPRITE_HURT
            sounds.eep.play()

    # Atualiza sprite de pulo
    if not on_ground and hurt_timer == 0:
        if direction == 'right':
            person.image = jumpingsprite
        elif direction == 'left':
            person.image = jumpingsprite_left
        walk_timer = 0

    # Animação de caminhada
    elif (keyboard.d or keyboard.a) and on_ground and hurt_timer == 0:
        walk_timer += 1
        if walk_timer >= WALK_SPEED:
            walk_timer = 0
            walk_index = (walk_index + 1) % len(walk_sprites_person_right)
            if direction == 'right':
                person.image = walk_sprites_person_right[walk_index]
            else:
                person.image = walk_sprites_person_left[walk_index]

    # Idle
    elif hurt_timer == 0:
        person.image = SPRITE_NORMAL
        walk_index = 0
        walk_timer = 0

    # Invencibilidade
    if invencible > 0:
        invencible -= 1

    # Timer de dano
    if hurt_timer > 0:
        hurt_timer -= 1
        if hurt_timer == 0:
            person.image = SPRITE_NORMAL

# Função especial do pgzero para detectar mudanças de tamanho
def on_resize(width, height):
    global current_width, current_height
    
    # Atualizar tamanho atual
    current_width = width
    current_height = height
    
    # Atualizar configurações dinâmicas
    update_screen_size(width, height)
    
    # Recriar elementos gráficos
    rebuild_game_elements()
    
    # Ajustar limites dos inimigos
    for e in enemies:
        if hasattr(e, 'territory_limits'):
            left, right = e.territory_limits
            # Ajustar limite direito para não ultrapassar a tela
            right = min(right, current_width - 50)
            e.territory_limits = (left, right)