# ==============================
# CONFIGURAÇÕES DO JOGO
# ==============================

# Tamanho inicial da janela (pode ser alterado pelo usuário)
WIDTH = 800
HEIGHT = 600

# Flag para saber se é a primeira execução
first_run = True

# Configurações do HUD (Heads-Up Display)
HUD_MARGIN_X = 30    # Margem horizontal para elementos do HUD
HUD_MARGIN_Y = 30    # Margem vertical para elementos do HUD
HEART_SPACING = 60   # Espaçamento entre os corações da vida

# Sistema de vida
MAX_LIFES = 3        # Número máximo de vidas do jogador
TEMPO_HURT = 42      # Duração do efeito visual de dano em frames (≈0.7s a 60 FPS)

# Configurações de animação
WALK_SPEED = 6       # Velocidade da animação de caminhada (frames por sprite)

# Configurações dos cenários
BG_SIZE = 256        # Tamanho do sprite de fundo (background)
GRASS_SIZE = 70      # Tamanho do sprite do chão
# NOTA: GROUND_Y será calculado dinamicamente

# Física do jogo
gravity = 1          # Força da gravidade aplicada aos personagens

# Variáveis para armazenar o tamanho atual da tela
current_width = WIDTH
current_height = HEIGHT

# Função para calcular posições dinâmicas
def update_screen_size(width, height):
    global current_width, current_height, GROUND_Y, SECOND_GROUND_Y
    current_width = width
    current_height = height
    GROUND_Y = current_height - GRASS_SIZE
    SECOND_GROUND_Y = GROUND_Y + GRASS_SIZE

# Inicializar com valores padrão
update_screen_size(WIDTH, HEIGHT)