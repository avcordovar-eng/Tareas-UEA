"""Módulo que define la clase Producto del restaurante."""


class Producto:
    """Clase base que representa un producto general del restaurante.

    Attributes:
        codigo (str): Código único del producto.
        nombre (str): Nombre del producto.
        categoria (str): Categoría del producto.
        precio (float): Precio del producto.
    """

    def __init__(self, codigo: str, nombre: str, categoria: str, precio: float) -> None:
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio

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
        if valor <= 0:
            raise ValueError("El precio del producto debe ser mayor que cero.")
        self._precio = float(valor)

    def a_diccionario(self) -> dict[str, object]:
        """Convierte el producto a un diccionario para persistirlo en JSON."""
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
        }

    @classmethod
    def desde_diccionario(cls, registro: dict[str, object]) -> "Producto":
        """Reconstruye un objeto Producto a partir de un diccionario.

        Args:
            registro: Diccionario con las claves codigo, nombre, categoria y
                precio. Si falta alguna clave se propaga un KeyError; si algún
                valor no es válido se propaga un ValueError o TypeError.

        Returns:
            Una nueva instancia de Producto con los datos del registro.
        """
        return cls(
            codigo=str(registro["codigo"]),
            nombre=str(registro["nombre"]),
            categoria=str(registro["categoria"]),
            precio=float(registro["precio"]),
        )

    def mostrar_informacion(self) -> None:
        """Muestra la información del producto."""
        print(f"  Código: {self.codigo}")
        print(f"  Nombre: {self.nombre}")
        print(f"  Categoría: {self.categoria}")
        print(f"  Precio: ${self.precio:.2f}")

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nombre} (${self.precio:.2f})"

    def __repr__(self) -> str:
        return (f"Producto(codigo='{self.codigo}', nombre='{self.nombre}', "
                f"categoria='{self.categoria}', precio={self.precio})")
