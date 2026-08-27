"""Módulo que define la clase Producto del restaurante."""


class Producto:
    """Clase base que representa un producto general del restaurante.

    Attributes:
        codigo (str): Código único del producto.
        nombre (str): Nombre del producto.
        categoria (str): Categoría del producto.
        precio (float): Precio del producto.
        stock (int): Cantidad disponible del producto.
    """

    def __init__(self, codigo: str, nombre: str, categoria: str, precio: float, stock: int = 0) -> None:
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock

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

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, valor: int) -> None:
        if valor < 0:
            raise ValueError("El stock del producto no puede ser negativo.")
        self._stock = int(valor)

    def vender(self, cantidad: int) -> bool:
        """Disminuye el stock si hay suficiente cantidad disponible.

        Args:
            cantidad: Cantidad a vender.

        Returns:
            True si se pudo vender, False si no hay stock suficiente.
        """
        if cantidad <= 0 or self.stock < cantidad:
            return False
        self.stock -= cantidad
        return True

    def a_diccionario(self) -> dict[str, object]:
        """Convierte el producto a un diccionario para persistirlo en JSON."""
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock,
        }

    @classmethod
    def desde_diccionario(cls, registro: dict[str, object]) -> "Producto":
        """Reconstruye un objeto Producto a partir de un diccionario.

        Args:
            registro: Diccionario con las claves codigo, nombre, categoria,
                precio y stock. Si falta alguna clave se propaga un KeyError;
                si algún valor no es válido se propaga un ValueError o TypeError.

        Returns:
            Una nueva instancia de Producto con los datos del registro.
        """
        return cls(
            codigo=str(registro["codigo"]),
            nombre=str(registro["nombre"]),
            categoria=str(registro["categoria"]),
            precio=float(registro["precio"]),
            stock=int(registro.get("stock", 0)),
        )

    def mostrar_informacion(self) -> None:
        """Muestra la información del producto."""
        print(f"  Código: {self.codigo}")
        print(f"  Nombre: {self.nombre}")
        print(f"  Categoría: {self.categoria}")
        print(f"  Precio: ${self.precio:.2f}")
        print(f"  Stock: {self.stock}")

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nombre} (${self.precio:.2f}) - Stock: {self.stock}"

    def __repr__(self) -> str:
        return (f"Producto(codigo='{self.codigo}', nombre='{self.nombre}', "
                f"categoria='{self.categoria}', precio={self.precio}, stock={self.stock})")
