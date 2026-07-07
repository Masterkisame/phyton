import pygame, sys, random

pygame.init()
W, H = 640, 640
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Puzzle de Gemas Finito")
clock = pygame.time.Clock()

ROWS, COLS = 8, 8
SIZE = 70
MARGIN = 5

COLORS = [
    (255,0,0),    # rojo
    (0,255,0),    # verde
    (0,0,255),    # azul
    (255,255,0),  # amarillo
    (255,0,255),  # magenta
    (0,255,255)   # cyan
]

# Crear tablero inicial
board = [[random.choice(COLORS) for _ in range(COLS)] for _ in range(ROWS)]

selected = []
score = 0
font = pygame.font.SysFont("Arial", 24)

def draw_board():
    for r in range(ROWS):
        for c in range(COLS):
            x = c*(SIZE+MARGIN)+MARGIN
            y = r*(SIZE+MARGIN)+MARGIN
            color = board[r][c]
            if color:
                pygame.draw.rect(screen, color, (x,y,SIZE,SIZE))
            else:
                pygame.draw.rect(screen, (50,50,50), (x,y,SIZE,SIZE))  # hueco vacío
            pygame.draw.rect(screen, (255,255,255), (x,y,SIZE,SIZE), 2)

def check_matches():
    global score
    matched = []
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS-2):
            if board[r][c] and board[r][c] == board[r][c+1] == board[r][c+2]:
                matched += [(r,c),(r,c+1),(r,c+2)]
    # Vertical
    for r in range(ROWS-2):
        for c in range(COLS):
            if board[r][c] and board[r][c] == board[r+1][c] == board[r+2][c]:
                matched += [(r,c),(r+1,c),(r+2,c)]
    for r,c in matched:
        board[r][c] = None   # ahora queda vacío
    score += len(matched)
    return len(matched) > 0

def apply_gravity():
    for c in range(COLS):
        for r in range(ROWS-1, -1, -1):
            if board[r][c] is None:
                # buscar arriba
                for k in range(r-1, -1, -1):
                    if board[k][c] is not None:
                        board[r][c] = board[k][c]
                        board[k][c] = None
                        break

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN:
            pos = e.pos
            c = pos[0] // (SIZE+MARGIN)
            r = pos[1] // (SIZE+MARGIN)
            if r < ROWS and c < COLS:
                selected.append((r,c))
                if len(selected) == 2:
                    r1,c1 = selected[0]
                    r2,c2 = selected[1]
                    # Solo intercambiar si son adyacentes
                    if abs(r1-r2)+abs(c1-c2) == 1:
                        board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]
                        if check_matches():
                            apply_gravity()
                        else:
                            # revertir si no hay match
                            board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]
                    selected = []

    screen.fill((0,0,0))
    draw_board()
    hud = font.render(f"Puntuación: {score}", True, (255,255,255))
    screen.blit(hud, (20, H-40))
    pygame.display.flip()
    clock.tick(30)
