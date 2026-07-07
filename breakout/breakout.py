import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de ventana
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Breakout - Proyecto Cumbre")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)

# Barra
barra = pygame.Rect(ANCHO//2 - 60, ALTO - 30, 120, 15)
vel_barra = 7

# Pelota
pelota = pygame.Rect(ANCHO//2, ALTO//2, 15, 15)
vel_pelota = [5, -5]

# Ladrillos
ladrillos = []
for fila in range(5):
    for col in range(10):
        ladrillo = pygame.Rect(10 + col*78, 50 + fila*30, 70, 20)
        ladrillos.append(ladrillo)

# Bucle principal
clock = pygame.time.Clock()
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimiento barra
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and barra.left > 0:
        barra.x -= vel_barra
    if teclas[pygame.K_RIGHT] and barra.right < ANCHO:
        barra.x += vel_barra

    # Movimiento pelota
    pelota.x += vel_pelota[0]
    pelota.y += vel_pelota[1]

    # Rebotes
    if pelota.left <= 0 or pelota.right >= ANCHO:
        vel_pelota[0] = -vel_pelota[0]
    if pelota.top <= 0:
        vel_pelota[1] = -vel_pelota[1]
    if pelota.colliderect(barra):
        vel_pelota[1] = -vel_pelota[1]

    # Colisión con ladrillos
    for ladrillo in ladrillos[:]:
        if pelota.colliderect(ladrillo):
            ladrillos.remove(ladrillo)
            vel_pelota[1] = -vel_pelota[1]
            break

    # Fondo
    ventana.fill(NEGRO)

    # Dibujar barra, pelota y ladrillos
    pygame.draw.rect(ventana, BLANCO, barra)
    pygame.draw.ellipse(ventana, ROJO, pelota)
    for ladrillo in ladrillos:
        pygame.draw.rect(ventana, AZUL, ladrillo)

    pygame.display.flip()
    clock.tick(60)
