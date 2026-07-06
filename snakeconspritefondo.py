import pygame
import random

pygame.init()

# Dimensiones de la ventana
ancho = 800
alto = 600
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Snake Game con Sprites")

fondo = pygame.image.load("fondo.png").convert()
fondo = pygame.transform.scale(fondo, (ancho, alto))

# Colores
negro = (0, 0, 0)
rojo = (213, 50, 80)

# Configuración de la serpiente
snake_block = 40   # tamaño aumentado
snake_velocidad = 10

clock = pygame.time.Clock()
font = pygame.font.SysFont("bahnschrift", 25)

# Cargar sprites escalados al nuevo tamaño
sprite_cabeza = pygame.transform.scale(pygame.image.load("cabeza.png").convert_alpha(), (snake_block, snake_block))
sprite_cuerpo = pygame.transform.scale(pygame.image.load("cuerpo.png").convert_alpha(), (snake_block, snake_block))
sprite_cola   = pygame.transform.scale(pygame.image.load("cola.png").convert_alpha(), (snake_block, snake_block))
sprite_comida = pygame.transform.scale(pygame.image.load("manzana.png").convert_alpha(), (snake_block, snake_block))

def puntuacion(score):
    valor = font.render("Puntos: " + str(score), True, negro)
    ventana.blit(valor, [0, 0])

def mensaje(msg, color):
    texto = font.render(msg, True, color)
    ventana.blit(texto, [ancho / 6, alto / 3])

def juego():
    game_over = False
    game_close = False
    snake_velocidad = 10

    x1 = ancho / 2
    y1 = alto / 2
    x1_cambio = 0
    y1_cambio = 0
    direccion = "RIGHT"

    snake_lista = []
    snake_longitud = 1
    score = 0

    comida_x = round(random.randrange(0, ancho - snake_block) / snake_block) * snake_block
    comida_y = round(random.randrange(0, alto - snake_block) / snake_block) * snake_block

    while not game_over:
        while game_close:
            ventana.blit(fondo, (0, 0))
            mensaje("Perdiste! Q para salir, C para jugar otra vez", rojo)
            pygame.display.update()

            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if evento.key == pygame.K_c:
                        juego()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                game_over = True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    x1_cambio = -snake_block
                    y1_cambio = 0
                    direccion = "LEFT"
                elif evento.key == pygame.K_RIGHT:
                    x1_cambio = snake_block
                    y1_cambio = 0
                    direccion = "RIGHT"
                elif evento.key == pygame.K_UP:
                    y1_cambio = -snake_block
                    x1_cambio = 0
                    direccion = "UP"
                elif evento.key == pygame.K_DOWN:
                    y1_cambio = snake_block
                    x1_cambio = 0
                    direccion = "DOWN"

        if x1 >= ancho or x1 < 0 or y1 >= alto or y1 < 0:
            game_close = True

        x1 += x1_cambio
        y1 += y1_cambio
        ventana.blit(fondo, (0, 0))
        ventana.blit(sprite_comida, (comida_x, comida_y))

        snake_cabeza = [x1, y1]
        snake_lista.append(snake_cabeza)
        if len(snake_lista) > snake_longitud:
            del snake_lista[0]

        for x in snake_lista[:-1]:
            if x == snake_cabeza:
                game_close = True

        # Dibujar serpiente con sprites + halo suave
        for i, bloque in enumerate(snake_lista):
            # sombra circular translúcida
            sombra = pygame.Surface((snake_block*2, snake_block*2), pygame.SRCALPHA)
            pygame.draw.circle(sombra, (0, 0, 0, 80), (snake_block, snake_block), snake_block)
            ventana.blit(sombra, (bloque[0]-snake_block//2, bloque[1]-snake_block//2))

            if i == len(snake_lista) - 1:   # último = cabeza
                if direccion == "RIGHT":
                    cabeza_rotada = pygame.transform.rotate(sprite_cabeza, 0)
                elif direccion == "LEFT":
                    cabeza_rotada = pygame.transform.rotate(sprite_cabeza, 180)
                elif direccion == "UP":
                    cabeza_rotada = pygame.transform.rotate(sprite_cabeza, 90)
                elif direccion == "DOWN":
                    cabeza_rotada = pygame.transform.rotate(sprite_cabeza, 270)
                ventana.blit(cabeza_rotada, (bloque[0], bloque[1]))
            elif i == 0:   # primero = cola
                ventana.blit(sprite_cola, (bloque[0], bloque[1]))
            else:
                ventana.blit(sprite_cuerpo, (bloque[0], bloque[1]))

        puntuacion(score)
        pygame.display.update()

        # Colisión más natural con la manzana
        rect_cabeza = pygame.Rect(x1, y1, snake_block, snake_block)
        rect_comida = pygame.Rect(comida_x, comida_y, snake_block, snake_block)
        if rect_cabeza.colliderect(rect_comida):
            comida_x = round(random.randrange(0, ancho - snake_block) / snake_block) * snake_block
            comida_y = round(random.randrange(0, alto - snake_block) / snake_block) * snake_block
            snake_longitud += 1
            score += 10
            if score % 50 == 0:
                snake_velocidad += 2

        clock.tick(snake_velocidad)

    pygame.quit()
    quit()

juego()
