# 💎 TestKodland: Jogo de Plataforma com Pygame Zero

## 📜 Sobre o Projeto

Este é um projeto de jogo de plataforma 2D desenvolvido em **Python** utilizando a biblioteca **Pygame Zero (pgzero)**. O objetivo principal do jogador é controlar um personagem para coletar diamantes que caem, enquanto evita o contato com inimigos. O jogo tem como gênero Platformer (visão lateral, gravidade, chão, pulo).

A nova estrutura do projeto foi **modularizada** para melhor organização e manutenção, separando a lógica principal, o estado do jogo e a interface do usuário em módulos distintos.

**Principais Funcionalidades:**

*   **Mecânica de Jogo Clássica:** Movimentação horizontal, pulo com gravidade e detecção de colisão.
*   **Inimigos:** Dois tipos de inimigos:
    *   **Voadores (`EnemyFly`):** Movem-se horizontalmente em um território definido.
    *   **Terrestres (`EnemySlug`):** Movem-se no chão e reaparecem fora da tela.
*   **Coleta de Pontos:** O item coletável (`Diamond`) aparece aleatoriamente e aumenta a pontuação ao ser pego.
*   **Dificuldade Dinâmica:** A cada 10 pontos, a velocidade dos inimigos e a taxa de queda dos diamantes aumentam, elevando o desafio.
*   **Interface Completa:** Inclui um menu inicial, tela de opções para controle de áudio e tela de *Game Over*.
*   **Suporte a Redimensionamento:** O cenário e os elementos do jogo se ajustam automaticamente ao tamanho da janela.

## 🚀 Como Usar

### Pré-requisitos

Certifique-se de ter o **Python 3** instalado em seu sistema. O projeto requer a biblioteca **Pygame Zero**.

*   **Python 3** (versão 3.6+)
*   **Pygame Zero**

### 📥 Clonando o Repositório

Para obter o código-fonte, utilize o comando `git clone` e navegue até o diretório do projeto:

```bash
git clone https://github.com/LuizLaikovski/testKodland
cd testKodland
```

### ⚙️ Instalação e Execução

1.  **Instale a biblioteca Pygame Zero** usando o gerenciador de pacotes `pip`:

    ```bash
    pip install pgzero
    ```

2.  **Execute o jogo** utilizando o *runner* dedicado do Pygame Zero, o `pgzrun`:

    ```bash
    pgzrun main.py
    ```

    > **Nota:** O Pygame Zero deve ser executado com `pgzrun` e não diretamente com `python main.py`.

### 🎮 Controles

| Ação | Tecla |
| :--- | :--- |
| Mover para a Esquerda | **A** |
| Mover para a Direita | **D** |
| Pular | **Espaço** |
| Interagir com Menus | **Mouse (Clique)** |

## 📁 Estrutura da Aplicação

O projeto foi refatorado para uma arquitetura modular, separando as responsabilidades em três módulos principais: `main`, `logic`, `game_state` e `ui`.

| Arquivo/Pasta | Tipo | Descrição |
| :--- | :--- | :--- |
| `main.py` | Arquivo | **Ponto de entrada** do jogo. Atua como um *wrapper* para o Pygame Zero, delegando a maior parte da lógica para o módulo `logic`. |
| `logic.py` | Módulo | Contém a **lógica principal** do jogo, incluindo o loop de atualização (`update`), manipulação de entrada do usuário e funções de início/reinício. |
| `game_state.py` | Módulo | **Gerenciamento de Estado.** Armazena todas as variáveis globais e objetos do jogo (personagem, inimigos, pontuação, flags de áudio, etc.) para que outros módulos possam acessá-los e modificá-los de forma centralizada. |
| `ui.py` | Módulo | **Interface do Usuário.** Contém funções auxiliares para o desenho de elementos visuais, como a recriação do cenário (`rebuild_game_elements`), o HUD e a pontuação. |
| `config.py` | Módulo | Define constantes do jogo, como `WIDTH`, `HEIGHT`, `MAX_LIFES`, `gravity` e a lógica de redimensionamento de tela. |
| `Diamond.py` | Classe | Implementa a lógica do item coletável (diamante), incluindo sua queda, coleta e sistema de *respawn* temporizado. |
| `Enemy.py` | Classe | Define a classe `EnemyFly` (inimigo voador) com movimento horizontal limitado e detecção de colisão. |
| `EnemySlug.py` | Classe | Define a classe `EnemySlug` (inimigo terrestre) com movimento no chão e lógica de reaparecimento fora da tela. |
| `sprites_*.py` | Módulos | Arquivos que contêm as listas de *sprites* (imagens) e animações para o personagem, inimigos e cenário. |
| `images/` | Pasta | Armazena os arquivos de imagem (`.png`) usados como *sprites* e *backgrounds*. |
| `music/` | Pasta | Contém os arquivos de música de fundo. |
| `sounds/` | Pasta | Contém os arquivos de efeitos sonoros. |

## 💻 Comandos Básicos

| Comando | Descrição |
| :--- | :--- |
| `git clone <url>` | Baixa o repositório para sua máquina local. |
| `pip install pgzero` | Instala a biblioteca Pygame Zero e suas dependências. |
| `pgzrun main.py` | **Comando principal** para iniciar o jogo. |
| `cd testKodland` | Navega para o diretório do projeto. |