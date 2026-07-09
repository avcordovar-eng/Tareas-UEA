"""Módulo que define la clase Cliente del restaurante.

Esta clase representa un cliente del restaurante,
implementando con el decorador @dataclass
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Cliente:
    """Clase que representa un cliente del restaurante.

    Attributes:
        nombre (str): Nombre del cliente.
        correo (str): Correo electrónico del cliente.
        id_cliente (int): Identificador único del cliente.
    """

    nombre: str
    correo: str
    id_cliente: int

    def mostrar_informacion(self) -> None:
        """Muestra la información del cliente de forma legible."""
        print(f"  Nombre: {self.nombre}")
        print(f"  Correo: {self.correo}")
        print(f"  ID Cliente: {self.id_cliente}")
        print("-" * 30)

    def __str__(self) -> str:
        """Representación en cadena del cliente."""
        return f"{self.nombre} ({self.correo}) - ID: {self.id_cliente}"

    def __repr__(self) -> str:
        """Representación oficial del objeto Cliente."""
        return (f"Cliente(nombre='{self.nombre}', correo='{self.correo}', "
                f"id_cliente={self.id_cliente})")