import pygame, sys, random

pygame.init()
W, H = 640, 480
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Juego de Memoria - Figuras Básicas")
clock = pygame.time.Clock()

# Colores
WHITE = (255,255,255)
BLACK = (0,0,0)
COLORS = [
    (255,0,0),   # rojo
    (0,255,0),   # verde
    (0,0,255),   # azul
    (255,255,0), # amarillo
    (255,0,255), # magenta
    (0,255,255)  # cyan
]

# Crear pares de colores
cards = COLORS * 2
random.shuffle(cards)

# Tablero 3x4 (12 cartas)
rows, cols = 3, 4
grid = []
for r in range(rows):
    row = []
    for c in range(cols):
        rect = pygame.Rect(c*150+20, r*140+20, 100, 100)
        row.append({"rect":rect, "color":cards.pop(), "revealed":False, "matched":False})
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
                            if selected[0]["color"] == selected[1]["color"]:
                                selected[0]["matched"] = True
                                selected[1]["matched"] = True
                                pares += 1
                            else:
                                pygame.time.delay(500)
                                selected[0]["revealed"] = False
                                selected[1]["revealed"] = False
                            selected = []

    # Dibujar
    screen.fill(BLACK)
    for row in grid:
        for card in row:
            if card["revealed"] or card["matched"]:
                pygame.draw.rect(screen, card["color"], card["rect"])
            else:
                pygame.draw.rect(screen, WHITE, card["rect"])
    hud = font.render(f"Pares: {pares}  Intentos: {intentos}", True, WHITE)
    screen.blit(hud, (20, H-40))

    pygame.display.flip()
    clock.tick(30)
