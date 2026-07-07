import pygame
import random
import sys

pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Barman Malote")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fuente
font = pygame.font.SysFont("Arial", 24)

# Ingredientes y teclas
ingredientes = {
    "Ginebra": pygame.K_a,
    "Hielo": pygame.K_q,
    "Vermouth": pygame.K_w,
    "Tequila": pygame.K_s,
    "Limón": pygame.K_e,
    "Cerveza": pygame.K_d
}

# Recetas
recetas = {
    "Martini": ["Ginebra", "Vermouth"],
    "Margarita": ["Tequila", "Limón"],
    "Cerveza": ["Cerveza"]
}

# Clientes
clientes = ["Juan", "María", "Pedro", "Lucía"]

# Estado del juego
seleccion = []
cliente_actual = random.choice(clientes)
bebida_actual = random.choice(list(recetas.keys()))

def mostrar_texto(texto, x, y):
    render = font.render(texto, True, BLACK)
    screen.blit(render, (x, y))

# Loop principal
running = True
while running:
    screen.fill(WHITE)

    # Mostrar cliente y bebida
    mostrar_texto(f"{cliente_actual} pide un {bebida_actual}", 50, 50)
    mostrar_texto("Ingredientes seleccionados: " + ", ".join(seleccion), 50, 100)

    # Mostrar anaquel
    y_pos = 200
    for ing, tecla in ingredientes.items():
        mostrar_texto(f"{ing} ({pygame.key.name(tecla).upper()})", 50, y_pos)
        y_pos += 40

    mostrar_texto("Presiona M para mezclar y servir", 50, y_pos + 40)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # Selección de ingredientes
            for ing, tecla in ingredientes.items():
                if event.key == tecla:
                    seleccion.append(ing)
            # Mezclar
            if event.key == pygame.K_m:
                if seleccion == recetas[bebida_actual]:
                    print("¡Cliente feliz! 🍹")
                else:
                    print("Cliente molesto 😡")
                # Reiniciar turno
                seleccion = []
                cliente_actual = random.choice(clientes)
                bebida_actual = random.choice(list(recetas.keys()))

    pygame.display.flip()
