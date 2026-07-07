import random

# Inventario inicial del jugador
inventario = {"rupias": 100, "pociones": 0, "flechas": 0, "bombas": 0}

# Precios iniciales del mercado
mercado = {"pociones": 20, "flechas": 5, "bombas": 15}

def mostrar_estado():
    print("\nInventario:", inventario)
    print("Precios del mercado:", mercado)

def comprar(item, cantidad):
    costo = mercado[item] * cantidad
    if inventario["rupias"] >= costo:
        inventario["rupias"] -= costo
        inventario[item] += cantidad
        print(f"Compraste {cantidad} {item}.")
    else:
        print("No tienes suficientes rupias.")

def vender(item, cantidad):
    if inventario[item] >= cantidad:
        inventario[item] -= cantidad
        ganancia = mercado[item] * cantidad
        inventario["rupias"] += ganancia
        print(f"Vendiste {cantidad} {item}.")
    else:
        print("No tienes suficientes para vender.")

def actualizar_precios():
    for item in mercado:
        cambio = random.randint(-3, 3)
        mercado[item] = max(1, mercado[item] + cambio)

# Ciclo de juego
for turno in range(5):
    print(f"\n--- Turno {turno+1} ---")
    mostrar_estado()
    accion = input("¿Quieres comprar, vender o pasar? ").lower()
    if accion in ["comprar", "vender"]:
        item = input("¿Qué objeto (pociones, flechas, bombas)? ").lower()
        cantidad = int(input("¿Cuántos? "))
        if accion == "comprar":
            comprar(item, cantidad)
        else:
            vender(item, cantidad)
    actualizar_precios()

print("\nJuego terminado. Estado final:")
mostrar_estado()
