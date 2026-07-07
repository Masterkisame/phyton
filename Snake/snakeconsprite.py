import pygame
import random

pygame.init()

# Dimensiones de la ventana
ancho = 600
alto = 400
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Snake Game con Sprites")

# Colores
blanco = (255, 255, 255)
negro = (0, 0, 0)
rojo = (213, 50, 80)

# Configuración de la serpiente
snake_block = 20
snake_velocidad = 10

clock = pygame.time.Clock()
font = pygame.font.SysFont("bahnschrift", 25)

# Cargar sprites
sprite_cabeza = pygame.image.load("cabeza.png").convert_alpha()
sprite_cabeza = pygame.transform.scale(sprite_cabeza, (snake_block, snake_block))

sprite_cuerpo = pygame.image.load("cuerpo.png").convert_alpha()
sprite_cuerpo = pygame.transform.scale(sprite_cuerpo, (snake_block, snake_block))

sprite_cola = pygame.image.load("cola.png").convert_alpha()
sprite_cola = pygame.transform.scale(sprite_cola, (snake_block, snake_block))

sprite_comida = pygame.image.load("manzana.png").convert_alpha()
sprite_comida = pygame.transform.scale(sprite_comida, (snake_block, snake_block))

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

    comida_x = round(random.randrange(0, ancho - snake_block) / 20.0) * 20.0
    comida_y = round(random.randrange(0, alto - snake_block) / 20.0) * 20.0

    while not game_over:
        while game_close:
            ventana.fill(blanco)
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
        ventana.fill(blanco)
        ventana.blit(sprite_comida, (comida_x, comida_y))

        snake_cabeza = [x1, y1]
        snake_lista.append(snake_cabeza)
        if len(snake_lista) > snake_longitud:
            del snake_lista[0]

        for x in snake_lista[:-1]:
            if x == snake_cabeza:
                game_close = True

        # Dibujar serpiente con sprites
        for i, bloque in enumerate(snake_lista):
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

        if x1 == comida_x and y1 == comida_y:
            comida_x = round(random.randrange(0, ancho - snake_block) / 20.0) * 20.0
            comida_y = round(random.randrange(0, alto - snake_block) / 20.0) * 20.0
            snake_longitud += 1
            score += 10
            if score % 50 == 0:
                snake_velocidad += 2

        clock.tick(snake_velocidad)

    pygame.quit()
    quit()

juego()


