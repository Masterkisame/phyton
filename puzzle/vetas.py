import pygame, sys, random

pygame.init()
W, H = 640, 640
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Puzzle de Gemas con Sprites")
clock = pygame.time.Clock()

ROWS, COLS = 8, 8
SIZE = 70
MARGIN = 5

SPRITE_PATH = "C:/python/puzzle/sprite/"

# Diccionario de sprites
GEMAS = {
    "Cobre": pygame.image.load(SPRITE_PATH+"cobre.png"),
    "Roca": pygame.image.load(SPRITE_PATH+"roca.png"),
    "Rupia": pygame.image.load(SPRITE_PATH+"rupia.png"),
    "Zafiro": pygame.image.load(SPRITE_PATH+"veta_zafiro.png"),
    "Diamante": pygame.image.load(SPRITE_PATH+"diamante.png"),
    "Oro": pygame.image.load(SPRITE_PATH+"veta_oro.png")
}

# Escalar sprites al tamaño de casilla
for k in GEMAS:
    GEMAS[k] = pygame.transform.scale(GEMAS[k], (SIZE,SIZE))

# Crear tablero inicial con gemas y algunas rocas
def new_board():
    board = [[random.choice(["Cobre","Rupia","Zafiro","Diamante","Oro"]) for _ in range(COLS)] for _ in range(ROWS)]
    # Insertar rocas como huecos fijos
    for r in range(ROWS):
        for c in range(COLS):
            if random.random() < 0.1:  # 10% del tablero serán rocas
                board[r][c] = "Roca"
    return board

board = new_board()
selected = []
score = 0
gem_count = {name:0 for name in GEMAS.keys()}
font = pygame.font.SysFont("Arial", 24)

def draw_board():
    for r in range(ROWS):
        for c in range(COLS):
            x = c*(SIZE+MARGIN)+MARGIN
            y = r*(SIZE+MARGIN)+MARGIN
            name = board[r][c]
            screen.blit(GEMAS[name], (x,y))  # dibujar sprite
            # ❌ Ya no dibujamos marcos

def check_matches():
    global score
    matched = []
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS-2):
            if board[r][c] != "Roca" and board[r][c] == board[r][c+1] == board[r][c+2]:
                matched += [(r,c),(r,c+1),(r,c+2)]
    # Vertical
    for r in range(ROWS-2):
        for c in range(COLS):
            if board[r][c] != "Roca" and board[r][c] == board[r+1][c] == board[r+2][c]:
                matched += [(r,c),(r+1,c),(r+2,c)]
    for r,c in matched:
        name = board[r][c]
        gem_count[name] += 1
        board[r][c] = "Roca"   # al eliminar, se convierte en roca
    score += len(matched)
    return len(matched) > 0

def apply_gravity():
    for c in range(COLS):
        for r in range(ROWS-1, -1, -1):
            if board[r][c] == "Roca":
                for k in range(r-1, -1, -1):
                    if board[k][c] != "Roca":
                        board[r][c] = board[k][c]
                        board[k][c] = "Roca"
                        break

def moves_available():
    # Solo verificar gemas, ignorar rocas
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == "Roca": 
                continue
            for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr,nc = r+dr,c+dc
                if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] != "Roca":
                    # simular intercambio
                    board[r][c], board[nr][nc] = board[nr][nc], board[r][c]
                    found = False
                    # checar horizontal
                    for cc in range(COLS-2):
                        if board[r][cc] != "Roca" and board[r][cc] == board[r][cc+1] == board[r][cc+2]:
                            found = True
                    # checar vertical
                    for rr in range(ROWS-2):
                        if board[rr][c] != "Roca" and board[rr][c] == board[rr+1][c] == board[rr+2][c]:
                            found = True
                    # revertir
                    board[r][c], board[nr][nc] = board[nr][nc], board[r][c]
                    if found:
                        return True
    return False

def reset_game():
    global board, selected, score, gem_count, game_over
    board = new_board()
    selected = []
    score = 0
    gem_count = {name:0 for name in GEMAS.keys()}
    game_over = False

game_over = False

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: sys.exit()
        if game_over and e.type == pygame.KEYDOWN and e.key == pygame.K_r:
            reset_game()
        if not game_over and e.type == pygame.MOUSEBUTTONDOWN:
            pos = e.pos
            c = pos[0] // (SIZE+MARGIN)
            r = pos[1] // (SIZE+MARGIN)
            if r < ROWS and c < COLS and board[r][c] != "Roca":
                selected.append((r,c))
                if len(selected) == 2:
                    r1,c1 = selected[0]
                    r2,c2 = selected[1]
                    if abs(r1-r2)+abs(c1-c2) == 1 and board[r2][c2] != "Roca":
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

    if not game_over and (not moves_available() or all(all(cell == "Roca" for cell in row) for row in board)):
        game_over = True

    if game_over:
        overlay = pygame.Surface((W,H))
        overlay.set_alpha(200)
        overlay.fill((0,0,0))
        screen.blit(overlay, (0,0))

        msg = font.render("GAME OVER", True, (255,255,255))
        screen.blit(msg, (W//2-80, H//2-120))

        pts = font.render(f"Puntuación: {score}", True, (255,255,255))
        screen.blit(pts, (W//2-80, H//2-80))

        y_offset = H//2-40
        for name,count in gem_count.items():
            txt = font.render(f"{name}: {count}", True, (255,255,255))
            screen.blit(txt, (W//2-80, y_offset))
            y_offset += 30

        restart = font.render("Presiona R para reiniciar", True, (200,200,200))
        screen.blit(restart, (W//2-120, H-60))

    pygame.display.flip()
    clock.tick(30)

