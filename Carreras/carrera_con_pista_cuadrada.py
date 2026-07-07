import pygame, random

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = pygame.Rect(WIDTH//2 - 20, HEIGHT - 60, 40, 60)
enemies = []
score = 0
speed = 5

# Fuente para el marcador
font = pygame.font.SysFont("Arial", 28, bold=True)

running = True
while running:
    clock.tick(60)
    screen.fill((50,50,50))  # carretera gris

    # Líneas de carretera
    for i in range(0, HEIGHT, 100):
        pygame.draw.rect(screen, (255,255,255), (WIDTH//2 - 5, i, 10, 50))  # rayas centrales
    pygame.draw.rect(screen, (255,255,0), (5, 0, 5, HEIGHT))   # línea amarilla izquierda
    pygame.draw.rect(screen, (255,255,0), (WIDTH-10, 0, 5, HEIGHT)) # línea amarilla derecha

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 10:
        player.move_ip(-5, 0)
    if keys[pygame.K_RIGHT] and player.right < WIDTH-10:
        player.move_ip(5, 0)
    if keys[pygame.K_UP]:
        speed = min(speed + 0.1, 15)
    if keys[pygame.K_DOWN]:
        speed = max(speed - 0.1, 2)

    # Crear enemigos
    if random.randint(1, 30) == 1:
        enemies.append(pygame.Rect(random.randint(20, WIDTH-60), -60, 40, 60))

    # Mover enemigos
    for enemy in enemies[:]:
        enemy.move_ip(0, speed)
        if enemy.top > HEIGHT:
            enemies.remove(enemy)
            score += 1

    # Dibujar jugador (rectángulo con parabrisas y luces)
    pygame.draw.rect(screen, (0,0,255), player)  # azul
    pygame.draw.rect(screen, (255,255,255), player, 2)  # borde blanco
    pygame.draw.rect(screen, (0,0,0), (player.x+5, player.y+10, 30, 15))  # parabrisas
    pygame.draw.circle(screen, (255,255,0), (player.x+10, player.y+55), 5)  # luz trasera izquierda
    pygame.draw.circle(screen, (255,255,0), (player.x+30, player.y+55), 5)  # luz trasera derecha

    # Dibujar enemigos con estilo
    for enemy in enemies:
        pygame.draw.rect(screen, (200,0,0), enemy)  # rojo
        pygame.draw.rect(screen, (255,255,255), enemy, 2)  # borde blanco
        pygame.draw.rect(screen, (255,255,0), (enemy.x+15, enemy.y, 10, 60))  # franja central
        pygame.draw.circle(screen, (255,255,255), (enemy.x+10, enemy.y+5), 4)  # luces delanteras
        pygame.draw.circle(screen, (255,255,255), (enemy.x+30, enemy.y+5), 4)

    # Colisiones
    for enemy in enemies:
        if player.colliderect(enemy):
            running = False

    # Marcador
    score_text = font.render(f"Score: {score}", True, (255,255,255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

print("Game Over! Score:", score)
pygame.quit()
