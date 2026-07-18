"""Módulo que define la clase Bebida del restaurante."""

from modelos.producto import Producto


class Bebida(Producto):
    """Clase que representa una bebida, hereda de Producto.

    Attributes:
        tamanio (str): Tamaño de la bebida (ej. pequeño, mediano, grande).
    """

    def __init__(self, codigo: str, nombre: str, categoria: str,
                 precio: float, tamanio: str) -> None:
        super().__init__(codigo, nombre, categoria, precio)
        self.tamanio = tamanio

    @property
    def tamanio(self) -> str:
        return self._tamanio

    @tamanio.setter
    def tamanio(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El tamaño de la bebida no puede estar vacío.")
        self._tamanio = valor.strip()

    def mostrar_informacion(self) -> None:
        """Sobrescribe el método para mostrar información específica de la bebida."""
        super().mostrar_informacion()
        print(f"  Tamaño: {self.tamanio}")

    def __str__(self) -> str:
        return (f"Bebida: {self.nombre} - {self.tamanio} - "
                f"${self.precio:.2f}")

    def __repr__(self) -> str:
        return (f"Bebida(codigo='{self.codigo}', nombre='{self.nombre}', "
                f"categoria='{self.categoria}', precio={self.precio}, "
                f"tamanio='{self.tamanio}')")
