"""Módulo que define la clase Restaurante como servicio del sistema."""

from modelos.producto import Producto
from modelos.cliente import Cliente


class Restaurante:
    """Clase de servicio encargada de administrar productos y clientes."""

    def __init__(self, nombre: str) -> None:
        self.nombre: str = nombre
        self._productos: list[Producto] = []
        self._clientes: list[Cliente] = []

    @property
    def productos(self) -> list[Producto]:
        return list(self._productos)

    @property
    def clientes(self) -> list[Cliente]:
        return list(self._clientes)

    def registrar_producto(self, producto: Producto) -> bool:
        """Registra un producto validando que el código no se repita.

        Returns:
            True si se registró, False si el código ya existe.
        """
        for existente in self._productos:
            if existente.codigo == producto.codigo:
                print(f"Error: Ya existe un producto con el código '{producto.codigo}'.")
                return False
        self._productos.append(producto)
        return True

    def registrar_cliente(self, cliente: Cliente) -> bool:
        """Registra un cliente validando que la identificación no se repita.

        Returns:
            True si se registró, False si la identificación ya existe.
        """
        for existente in self._clientes:
            if existente.identificacion == cliente.identificacion:
                print(f"Error: Ya existe un cliente con identificación '{cliente.identificacion}'.")
                return False
        self._clientes.append(cliente)
        return True

    def listar_productos(self) -> None:
        """Lista todos los productos usando polimorfismo con mostrar_informacion()."""
        if not self._productos:
            print("No hay productos registrados.")
            return
        print(f"\n--- Productos de {self.nombre} ---")
        for i, producto in enumerate(self._productos, 1):
            print(f"{i}. ", end="")
            producto.mostrar_informacion()
            print("-" * 30)

    def listar_clientes(self) -> None:
        """Lista todos los clientes registrados."""
        if not self._clientes:
            print("No hay clientes registrados.")
            return
        print(f"\n--- Clientes de {self.nombre} ---")
        for i, cliente in enumerate(self._clientes, 1):
            print(f"{i}. ", end="")
            cliente.mostrar_informacion()
            print("-" * 30)
