"""Módulo que define la clase Producto del restaurante.

Esta clase representa un producto del menú del restaurante,
implementando constructor tradicional, propiedades y validaciones.
"""


class Producto:
    """Clase que representa un producto del restaurante.

    Attributes:
        nombre (str): Nombre del producto.
        categoria (str): Categoría del producto (ej. Entrada, Plato Principal, Bebida).
        precio (float): Precio del producto (debe ser > 0).
        disponible (bool): Disponibilidad del producto en el menú.
    """

    def __init__(self, nombre: str, categoria: str, precio: float, disponible: bool = True) -> None:
        """Inicializa un nuevo producto con validaciones.

        Args:
            nombre: Nombre del producto (no puede estar vacío).
            categoria: Categoría del producto (no puede estar vacía).
            precio: Precio del producto (debe ser mayor a 0).
            disponible: Disponibilidad del producto (por defecto True).

        Raises:
            ValueError: Si nombre o categoría están vacíos, o precio <= 0.
        """
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.disponible = disponible

    @property
    def nombre(self) -> str:
        """Getter para el nombre del producto."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Setter para el nombre con validación de no vacío."""
        if not valor or not valor.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def categoria(self) -> str:
        """Getter para la categoría del producto."""
        return self._categoria

    @categoria.setter
    def categoria(self, valor: str) -> None:
        """Setter para la categoría con validación de no vacío."""
        if not valor or not valor.strip():
            raise ValueError("La categoría del producto no puede estar vacía.")
        self._categoria = valor.strip()

    @property
    def precio(self) -> float:
        """Getter para el precio del producto."""
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        """Setter para el precio con validación de valor positivo."""
        if valor <= 0:
            raise ValueError("El precio del producto debe ser mayor que cero.")
        self._precio = float(valor)

    @property
    def disponible(self) -> bool:
        """Getter para la disponibilidad del producto."""
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        """Setter para la disponibilidad."""
        self._disponible = bool(valor)

    def mostrar_informacion(self) -> None:
        """Muestra la información del producto de forma legible."""
        estado = "Disponible" if self.disponible else "No disponible"
        print(f"  Nombre: {self.nombre}")
        print(f"  Categoría: {self.categoria}")
        print(f"  Precio: ${self.precio:.2f}")
        print(f"  Estado: {estado}")
        print("-" * 30)

    def __str__(self) -> str:
        """Representación en cadena del producto."""
        estado = "Disponible" if self.disponible else "No disponible"
        return f"{self.nombre} ({self.categoria}) - ${self.precio:.2f} - {estado}"

    def __repr__(self) -> str:
        """Representación oficial del objeto Producto."""
        return (f"Producto(nombre='{self.nombre}', categoria='{self.categoria}', "
                f"precio={self.precio}, disponible={self.disponible})")