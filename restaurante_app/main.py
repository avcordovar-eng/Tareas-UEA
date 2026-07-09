#!/usr/bin/env python3
"""
Punto de entrada principal del sistema restaurante_app.

Este archivo implementa un menú interactivo para gestionar productos y clientes
en un restaurante utilizando conceptos de Programación Orientada a Objetos (POO).
"""

from modelos.platillo import Platillo
from modelos.bebida import Bebida
from modelos.cliente import Cliente
from servicios.restaurante import Restaurante
def obtener_opcion_menu() -> str:
    """Muestra el menú y retorna la opción seleccionada por el usuario."""
    print("\n========================================")
    print("        SISTEMA DE RESTAURANTE")
    print("========================================")
    print("1. Registrar producto")
    print("2. Listar productos")
    print("3. Buscar producto")
    print("----------------------------------------")
    print("4. Registrar cliente")
    print("5. Listar clientes")
    print("6. Buscar cliente")
    print("----------------------------------------")
    print("7. Salir")
    print("========================================")
    return input("Seleccione una opción (1-7): ").strip()
def registrar_producto(restaurante: Restaurante) -> None:
    """Solicita datos para registrar un nuevo producto (Platillo o Bebida)."""
    try:
        print("\n--- Registrar Producto ---")
        print("Tipo de producto: 1) Platillo  2) Bebida")
        tipo = input("Seleccione tipo (1/2): ").strip()

        nombre = input("Nombre del producto: ").strip()
        categoria = input("Categoría (Entrada/Plato Principal/Postre/Bebida: )").strip()
        precio_input = input("Precio: ").strip()

        try:
            precio = float(precio_input)
        except ValueError:
            print("Error: El precio debe ser un número válido.")
            return

        if tipo == "1":
            calorias_input = input("Calorías: ").strip()
            try:
                calorias = int(calorias_input)
            except ValueError:
                print("Error: Las calorías deben ser un número entero válido.")
                return

            ingredientes_input = input("Ingredientes (separados por comas): ").strip()
            ingredientes = [ing.strip() for ing in ingredientes_input.split(",") if ing.strip()]

            if not ingredientes:
                print("Error: El platillo debe tener al menos un ingrediente.")
                return

            disponible_input = input("Disponible (si/no, por defecto si): ").strip().lower()
            disponible = disponible_input != "no"

            producto = Platillo(
                nombre=nombre,
                categoria=categoria,
                precio=precio,
                calorias=calorias,
                ingredientes=ingredientes,
                disponible=disponible
            )

        elif tipo == "2":
            volumen_input = input("Volumen en ml: ").strip()
            try:
                volumen = int(volumen_input)
            except ValueError:
                print("Error: El volumen debe ser un número entero válido.")
                return

            disponible_input = input("Disponible (si/no, por defecto si): ").strip().lower()
            disponible = disponible_input != "no"

            producto = Bebida(
                nombre=nombre,
                categoria=categoria,
                precio=precio,
                volumen_ml=volumen,
                disponible=disponible
            )

        else:
            print("Opción inválida.")
            return

        restaurante.registrar_producto(producto)
        print(f"✓ Producto '{producto.nombre}' registrado exitosamente!")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
def listar_productos(restaurante: Restaurante) -> None:
    """Muestra todos los productos registrados."""
    if not restaurante.lista_productos:
        print("\nNo hay productos registrados.")
        return

    print("\n--- Lista de Productos ---")
    for i, producto in enumerate(restaurante.lista_productos, 1):
        print(f"{i}. ", end="")
        producto.mostrar_informacion()
def buscar_producto(restaurante: Restaurante) -> None:
    """Busca un producto por nombre."""
    if not restaurante.lista_productos:
        print("\nNo hay productos registrados para buscar.")
        return

    print("\n--- Buscar Producto ---")
    termino = input("Ingrese nombre del producto a buscar: ").strip().lower()

    encontrados = []
    for producto in restaurante.lista_productos:
        if termino in producto.nombre.lower():
            encontrados.append(producto)

    if not encontrados:
        print("No se encontraron productos con ese nombre.")
        return

    print(f"\nSe encontraron {len(encontrados)} producto(s):")
    for i, producto in enumerate(encontrados, 1):
        print(f"{i}. ", end="")
        producto.mostrar_informacion()
def registrar_cliente(restaurante: Restaurante) -> None:
    """Solicita datos para registrar un nuevo cliente."""
    try:
        print("\n--- Registrar Cliente ---")

        nombre = input("Nombre del cliente: ").strip()
        if not nombre:
            print("Error: El nombre no puede estar vacío.")
            return

        correo = input("Correo electrónico: ").strip()
        if not correo or "@" not in correo:
            print("Error: El correo electrónico no es válido.")
            return

        id_input = input("ID del cliente: ").strip()
        try:
            id_cliente = int(id_input)
        except ValueError:
            print("Error: El ID debe ser un número entero válido.")
            return

        cliente = Cliente(nombre=nombre, correo=correo, id_cliente=id_cliente)
        restaurante.registrar_cliente(cliente)
        print(f"✓ Cliente '{cliente.nombre}' registrado exitosamente!")

    except Exception as e:
        print(f"Error inesperado: {e}")
def listar_clientes(restaurante: Restaurante) -> None:
    """Muestra todos los clientes registrados."""
    if not restaurante.lista_clientes:
        print("\nNo hay clientes registrados.")
        return

    print("\n--- Lista de Clientes ---")
    for i, cliente in enumerate(restaurante.lista_clientes, 1):
        print(f"{i}. ", end="")
        cliente.mostrar_informacion()
def buscar_cliente(restaurante: Restaurante) -> None:
    """Busca un cliente por ID."""
    if not restaurante.lista_clientes:
        print("\nNo hay clientes registrados para buscar.")
        return

    print("\n--- Buscar Cliente ---")
    id_input = input("Ingrese ID del cliente: ").strip()

    try:
        id_buscar = int(id_input)
    except ValueError:
        print("Error: El ID debe ser un número entero válido.")
        return

    encontrado = next((c for c in restaurante.lista_clientes if c.id_cliente == id_buscar), None)

    if not encontrado:
        print("No se encontró un cliente con ese ID.")
        return

    print("\nCliente encontrado:")
    encontrado.mostrar_informacion()
def main() -> None:
    """Función principal que ejecuta el sistema de restaurante con menú interactivo."""
    restaurante = Restaurante("Mi Restaurante")

    print("¡Bienvenido al Sistema de Restaurante!")

    while True:
        opcion = obtener_opcion_menu()

        if opcion == "1":
            registrar_producto(restaurante)
        elif opcion == "2":
            listar_productos(restaurante)
        elif opcion == "3":
            buscar_producto(restaurante)
        elif opcion == "4":
            registrar_cliente(restaurante)
        elif opcion == "5":
            listar_clientes(restaurante)
        elif opcion == "6":
            buscar_cliente(restaurante)
        elif opcion == "7":
            print("\n¡Gracias por usar el Sistema de Restaurante! ¡Hasta luego!")
            break
        else:
            print("\nOpción inválida. Por favor, seleccione una opción del 1 al 7.")
if __name__ == "__main__":
    main()