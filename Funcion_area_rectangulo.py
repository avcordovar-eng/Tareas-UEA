# Función para calcular el área de un rectángulo
def calcular_area(base, altura):
    area = base * altura
    return area  # Retorna el resultado

# Parámetros de entrada (pueden ser ingresados por el usuario)
base = float(input("Ingrese la base del rectángulo: "))
altura = float(input("Ingrese la altura del rectángulo: "))

# Llamada a la función
resultado = calcular_area(base, altura)

# Mostrar el resultado en pantalla
print("El área del rectángulo es:", resultado)