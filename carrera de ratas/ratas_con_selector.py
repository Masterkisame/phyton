import pygame, sys, random

pygame.init()
W, H = 800, 400
screen = pygame.display.set_mode((W,H))
pygame.display.set_caption("Carrera de Ratas")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

class Rata:
    def __init__(self, nombre, color, y):
        self.nombre = nombre
        self.color = color
        self.x = 50
        self.y = y
        self.velocidad = random.randint(3,6)
        self.suerte = random.randint(1,10)
        self.finished = False

    def avanzar(self):
        if not self.finished:
            if random.randint(1,100) < self.suerte:
                self.x += self.velocidad + random.randint(2,5)  # boost
            else:
                self.x += self.velocidad + random.randint(-2,2)
            if self.x >= W-100:
                self.finished = True

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x,self.y,40,20))

def nueva_carrera():
    return [
        Rata("Gris",(200,200,200),50),
        Rata("Gorda",(150,75,0),100),
        Rata("Ágil",(0,255,0),150),
        Rata("Vieja",(100,100,50),200)
    ]

rupias = 100
apostada = None
apuesta = 10
ratas = nueva_carrera()
ganador = None
fase = "menu"  # menu, carrera, resultado

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: sys.exit()
        if fase == "menu" and e.type == pygame.KEYDOWN:
            # elegir rata
            if e.key == pygame.K_1: apostada = "Gris"
            if e.key == pygame.K_2: apostada = "Gorda"
            if e.key == pygame.K_3: apostada = "Ágil"
            if e.key == pygame.K_4: apostada = "Vieja"
            # ajustar apuesta
            if e.key == pygame.K_UP and apuesta < rupias:
                apuesta += 10
            if e.key == pygame.K_DOWN and apuesta > 10:
                apuesta -= 10
            # confirmar apuesta
            if e.key == pygame.K_RETURN and apostada and rupias >= apuesta:
                rupias -= apuesta
                fase = "carrera"
        if fase == "resultado" and e.type == pygame.KEYDOWN:
            if e.key == pygame.K_v and rupias > 0:
                apostada = None
                apuesta = 10
                ratas = nueva_carrera()
                ganador = None
                fase = "menu"
            if e.key == pygame.K_c:
                sys.exit()

    screen.fill((0,0,0))

    if fase == "menu":
        msg = font.render(f"Tienes {rupias} rupias", True, (255,255,255))
        screen.blit(msg,(50,50))
        txt = font.render("Elige tu rata (1-Gris, 2-Gorda, 3-Ágil, 4-Vieja)", True, (255,255,0))
        screen.blit(txt,(50,100))
        apuesta_txt = font.render(f"Apuesta actual: {apuesta} rupias (Arriba/Abajo)", True, (0,200,200))
        screen.blit(apuesta_txt,(50,150))
        confirm_txt = font.render("Presiona ENTER para confirmar", True, (200,200,200))
        screen.blit(confirm_txt,(50,200))

    elif fase == "carrera":
        for rata in ratas:
            rata.avanzar()
            rata.draw()
        if all(r.finished for r in ratas):
            ganador = max(ratas, key=lambda r: r.x).nombre
            fase = "resultado"
            if ganador == apostada:
                premio = apuesta*3
                rupias += premio
            else:
                premio = 0

    elif fase == "resultado":
        msg = font.render(f"Ganó la {ganador}", True, (255,255,255))
        screen.blit(msg,(W//2-100,H//2-60))
        if ganador == apostada:
            txt = font.render(f"¡Ganaste {apuesta*3} rupias!", True, (0,255,0))
        else:
            txt = font.render("Perdiste tu apuesta...", True, (255,0,0))
        screen.blit(txt,(W//2-120,H//2-20))
        saldo = font.render(f"Saldo: {rupias} rupias", True, (255,255,255))
        screen.blit(saldo,(W//2-100,H//2+20))
        opciones = font.render("Presiona V para volver a apostar, C para salir", True, (200,200,200))
        screen.blit(opciones,(W//2-200,H//2+60))

    pygame.display.flip()
    clock.tick(30)
