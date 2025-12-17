"""Helpers de UI e desenho.

Este módulo desenha fundos, terrenos, HUD e imagens de pontuação usando o `game_state`.
"""
from pgzero.builtins import Actor
import game_state
from config import BG_SIZE, GRASS_SIZE, HUD_MARGIN_X, HUD_MARGIN_Y, HEART_SPACING, current_width, current_height, GROUND_Y, SECOND_GROUND_Y


def rebuild_game_elements():
    """Recria fundos, terrenos e corações do HUD com base no tamanho atual da tela.

    Isso espelha o comportamento antigo de `rebuild_game_elements`, mas usa as listas em `game_state`.
    """
    game_state.backgrounds.clear()
    game_state.grounds.clear()
    game_state.hearts.clear()

    # Recriar fundo
    for x in range(0, current_width + BG_SIZE, BG_SIZE):
        for y in range(0, current_height + BG_SIZE, BG_SIZE):
            bg = Actor('bg_cloud')
            bg.x = x + BG_SIZE // 2
            bg.y = y + BG_SIZE // 2
            game_state.backgrounds.append(bg)

    # Recriar chão (linha de cima - grama)
    for x in range(0, current_width + GRASS_SIZE, GRASS_SIZE):
        grass = Actor('ground_grass')
        grass.x = x + GRASS_SIZE // 2
        grass.y = GROUND_Y
        game_state.grounds.append(grass)

    # Linha de baixo - terra/pedra
    for x in range(0, current_width + GRASS_SIZE, GRASS_SIZE):
        stone = Actor('ground_earth')
        stone.x = x + GRASS_SIZE // 2
        stone.y = SECOND_GROUND_Y
        game_state.grounds.append(stone)

    # HUD hearts
    # rebuild hearts list: clear then append according to MAX_LIFES in config if needed
    # here we default to 3 as a safe initial value
    for i in range(3):
        heart = Actor('hud_heartfull')
        heart.x = HUD_MARGIN_X + i * HEART_SPACING
        heart.y = HUD_MARGIN_Y
        game_state.hearts.append(heart)


def draw_hud(current_lifes):
    for i in range(current_lifes):
        game_state.hearts[i].draw()


def draw_score_images(value, topright=(20, 60), digit_spacing=2):
    """Desenha o score usando sprites `hud_0`..`hud_9` alinhados em `topright`.

    Desenha os dígitos da direita para a esquerda para que `topright` seja o canto superior direito.
    """
    try:
        x_right, y_top = topright
        s = str(int(value)) if value is not None else '0'
    except Exception:
        x_right, y_top = 20, 60
        s = '0'

    if s == '':
        s = '0'

    cur_x = x_right
    for ch in reversed(s):
        img_name = f'hud_{ch}'
        try:
            d = Actor(img_name)
        except Exception:
            continue
        d.topleft = (cur_x - d.width, y_top)
        d.draw()
        cur_x -= (d.width + digit_spacing)


def draw_game(current_lifes):
    # draw backgrounds and grounds
    for bg in game_state.backgrounds:
        bg.draw()
    for g in game_state.grounds:
        g.draw()

    # draw enemies and diamond
    for e in game_state.enemies:
        e.draw()
    if game_state.diamond:
        game_state.diamond.draw()

    # draw score and player and HUD
    draw_score_images(value=game_state.score, topright=(20, 60))
    if game_state.person:
        game_state.person.draw()
    draw_hud(current_lifes)
