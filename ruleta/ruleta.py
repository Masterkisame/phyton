import pygame, sys, random, math

pygame.init()
W, H = 800, 600
screen = pygame.display.set_mode((W,H))
pygame.display.set_caption("Ruleta Dinámica con Tabla")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

colores = ["rojo","azul","verde","amarillo","morado"]
rgb = {"rojo":(255,0,0),"azul":(0,0,255),"verde":(0,255,0),
       "amarillo":(255,255,0),"morado":(150,0,150)}

probabilidades = {"rojo":3,"azul":3,"verde":3,"amarillo":3,"morado":1}
multiplicadores = {"rojo":2,"azul":2,"verde":2,"amarillo":2,"morado":88}

apuesta_color = "rojo"
apuesta = 10
saldo = 100
resultado = None
fase = "menu"
ronda = 1
angulo = 0
velocidad = 0

def girar_ruleta():
    lista = []
    for c,p in probabilidades.items():
        lista += [c]*p
    return random.choice(lista)

def actualizar_probabilidades():
    global probabilidades, multiplicadores, ronda
    ronda += 1
    for c in probabilidades:
        cambio = random.choice([-1,0,1])
        prob = max(1, probabilidades[c]+cambio)
        probabilidades[c] = prob
    total = sum(probabilidades.values())
    for c in colores:
        multiplicadores[c] = max(2, int(total/probabilidades[c]))

def dibujar_ruleta():
    centro = (W//2,H//2)
    radio = 200
    start_angle = angulo
    for i,c in enumerate(colores):
        end_angle = start_angle + (360/len(colores))
        pygame.draw.polygon(screen,rgb[c],[
            centro,
            (centro[0]+radio*math.cos(math.radians(start_angle)),
             centro[1]+radio*math.sin(math.radians(start_angle))),
            (centro[0]+radio*math.cos(math.radians(end_angle)),
             centro[1]+radio*math.sin(math.radians(end_angle)))
        ])
        start_angle = end_angle
    # flecha arriba
    pygame.draw.polygon(screen,(255,255,255),[(W//2,H//2-220),(W//2-20,H//2-260),(W//2+20,H//2-260)])

def dibujar_tabla():
    x,y = W-200,20
    for i,c in enumerate(colores):
        pygame.draw.rect(screen,rgb[c],(x,y+i*40,30,30))
        mult_txt = font.render(f"x{multiplicadores[c]}",True,(255,255,255))
        screen.blit(mult_txt,(x+40,y+i*40))
        if c == apuesta_color:
            pygame.draw.circle(screen,(255,255,255),(x-20,y+i*40+15),10)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: sys.exit()
        if fase == "menu" and e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RIGHT:
                idx = colores.index(apuesta_color)
                apuesta_color = colores[(idx+1)%len(colores)]
            if e.key == pygame.K_LEFT:
                idx = colores.index(apuesta_color)
                apuesta_color = colores[(idx-1)%len(colores)]
            if e.key == pygame.K_RETURN and apuesta > 0:
                saldo -= apuesta
                velocidad = random.randint(20,30)
                fase = "girando"
        if fase == "resultado" and e.type == pygame.KEYDOWN:
            if e.key == pygame.K_v:
                actualizar_probabilidades()
                fase = "menu"
            if e.key == pygame.K_c: sys.exit()

    screen.fill((0,0,0))

    if fase == "menu":
        msg = font.render(f"Saldo: {saldo} rupias", True, (255,255,255))
        screen.blit(msg,(20,20))
        txt = font.render(f"Apuesta: {apuesta} en {apuesta_color.upper()}", True, (255,255,0))
        screen.blit(txt,(20,60))
        instr = font.render("← → para elegir color, ENTER para girar", True, (200,200,200))
        screen.blit(instr,(20,100))
        ronda_txt = font.render(f"Ronda {ronda}", True, (0,255,255))
        screen.blit(ronda_txt,(20,140))
        dibujar_tabla()

    elif fase == "girando":
        angulo += velocidad
        velocidad = max(velocidad-0.2,0)
        dibujar_ruleta()
        dibujar_tabla()
        if velocidad <= 0.1:
            resultado = girar_ruleta()
            if resultado == apuesta_color:
                saldo += apuesta*multiplicadores[resultado]
            fase = "resultado"

    elif fase == "resultado":
        msg = font.render(f"Resultado: {resultado.upper()}", True, (255,255,255))
        screen.blit(msg,(20,20))
        txt = font.render(f"Saldo: {saldo} rupias", True, (0,255,0))
        screen.blit(txt,(20,60))
        mult_txt = font.render(f"Multiplicador {resultado}: x{multiplicadores[resultado]}", True, (255,255,0))
        screen.blit(mult_txt,(20,100))
        opciones = font.render("Presiona V para siguiente ronda, C para salir", True, (200,200,200))
        screen.blit(opciones,(20,140))
        dibujar_ruleta()
        dibujar_tabla()

    pygame.display.flip()
    clock.tick(30)
