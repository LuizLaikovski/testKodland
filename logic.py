"""Lógica do jogo: loop de atualização, manipuladores de entrada, funções de início/reinício.

Este módulo opera sobre `game_state` e usa os helpers de `ui` para desenho e layout.
"""
from pgzero.builtins import music, sounds, keyboard
import game_state
import ui
from config import *
from Enemy import EnemyFly
from EnemySlug import EnemySlug
from Diamond import Diamond
from sprites_fly import *
from sprites_slug import *
from sprites_person import *


def init_game():
    """Configuração inicial do jogo: criar inimigos, diamante e chamar a recriação do UI."""
    # inicializa o jogador caso necessário
    game_state.init_state()

    # create enemies list if empty
    if not game_state.enemies:
        game_state.enemies.append(EnemyFly(
            sprite_idle_list=[fly_stop],
            sprite_walk_list_right=fly_enemy_right,
            sprite_walk_list_left=fly_enemy_left,
            start_pos=(200, HEIGHT // 2),
            territory_limits=(50, min(350, WIDTH - 50)),
            speed=2
        ))

        game_state.enemies.append(EnemyFly(
            sprite_idle_list=[fly_stop],
            sprite_walk_list_right=fly_enemy_right,
            sprite_walk_list_left=fly_enemy_left,
            start_pos=(500, HEIGHT // 2),
            territory_limits=(50, WIDTH - 50),
            speed=2
        ))

        game_state.enemies.append(EnemySlug(
            position_start=(600, GROUND_Y),
            sprite_idle_list=slug_idle,
            sprite_walk_list_right=slug_walk_right,
            sprite_walk_list_left=slug_walk_left
        ))

    # diamond
    if game_state.diamond is None:
        game_state.diamond = Diamond()

    ui.rebuild_game_elements()

    # tocar música se estiver habilitada
    try:
        if game_state.music_on:
            music.play('musicbackground')
            music.set_volume(0.4)
    except Exception:
        pass


def start_game():
    game_state.game_state = 'game'
    # reset some runtime vars
    # person position
    if game_state.person:
        game_state.person.x, game_state.person.y = 100, 0
    game_state.score = 0
    game_state.difficulty = 0


def restart_game():
    game_state.score = 0
    game_state.difficulty = 0
    if game_state.person:
        game_state.person.x, game_state.person.y = 100, 0
    # reset enemy positions roughly
    for e in game_state.enemies:
        if hasattr(e, 'actor'):
            e.actor.x, e.actor.y = 500, 0


def draw():
    # delegar para funções de desenho da UI dependendo do estado
    from pgzero import screen as _screen
    if game_state.game_state == 'menu':
        _screen.draw.text("MEU JOGO", center=(current_width//2, 150), fontsize=80)
        _screen.draw.text("INICIAR", center=(current_width//2, 350), fontsize=50)
        _screen.draw.text("OPÇÕES", center=(current_width//2, 430), fontsize=50)
        _screen.draw.text("SAIR", center=(current_width//2, 510), fontsize=50)
    elif game_state.game_state == 'options':
        _screen.draw.text("OPÇÕES", center=(current_width//2, 150), fontsize=80)
        _screen.draw.text(f"MÚSICA: {'ON' if game_state.music_on else 'OFF'}",
                          center=(current_width//2, 350), fontsize=50)
        _screen.draw.text(f"SONS: {'ON' if game_state.sound_on else 'OFF'}",
                          center=(current_width//2, 430), fontsize=50)
        _screen.draw.text("VOLTAR", center=(current_width//2, 550), fontsize=40)
    elif game_state.game_state == 'game':
        if current_lifes_global() > 0:
            ui.draw_game(current_lifes_global())
        else:
            _screen.fill((0, 0, 0))
            _screen.draw.text("GAME OVER", center=(current_width//2, current_height//2 - 50), fontsize=100, color="red")
            _screen.draw.text("Clique para voltar ao menu", center=(current_width//2, current_height//2 + 50), fontsize=40, color="white")


def current_lifes_global():
    # acessor seguro: se `main` define `current_lifes` no nível do módulo, tentar importar, senão retornar 3
    try:
        from main import current_lifes
        return current_lifes
    except Exception:
        return 3


def update(dt):
    # Atualização completa do jogo: movimento do jogador, gravidade, inimigos e colisões.
    if game_state.game_state != 'game':
        return

    # import local para evitar importação circular com o módulo main
    import main

    # update diamond
    try:
        if game_state.diamond:
            game_state.diamond.update(dt)
    except Exception:
        pass

    # Se o jogador estiver morto, pular atualizações
    try:
        if main.current_lifes <= 0:
            return
    except Exception:
        pass

    moving = False
    direction = None

    # Idle (parado) se não estiver se movendo
    if (not keyboard.d and not keyboard.a and not keyboard.w) or (keyboard.space and not keyboard.s):
        if game_state.person:
            game_state.person.image = SPRITE_NORMAL

    # Movimento horizontal
    if keyboard.d and game_state.person:
        game_state.person.x += 8
        moving = True
        direction = 'right'
    if keyboard.a and game_state.person:
        game_state.person.x -= 8
        moving = True
        direction = 'left'

    # Limitar jogador à tela
    if game_state.person:
        game_state.person.x = max(0, min(game_state.person.x, current_width - 50))
        game_state.person.y = max(0, min(game_state.person.y, current_height - 100))

    # Pulo
    if keyboard.space and main.on_ground:
        main.velocity_y = -18
        main.on_ground = False

    # Gravidade
    main.velocity_y += gravity
    if game_state.person:
        game_state.person.y += main.velocity_y

    # Atualizar inimigos
    for e in game_state.enemies:
        if isinstance(e, EnemySlug):
            e.update()
        else:
            e.update(enemies_list=game_state.enemies)
        if hasattr(e, 'actor'):
            # keep enemies vertically inside screen; slug may leave horizontally
            if isinstance(e, EnemySlug):
                e.actor.y = max(0, min(e.actor.y, current_height - 100))
            else:
                e.actor.x = max(0, min(e.actor.x, current_width - 50))
                e.actor.y = max(0, min(e.actor.y, current_height - 100))

    # Colisão com o chão (jogador)
    main.on_ground = False
    for g in game_state.grounds:
        try:
            if game_state.person.colliderect(g) and main.velocity_y >= 0:
                game_state.person.bottom = g.top
                main.velocity_y = 0
                main.on_ground = True
        except Exception:
            pass

    # Coleta de diamante
    try:
        if game_state.diamond and game_state.diamond.active and game_state.person.colliderect(game_state.diamond.actor):
            main.score += 1
            game_state.diamond.collect()

            new_difficulty = main.score // 10
            if new_difficulty > main.difficulty:
                diff_increase = new_difficulty - main.difficulty
                main.difficulty = new_difficulty

                # aumentar velocidade do diamante uma vez por nível
                try:
                    game_state.diamond.speed += 17 * diff_increase
                except Exception:
                    pass

                # aumentar velocidade dos inimigos
                for ee in game_state.enemies:
                    if hasattr(ee, 'speed'):
                        ee.speed += 0.5 * diff_increase
    except Exception:
        pass

    # Colisão com inimigos (dano)
    for e in game_state.enemies:
        rect = None
        if hasattr(e, 'get_rect'):
            try:
                rect = e.get_rect()
            except Exception:
                rect = None
        target = rect if rect is not None else (e.actor if hasattr(e, 'actor') else None)
        try:
            if target is not None and game_state.person.colliderect(target) and main.invencible == 0:
                main.current_lifes -= 1
                main.invencible = 60
                main.hurt_timer = TEMPO_HURT
                if game_state.person:
                    game_state.person.image = SPRITE_HURT
                try:
                    sounds.eep.play()
                except Exception:
                    pass
        except Exception:
            pass

    # Atualizar sprite de pulo
    if not main.on_ground and main.hurt_timer == 0:
        if direction == 'right' and 'jumpingsprite' in globals():
            game_state.person.image = jumpingsprite
        elif direction == 'left' and 'jumpingsprite_left' in globals():
            game_state.person.image = jumpingsprite_left
        main.walk_timer = 0

    # Animação de caminhada
    elif (keyboard.d or keyboard.a) and main.on_ground and main.hurt_timer == 0:
        main.walk_timer += 1
        if main.walk_timer >= WALK_SPEED:
            main.walk_timer = 0
            # ciclo seguro usando as listas de sprites disponíveis
            try:
                main.walk_index = (main.walk_index + 1) % len(walk_sprites_person_right)
                if direction == 'right':
                    game_state.person.image = walk_sprites_person_right[main.walk_index]
                else:
                    game_state.person.image = walk_sprites_person_left[main.walk_index]
            except Exception:
                pass

    # Idle (parado)
    elif main.hurt_timer == 0:
        game_state.person.image = SPRITE_NORMAL
        main.walk_index = 0
        main.walk_timer = 0

    # Invencibilidade
    if main.invencible > 0:
        main.invencible -= 1

    # Timer de dano
    if main.hurt_timer > 0:
        main.hurt_timer -= 1
        if main.hurt_timer == 0:
            game_state.person.image = SPRITE_NORMAL


def on_mouse_down(pos):
    x, y = pos
    if game_state.game_state == 'menu':
        if 330 < y < 380:
            start_game()
        elif 410 < y < 460:
            game_state.game_state = 'options'
        elif 490 < y < 540:
            quit()
    elif game_state.game_state == 'options':
        if 330 < y < 380:
            game_state.music_on = not game_state.music_on
            if game_state.music_on:
                try:
                    music.play('musicbackground')
                except Exception:
                    pass
            else:
                music.stop()
        elif 410 < y < 460:
            game_state.sound_on = not game_state.sound_on
        elif 530 < y < 580:
            game_state.game_state = 'menu'
    elif game_state.game_state == 'game' and current_lifes_global() <= 0:
        restart_game()
        game_state.game_state = 'menu'


def on_resize(width, height):
    try:
        from config import update_screen_size
        update_screen_size(width, height)
    except Exception:
        pass
    ui.rebuild_game_elements()


def increase_difficulty(amount):
    if amount <= 0:
        return
    for e in game_state.enemies:
        try:
            if hasattr(e, 'speed'):
                max_speed = 12
                e.speed = min(max_speed, e.speed + amount)
        except Exception:
            pass
