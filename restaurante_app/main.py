#!/usr/bin/env python3
"""Punto de entrada principal del sistema restaurante_app."""

from modelos.producto import Producto
from modelos.bebida import Bebida
from modelos.cliente import Cliente
from servicios.restaurante import Restaurante


def obtener_opcion_menu() -> str:
    """Muestra el menú y retorna la opción seleccionada."""
    print("\n========================================")
    print("        SISTEMA DE RESTAURANTE")
    print("========================================")
    print("1. Registrar producto")
    print("2. Registrar bebida")
    print("3. Registrar cliente")
    print("----------------------------------------")
    print("4. Listar productos")
    print("5. Listar clientes")
    print("----------------------------------------")
    print("6. Salir")
    return input("Seleccione una opción (1-6): ").strip()


def registrar_producto(restaurante: Restaurante) -> None:
    """Solicita datos y registra un nuevo producto."""
    print("\n--- Registrar Producto ---")
    codigo = input("Código del producto: ").strip()
    if not codigo:
        print("Error: El código no puede estar vacío.")
        return
    nombre = input("Nombre del producto: ").strip()
    if not nombre:
        print("Error: El nombre no puede estar vacío.")
        return
    categoria = input("Categoría del producto: ").strip()
    if not categoria:
        print("Error: La categoría no puede estar vacía.")
        return
    try:
        precio = float(input("Precio del producto: ").strip())
    except ValueError:
        print("Error: El precio debe ser un número válido.")
        return
    try:
        producto = Producto(codigo, nombre, categoria, precio)
        if restaurante.registrar_producto(producto):
            print(f"OK Producto '{producto.nombre}' registrado exitosamente.")
    except ValueError as e:
        print(f"Error: {e}")


def registrar_bebida(restaurante: Restaurante) -> None:
    """Solicita datos y registra una nueva bebida."""
    print("\n--- Registrar Bebida ---")
    codigo = input("Código de la bebida: ").strip()
    if not codigo:
        print("Error: El código no puede estar vacío.")
        return
    nombre = input("Nombre de la bebida: ").strip()
    if not nombre:
        print("Error: El nombre no puede estar vacío.")
        return
    categoria = input("Categoría de la bebida: ").strip()
    if not categoria:
        print("Error: La categoría no puede estar vacía.")
        return
    try:
        precio = float(input("Precio de la bebida: ").strip())
    except ValueError:
        print("Error: El precio debe ser un número válido.")
        return
    tamanio = input("Tamaño de la bebida (pequeño/mediano/grande): ").strip()
    if not tamanio:
        print("Error: El tamaño no puede estar vacío.")
        return
    try:
        bebida = Bebida(codigo, nombre, categoria, precio, tamanio)
        if restaurante.registrar_producto(bebida):
            print(f"OK Bebida '{bebida.nombre}' registrada exitosamente.")
    except ValueError as e:
        print(f"Error: {e}")


def registrar_cliente(restaurante: Restaurante) -> None:
    """Solicita datos y registra un nuevo cliente."""
    print("\n--- Registrar Cliente ---")
    identificacion = input("Identificación del cliente: ").strip()
    if not identificacion:
        print("Error: La identificación no puede estar vacía.")
        return
    nombre = input("Nombre del cliente: ").strip()
    if not nombre:
        print("Error: El nombre no puede estar vacío.")
        return
    correo = input("Correo electrónico del cliente: ").strip()
    if not correo:
        print("Error: El correo no puede estar vacío.")
        return
    try:
        cliente = Cliente(identificacion, nombre, correo)
        if restaurante.registrar_cliente(cliente):
            print(f"OK Cliente '{cliente.nombre}' registrado exitosamente.")
    except ValueError as e:
        print(f"Error: {e}")


def main() -> None:
    """Función principal que ejecuta el sistema de restaurante."""
    restaurante = Restaurante("Mi Restaurante")
    print("¡Bienvenido al Sistema de Restaurante!")
    while True:
        opcion = obtener_opcion_menu()
        if opcion == "1":
            registrar_producto(restaurante)
        elif opcion == "2":
            registrar_bebida(restaurante)
        elif opcion == "3":
            registrar_cliente(restaurante)
        elif opcion == "4":
            restaurante.listar_productos()
        elif opcion == "5":
            restaurante.listar_clientes()
        elif opcion == "6":
            print("\n¡Gracias por usar el Sistema de Restaurante! ¡Hasta luego!")
            break
        else:
            print("\nOpción inválida. Por favor, seleccione una opción del 1 al 6.")


if __name__ == "__main__":
    main()
