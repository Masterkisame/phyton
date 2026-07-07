import random

inventario = {"rupias": 100, "pociones": 0, "flechas": 0, "bombas": 0, "escudos": 0}
mercado = {"pociones": 20, "flechas": 8, "bombas": 12, "escudos": 30}

eventos = [
    ("Festival Kokiri 🎉", {"pociones": -5}),
    ("Guerra en Gerudo ⚔️", {"bombas": +10}),
    ("Escasez de flechas 🏹", {"flechas": +7}),
    ("Visita real 👑", {"pociones": +8, "bombas": +5})
]

def mostrar_estado():
    print("\nInventario:", inventario)
    print("Precios del mercado:", mercado)

def hablar_con_vendedor():
    frases = [
        "¡Bienvenido al Mercado de Hyrule, viajero!",
        "Hoy las bombas están muy solicitadas…",
        "Dicen que habrá un festival Kokiri pronto.",
        "Las flechas escasean, mejor compra ahora."
    ]
    print("Vendedor:", random.choice(frases))

def evento_aleatorio():
    nombre, efecto = random.choice(eventos)
    print(f"\n¡Evento!: {nombre}")
    for item, cambio in efecto.items():
        mercado[item] = max(1, mercado[item] + cambio)

# Ciclo de juego
for turno in range(5):
    print(f"\n--- Turno {turno+1} ---")
    mostrar_estado()
    hablar_con_vendedor()
    accion = input("¿Quieres comprar, vender o hablar? ").lower()
    if accion == "comprar":
        item = input("¿Qué objeto (pociones, flechas, bombas, escudos)? ").lower()
        cantidad = int(input("¿Cuántos? "))
        costo = mercado[item] * cantidad
        if inventario["rupias"] >= costo:
            inventario["rupias"] -= costo
            inventario[item] += cantidad
            print(f"Compraste {cantidad} {item}.")
        else:
            print("No tienes suficientes rupias.")
    elif accion == "vender":
        item = input("¿Qué objeto? ").lower()
        cantidad = int(input("¿Cuántos? "))
        if inventario[item] >= cantidad:
            inventario[item] -= cantidad
            inventario["rupias"] += mercado[item] * cantidad
            print(f"Vendiste {cantidad} {item}.")
        else:
            print("No tienes suficientes para vender.")
    else:
        print("Decidiste hablar con el vendedor.")
    evento_aleatorio()

print("\nJuego terminado. Estado final:")
mostrar_estado()
