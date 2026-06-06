# Definición de la clase Automovil

class Automovil:
    def __init__(self, marca, modelo, color):
        # Atributos
        self.marca = marca
        self.modelo = modelo
        self.color = color

    # Método para mostrar la información del automóvil
    def mostrar_informacion(self):
        print(f"Marca: {self.marca}")
        print(f"Modelo: {self.modelo}")
        print(f"Color: {self.color}")

    # Método para simular el encendido del automóvil
    def encender(self):
        print(f"El automóvil {self.marca} {self.modelo} ha sido encendido.")


# Creación de objetos

automovil1 = Automovil("Toyota", "Corolla", "Blanco")
automovil2 = Automovil("Chevrolet", "Spark", "Rojo")

# Uso de los métodos

print("=== Automóvil 1 ===")
automovil1.mostrar_informacion()
automovil1.encender()

print("\n=== Automóvil 2 ===")
automovil2.mostrar_informacion()
automovil2.encender()