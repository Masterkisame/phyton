import pygame, random

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Auto del jugador
player = pygame.Rect(WIDTH//2 - 20, HEIGHT - 60, 40, 60)

# Lista de enemigos
enemies = []

score = 0
running = True
while running:
    clock.tick(60)
    screen.fill((0,0,0))  # fondo negro
    
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.move_ip(-5, 0)
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.move_ip(5, 0)
    
    # Crear enemigos
    if random.randint(1, 30) == 1:
        enemies.append(pygame.Rect(random.randint(0, WIDTH-40), -60, 40, 60))
    
    # Mover enemigos
    for enemy in enemies[:]:
        enemy.move_ip(0, 5)
        if enemy.top > HEIGHT:
            enemies.remove(enemy)
            score += 1
    
    # Dibujar
    pygame.draw.rect(screen, (0,0,255), player)  # azul
    for enemy in enemies:
        pygame.draw.rect(screen, (255,0,0), enemy)  # rojo
    
    # Colisiones
    for enemy in enemies:
        if player.colliderect(enemy):
            running = False
    
    pygame.display.flip()

print("Game Over! Score:", score)
pygame.quit()
