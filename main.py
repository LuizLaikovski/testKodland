from sprites_person import *
from sprites_bg import *

WIDTH = 900
HEIGHT = 800
HUD_MARGIN_X = 30
HUD_MARGIN_Y = 30

backgrounds = []

BG_SIZE = 256

for x in range(0, WIDTH + BG_SIZE, BG_SIZE):
    for y in range(0, HEIGHT + BG_SIZE, BG_SIZE):
        bg = Actor(bg_cloud)
        bg.x = x + BG_SIZE // 2
        bg.y = y + BG_SIZE // 2
        backgrounds.append(bg)

grounds = []

GRASS_SIZE = 70
GROUND_Y = 700

for x in range(0, WIDTH + GRASS_SIZE, GRASS_SIZE):
    grass = Actor(ground_grass)
    grass.x = x + GRASS_SIZE // 2
    grass.y = GROUND_Y
    grounds.append(grass)

# gravidade
gravity = 1
velocity_y = 0
enemy_velocity_y = 0


# Personagem
person = Actor(SPRITE_NORMAL, (100, 0))
# inimigo
enemy = Actor('pokermad', (500, 0))


# background do castelo

MAX_LIFES = 3
current_lifes = 3
invencible = 0

hearts = []
HEART_SPACING = 60
HEART_Y = 20

for i in range(MAX_LIFES):
    heart = Actor('hud_heartfull', )
    heart.x = HUD_MARGIN_X + i * HEART_SPACING
    heart.y = HUD_MARGIN_Y
    hearts.append(heart)


hurt_timer = 0

TEMPO_HURT = 42  # 0.7s a 60 FPS

# variaveis de andar
walk_index = 0
walk_timer = 0
WALK_SPEED = 6  # troca sprite a cada 6 frames


# adicionando musica de fundo
music.play('musicbackground')
music.set_volume(0.4)


on_ground = False
enemy_on_ground = False


def draw():
    screen.fill((255, 255, 255))
    
    for bg in backgrounds:
        bg.draw()

    for g in grounds:
        g.draw()


    person.draw()
    enemy.draw()
    for i in range(MAX_LIFES):
        if i < current_lifes:
            hearts[i].image = 'hud_heartfull'
        else:
            hearts[i].image = 'hud_heartempty'
        hearts[i].draw()


def update():
    global invencible, hurt_timer, walk_index, walk_timer, current_lifes, velocity_y, enemy_velocity_y
    global on_ground, enemy_on_ground

    moving = False
    direction = None

    # Caso nn se mover, deixa o sprint normal frontal
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

    # PULO
    if keyboard.space and on_ground:
        velocity_y = -22
        on_ground = False

    # Gravidade
    velocity_y += gravity
    person.y += velocity_y

    enemy_velocity_y += gravity
    enemy.y += enemy_velocity_y


    # Colisão com o chão (personagem)
    on_ground = False
    for g in grounds:
        if person.colliderect(g) and velocity_y >= 0:
            person.bottom = g.top
            velocity_y = 0
            on_ground = True


    # Colisão com o chão (inimigo)
    for g in grounds:
        if enemy.colliderect(g) and enemy_velocity_y >= 0:
            enemy.bottom = g.top
            enemy_velocity_y = 0



    # SPRITE DE PULO TEM PRIORIDADE
    if not on_ground and hurt_timer == 0:
        if direction == 'right':
            person.image = jumpingsprite
        elif direction == 'left':
            person.image = jumpingsprite_left
        walk_timer = 0

    # Animação de caminhada (SÓ SE ESTIVER NO CHÃO e enquanto a tecla estiver pressionada)
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

    # Colisão com dano
    if person.colliderect(enemy) and invencible == 0:
        current_lifes -= 1
        invencible = 60
        hurt_timer = TEMPO_HURT
        person.image = SPRITE_HURT
        sounds.eep.play()

        if current_lifes <= 0:
            screen.close()
            print("MORREU, GÊNIO DA PROGRAMAÇÃO 💀")