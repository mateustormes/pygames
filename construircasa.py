import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Inicialização do Pygame
pygame.init()
width, height = 800, 600
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)

# Configuração inicial da câmera
glMatrixMode(GL_PROJECTION)
gluPerspective(45, (width / height), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)
gluLookAt(0, -10, 0, 0, 0, 0, 0, 0, 1)

# Posição inicial do jogador
player_pos = [0, 0, 0]

# Variável para controlar o modo de câmera
camera_mode = "follow_mouse"

# Função para desenhar um cubo
def draw_cube():
    vertices = (
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, -1, 1),
        (-1, 1, 1)
    )

    edges = (
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4),
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7)
    )

    faces = (
        (0, 1, 2, 3),
        (3, 2, 7, 6),
        (6, 7, 5, 4),
        (4, 5, 1, 0),
        (1, 5, 7, 2),
        (4, 0, 3, 6)
    )

    glBegin(GL_QUADS)
    for face in faces:
        glColor3fv((1, 0, 0))
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

    glColor3fv((0, 0, 0))
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botão esquerdo do mouse pressionado
                camera_mode = "rotate_camera"
            elif event.button == 3:  # Botão direito do mouse pressionado
                camera_mode = "follow_mouse"

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Botão esquerdo do mouse solto
                camera_mode = "follow_mouse"

    # Captura os eventos de teclado
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] += 0.1
    if keys[pygame.K_RIGHT]:
        player_pos[0] -= 0.1
    if keys[pygame.K_UP]:
        player_pos[2] += 0.1
    if keys[pygame.K_DOWN]:
        player_pos[2] -= 0.1

    # Captura a posição do mouse
    if camera_mode == "rotate_camera":
        mouse_x, mouse_y = pygame.mouse.get_rel()
        player_pos[0] += mouse_x * 0.1
        player_pos[1] += mouse_y * 0.1

    # Limpa a tela
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Desenha o chão
    glBegin(GL_QUADS)
    glVertex3fv((-25, -1, -500))
    glVertex3fv((-25, -1, 500))
    glVertex3fv((25, -1, 500))
    glVertex3fv((25, -1, -500))
    glEnd()

    # Desenha as paredes laterais
    glBegin(GL_QUADS)
    glVertex3fv((-25, -1, -500))
    glVertex3fv((-25, -1, 500))
    glVertex3fv((-25, 5, 500))
    glVertex3fv((-25, 5, -500))

    glVertex3fv((25, -1, -500))
    glVertex3fv((25, -1, 500))
    glVertex3fv((25, 5, 500))
    glVertex3fv((25, 5, -500))
    glEnd()

    # Desenha o jogador
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])
    draw_cube()
    glPopMatrix()

    # Verifica se o jogador caiu do chão
    if player_pos[1] < -10:
        font = pygame.font.Font(None, 36)
        text = font.render("Você morreu!", True, (255, 0, 0))
        textpos = text.get_rect(center=(width / 2, height / 2))
        pygame.display.get_surface().blit(text, textpos)
        pygame.display.flip()
        pygame.time.wait(2000)
        player_pos = [0, 0, 0]

    pygame.display.flip()
    pygame.time.wait(10)
