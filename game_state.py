"""Módulo que armazena variáveis globais do estado do jogo.

Outros módulos importam este módulo para ler e modificar essas variáveis.
"""
from pgzero.builtins import Actor
from sprites_person import SPRITE_NORMAL

# Game flags
game_state = "menu"
music_on = True
sound_on = True

# Player state
person = None

# Collections
hearts = []
backgrounds = []
grounds = []
enemies = []

# Score / difficulty
score = 0
difficulty = 0

# HUD / misc
diamond = None

def init_state(person_start=(100, 0)):
    """Inicializa objetos básicos que dependem de constantes de sprite.

    Chame esta função a partir de `main.py` depois de importar os sprites e o `config`.
    """
    global person
    if person is None:
        person = Actor(SPRITE_NORMAL, person_start)
