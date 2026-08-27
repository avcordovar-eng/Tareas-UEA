"""Módulo que define la clase Venta del restaurante."""


class Venta:
    """Clase que representa una venta realizada en el restaurante.

    Relaciona a un usuario con un producto vendido y la cantidad.

    Attributes:
        usuario_id (str): Identificación del usuario que realizó la compra.
        producto_codigo (str): Código del producto vendido.
        cantidad (int): Cantidad del producto vendida.
    """

    def __init__(
        self,
        usuario_id: str,
        producto_codigo: str,
        cantidad: int
    ) -> None:
        self.usuario_id = usuario_id
        self.producto_codigo = producto_codigo
        self.cantidad = cantidad

    @property
    def usuario_id(self) -> str:
        return self._usuario_id

    @usuario_id.setter
    def usuario_id(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El ID del usuario no puede estar vacío.")
        self._usuario_id = valor.strip()

    @property
    def producto_codigo(self) -> str:
        return self._producto_codigo

    @producto_codigo.setter
    def producto_codigo(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El código del producto no puede estar vacío.")
        self._producto_codigo = valor.strip()

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        if valor <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
        self._cantidad = int(valor)

    def a_diccionario(self) -> dict[str, object]:
        """Convierte la venta a un diccionario para persistirla en JSON."""
        return {
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "cantidad": self.cantidad,
        }

    @classmethod
    def desde_diccionario(cls, registro: dict[str, object]) -> "Venta":
        """Reconstruye un objeto Venta a partir de un diccionario.

        Args:
            registro: Diccionario con las claves usuario_id, producto_codigo
                y cantidad. Si falta alguna clave se propaga un KeyError; si
                algún valor no es válido se propaga un ValueError o TypeError.

        Returns:
            Una nueva instancia de Venta con los datos del registro.
        """
        return cls(
            usuario_id=str(registro["usuario_id"]),
            producto_codigo=str(registro["producto_codigo"]),
            cantidad=int(registro["cantidad"]),
        )

    def __str__(self) -> str:
        return (f"Venta(usuario={self.usuario_id}, producto={self.producto_codigo}, "
                f"cantidad={self.cantidad})")

    def __repr__(self) -> str:
        return (f"Venta(usuario_id='{self.usuario_id}', "
                f"producto_codigo='{self.producto_codigo}', cantidad={self.cantidad})")