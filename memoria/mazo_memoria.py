import pygame, sys, random

pygame.init()
W, H = 800, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Juego de Memoria RPG")
clock = pygame.time.Clock()

WHITE = (255,255,255)
BLACK = (0,0,0)

SPRITE_PATH = "C:/python/memoria/sprite/"
SIZE_CARD = (80,100)

NAMES = [
    "burro.png","caballo.png","lobo.png","murcielago.png",
    "vendedor_gerudo.png","vendedor_goron.png",
    "vendedor_hyrule.png","vendedor_orni.png","vendedor_zora.png"
]

IMAGES = [pygame.transform.scale(pygame.image.load(SPRITE_PATH+n), SIZE_CARD) for n in NAMES]
back_img = pygame.transform.scale(pygame.image.load(SPRITE_PATH+"misterioso.png"), SIZE_CARD)

# Crear pares
cards = IMAGES * 2
random.shuffle(cards)

rows, cols = 3, 6
total_width  = cols * SIZE_CARD[0] + (cols-1)*20
total_height = rows * SIZE_CARD[1] + (rows-1)*20
offset_x = (W - total_width)//2
offset_y = (H - total_height)//2

grid = []
for r in range(rows):
    row = []
    for c in range(cols):
        x = offset_x + c*(SIZE_CARD[0]+20)
        y = offset_y + r*(SIZE_CARD[1]+20)
        rect = pygame.Rect(x, y, SIZE_CARD[0], SIZE_CARD[1])
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
                            # Dibujar inmediatamente las dos cartas
                            screen.fill(BLACK)
                            for row2 in grid:
                                for card2 in row2:
                                    pygame.draw.rect(screen, WHITE, card2["rect"])
                                    if card2["revealed"] or card2["matched"]:
                                        screen.blit(card2["image"], card2["rect"])
                                    else:
                                        screen.blit(back_img, card2["rect"])
                            hud = font.render(f"Pares: {pares}  Intentos: {intentos}", True, WHITE)
                            screen.blit(hud, (20, H-40))
                            pygame.display.flip()

                            # Mantenerlas visibles un instante
                            pygame.time.delay(800)

                            if selected[0]["image"] == selected[1]["image"]:
                                selected[0]["matched"] = True
                                selected[1]["matched"] = True
                                pares += 1
                            else:
                                selected[0]["revealed"] = False
                                selected[1]["revealed"] = False
                            selected = []

    # Dibujar tablero
    screen.fill(BLACK)
    for row in grid:
        for card in row:
            pygame.draw.rect(screen, WHITE, card["rect"])  # fondo blanco
            if card["revealed"] or card["matched"]:
                screen.blit(card["image"], card["rect"])
            else:
                screen.blit(back_img, card["rect"])
    hud = font.render(f"Pares: {pares}  Intentos: {intentos}", True, WHITE)
    screen.blit(hud, (20, H-40))

    pygame.display.flip()
    clock.tick(30)


