import pygame
import random

# Definir as constantes
CELL_SIZE = 32
GRID_WIDTH = 64
GRID_HEIGHT = 64
WIN_WIDTH = 800
WIN_HEIGHT = 600
CAMERA_WIDTH = WIN_WIDTH // CELL_SIZE
CAMERA_HEIGHT = WIN_HEIGHT // CELL_SIZE
FPS = 60

# Definir as cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Inicializar o Pygame
pygame.init()
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Labirinto 2D")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Classe do jogador
class Player:
    def __init__(self):
        self.row = 0
        self.col = 0

    def move(self, drow, dcol):
        new_row = self.row + drow
        new_col = self.col + dcol

        # Verificar se o movimento é válido
        if new_row >= 0 and new_row < GRID_HEIGHT and new_col >= 0 and new_col < GRID_WIDTH:
            cell_value = grid[new_row][new_col]
            if cell_value == 2:
                print("Você não sabe nadar!")
            elif cell_value == 3:
                print("Você precisa de uma picareta!")
            else:
                self.row = new_row
                self.col = new_col

# Classe do monstro
class Monster:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.trapped = False

    def move(self):
        if self.trapped:
            self.move_trapped()
        else:
            self.move_follow()

    def move_trapped(self):
        # Movimento aleatório dentro da área restrita
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        drow, dcol = random.choice(directions)
        new_row = self.row + drow
        new_col = self.col + dcol

        # Verificar se o movimento é válido
        if new_row >= 0 and new_row < GRID_HEIGHT and new_col >= 0 and new_col < GRID_WIDTH and grid[new_row][new_col] != 1:
            self.row = new_row
            self.col = new_col

    def move_follow(self):
        player_row, player_col = player.row, player.col

        if self.row < player_row:
            drow = 1
        elif self.row > player_row:
            drow = -1
        else:
            drow = 0

        if self.col < player_col:
            dcol = 1
        elif self.col > player_col:
            dcol = -1
        else:
            dcol = 0

        # Verificar se o movimento é válido
        new_row = self.row + drow
        new_col = self.col + dcol
        if new_row >= 0 and new_row < GRID_HEIGHT and new_col >= 0 and new_col < GRID_WIDTH:
            cell_value = grid[new_row][new_col]
            if cell_value != 1:
                self.row = new_row
                self.col = new_col


# Função para criar um novo mapa utilizando busca em profundidade (DFS)
def create_map():
    grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

    def dfs(row, col):
        grid[row][col] = 1
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        random.shuffle(directions)
        for drow, dcol in directions:
            new_row = row + 2 * drow
            new_col = col + 2 * dcol
            if new_row >= 0 and new_row < GRID_HEIGHT and new_col >= 0 and new_col < GRID_WIDTH and grid[new_row][new_col] == 0:
                grid[row + drow][col + dcol] = 1
                dfs(new_row, new_col)

    dfs(0, 0)

    exit_row = random.randint(0, GRID_HEIGHT - 1)
    exit_col = random.randint(0, GRID_WIDTH - 1)
    grid[exit_row][exit_col] = 100

    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if grid[row][col] != 100 and grid[row][col] != 1:
                grid[row][col] = random.randint(1, 5)

    return grid

# Inicializar o jogador, o monstro e o mapa
player = Player()
monster = Monster(GRID_HEIGHT - 1, GRID_WIDTH - 1)
grid = create_map()

# Variáveis de câmera
camera_x = 0
camera_y = 0

# Variáveis de jogo
game_over = False

# Loop principal do jogo
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_UP:
                    player.move(-1, 0)
                elif event.key == pygame.K_DOWN:
                    player.move(1, 0)
                elif event.key == pygame.K_LEFT:
                    player.move(0, -1)
                elif event.key == pygame.K_RIGHT:
                    player.move(0, 1)
            else:
                if event.key == pygame.K_RETURN:
                    grid = create_map()
                    player.row = 0
                    player.col = 0
                    game_over = False

    # Movimentar o monstro
    monster.move()

    # Verificar se o monstro alcançou o jogador
    if monster.row == player.row and monster.col == player.col:
        game_over = True

    # Atualizar a posição da câmera para manter o jogador no centro da visão
    camera_x = max(0, min(player.col - CAMERA_WIDTH // 2, GRID_WIDTH - CAMERA_WIDTH))
    camera_y = max(0, min(player.row - CAMERA_HEIGHT // 2, GRID_HEIGHT - CAMERA_HEIGHT))

    # Desenhar o mapa
    win.fill(WHITE)
    for row in range(camera_y, camera_y + CAMERA_HEIGHT):
        for col in range(camera_x, camera_x + CAMERA_WIDTH):
            cell_value = grid[row][col]
            color = WHITE
            if cell_value == 2:
                color = BLUE
            elif cell_value == 3:
                color = BLACK
            elif cell_value == 100:
                color = RED

            pygame.draw.rect(win, color, ((col - camera_x) * CELL_SIZE, (row - camera_y) * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Desenhar o jogador
    pygame.draw.rect(win, RED, ((player.col - camera_x) * CELL_SIZE, (player.row - camera_y) * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Desenhar o monstro
    pygame.draw.rect(win, GREEN, ((monster.col - camera_x) * CELL_SIZE, (monster.row - camera_y) * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Verificar se o jogador chegou na saída
    if grid[player.row][player.col] == 100 and (monster.row != player.row or monster.col != player.col):
        game_over = True
        text = font.render("Você venceu! Pressione Enter para jogar novamente.", True, BLACK)
        text_rect = text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
        win.blit(text, text_rect)

    # Verificar se o monstro alcançou o jogador
    if game_over and (monster.row == player.row and monster.col == player.col):
        text = font.render("Você foi pego pelo monstro! Pressione Enter para jogar novamente.", True, BLACK)
        text_rect = text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
        win.blit(text, text_rect)

    # Atualizar a janela
    pygame.display.update()

pygame.quit()
