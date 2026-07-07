import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

ANCHO, ALTO = 800, 600
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mercado de Hyrule")

# Cargar sprites
fondo = pygame.image.load("Sprite/fondo_tienda.png")
mostrador = pygame.image.load("Sprite/mostrador.png")
vendedor = pygame.image.load("Sprite/vendedor_goron.png")
inventario = pygame.image.load("Sprite/inventario_items.png")

# Escalar
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
mostrador = pygame.transform.scale(mostrador, (800, 200))
vendedor = pygame.transform.scale(vendedor, (200, 200))
inventario = pygame.transform.scale(inventario, (400, 150))

# Fuente
fuente = pygame.font.Font(None, 22)

# Precios iniciales
precios = {
    "pocion": 20,
    "flechas": 8,
    "bombas": 12,
    "escudo": 30
}

# Inventario del jugador
inventario_jugador = {"rupias": 100, "pocion": 0, "flechas": 0, "bombas": 0, "escudo": 0}

# Eventos aleatorios
eventos = [
    ("Festival Kokiri 🎉", {"pocion": -5}),
    ("Guerra en Gerudo ⚔️", {"bombas": +10}),
    ("Escasez de flechas 🏹", {"flechas": +7}),
    ("Visita real 👑", {"pocion": +8, "bombas": +5})
]

# Frases del vendedor
frases_vendedor = [
    "¡Bienvenido viajero, mira mis artículos!",
    "Las bombas están muy solicitadas hoy…",
    "Dicen que habrá un festival Kokiri pronto.",
    "Las flechas escasean, mejor compra ahora."
]

def evento_aleatorio():
    nombre, efecto = random.choice(eventos)
    for item, cambio in efecto.items():
        precios[item] = max(1, precios[item] + cambio)
    return nombre

def hablar_con_vendedor():
    return random.choice(frases_vendedor)

# Rectángulos de colisión para ítems
pocion_rect = pygame.Rect(300, 320, 80, 80)
flechas_rect = pygame.Rect(350, 320, 80, 80)
bombas_rect = pygame.Rect(500, 320, 80, 80)
escudo_rect = pygame.Rect(650, 320, 80, 80)
vendedor_rect = pygame.Rect(100, 200, 200, 200)

# Variables de juego
evento_texto = ""
dia = 1

# Bucle principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Pasar de día con tecla ESPACIO
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dia += 1
                evento_texto = evento_aleatorio()

        # Clic izquierdo: comprar o hablar
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if vendedor_rect.collidepoint(event.pos):
                evento_texto = hablar_con_vendedor()
            elif pocion_rect.collidepoint(event.pos):
                costo = precios["pocion"]
                if inventario_jugador["rupias"] >= costo:
                    inventario_jugador["rupias"] -= costo
                    inventario_jugador["pocion"] += 1
                    evento_texto = "Compraste una poción."
                else:
                    evento_texto = "No tienes suficientes rupias."
            elif flechas_rect.collidepoint(event.pos):
                costo = precios["flechas"]
                if inventario_jugador["rupias"] >= costo:
                    inventario_jugador["rupias"] -= costo
                    inventario_jugador["flechas"] += 1
                    evento_texto = "Compraste flechas."
                else:
                    evento_texto = "No tienes suficientes rupias."
            elif bombas_rect.collidepoint(event.pos):
                costo = precios["bombas"]
                if inventario_jugador["rupias"] >= costo:
                    inventario_jugador["rupias"] -= costo
                    inventario_jugador["bombas"] += 1
                    evento_texto = "Compraste una bomba."
                else:
                    evento_texto = "No tienes suficientes rupias."
            elif escudo_rect.collidepoint(event.pos):
                costo = precios["escudo"]
                if inventario_jugador["rupias"] >= costo:
                    inventario_jugador["rupias"] -= costo
                    inventario_jugador["escudo"] += 1
                    evento_texto = "Compraste un escudo."
                else:
                    evento_texto = "No tienes suficientes rupias."

        # Clic derecho: vender
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if pocion_rect.collidepoint(event.pos) and inventario_jugador["pocion"] > 0:
                inventario_jugador["pocion"] -= 1
                inventario_jugador["rupias"] += precios["pocion"]
                evento_texto = "Vendiste una poción."
            elif flechas_rect.collidepoint(event.pos) and inventario_jugador["flechas"] > 0:
                inventario_jugador["flechas"] -= 1
                inventario_jugador["rupias"] += precios["flechas"]
                evento_texto = "Vendiste flechas."
            elif bombas_rect.collidepoint(event.pos) and inventario_jugador["bombas"] > 0:
                inventario_jugador["bombas"] -= 1
                inventario_jugador["rupias"] += precios["bombas"]
                evento_texto = "Vendiste una bomba."
            elif escudo_rect.collidepoint(event.pos) and inventario_jugador["escudo"] > 0:
                inventario_jugador["escudo"] -= 1
                inventario_jugador["rupias"] += precios["escudo"]
                evento_texto = "Vendiste un escudo."
            else:
                evento_texto = "No tienes suficientes objetos para vender."

    # Dibujar elementos
    screen.blit(fondo, (0, 0))
    screen.blit(mostrador, (0, 375))
    screen.blit(vendedor, (100, 200))
    screen.blit(inventario, (300, 280))

    # Texto del vendedor
    texto = fuente.render("¡Bienvenido al Mercado de Hyrule!", True, (255, 255, 255))
    screen.blit(texto, (200, 100))

    # Precios dinámicos
    screen.blit(fuente.render(f"Poción: {precios['pocion']}$", True, (255, 255, 0)), (300, 440))
    screen.blit(fuente.render(f"Flechas: {precios['flechas']}$", True, (255, 255, 0)), (395, 440))
    screen.blit(fuente.render(f"Bombas: {precios['bombas']}$", True, (255, 255, 0)), (500, 440))
    screen.blit(fuente.render(f"Escudo: {precios['escudo']}$", True, (255, 255, 0)), (600, 440))

    # Inventario del jugador
    texto_inv = fuente.render(
        f"Rupias: {inventario_jugador['rupias']} | Pociones: {inventario_jugador['pocion']} | Flechas: {inventario_jugador['flechas']} | Bombas: {inventario_jugador['bombas']} | Escudos: {inventario_jugador['escudo']}",
        True, (255,255,255))
    screen.blit(texto_inv, (100, 500))

    # Mostrar evento o diálogo
    if evento_texto:
        evento_msg = fuente.render(f"Día {dia}: {evento_texto}", True, (0, 255, 0))
        screen.blit(evento_msg, (200, 150))

    # Instrucciones
    instr = fuente.render("Pulsa ESPACIO para pasar de día", True, (200,200,200))
    screen.blit(instr, (200, 560))

    pygame.display.flip()

