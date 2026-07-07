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
font = pygame.font.SysFont(None, 36)

running = True
while running:
    clock.tick(60)
    screen.fill((0,0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.move_ip(-5, 0)
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.move_ip(5, 0)
    if keys[pygame.K_UP]:
        speed = min(speed + 0.1, 15)
    if keys[pygame.K_DOWN]:
        speed = max(speed - 0.1, 2)
    
    if random.randint(1, 30) == 1:
        enemies.append(pygame.Rect(random.randint(0, WIDTH-40), -60, 40, 60))
    
    for enemy in enemies[:]:
        enemy.move_ip(0, speed)
        if enemy.top > HEIGHT:
            enemies.remove(enemy)
            score += 1
    
    pygame.draw.rect(screen, (0,0,255), player)
    for enemy in enemies:
        pygame.draw.rect(screen, (255,0,0), enemy)
    
    # Colisiones
    for enemy in enemies:
        if player.colliderect(enemy):
            running = False
    
    # Dibujar marcador
    score_text = font.render(f"Score: {score}", True, (255,255,255))
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()

pygame.quit()

