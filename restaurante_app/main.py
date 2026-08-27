#!/usr/bin/env python3
"""Punto de entrada principal del sistema restaurante_app.

Responsable únicamente de la interacción por consola: muestra el menú,
solicita datos, crea los objetos y delega en el servicio Restaurante.
Además coordina la persistencia: carga los productos almacenados al
iniciar la aplicación y solicita su guardado después de cada operación
que modifica la colección.
No administra directamente las colecciones internas del servicio.
"""

from typing import Callable

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio
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
    "9. Vender producto",
    "10. Consultar ventas de usuario",
    "11. Salir",
)


def mostrar_menu() -> str:
    """Muestra el menú principal y retorna la opción seleccionada."""
    print("\n========================================")
    print("        SISTEMA DE RESTAURANTE")
    print("========================================")
    for i, opcion in enumerate(OPCIONES_MENU, 1):
        print(opcion)
        if i == 5 or i == 8 or i == 10:
            print("----------------------------------------")
    return input("Seleccione una opción (1-11): ").strip()


def persistir_productos(archivo_servicio: ArchivoServicio,
                        restaurante: Restaurante) -> None:
    """Solicita a ArchivoServicio guardar el estado actual de los productos."""
    if not archivo_servicio.guardar_productos(restaurante.productos):
        print("Advertencia: no se pudo actualizar datos/productos.json "
              "con los últimos cambios.")


def persistir_usuarios(archivo_servicio: ArchivoServicio,
                       restaurante: Restaurante) -> None:
    """Solicita a ArchivoServicio guardar el estado actual de los usuarios."""
    if not archivo_servicio.guardar_usuarios(restaurante.usuarios):
        print("Advertencia: no se pudo actualizar datos/usuarios.json "
              "con los últimos cambios.")


def persistir_ventas(archivo_servicio: ArchivoServicio,
                     restaurante: Restaurante) -> None:
    """Solicita a ArchivoServicio guardar el estado actual de las ventas."""
    if not archivo_servicio.guardar_ventas(restaurante.ventas):
        print("Advertencia: no se pudo actualizar datos/ventas.json "
              "con los últimos cambios.")


def registrar_producto(restaurante: Restaurante,
                       archivo_servicio: ArchivoServicio) -> None:
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
        stock = int(input("Stock inicial: ").strip())
        if stock < 0:
            print("Error: El stock no puede ser negativo.")
            return
    except ValueError:
        print("Error: El stock debe ser un número entero válido.")
        return
    try:
        producto = Producto(codigo, nombre, categoria, precio, stock)
        if restaurante.registrar_producto(producto):
            print(f"Producto '{producto.nombre}' registrado exitosamente.")
            persistir_productos(archivo_servicio, restaurante)
    except ValueError as e:
        print(f"Error: {e}")


def buscar_producto(restaurante: Restaurante,
                    archivo_servicio: ArchivoServicio) -> None:
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


def actualizar_producto(restaurante: Restaurante,
                        archivo_servicio: ArchivoServicio) -> None:
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
            persistir_productos(archivo_servicio, restaurante)
    except ValueError as e:
        print(f"Error: {e}")


def eliminar_producto(restaurante: Restaurante,
                      archivo_servicio: ArchivoServicio) -> None:
    """Solicita un código y elimina el producto correspondiente."""
    print("\n--- Eliminar Producto ---")
    codigo = input("Código del producto a eliminar: ").strip()
    if not codigo:
        print("Error: El código no puede estar vacío.")
        return
    if restaurante.eliminar_producto(codigo):
        print(f"Producto con código '{codigo}' eliminado exitosamente.")
        persistir_productos(archivo_servicio, restaurante)
    else:
        print(f"No se encontró ningún producto con el código '{codigo}'.")


def listar_productos(restaurante: Restaurante,
                     archivo_servicio: ArchivoServicio) -> None:
    """Solicita al servicio el listado de productos."""
    restaurante.listar_productos()


def registrar_usuario(restaurante: Restaurante,
                      archivo_servicio: ArchivoServicio) -> None:
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
            persistir_usuarios(archivo_servicio, restaurante)
    except ValueError as e:
        print(f"Error: {e}")


def listar_usuarios(restaurante: Restaurante,
                    archivo_servicio: ArchivoServicio) -> None:
    """Solicita al servicio el listado de usuarios."""
    restaurante.listar_usuarios()


def mostrar_categorias(restaurante: Restaurante,
                       archivo_servicio: ArchivoServicio) -> None:
    """Muestra las categorías únicas de los productos registrados."""
    print("\n--- Categorías de Productos ---")
    categorias = restaurante.obtener_categorias()
    if not categorias:
        print("No hay categorías registradas.")
        return
    for categoria in sorted(categorias):
        print(f"- {categoria}")


def vender_producto(restaurante: Restaurante,
                    archivo_servicio: ArchivoServicio) -> None:
    """Realiza la venta de un producto a un usuario."""
    print("\n--- Vender Producto ---")
    identificacion = input("Identificación del usuario: ").strip()
    if not identificacion:
        print("Error: La identificación no puede estar vacía.")
        return
    codigo = input("Código del producto: ").strip()
    if not codigo:
        print("Error: El código no puede estar vacío.")
        return
    try:
        cantidad = int(input("Cantidad: ").strip())
    except ValueError:
        print("Error: La cantidad debe ser un número entero válido.")
        return

    if restaurante.vender_producto(codigo, identificacion, cantidad):
        persistir_ventas(archivo_servicio, restaurante)
        persistir_productos(archivo_servicio, restaurante)


def consultar_ventas_usuario(restaurante: Restaurante,
                             archivo_servicio: ArchivoServicio) -> None:
    """Consulta las ventas realizadas por un usuario."""
    print("\n--- Consultar Ventas de Usuario ---")
    identificacion = input("Identificación del usuario: ").strip()
    if not identificacion:
        print("Error: La identificación no puede estar vacía.")
        return
    restaurante.listar_ventas_usuario(identificacion)


ACCIONES_MENU: dict[str, Callable[[Restaurante, ArchivoServicio], None]] = {
    "1": registrar_producto,
    "2": buscar_producto,
    "3": actualizar_producto,
    "4": eliminar_producto,
    "5": listar_productos,
    "6": registrar_usuario,
    "7": listar_usuarios,
    "8": mostrar_categorias,
    "9": vender_producto,
    "10": consultar_ventas_usuario,
}


def main() -> None:
    """Función principal que coordina la carga, el menú y el guardado."""
    archivo_servicio = ArchivoServicio()
    restaurante = Restaurante("Mi Restaurante")
    productos_cargados = archivo_servicio.cargar_productos()
    restaurante.cargar_productos(productos_cargados)
    usuarios_cargados = archivo_servicio.cargar_usuarios()
    restaurante.cargar_usuarios(usuarios_cargados)
    ventas_cargadas = archivo_servicio.cargar_ventas()
    restaurante.cargar_ventas(ventas_cargadas)
    print("¡Bienvenido al Sistema de Restaurante!")
    while True:
        opcion = mostrar_menu()
        if opcion == "11":
            print("\n¡Gracias por usar el Sistema de Restaurante! ¡Hasta luego!")
            break
        accion = ACCIONES_MENU.get(opcion)
        if accion is None:
            print("Opción inválida. Por favor, seleccione una opción del 1 al 11.")
            continue
        accion(restaurante, archivo_servicio)


if __name__ == "__main__":
    main()