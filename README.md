# testKodland - Jogo de Plataforma com Pygame Zero

## Sobre

Este projeto é um jogo de plataforma simples desenvolvido em **Python** utilizando a biblioteca **Pygame Zero (pgzero)**. O jogo apresenta um personagem que deve coletar diamantes enquanto evita inimigos voadores e terrestres.

**Principais Características:**

*   **Mecânica de Plataforma:** Movimentação horizontal, pulo e gravidade.
*   **Inimigos:** Inimigos voadores (`EnemyFly`) e terrestres (`EnemySlug`) com lógica de movimento e colisão.
*   **Coletáveis:** Diamantes (`Diamond`) que caem do topo da tela e aumentam a pontuação.
*   **Sistema de Dificuldade:** A dificuldade aumenta a cada 10 pontos, elevando a velocidade dos inimigos e do diamante.
*   **Interface:** Menu principal, tela de opções (música/som) e tela de *Game Over*.
*   **Responsividade:** O jogo se adapta a mudanças de tamanho da janela (função `on_resize`).

## Como Usar

### Pré-requisitos

Para executar este jogo, você precisa ter o **Python 3** instalado em seu sistema. Além disso, o projeto depende da biblioteca **Pygame Zero**, que pode ser instalada via `pip`.

*   **Python 3** (versão 3.6 ou superior)
*   **Pygame Zero**

### Clonar Repositório

Abra o terminal ou prompt de comando e execute o seguinte comando para clonar o repositório:

```bash
git clone https://github.com/LuizLaikovski/testKodland
cd testKodland
```

### Como Executar

1.  **Instalar Pygame Zero:**
    ```bash
    pip install pgzero
    ```

2.  **Executar o Jogo:**
    O jogo deve ser executado usando o comando `pgzrun` (o *runner* do Pygame Zero), apontando para o arquivo principal (`main.py`).

    ```bash
    pgzrun main.py
    ```

    **Controles:**
    *   **A / D:** Mover para a esquerda / direita.
    *   **Espaço:** Pular.
    *   **Mouse:** Interagir com o menu principal e opções.

## Estrutura da Aplicação

A estrutura do projeto é organizada em módulos Python e pastas para recursos (sprites, música, sons).

| Arquivo/Pasta | Descrição |
| :--- | :--- |
| `main.py` | O arquivo principal do jogo. Contém a lógica central, o *loop* do jogo (`draw`, `update`), o menu e a gestão de estados. |
| `config.py` | Módulo de configuração com constantes globais (tamanho da tela, gravidade, vidas, etc.). |
| `Diamond.py` | Classe que gerencia o item coletável (diamante), sua queda e *respawn*. |
| `Difficulty.py` | Classe simples para gerenciar o nível de dificuldade do jogo. |
| `Enemy.py` | Classe base para inimigos voadores (`EnemyFly`), incluindo lógica de movimento horizontal e colisão. |
| `EnemySlug.py` | Classe para inimigos terrestres (`EnemySlug`), com lógica de movimento horizontal e *respawn* fora da tela. |
| `sprites_*.py` | Módulos que contêm as listas de *sprites* e animações para o personagem, inimigos e cenário. |
| `images/` | Pasta que armazena os arquivos de imagem (`.png`) usados como *sprites* e *backgrounds*. |
| `music/` | Pasta para arquivos de música de fundo (`.ogg`, `.mp3`). |
| `sounds/` | Pasta para arquivos de efeitos sonoros (`.ogg`, `.wav`). |

## Comandos Básicos

| Comando | Descrição |
| :--- | :--- |
| `git clone <url>` | Clona o repositório para sua máquina local. |
| `pip install pgzero` | Instala a biblioteca Pygame Zero e suas dependências. |
| `pgzrun main.py` | Executa o jogo. |
| `python main.py` | **Não recomendado.** O Pygame Zero deve ser executado com `pgzrun`. |
