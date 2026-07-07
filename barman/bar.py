import random

# Moneda inicial
rupias = 50

# Bebidas disponibles
bebidas = {
    "Cerveza": {"ingredientes": ["Malta", "Agua", "Lúpulo"], "precio": 10},
    "Margarita": {"ingredientes": ["Tequila", "Triple Sec", "Jugo de Limón"], "precio": 15},
    "Martini": {"ingredientes": ["Ginebra", "Vermouth"], "precio": 20}
}

# Clientes aleatorios
clientes = ["Juan", "María", "Pedro", "Lucía"]

def atender_cliente(rupias):
    cliente = random.choice(clientes)
    bebida = random.choice(list(bebidas.keys()))
    receta = bebidas[bebida]["ingredientes"]
    precio = bebidas[bebida]["precio"]

    print(f"\n{cliente} pide un {bebida} (Precio: {precio} rupias)")
    print("Ingredientes necesarios:", receta)

    seleccion = input("Escribe los ingredientes separados por coma: ").split(",")
    seleccion = [s.strip() for s in seleccion]

    if seleccion == receta:
        print("¡Perfecto! El cliente está feliz 🍹")
        rupias += precio
    else:
        print("Ups... el cliente se va molesto 😡")
        rupias -= precio

    print(f"Saldo actual: {rupias} rupias")
    return rupias

# Loop del juego
while rupias > 0:
    rupias = atender_cliente(rupias)
    if rupias <= 0:
        print("Te quedaste sin rupias. ¡Juego terminado!")
        break
