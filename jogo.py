import pygame
import random
import sys
pygame.init()

# Defina as dimensões da janela do jogo
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Meu Jogo")

# Defina as cores
branco = (255, 255, 255)
branco2 = (255, 0, 255)
preto = (0, 0, 0)

# Defina a fonte do texto
fonte = pygame.font.SysFont(None, 36)

# Defina a taxa de atualização da tela
clock = pygame.time.Clock()
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(branco2)
        self.rect = self.image.get_rect()
        self.rect.centerx = largura // 2
        self.rect.bottom = altura - 10
        self.velocidade = 5

    def update(self):
        # Movimentação do jogador
        teclas_pressionadas = pygame.key.get_pressed()
        if teclas_pressionadas[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
        if teclas_pressionadas[pygame.K_RIGHT]:
            self.rect.x += self.velocidade

        # Mantém o jogador dentro dos limites da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > largura:
            self.rect.right = largura

    def draw(self, tela):
        tela.blit(self.image, self.rect)



class Obstaculo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((random.randint(50, 100), 20))
        self.image.fill(preto)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, largura - self.rect.width)
        self.rect.y = -self.rect.height
        self.velocidade = random.randint(1, 5)

    def update(self):
        # Movimentação do obstáculo
        self.rect.y += self.velocidade

    def draw(self, tela):
        tela.blit(self.image, self.rect)

def game_over():
    tela.fill(branco)
    mensagem = fonte.render("Game Over", True, preto)
    retangulo_mensagem = mensagem.get_rect()
    retangulo_mensagem.center = (largura // 2, altura // 2)
    tela.blit(mensagem, retangulo_mensagem)
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()


def main():
    jogador = Jogador()
    obstaculos = pygame.sprite.Group()
    todos_sprites = pygame.sprite.Group()
    todos_sprites.add(jogador)

    pontos = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Criação dos obstáculos
        if random.randint(1, 100) <= 5:
            obstaculo = Obstaculo()
            obstaculos.add(obstaculo)
            todos_sprites.add(obstaculo)

        # Atualização dos sprites
        todos_sprites.update()

        # Verificação de colisão
        if pygame.sprite.spritecollide(jogador, obstaculos, False):
            game_over()

        # Limpa a tela
        tela.fill(branco)

        # Desenha os sprites na tela
        todos_sprites.draw(tela)

        # Atualiza a pontuação
        pontos += 1
        texto_pontos = fonte.render("Pontos: {}".format(pontos), True, preto)
        tela.blit(texto_pontos, (10, 10))

        # Atualiza a tela
        pygame.display.flip()

        # Define a taxa de atualização
        clock.tick(60)


if __name__ == "__main__":
    main()
