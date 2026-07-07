import pygame, random, os

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Carpeta base (donde está juego.py)
base_path = os.path.dirname(__file__)
sprite_path = os.path.join(base_path, "Sprite")

# Fondo loop
bg_img = pygame.image.load(os.path.join(sprite_path, "fondo_loop.png")).convert()
bg_y = 0

# Auto del jugador
player_img = pygame.image.load(os.path.join(sprite_path, "auto_jugador.png")).convert_alpha()
player_img = pygame.transform.scale(player_img, (40, 60))
player_rect = player_img.get_rect(center=(WIDTH//2, HEIGHT - 80))

# Rivales (varios tipos de autos y camiones)
enemy_imgs = [
    pygame.transform.scale(pygame.image.load(os.path.join(sprite_path, "auto_rojo.png")).convert_alpha(), (40, 60)),
    pygame.transform.scale(pygame.image.load(os.path.join(sprite_path, "auto_verde.png")).convert_alpha(), (40, 60)),
    pygame.transform.scale(pygame.image.load(os.path.join(sprite_path, "auto_amarillo.png")).convert_alpha(), (40, 60)),
    pygame.transform.scale(pygame.image.load(os.path.join(sprite_path, "camion.png")).convert_alpha(), (50, 80)),
    pygame.transform.scale(pygame.image.load(os.path.join(sprite_path, "van.png")).convert_alpha(), (45, 70))
]

enemies = []
score = 0
speed = 5
font = pygame.font.SysFont(None, 36)

running = True
while running:
    clock.tick(60)

    # Fondo loop
    bg_y += speed
    if bg_y >= HEIGHT:
        bg_y = 0
    screen.blit(bg_img, (0, bg_y - HEIGHT))
    screen.blit(bg_img, (0, bg_y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.move_ip(-5, 0)
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.move_ip(5, 0)
    if keys[pygame.K_UP]:
        speed = min(speed + 0.1, 15)
    if keys[pygame.K_DOWN]:
        speed = max(speed - 0.1, 2)

    # Crear enemigos
    if random.randint(1, 30) == 1:
        img = random.choice(enemy_imgs)
        rect = img.get_rect(center=(random.randint(40, WIDTH-40), -60))
        enemies.append((img, rect))

    # Mover enemigos
    for img, rect in enemies[:]:
        rect.move_ip(0, speed)
        if rect.top > HEIGHT:
            enemies.remove((img, rect))
            score += 1

    # Dibujar jugador y enemigos
    screen.blit(player_img, player_rect)
    for img, rect in enemies:
        screen.blit(img, rect)

    # Colisiones
    for img, rect in enemies:
        if player_rect.colliderect(rect):
            running = False

    # Marcador
    score_text = font.render(f"Score: {score}", True, (255,255,255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    
print("Game Over! Score:", score)
pygame.quit()
