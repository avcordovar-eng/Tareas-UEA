"""Módulo que define la clase Platillo del restaurante.

Esta clase representa un platillo (comida) del menú del restaurante,
implementando constructor tradicional, propiedades, herencia y polimorfismo.
"""

from ..producto import Producto
class Platillo(Producto):
    """Clase que representa un platillo del restaurante, heredando de Producto.

    Attributes:
        tiempo_preparacion (int): Tiempo de preparación en minutos.
        ingredientes (list[str]): Lista de ingredientes del platillo.
    """

    def __init__(
        self,
        nombre: str,
        categoria: str,
        precio: float,
        tiempo_preparacion: int,
        ingredientes: list[str],
        disponible: bool = True,
    ) -> None:
        """Inicializa un nuevo platillo.

        Args:
            nombre: Nombre del platillo.
            categoria: Categoría del platillo.
            precio: Precio del platillo.
            tiempo_preparacion: Tiempo de preparación en minutos.
            ingredientes: Lista de ingredientes del platillo.
            disponible: Disponibilidad del platillo (por defecto True).
        """
        super().__init__(nombre, categoria, precio, disponible)
        self.tiempo_preparacion = tiempo_preparacion
        self.ingredientes = ingredientes

    @property
    def tiempo_preparacion(self) -> int:
        """Getter para el tiempo de preparación."""
        return self._tiempo_preparacion

    @tiempo_preparacion.setter
    def tiempo_preparacion(self, valor: int) -> None:
        """Setter para el tiempo de preparación con validación."""
        if valor < 0:
            raise ValueError("El tiempo de preparación no puede ser negativo.")
        self._tiempo_preparacion = int(valor)

    @property
    def ingredientes(self) -> list[str]:
        """Getter para la lista de ingredientes."""
        return self._ingredientes

    @ingredientes.setter
    def ingredientes(self, valor: list[str]) -> None:
        """Setter para los ingredientes con validación."""
        if not valor or not isinstance(valor, list):
            raise ValueError("La lista de ingredientes no puede estar vacía.")
        self._ingredientes = [ing.strip() for ing in valor if ing.strip()]

    def mostrar_informacion(self) -> None:
        """Sobrescribe el método para mostrar información específica del platillo."""
        print(f"Nombre del platillo: {self.nombre}")
        super().mostrar_informacion()
        print(f"  Tiempo de preparación: {self.tiempo_preparacion} min")
        print(f"  Ingredientes: {', '.join(self.ingredientes)}")
        print("-" * 40)

    def __str__(self) -> str:
        """Representación en cadena del platillo."""
        return (f"Platillo: {self.nombre} - ${self.precio:.2f} - "
                f"{self.tiempo_preparacion} min - {len(self.ingredientes)} ingredientes")

    def __repr__(self) -> str:
        """Representación oficial del objeto Platillo."""
        return (f"Platillo(nombre='{self.nombre}', categoria='{self.categoria}', "
                f"precio={self.precio}, tiempo_preparacion={self.tiempo_preparacion}, "
                f"ingredientes={self.ingredientes}, disponible={self.disponible})")