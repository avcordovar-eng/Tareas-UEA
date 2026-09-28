"""Módulo que define la clase Producto del restaurante."""


class Producto:
    """Representa un producto disponible en el restaurante.

    En esta primera versión gráfica el producto es una entidad de solo
    consulta: se reconstruye desde datos/productos.json y se muestra en la
    interfaz principal. Las operaciones de venta se incorporarán en etapas
    posteriores de la unidad.

    Attributes:
        codigo (str): Código único del producto.
        nombre (str): Nombre del producto.
        categoria (str): Categoría a la que pertenece el producto.
        precio (float): Precio unitario del producto.
        cantidad (int): Cantidad disponible del producto.
    """

    def __init__(self, codigo: str, nombre: str, categoria: str,
                 precio: float, cantidad: int = 0) -> None:
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.cantidad = cantidad

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El código del producto no puede estar vacío.")
        self._codigo = valor.strip()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def categoria(self) -> str:
        return self._categoria

    @categoria.setter
    def categoria(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La categoría del producto no puede estar vacía.")
        self._categoria = valor.strip()

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        if float(valor) <= 0:
            raise ValueError("El precio del producto debe ser mayor que cero.")
        self._precio = float(valor)

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        if int(valor) < 0:
            raise ValueError("La cantidad del producto no puede ser negativa.")
        self._cantidad = int(valor)

    @property
    def disponible(self) -> bool:
        """Indica si el producto tiene existencias para atender un pedido."""
        return self.cantidad > 0

    def a_diccionario(self) -> dict[str, object]:
        """Convierte el producto a un diccionario con el formato del JSON."""
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "cantidad": self.cantidad,
        }

    @classmethod
    def desde_diccionario(cls, registro: dict[str, object]) -> "Producto":
        """Reconstruye un objeto Producto a partir de un diccionario.

        Args:
            registro: Diccionario con las claves codigo, nombre, categoria,
                precio y cantidad. Si falta una clave obligatoria se propaga
                un KeyError; si un valor no es válido se propaga un
                ValueError o un TypeError.

        Returns:
            Una nueva instancia de Producto con los datos del registro.
        """
        return cls(
            codigo=str(registro["codigo"]),
            nombre=str(registro["nombre"]),
            categoria=str(registro["categoria"]),
            precio=float(registro["precio"]),
            cantidad=int(registro.get("cantidad", 0)),
        )

    def __str__(self) -> str:
        return (f"{self.codigo} - {self.nombre} ({self.categoria}) - "
                f"${self.precio:.2f} - Cantidad: {self.cantidad}")

    def __repr__(self) -> str:
        return (f"Producto(codigo='{self.codigo}', nombre='{self.nombre}', "
                f"categoria='{self.categoria}', precio={self.precio}, "
                f"cantidad={self.cantidad})")
