import pygame, sys

pygame.init()
ANCHO, ALTO = 1000, 700   # pantalla más grande
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Breakout - Proyecto Cumbre")

NEGRO, BLANCO, AZUL, ROJO = (0,0,0), (255,255,255), (0,0,255), (255,0,0)

# Barra
barra = pygame.Rect(ANCHO//2 - 60, ALTO - 50, 120, 15)
vel_barra = 7

# Pelota
pelota = pygame.Rect(ANCHO//2, ALTO//2, 15, 15)
vel_pelota = [5, -5]

# Ladrillos
ladrillos = [pygame.Rect(10+col*95, 50+fila*30, 85, 20)
             for fila in range(5) for col in range(15)]

# Franja negra de peligro
franja = pygame.Rect(0, ALTO-20, ANCHO, 20)

fuente = pygame.font.SysFont(None, 60)
clock = pygame.time.Clock()
estado = "jugando"
puntos = 0

while estado == "jugando":
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    # Movimiento barra
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and barra.left > 0: barra.x -= vel_barra
    if teclas[pygame.K_RIGHT] and barra.right < ANCHO: barra.x += vel_barra

    # Movimiento pelota
    pelota.x += vel_pelota[0]; pelota.y += vel_pelota[1]

    # Rebotes
    if pelota.left <= 0 or pelota.right >= ANCHO: vel_pelota[0] *= -1
    if pelota.top <= 0: vel_pelota[1] *= -1
    if pelota.colliderect(barra): vel_pelota[1] *= -1

    # Colisión con ladrillos
    for ladrillo in ladrillos[:]:
        if pelota.colliderect(ladrillo):
            ladrillos.remove(ladrillo); vel_pelota[1] *= -1;
            puntos +=15
            break

    # Condiciones de fin
    if pelota.colliderect(franja): estado = "gameover"
    if not ladrillos: estado = "win"

    # Dibujar
    ventana.fill(NEGRO)
    pygame.draw.rect(ventana, BLANCO, barra)
    pygame.draw.ellipse(ventana, ROJO, pelota)
    for l in ladrillos: pygame.draw.rect(ventana, AZUL, l)
    pygame.draw.rect(ventana, NEGRO, franja)  # franja negra al fondo
    texto_puntos = fuente.render(f"Puntos: {puntos}", True, BLANCO)
    ventana.blit(texto_puntos, (10, 10))
    pygame.display.flip(); clock.tick(60)

# Bucle final
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    ventana.fill(NEGRO)
    if estado == "gameover":
        msg = fuente.render("GAME OVER", True, ROJO)
    else:
        msg = fuente.render("YOU WIN!", True, AZUL)
    ventana.blit(msg, (ANCHO//2 - msg.get_width()//2, ALTO//2))

    # Mostrar puntuación final
    texto_final = fuente.render(f"Puntos: {puntos}", True, BLANCO)
    ventana.blit(texto_final, (ANCHO//2 - texto_final.get_width()//2, ALTO//2 + 60))


    pygame.display.flip(); clock.tick(30)

