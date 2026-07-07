import pygame, random, sys

pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Barman Malote")

font = pygame.font.SysFont("Arial", 24)
WHITE, BLACK, GREEN, RED, GRAY = (255,255,255), (0,0,0), (0,200,0), (200,0,0), (180,180,180)

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

# Teclas para ingredientes
mapa_teclas = {
    pygame.K_a: "Ginebra",
    pygame.K_q: "Hielo",
    pygame.K_w: "Vermouth",
    pygame.K_s: "Tequila",
    pygame.K_e: "Limón",
    pygame.K_d: "Cerveza"
}
# Etiquetas visibles
etiquetas_teclas = {
    "Ginebra": "A",
    "Hielo": "Q",
    "Vermouth": "W",
    "Tequila": "S",
    "Limón": "E",
    "Cerveza": "D"
}

def mostrar_texto(texto, x, y, color=BLACK):
    render = font.render(texto, True, color)
    screen.blit(render, (x, y))

def atender_cliente():
    global rupias, seleccion, cliente_actual, bebida_actual, mensaje_feedback
    receta = bebidas[bebida_actual]
    if sorted(seleccion) == sorted(receta):  # mezcla correcta
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
    global proveedor_activo
    if not proveedor_activo and random.randint(1, 20) == 1:  # 5% probabilidad
        proveedor_activo = random.choice(proveedores)

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
    screen.fill(WHITE)
    evento_proveedor()

    # HUD superior
    mostrar_texto(f"Rupias: {rupias}", 50, 20)

    # Inventario con teclas
    mostrar_texto("Inventario:", 650, 20)
    y_inv = 50
    for ing, cant in ingredientes.items():
        mostrar_texto(f"{etiquetas_teclas[ing]} - {ing}: {cant}", 650, y_inv)
        y_inv += 25

    # Recetario a la izquierda
    mostrar_texto("Recetario (I/O/P):", 50, 60)
    if receta_visible:
        y_rec = 90
        mostrar_texto(f"{receta_visible} lleva:", 50, y_rec)
        for ing in bebidas[receta_visible]:
            y_rec += 25
            mostrar_texto(f"- {ing}", 70, y_rec)

    # Cliente y pedido
    mostrar_texto(f"{cliente_actual} pide un {bebida_actual}", 50, 300)
    mostrar_texto("Seleccionados: " + ", ".join(seleccion), 50, 340)

    # Feedback
    if mensaje_feedback == "bien":
        mostrar_texto("¡Cliente feliz! ", 50, 380, GREEN)
    elif mensaje_feedback == "mal":
        mostrar_texto("Cliente molesto", 50, 380, RED)
    elif mensaje_feedback:
        mostrar_texto(mensaje_feedback, 50, 380, GRAY)

    # Proveedor
    if proveedor_activo:
        mostrar_texto(f"Proveedor: {proveedor_activo} (Z=aceptar / X=rechazar)", 50, 500, GREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # Selección de ingredientes
            if event.key in mapa_teclas:
                ing = mapa_teclas[event.key]
                if ingredientes[ing] > 0:
                    seleccion.append(ing)
            # Mezclar y servir
            if event.key == pygame.K_m:
                atender_cliente()
            # Recetario
            if event.key == pygame.K_i:
                receta_visible = "Martini"
            elif event.key == pygame.K_o:
                receta_visible = "Margarita"
            elif event.key == pygame.K_p:
                receta_visible = "Cerveza"
            # Proveedor
            if event.key == pygame.K_z:
                aceptar_proveedor()
            elif event.key == pygame.K_x:
                rechazar_proveedor()

    pygame.display.flip()
