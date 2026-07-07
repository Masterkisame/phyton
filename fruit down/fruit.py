import pygame, sys, random

pygame.init()
W, H = 800, 600   # ventana más grande
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Fruit Down Arcade")
clock = pygame.time.Clock()

# Colores
BLACK = (0,0,0)
WHITE = (255,255,255)

# Jugador
player = pygame.Rect(W//2, H-80, 80, 20)

# Sprites path
SPRITE_PATH = "C:/python/fruit down/sprite/"
FRUIT_SIZE = (40, 40)   # tamaño frutas en juego
HUD_SIZE   = (24, 24)   # tamaño íconos HUD

ITEMS = {
    "Manzana": {"sprite": pygame.image.load(SPRITE_PATH+"manzana.png"), "puntos":1},
    "Naranja": {"sprite": pygame.image.load(SPRITE_PATH+"naranja.png"), "puntos":2},
    "Uva": {"sprite": pygame.image.load(SPRITE_PATH+"uva.png"), "puntos":3},
    "Rupia": {"sprite": pygame.image.load(SPRITE_PATH+"rupia.png"), "puntos":5},
    "Zanahoria": {"sprite": pygame.image.load(SPRITE_PATH+"zanahoria.png"), "puntos":2}
}

# Escalar sprites
for nombre, datos in ITEMS.items():
    datos["sprite_game"] = pygame.transform.scale(datos["sprite"], FRUIT_SIZE)
    datos["sprite_hud"]  = pygame.transform.scale(datos["sprite"], HUD_SIZE)

# Lista de frutas
frutas = []
puntos = 0
contador = {nombre:0 for nombre in ITEMS.keys()}

font = pygame.font.SysFont("Arial", 22)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: player.x -= 20
    if keys[pygame.K_RIGHT]: player.x += 20
    player.x = max(0, min(W-player.width, player.x))

    # Generar frutas
    if random.randint(1, 25) == 1:
        nombre, datos = random.choice(list(ITEMS.items()))
        frutas.append({
            "nombre": nombre,
            "sprite": datos["sprite_game"],
            "rect": datos["sprite_game"].get_rect(topleft=(random.randint(0, W-40), 0)),
            "puntos": datos["puntos"]
        })

    # Mover frutas
    for f in frutas[:]:
        f["rect"].y += 6
        if f["rect"].colliderect(player):
            puntos += f["puntos"]
            contador[f["nombre"]] += 1
            frutas.remove(f)
        elif f["rect"].y > H:
            frutas.remove(f)

    # Dibujar
    screen.fill(BLACK)
    pygame.draw.rect(screen, (0,255,0), player)

    for f in frutas:
        screen.blit(f["sprite"], f["rect"])

    # HUD arcade abajo
    hud_y = H-50
    x_offset = 10
    for nombre, datos in ITEMS.items():
        screen.blit(datos["sprite_hud"], (x_offset, hud_y))
        txt = font.render(str(contador[nombre]), True, WHITE)
        screen.blit(txt, (x_offset+30, hud_y+5))
        x_offset += 100

    puntos_txt = font.render(f"Puntos: {puntos}", True, WHITE)
    screen.blit(puntos_txt, (W-180, hud_y+5))

    pygame.display.flip()
    clock.tick(30)

