"""Paquete de modelos del restaurante.

Contiene las entidades del dominio: Producto, Usuario y Venta.
"""

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

__all__ = ["Producto", "Usuario", "Venta"]
