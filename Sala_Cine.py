# Programa: Reserva de un asiento en una sala de cine

# Crear matriz 3x4 con todos los asientos libres (0)
asientos = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

# Pedir al usuario la fila y la columna
fila = int(input("Ingrese fila (0 a 2): "))
columna = int(input("Ingrese columna (0 a 3): "))

# Reservar el asiento
asientos[fila][columna] = 1

# Mostrar el estado de la sala
print("\nEstado de la sala:")

for i in range(3):
    for j in range(4):
        print(asientos[i][j], end=" ")
    print()