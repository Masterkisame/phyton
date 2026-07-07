import pygame, sys, random

pygame.init()
W, H = 800, 400
screen = pygame.display.set_mode((W,H))
pygame.display.set_caption("Carrera de Ratas")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Cargar sprites desde carpeta "sprite"
sprites = {
    "azul": [
        pygame.image.load("sprite/ratazul_pose1.png"),
        pygame.image.load("sprite/ratazul_pose2.png")
    ],
    "blanca": [
        pygame.image.load("sprite/ratblanca_pose1.png"),
        pygame.image.load("sprite/ratblanca_pose2.png")
    ],
    "cafe": [
        pygame.image.load("sprite/ratcafe_pose1.png"),
        pygame.image.load("sprite/ratcafe_pose2.png")
    ]
}

menu_sprites = {
    "azul": pygame.image.load("sprite/rataazul.png"),
    "blanca": pygame.image.load("sprite/ratablanca.png"),
    "cafe": pygame.image.load("sprite/ratacafe.png")
}

# Escalar sprites
for k in sprites:
    sprites[k] = [pygame.transform.scale(img,(64,64)) for img in sprites[k]]
for k in menu_sprites:
    menu_sprites[k] = pygame.transform.scale(menu_sprites[k],(64,64))

class Rata:
    def __init__(self, nombre, y):
        self.nombre = nombre
        self.x = 50
        self.y = y
        self.velocidad = random.randint(3,6)
        self.suerte = random.randint(1,10)
        self.finished = False
        self.frame = 0

    def avanzar(self):
        if not self.finished:
            if random.randint(1,100) < self.suerte:
                self.x += self.velocidad + random.randint(2,5)
            else:
                self.x += self.velocidad + random.randint(-2,2)
            if self.x >= W-100:
                self.finished = True
        self.frame = (self.frame+1)%20

    def draw(self):
        img = sprites[self.nombre][0] if self.frame<10 else sprites[self.nombre][1]
        screen.blit(img,(self.x,self.y))

def nueva_carrera():
    return [
        Rata("azul",50),
        Rata("blanca",150),
        Rata("cafe",250)
    ]

rupias = 100
apostada = None
apuesta = 10
ratas = nueva_carrera()
orden_llegada = []
ganador = None
fase = "menu"
selector_index = 0
opciones = ["azul","blanca","cafe"]

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: sys.exit()
        if fase == "menu" and e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RIGHT: selector_index = (selector_index+1)%len(opciones)
            if e.key == pygame.K_LEFT: selector_index = (selector_index-1)%len(opciones)
            if e.key == pygame.K_UP and apuesta < rupias: apuesta += 10
            if e.key == pygame.K_DOWN and apuesta > 10: apuesta -= 10
            if e.key == pygame.K_RETURN:
                apostada = opciones[selector_index]
                rupias -= apuesta
                ratas = nueva_carrera()
                orden_llegada = []
                ganador = None
                fase = "carrera"
        if fase == "resultado" and e.type == pygame.KEYDOWN:
            if e.key == pygame.K_v and rupias > 0:
                apostada = None
                apuesta = 10
                ratas = nueva_carrera()
                orden_llegada = []
                ganador = None
                fase = "menu"
            if e.key == pygame.K_c: sys.exit()

    screen.fill((0,0,0))

    if fase == "menu":
        msg = font.render(f"Tienes {rupias} rupias", True, (255,255,255))
        screen.blit(msg,(50,20))
        txt = font.render("Usa ← → para elegir rata, ↑ ↓ para monto", True, (255,255,0))
        screen.blit(txt,(50,50))
        apuesta_txt = font.render(f"Apuesta: {apuesta} rupias", True, (0,200,200))
        screen.blit(apuesta_txt,(50,80))
        for i,nombre in enumerate(opciones):
            img = menu_sprites[nombre]
            x = 200+i*150
            y = 200
            if i == selector_index:
                pygame.draw.rect(screen,(255,255,0),(x-5,y-5,74,74),3)
            screen.blit(img,(x,y))

    elif fase == "carrera":
        for rata in ratas:
            if not rata.finished:
                rata.avanzar()
                if rata.x >= W-100 and rata.nombre not in orden_llegada:
                    orden_llegada.append(rata.nombre)
        for rata in ratas:
            rata.draw()
        if len(orden_llegada) == len(ratas):
            ganador = orden_llegada[0]
            fase = "resultado"
            if ganador == apostada:
                rupias += apuesta*3

    elif fase == "resultado":
        msg = font.render("Resultados de la carrera:", True, (255,255,255))
        screen.blit(msg,(W//2-120,H//2-120))
        for i,nombre in enumerate(orden_llegada):
            txt = font.render(f"{i+1}° lugar: {nombre}", True, (200,200,200))
            screen.blit(txt,(W//2-120,H//2-90 + i*30))

        if ganador == apostada:
            txt = font.render(f"¡Ganaste {apuesta*3} rupias!", True, (0,255,0))
        else:
            txt = font.render("Perdiste tu apuesta...", True, (255,0,0))
        screen.blit(txt,(W//2-120,H//2+40))

        saldo = font.render(f"Saldo: {rupias} rupias", True, (255,255,255))
        screen.blit(saldo,(W//2-100,H//2+70))
        opciones_txt = font.render("Presiona V para volver a apostar, C para salir", True, (200,200,200))
        screen.blit(opciones_txt,(W//2-220,H//2+100))

    pygame.display.flip()
    clock.tick(30)
