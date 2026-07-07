import pygame, sys, random

pygame.init()
W, H = 800, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Juego de Memoria RPG")
clock = pygame.time.Clock()

WHITE = (255,255,255)
BLACK = (0,0,0)

SPRITE_PATH = "C:\\python\\memoria\\sprite\\"
SIZE_CARD = (80,80)

# Lista de sprites
NAMES = [
    "burro.png","caballo.png","lobo.png","murcielago.png",
    "vendedor_gerudo.png","vendedor_goron.png",
    "vendedor_hyrule.png","vendedor_orni.png","vendedor_zora.png"
]

IMAGES = [pygame.transform.scale(pygame.image.load(SPRITE_PATH+n), SIZE_CARD) for n in NAMES]

# Crear pares
cards = IMAGES * 2
random.shuffle(cards)

rows, cols = 3, 6   # tablero 18 cartas
grid = []
for r in range(rows):
    row = []
    for c in range(cols):
        rect = pygame.Rect(c*120+20, r*160+20, SIZE_CARD[0], SIZE_CARD[1])
        row.append({"rect":rect, "image":cards.pop(), "revealed":False, "matched":False})
    grid.append(row)

font = pygame.font.SysFont("Arial", 24)
selected = []
pares = 0
intentos = 0

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN:
            pos = e.pos
            for row in grid:
                for card in row:
                    if card["rect"].collidepoint(pos) and not card["revealed"] and not card["matched"]:
                        card["revealed"] = True
                        selected.append(card)
                        if len(selected) == 2:
                            intentos += 1
                            if selected[0]["image"] == selected[1]["image"]:
                                selected[0]["matched"] = True
                                selected[1]["matched"] = True
                                pares += 1
                            else:
                                pygame.time.delay(600)
                                selected[0]["revealed"] = False
                                selected[1]["revealed"] = False
                            selected = []

    # Dibujar
    screen.fill(BLACK)
    for row in grid:
        for card in row:
            if card["revealed"] or card["matched"]:
                screen.blit(card["image"], card["rect"])
            else:
                pygame.draw.rect(screen, WHITE, card["rect"])
    hud = font.render(f"Pares: {pares}  Intentos: {intentos}", True, WHITE)
    screen.blit(hud, (20, H-40))

    pygame.display.flip()
    clock.tick(30)
