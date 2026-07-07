import pygame, random, sys

pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Barman Malote")

font = pygame.font.SysFont("Arial", 20)
BLACK, WHITE, GREEN, RED, GRAY = (0,0,0), (255,255,255), (0,200,0), (200,0,0), (180,180,180)

# Estado inicial
rupias = 50
ingredientes = {"Ginebra": 5, "Hielo": 10, "Vermouth": 4, "Tequila": 6, "Limón": 8, "Cerveza": 12}
bebidas = {
    "Martini": ["Ginebra", "Vermouth"],
    "Margarita": ["Tequila", "Limón"],
    "Cerveza": ["Cerveza"]
}
clientes = ["Juan", "María", "Pedro", "Lucía"]
proveedores = ["Carlos el Distribuidor", "Mina la Proveedora"]

seleccion = []
cliente_actual = random.choice(clientes)
bebida_actual = random.choice(list(bebidas.keys()))
mensaje_feedback = ""
proveedor_activo = None
receta_visible = None

# Temporizador de proveedores
ultimo_proveedor = pygame.time.get_ticks()
intervalo_proveedor = 10000  # cada 10 segundos

# Cargar sprites
ruta = "C:\\python\\barman\\Sprite\\"
barman_sprite = pygame.image.load(ruta + "barman.png")
barman_sprite = pygame.transform.scale(barman_sprite, (300, 330))  # más grande

rupia_sprite = pygame.image.load(ruta + "rupia.png")
rupia_sprite = pygame.transform.scale(rupia_sprite, (32, 32))

# Sprites de bebidas e ingredientes
sprites = {
    "Martini": pygame.image.load(ruta + "martini.png"),
    "Margarita": pygame.image.load(ruta + "margarita.png"),
    "Cerveza": pygame.image.load(ruta + "cerveza.png"),
    "Ginebra": pygame.image.load(ruta + "ginebra.png"),
    "Vermouth": pygame.image.load(ruta + "vermouth.png"),
    "Tequila": pygame.image.load(ruta + "tequila.png"),
    "Limón": pygame.image.load(ruta + "limon.png"),
    "Hielo": pygame.image.load(ruta + "hielo.png"),
}

# Escalar todos los sprites a tamaño más pequeño
for k in sprites:
    sprites[k] = pygame.transform.scale(sprites[k], (70, 70))

# Teclas para ingredientes
mapa_teclas = {
    pygame.K_a: "Ginebra",
    pygame.K_q: "Hielo",
    pygame.K_w: "Vermouth",
    pygame.K_s: "Tequila",
    pygame.K_e: "Limón",
    pygame.K_d: "Cerveza"
}
etiquetas_teclas = {
    "Ginebra": "A Ginebra",
    "Hielo": "Q Hielo",
    "Vermouth": "W Vermouth",
    "Tequila": "S Tequila",
    "Limón": "E Limón",
    "Cerveza": "D Cerveza"
}

def mostrar_texto(texto, x, y, color=WHITE):
    render = font.render(texto, True, color)
    screen.blit(render, (x, y))

def atender_cliente():
    global rupias, seleccion, cliente_actual, bebida_actual, mensaje_feedback
    receta = bebidas[bebida_actual]
    if sorted(seleccion) == sorted(receta):
        mensaje_feedback = "bien"
        rupias += 10
        for ing in receta:
            ingredientes[ing] -= 1
    else:
        mensaje_feedback = "mal"
        rupias -= 10
    seleccion.clear()
    cliente_actual = random.choice(clientes)
    bebida_actual = random.choice(list(bebidas.keys()))

def evento_proveedor():
    global proveedor_activo, ultimo_proveedor
    tiempo_actual = pygame.time.get_ticks()
    if not proveedor_activo and tiempo_actual - ultimo_proveedor >= intervalo_proveedor:
        proveedor_activo = random.choice(proveedores)
        ultimo_proveedor = tiempo_actual

def aceptar_proveedor():
    global proveedor_activo, ingredientes, rupias, mensaje_feedback
    if proveedor_activo and rupias >= 15:
        mensaje_feedback = f"Compraste ingredientes de {proveedor_activo}"
        rupias -= 15
        for ing in ingredientes:
            ingredientes[ing] += random.randint(1, 3)
        proveedor_activo = None

def rechazar_proveedor():
    global proveedor_activo, mensaje_feedback
    if proveedor_activo:
        mensaje_feedback = f"Rechazaste a {proveedor_activo}"
        proveedor_activo = None

# Loop principal
running = True
while running:
    screen.fill(BLACK)
    evento_proveedor()

    # Barman en el centro
    screen.blit(barman_sprite, (WIDTH//2 - 150, HEIGHT//2 - 165))

    # Rupia y contador
    screen.blit(rupia_sprite, (50, 20))
    mostrar_texto(str(rupias), 90, 20)

    # Inventario en dos columnas
    mostrar_texto("Inventario:", 580, 20)
    y_inv = 50
    col = 0
    for idx, (ing, cant) in enumerate(ingredientes.items()):
        x_pos = 630 + (col * 120)  # segunda columna desplazada
        screen.blit(sprites[ing], (x_pos, y_inv))
        mostrar_texto(f"{etiquetas_teclas[ing]}-{cant}", x_pos, y_inv + 75)
        col += 1
        if col > 1:  # dos columnas
            col = 0
            y_inv += 120

    # Recetario
    mostrar_texto("Recetario (I/O/P):", 50, 60)
    if receta_visible:
        y_rec = 90
        mostrar_texto(f"{receta_visible} lleva:", 50, y_rec)
        screen.blit(sprites[receta_visible], (50, y_rec + 30))
        y_rec += 120
        for ing in bebidas[receta_visible]:
            mostrar_texto(f"- {ing}", 70, y_rec)
            y_rec += 25

    # Cliente
    mostrar_texto(f"{cliente_actual} pide un {bebida_actual}", 50, 300)
    mostrar_texto("Seleccionados: " + ", ".join(seleccion), 50, 340)

    # Feedback
    if mensaje_feedback == "bien":
        mostrar_texto("¡Cliente feliz! 🍹", 50, 380, GREEN)
    elif mensaje_feedback == "mal":
        mostrar_texto("Cliente molesto 😡", 50, 380, RED)
    elif mensaje_feedback:
        mostrar_texto(mensaje_feedback, 50, 380, GRAY)

    # Proveedor
    if proveedor_activo:
        mostrar_texto(f"Proveedor: {proveedor_activo} (Z=aceptar / X=rechazar)", 50, 600, GREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key in mapa_teclas:
                ing = mapa_teclas[event.key]
                if ingredientes[ing] > 0:
                    seleccion.append(ing)
            if event.key == pygame.K_m:
                atender_cliente()
            if event.key == pygame.K_i:
                receta_visible = "Martini"
            elif event.key == pygame.K_o:
                receta_visible = "Margarita"
            elif event.key == pygame.K_p:
                receta_visible = "Cerveza"
            if event.key == pygame.K_z:
                aceptar_proveedor()
            elif event.key == pygame.K_x:
                rechazar_proveedor()

    pygame.display.flip()
