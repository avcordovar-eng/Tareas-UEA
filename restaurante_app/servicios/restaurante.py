"""Módulo que define la clase Restaurante como servicio del sistema."""

from modelos.producto import Producto
from modelos.usuario import Usuario


class Restaurante:
    """Servicio encargado de administrar las colecciones y operaciones del sistema.

    Gestiona una lista de productos y una lista de usuarios. Todos los
    registros, búsquedas, actualizaciones, eliminaciones y consultas se
    realizan a través de los métodos de esta clase; main.py nunca manipula
    directamente las listas internas.
    """

    def __init__(self, nombre: str) -> None:
        self.nombre: str = nombre
        self._productos: list[Producto] = []
        self._usuarios: list[Usuario] = []

    @property
    def productos(self) -> list[Producto]:
        """Devuelve una copia de la lista interna de productos."""
        return list(self._productos)

    @property
    def usuarios(self) -> list[Usuario]:
        """Devuelve una copia de la lista interna de usuarios."""
        return list(self._usuarios)

    def registrar_producto(self, producto: Producto) -> bool:
        """Registra un producto evitando códigos duplicados.

        Returns:
            True si el producto se registró, False si el código ya existe.
        """
        if self.buscar_producto(producto.codigo) is not None:
            print(f"Error: Ya existe un producto con el código '{producto.codigo}'.")
            return False
        self._productos.append(producto)
        return True

    def buscar_producto(self, codigo: str) -> Producto | None:
        """Busca un producto por su código.

        Returns:
            El producto encontrado o None si no existe.
        """
        for producto in self._productos:
            if producto.codigo == codigo.strip():
                return producto
        return None

    def actualizar_producto(self, codigo: str, nombre: str,
                            categoria: str, precio: float) -> bool:
        """Actualiza los datos de un producto existente.

        Returns:
            True si se actualizó, False si el producto no existe.
        """
        producto = self.buscar_producto(codigo)
        if producto is None:
            print(f"Error: No se encontró un producto con el código '{codigo}'.")
            return False
        producto.nombre = nombre
        producto.categoria = categoria
        producto.precio = precio
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        """Elimina un producto por su código.

        Returns:
            True si se eliminó, False si el producto no existe.
        """
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        self._productos.remove(producto)
        return True

    def listar_productos(self) -> None:
        """Lista todos los productos registrados."""
        if not self._productos:
            print("No hay productos registrados.")
            return
        print(f"\n--- Productos de {self.nombre} ---")
        for i, producto in enumerate(self._productos, 1):
            print(f"{i}. {producto.nombre} ({producto.codigo}) - "
                  f"Categoría: {producto.categoria} - ${producto.precio:.2f}")

    def registrar_usuario(self, usuario: Usuario) -> bool:
        """Registra un usuario evitando identificaciones duplicadas.

        Returns:
            True si el usuario se registró, False si la identificación ya existe.
        """
        for existente in self._usuarios:
            if existente.identificacion == usuario.identificacion:
                print(f"Error: Ya existe un usuario con identificación "
                      f"'{usuario.identificacion}'.")
                return False
        self._usuarios.append(usuario)
        return True

    def listar_usuarios(self) -> None:
        """Lista todos los usuarios registrados."""
        if not self._usuarios:
            print("No hay usuarios registrados.")
            return
        print(f"\n--- Usuarios de {self.nombre} ---")
        for i, usuario in enumerate(self._usuarios, 1):
            print(f"{i}. {usuario.nombre} - Identificación: "
                  f"{usuario.identificacion} - Correo: {usuario.correo}")

    def obtener_categorias(self) -> set[str]:
        """Retorna el conjunto de categorías únicas de los productos.

        El conjunto elimina automáticamente los duplicados, garantizando
        que cada categoría se presente una sola vez.

        Returns:
            Conjunto con las categorías de los productos registrados.
        """
        return {producto.categoria for producto in self._productos}
