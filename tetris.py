import pygame, sys, random

pygame.init()
ANCHO, ALTO = 400, 800
TAM_CASILLA = 30
ALTO_JUEGO = ALTO - 60   # dejamos 60 px para HUD
COLUMNAS, FILAS = ANCHO // TAM_CASILLA, ALTO_JUEGO // TAM_CASILLA

ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Tetris - Proyecto Cumbre")

NEGRO, BLANCO, ROJO, AZUL, VERDE, AMARILLO, CYAN, MAGENTA = \
    (0,0,0), (255,255,255), (255,0,0), (0,0,255), (0,255,0), (255,255,0), (0,255,255), (255,0,255)

# Formas de Tetris (Tetrominos)
PIEZAS = [
    [[1,1,1,1]],              # I
    [[1,1],[1,1]],            # O
    [[0,1,0],[1,1,1]],        # T
    [[1,0,0],[1,1,1]],        # J
    [[0,0,1],[1,1,1]],        # L
    [[1,1,0],[0,1,1]],        # S
    [[0,1,1],[1,1,0]]         # Z
]

COLORES = [ROJO, AZUL, VERDE, AMARILLO, CYAN, MAGENTA, BLANCO]

# Tablero vacío
tablero = [[0 for _ in range(COLUMNAS)] for _ in range(FILAS)]

# Puntos y fuente
puntos = 0
fuente_peque = pygame.font.SysFont(None, 30)

def game_over(puntos):
    fuente_grande = pygame.font.SysFont(None, 72)
    fuente_mediana = pygame.font.SysFont(None, 34)

    ventana.fill(NEGRO)
    texto_gameover = fuente_grande.render("GAME OVER", True, ROJO)
    texto_puntos = fuente_mediana.render(f"Puntaje final: {puntos}", True, BLANCO)
    texto_instr = fuente_mediana.render("Presiona cualquier tecla para salir", True, BLANCO)

    ventana.blit(texto_gameover, (ANCHO//2 - texto_gameover.get_width()//2, ALTO//2 - 100))
    ventana.blit(texto_puntos, (ANCHO//2 - texto_puntos.get_width()//2, ALTO//2))
    ventana.blit(texto_instr, (ANCHO//2 - texto_instr.get_width()//2, ALTO//2 + 80))

    pygame.display.flip()

    # Esperar a que el jugador presione una tecla
    esperando = True
    while esperando:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                esperando = False
    pygame.quit(); sys.exit()


def nueva_pieza():
    forma = random.choice(PIEZAS)
    color = random.choice(COLORES)
    return forma, color, COLUMNAS//2 - len(forma[0])//2, 0

def rotar(forma):
    return [list(fila) for fila in zip(*forma[::-1])]

def colision(forma, x, y):
    for fila in range(len(forma)):
        for col in range(len(forma[0])):
            if forma[fila][col]:
                nx, ny = x+col, y+fila
                if nx < 0 or nx >= COLUMNAS or ny >= FILAS:
                    return True
                if ny >= 0 and tablero[ny][nx]:
                    return True
    return False

def fijar(forma, color, x, y):
    for fila in range(len(forma)):
        for col in range(len(forma[0])):
            if forma[fila][col]:
                tablero[y+fila][x+col] = color

def limpiar_lineas():
    global tablero, puntos
    lineas = [fila for fila in tablero if any(c==0 for c in fila)]
    eliminadas = FILAS - len(lineas)
    puntos += eliminadas * 100   # 100 puntos por línea
    tablero = lineas
    while len(tablero) < FILAS:
        tablero.insert(0,[0 for _ in range(COLUMNAS)])

clock = pygame.time.Clock()
pieza, color, pos_x, pos_y = nueva_pieza()

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT and not colision(pieza,pos_x-1,pos_y):
                pos_x -= 1
            if e.key == pygame.K_RIGHT and not colision(pieza,pos_x+1,pos_y):
                pos_x += 1
            if e.key == pygame.K_DOWN and not colision(pieza,pos_x,pos_y+1):
                pos_y += 1
            if e.key == pygame.K_UP:
                # Hard drop
                while not colision(pieza,pos_x,pos_y+1):
                    pos_y += 1
            if e.key == pygame.K_SPACE:
                # Rotar pieza
                nueva = rotar(pieza)
                if not colision(nueva,pos_x,pos_y):
                    pieza = nueva

    # Caída automática
    if not colision(pieza,pos_x,pos_y+1):
        pos_y += 1
    else:
        fijar(pieza,color,pos_x,pos_y)
        limpiar_lineas()
        pieza,color,pos_x,pos_y = nueva_pieza()
        if colision(pieza,pos_x,pos_y):
            game_over(puntos)


    # Dibujar
    ventana.fill(NEGRO)
    # Tablero
    for fila in range(FILAS):
        for col in range(COLUMNAS):
            if tablero[fila][col]:
                pygame.draw.rect(ventana, tablero[fila][col],
                    (col*TAM_CASILLA, fila*TAM_CASILLA, TAM_CASILLA, TAM_CASILLA))
    # Pieza actual
    for fila in range(len(pieza)):
        for col in range(len(pieza[0])):
            if pieza[fila][col]:
                pygame.draw.rect(ventana, color,
                    ((pos_x+col)*TAM_CASILLA, (pos_y+fila)*TAM_CASILLA,
                     TAM_CASILLA, TAM_CASILLA))

    # Cuadrícula del tablero
    for fila in range(FILAS):
        for col in range(COLUMNAS):
            rect = pygame.Rect(col*TAM_CASILLA, fila*TAM_CASILLA, TAM_CASILLA, TAM_CASILLA)
            pygame.draw.rect(ventana, (40,40,40), rect, 1)  # gris tenue para la cuadrícula


    # HUD inferior
    pygame.draw.rect(ventana, NEGRO, (0, ALTO_JUEGO, ANCHO, 60))  # franja negra

    # Puntaje
    texto_puntos = fuente_peque.render(f"Puntos: {puntos}", True, BLANCO)
    ventana.blit(texto_puntos, (10, ALTO_JUEGO + 10))

    # Instrucciones
    texto_instr = fuente_peque.render("← → mover | ↑ hard drop | ↓ bajar | Espacio rotar", True, BLANCO)
    ventana.blit(texto_instr, (10, ALTO_JUEGO + 30))

    pygame.display.flip()
    clock.tick(5)  # velocidad de caída

