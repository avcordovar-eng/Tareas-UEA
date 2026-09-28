"""Módulo que define la clase Venta del restaurante."""

from datetime import datetime


class Venta:
    """Representa una venta registrada en el restaurante.

    Relaciona a un usuario con un producto y guarda la fecha en que se
    realizó la operación. Es el registro histórico que produce la sección
    de Ventas de la interfaz: esta etapa solo busca demostrar el flujo
    básico de manejo de eventos sobre una operación real del restaurante,
    por lo que el modelo no calcula totales ni administra más de un
    producto por venta.

    Attributes:
        usuario_identificacion (str): Identificación del usuario que
            registró la venta.
        producto_codigo (str): Código del producto vendido.
        fecha (str): Fecha y hora de la venta, en formato "AAAA-MM-DD HH:MM".
    """

    def __init__(self, usuario_identificacion: str, producto_codigo: str,
                 fecha: str | None = None) -> None:
        self.usuario_identificacion = usuario_identificacion
        self.producto_codigo = producto_codigo
        self.fecha = fecha if fecha else datetime.now().strftime("%Y-%m-%d %H:%M")

    @property
    def usuario_identificacion(self) -> str:
        return self._usuario_identificacion

    @usuario_identificacion.setter
    def usuario_identificacion(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La venta debe indicar el usuario que la registra.")
        self._usuario_identificacion = valor.strip()

    @property
    def producto_codigo(self) -> str:
        return self._producto_codigo

    @producto_codigo.setter
    def producto_codigo(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La venta debe indicar el producto vendido.")
        self._producto_codigo = valor.strip()

    @property
    def fecha(self) -> str:
        return self._fecha

    @fecha.setter
    def fecha(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La venta debe registrar una fecha.")
        self._fecha = valor.strip()

    def a_diccionario(self) -> dict[str, object]:
        """Convierte la venta a un diccionario con el formato del JSON."""
        return {
            "usuario_identificacion": self.usuario_identificacion,
            "producto_codigo": self.producto_codigo,
            "fecha": self.fecha,
        }

    @classmethod
    def desde_diccionario(cls, registro: dict[str, object]) -> "Venta":
        """Reconstruye un objeto Venta a partir de un diccionario.

        Args:
            registro: Diccionario con las claves usuario_identificacion,
                producto_codigo y fecha. Si falta una clave obligatoria se
                propaga un KeyError; si un valor no es válido se propaga un
                ValueError o un TypeError.

        Returns:
            Una nueva instancia de Venta con los datos del registro.
        """
        return cls(
            usuario_identificacion=str(registro["usuario_identificacion"]),
            producto_codigo=str(registro["producto_codigo"]),
            fecha=str(registro["fecha"]),
        )

    def __str__(self) -> str:
        return (f"Venta del producto {self.producto_codigo} registrada por "
                f"{self.usuario_identificacion} el {self.fecha}")

    def __repr__(self) -> str:
        return (f"Venta(usuario_identificacion='{self.usuario_identificacion}', "
                f"producto_codigo='{self.producto_codigo}', fecha='{self.fecha}')")
