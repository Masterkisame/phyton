import pygame, sys, random

pygame.init()
W, H = 640, 640
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Puzzle de Gemas Finito")
clock = pygame.time.Clock()

ROWS, COLS = 8, 8
SIZE = 70
MARGIN = 5

COLORS = {
    "Rojo": (255,0,0),
    "Verde": (0,255,0),
    "Azul": (0,0,255),
    "Amarillo": (255,255,0),
    "Magenta": (255,0,255),
    "Cyan": (0,255,255)
}

board = [[random.choice(list(COLORS.values())) for _ in range(COLS)] for _ in range(ROWS)]

selected = []
score = 0
gem_count = {name:0 for name in COLORS.keys()}
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
        color = board[r][c]
        for name,val in COLORS.items():
            if val == color:
                gem_count[name] += 1
        board[r][c] = None
    score += len(matched)
    return len(matched) > 0

def apply_gravity():
    for c in range(COLS):
        for r in range(ROWS-1, -1, -1):
            if board[r][c] is None:
                for k in range(r-1, -1, -1):
                    if board[k][c] is not None:
                        board[r][c] = board[k][c]
                        board[k][c] = None
                        break

def moves_available():
    # Solo verificar si hay movimientos posibles, sin resolver
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] is None: continue
            for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr,nc = r+dr,c+dc
                if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc]:
                    # simular intercambio
                    board[r][c], board[nr][nc] = board[nr][nc], board[r][c]
                    # comprobar si habría match
                    found = False
                    # horizontal
                    for cc in range(COLS-2):
                        if board[r][cc] and board[r][cc] == board[r][cc+1] == board[r][cc+2]:
                            found = True
                    # vertical
                    for rr in range(ROWS-2):
                        if board[rr][c] and board[rr][c] == board[rr+1][c] == board[rr+2][c]:
                            found = True
                    # revertir
                    board[r][c], board[nr][nc] = board[nr][nc], board[r][c]
                    if found:
                        return True
    return False

game_over = False

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: sys.exit()
        if not game_over and e.type == pygame.MOUSEBUTTONDOWN:
            pos = e.pos
            c = pos[0] // (SIZE+MARGIN)
            r = pos[1] // (SIZE+MARGIN)
            if r < ROWS and c < COLS:
                selected.append((r,c))
                if len(selected) == 2:
                    r1,c1 = selected[0]
                    r2,c2 = selected[1]
                    if abs(r1-r2)+abs(c1-c2) == 1:
                        board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]
                        if check_matches():
                            apply_gravity()
                        else:
                            board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]
                    selected = []

    screen.fill((0,0,0))
    draw_board()
    hud = font.render(f"Puntuación: {score}", True, (255,255,255))
    screen.blit(hud, (20, H-40))

    if not game_over and (not moves_available() or all(all(cell is None for cell in row) for row in board)):
        game_over = True

    if game_over:
        msg = font.render("GAME OVER", True, (255,255,255))
        screen.blit(msg, (W//2-80, H//2-40))
        y_offset = H//2
        for name,count in gem_count.items():
            txt = font.render(f"{name}: {count}", True, (255,255,255))
            screen.blit(txt, (W//2-80, y_offset))
            y_offset += 30

    pygame.display.flip()
    clock.tick(30)

