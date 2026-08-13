#!/usr/bin/env python3
"""Punto de entrada principal del sistema restaurante_app.

Responsable únicamente de la interacción por consola: muestra el menú,
solicita datos, crea los objetos y delega en el servicio Restaurante.
No administra directamente las colecciones internas del servicio.
"""

from typing import Callable

from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.restaurante import Restaurante


OPCIONES_MENU: tuple[str, ...] = (
    "1. Registrar producto",
    "2. Buscar producto",
    "3. Actualizar producto",
    "4. Eliminar producto",
    "5. Listar productos",
    "6. Registrar usuario",
    "7. Listar usuarios",
    "8. Mostrar categorías",
    "9. Salir",
)


def mostrar_menu() -> str:
    """Muestra el menú principal y retorna la opción seleccionada."""
    print("\n========================================")
    print("        SISTEMA DE RESTAURANTE")
    print("========================================")
    for i, opcion in enumerate(OPCIONES_MENU, 1):
        print(opcion)
        if i == 5 or i == 7:
            print("----------------------------------------")
    return input("Seleccione una opción (1-9): ").strip()


def registrar_producto(restaurante: Restaurante) -> None:
    """Solicita los datos y registra un nuevo producto."""
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
            print(f"Producto '{producto.nombre}' registrado exitosamente.")
    except ValueError as e:
        print(f"Error: {e}")


def buscar_producto(restaurante: Restaurante) -> None:
    """Solicita un código y muestra el producto correspondiente."""
    print("\n--- Buscar Producto ---")
    codigo = input("Código del producto a buscar: ").strip()
    if not codigo:
        print("Error: El código no puede estar vacío.")
        return
    producto = restaurante.buscar_producto(codigo)
    if producto is None:
        print(f"No se encontró ningún producto con el código '{codigo}'.")
        return
    print("Producto encontrado:")
    producto.mostrar_informacion()


def actualizar_producto(restaurante: Restaurante) -> None:
    """Solicita un código y los nuevos datos para actualizar un producto."""
    print("\n--- Actualizar Producto ---")
    codigo = input("Código del producto a actualizar: ").strip()
    if not codigo:
        print("Error: El código no puede estar vacío.")
        return
    producto = restaurante.buscar_producto(codigo)
    if producto is None:
        print(f"No se encontró ningún producto con el código '{codigo}'.")
        return
    nombre = input(f"Nuevo nombre (Enter para mantener '{producto.nombre}'): ").strip()
    nombre = nombre if nombre else producto.nombre
    categoria = input(f"Nueva categoría (Enter para mantener '{producto.categoria}'): ").strip()
    categoria = categoria if categoria else producto.categoria
    precio = input(f"Nuevo precio (Enter para mantener ${producto.precio:.2f}): ").strip()
    if precio:
        try:
            precio_nuevo = float(precio)
        except ValueError:
            print("Error: El precio debe ser un número válido.")
            return
    else:
        precio_nuevo = producto.precio
    try:
        if restaurante.actualizar_producto(codigo, nombre, categoria, precio_nuevo):
            print(f"Producto '{nombre}' actualizado exitosamente.")
    except ValueError as e:
        print(f"Error: {e}")


def eliminar_producto(restaurante: Restaurante) -> None:
    """Solicita un código y elimina el producto correspondiente."""
    print("\n--- Eliminar Producto ---")
    codigo = input("Código del producto a eliminar: ").strip()
    if not codigo:
        print("Error: El código no puede estar vacío.")
        return
    if restaurante.eliminar_producto(codigo):
        print(f"Producto con código '{codigo}' eliminado exitosamente.")
    else:
        print(f"No se encontró ningún producto con el código '{codigo}'.")


def listar_productos(restaurante: Restaurante) -> None:
    """Solicita al servicio el listado de productos."""
    restaurante.listar_productos()


def registrar_usuario(restaurante: Restaurante) -> None:
    """Solicita los datos y registra un nuevo usuario."""
    print("\n--- Registrar Usuario ---")
    identificacion = input("Identificación del usuario: ").strip()
    if not identificacion:
        print("Error: La identificación no puede estar vacía.")
        return
    nombre = input("Nombre del usuario: ").strip()
    if not nombre:
        print("Error: El nombre no puede estar vacío.")
        return
    correo = input("Correo electrónico del usuario: ").strip()
    if not correo:
        print("Error: El correo no puede estar vacío.")
        return
    try:
        usuario = Usuario(identificacion, nombre, correo)
        if restaurante.registrar_usuario(usuario):
            print(f"Usuario '{usuario.nombre}' registrado exitosamente.")
    except ValueError as e:
        print(f"Error: {e}")


def listar_usuarios(restaurante: Restaurante) -> None:
    """Solicita al servicio el listado de usuarios."""
    restaurante.listar_usuarios()


def mostrar_categorias(restaurante: Restaurante) -> None:
    """Muestra las categorías únicas de los productos registrados."""
    print("\n--- Categorías de Productos ---")
    categorias = restaurante.obtener_categorias()
    if not categorias:
        print("No hay categorías registradas.")
        return
    for categoria in sorted(categorias):
        print(f"- {categoria}")


ACCIONES_MENU: dict[str, Callable[[Restaurante], None]] = {
    "1": registrar_producto,
    "2": buscar_producto,
    "3": actualizar_producto,
    "4": eliminar_producto,
    "5": listar_productos,
    "6": registrar_usuario,
    "7": listar_usuarios,
    "8": mostrar_categorias,
}


def main() -> None:
    """Función principal que coordina el menú y las acciones del sistema."""
    restaurante = Restaurante("Mi Restaurante")
    print("¡Bienvenido al Sistema de Restaurante!")
    while True:
        opcion = mostrar_menu()
        if opcion == "9":
            print("\n¡Gracias por usar el Sistema de Restaurante! ¡Hasta luego!")
            break
        accion = ACCIONES_MENU.get(opcion)
        if accion is None:
            print("Opción inválida. Por favor, seleccione una opción del 1 al 9.")
            continue
        accion(restaurante)


if __name__ == "__main__":
    main()
