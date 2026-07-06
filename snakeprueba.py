import pygame
import random

pygame.init()

# Dimensiones de la ventana
ancho = 800
alto = 600
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Snake Game con Selector de Skins")

# Fondo dentro de carpeta sprites
fondo = pygame.image.load("sprites/fondo.png").convert()
fondo = pygame.transform.scale(fondo, (ancho, alto))

# Sonidos
sonido_comer = pygame.mixer.Sound("sprites/comer.mp3")
sonido_bomba = pygame.mixer.Sound("sprites/boom.mp3")
sonido_gameover = pygame.mixer.Sound("sprites/gameover.mp3")

# Música de fondo (loop infinito)
pygame.mixer.music.load("sprites/Musica_de_fondo.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

# Colores
negro = (0, 0, 0)
rojo = (213, 50, 80)

# Configuración de la serpiente
snake_block = 30
snake_velocidad = 10

clock = pygame.time.Clock()
font = pygame.font.SysFont("bahnschrift", 25)

def puntuacion(score):
    valor = font.render("Puntos: " + str(score), True, negro)
    ventana.blit(valor, [0, 0])

def mensaje(msg, color):
    texto = font.render(msg, True, color)
    sombra = font.render(msg, True, (0,0,0))
    ventana.blit(sombra, [ancho/6+2, alto/3+2])
    ventana.blit(texto, [ancho/6, alto/3])

def seleccionar_skin():
    ventana.blit(fondo, (0, 0))
    mensaje("Elige tu víbora: 1-Roja, 2-Azul, 3-Verde, 4-Amarilla", (255,255,0))
    pygame.display.update()
    skin = "roja"
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    skin = "roja"; esperando = False
                elif evento.key == pygame.K_2:
                    skin = "azul"; esperando = False
                elif evento.key == pygame.K_3:
                    skin = "verde"; esperando = False
                elif evento.key == pygame.K_4:
                    skin = "amarilla"; esperando = False
    return skin

def juego():
    game_over = False
    game_close = False
    snake_velocidad = 10

    # Selección de skin
    skin = seleccionar_skin()
    sprite_cabeza = pygame.transform.scale(pygame.image.load(f"sprites/cabeza_{skin}.png").convert_alpha(), (snake_block, snake_block))
    sprite_cuerpo = pygame.transform.scale(pygame.image.load(f"sprites/cuerpo_{skin}.png").convert_alpha(), (snake_block, snake_block))
    sprite_cola   = pygame.transform.scale(pygame.image.load(f"sprites/cola_{skin}.png").convert_alpha(), (snake_block, snake_block))
    sprite_comida = pygame.transform.scale(pygame.image.load("sprites/manzana.png").convert_alpha(), (snake_block, snake_block))
    sprite_bomba = pygame.transform.scale(pygame.image.load("sprites/bomba.png").convert_alpha(), (snake_block, snake_block))
    sprite_naranja = pygame.transform.scale(pygame.image.load("sprites/naranja.png").convert_alpha(), (snake_block, snake_block))
    sprite_uva = pygame.transform.scale(pygame.image.load("sprites/uva.png").convert_alpha(), (snake_block, snake_block))

    x1 = ancho / 2
    y1 = alto / 2
    x1_cambio = 0
    y1_cambio = 0
    direccion = "RIGHT"

    snake_lista = []
    snake_longitud = 1
    score = 0

    # Posiciones iniciales
    comida_x = round(random.randrange(0, ancho - snake_block) / snake_block) * snake_block
    comida_y = round(random.randrange(0, alto - snake_block) / snake_block) * snake_block
    bomba_x = round(random.randrange(0, ancho - snake_block) / snake_block) * snake_block
    bomba_y = round(random.randrange(0, alto - snake_block) / snake_block) * snake_block
    naranja_x = round(random.randrange(0, ancho - snake_block) / snake_block) * snake_block
    naranja_y = round(random.randrange(0, alto - snake_block) / snake_block) * snake_block
    uva_x = round(random.randrange(0, ancho - snake_block) / snake_block) * snake_block
    uva_y = round(random.randrange(0, alto - snake_block) / snake_block) * snake_block

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
                    x1_cambio = -snake_block; y1_cambio = 0; direccion = "LEFT"
                elif evento.key == pygame.K_RIGHT:
                    x1_cambio = snake_block; y1_cambio = 0; direccion = "RIGHT"
                elif evento.key == pygame.K_UP:
                    y1_cambio = -snake_block; x1_cambio = 0; direccion = "UP"
                elif evento.key == pygame.K_DOWN:
                    y1_cambio = snake_block; x1_cambio = 0; direccion = "DOWN"

        if x1 >= ancho or x1 < 0 or y1 >= alto or y1 < 0:
            game_close = True

        x1 += x1_cambio
        y1 += y1_cambio
        ventana.blit(fondo, (0, 0))
        ventana.blit(sprite_comida, (comida_x, comida_y))
        ventana.blit(sprite_bomba, (bomba_x, bomba_y))
        ventana.blit(sprite_naranja, (naranja_x, naranja_y))
        ventana.blit(sprite_uva, (uva_x, uva_y))

        snake_cabeza = [x1, y1]
        snake_lista.append(snake_cabeza)
        if len(snake_lista) > snake_longitud:
            del snake_lista[0]

        for x in snake_lista[:-1]:
            if x == snake_cabeza:
                game_close = True

        # Dibujar serpiente
        for i, bloque in enumerate(snake_lista):
            if i == len(snake_lista) - 1:   # cabeza
                if direccion == "RIGHT":
                    cabeza_rotada = pygame.transform.rotate(sprite_cabeza, 0)
                elif direccion == "LEFT":
                    cabeza_rotada = pygame.transform.rotate(sprite_cabeza, 180)
                elif direccion == "UP":
                    cabeza_rotada = pygame.transform.rotate(sprite_cabeza, 90)
                elif direccion == "DOWN":
                    cabeza_rotada = pygame.transform.rotate(sprite_cabeza, 270)
                ventana.blit(cabeza_rotada, (bloque[0], bloque[1]))
            elif i == 0:   # cola
                ventana.blit(sprite_cola, (bloque[0], bloque[1]))
            else:
                ventana.blit(sprite_cuerpo, (bloque[0], bloque[1]))

        puntuacion(score)
        pygame.display.update()

        # Colisiones
        rect_cabeza = pygame.Rect(x1, y1, snake_block, snake_block)

        if rect_cabeza.colliderect(pygame.Rect(comida_x, comida_y, snake_block, snake_block)):
            sonido_comer.play(maxtime=200)
            comida_x = round(random.randrange(0, ancho - snake_block) / snake_block) * snake_block
            comida_y = round(random.randrange(0, alto - snake_block) / snake_block) * snake_block
            snake_longitud += 1
            score += 10
            if score % 50 == 0:
                snake_velocidad += 2

        if rect_cabeza.colliderect(pygame.Rect(naranja_x, naranja_y, snake_block, snake_block)):
            sonido_comer.play(maxtime=200)
            naranja_x = round(random.randrange(0, ancho - snake_block) / snake_block) * snake_block
            naranja_y = round(random.randrange(0, alto - snake_block) / snake_block) * snake_block
            snake_longitud += 1
            score += 30

        if rect_cabeza.colliderect(pygame.Rect(uva_x, uva_y, snake_block, snake_block)):
            sonido_comer.play(maxtime=200)
            uva_x = round(random.randrange(0, ancho - snake_block) / snake_block) * snake_block
            uva_y = round(random.randrange(0, alto - snake_block) / snake_block) * snake_block
            snake_longitud += 1
            score += 50

        if rect_cabeza.colliderect(pygame.Rect(bomba_x, bomba_y, snake_block, snake_block)):
            sonido_bomba.play(maxtime=400)
            sonido_gameover.play(maxtime=800)
            game_close = True

        clock.tick(snake_velocidad)

    pygame.quit()
    quit()

# Llamada principal
if __name__ == "__main__":
    juego()
