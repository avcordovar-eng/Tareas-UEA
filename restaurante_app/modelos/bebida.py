"""Módulo que define la clase Bebida del restaurante.

Esta clase representa una bebida del menú del restaurante,
implementando constructor tradicional, propiedades, herencia y polimorfismo.
"""

from ..producto import Producto
class Bebida(Producto):
    """Clase que representa una bebida del restaurante, heredando de Producto.

    Attributes:
        volumen_ml (int): Volumen de la bebida en mililitros.
    """

    def __init__(
        self,
        nombre: str,
        categoria: str,
        precio: float,
        volumen_ml: int,
        disponible: bool = True,
    ) -> None:
        """Inicializa una nueva bebida.

        Args:
            nombre: Nombre de la bebida.
            categoria: Categoría de la bebida.
            precio: Precio de la bebida.
            volumen_ml: Volumen de la bebida en ml.
            disponible: Disponibilidad de la bebida (por defecto True).
        """
        super().__init__(nombre, categoria, precio, disponible)
        self.volumen_ml = volumen_ml

    @property
    def volumen_ml(self) -> int:
        """Getter para el volumen de la bebida."""
        return self._volumen_ml

    @volumen_ml.setter
    def volumen_ml(self, valor: int) -> None:
        """Setter para el volumen de la bebida con validación."""
        if valor <= 0:
            raise ValueError("El volumen de la bebida debe ser mayor que cero.")
        self._volumen_ml = int(valor)

    def mostrar_informacion(self) -> None:
        """Sobrescribe el método para mostrar información específica de la bebida."""
        print(f"BEBIDA: {self.nombre}")
        super().mostrar_informacion()
        print(f"  Volumen: {self.volumen_ml} ml")
        print("-" * 40)

    def __str__(self) -> str:
        """Representación en cadena de la bebida."""
        return (f"Bebida: {self.nombre} - ${self.precio:.2f} - "
                f"{self.volumen_ml} ml")

    def __repr__(self) -> str:
        """Representación oficial del objeto Bebida."""
        return (f"Bebida(nombre='{self.nombre}', categoria='{self.categoria}', "
                f"precio={self.precio}, volumen_ml={self.volumen_ml}, "
                f"disponible={self.disponible})")