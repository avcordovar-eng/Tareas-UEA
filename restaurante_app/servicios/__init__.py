"""Paquete de servicios del restaurante.

ArchivoServicio lee y guarda los datos locales; RestauranteServicio los
convierte en objetos, aplica las reglas del restaurante y resuelve las
operaciones que solicitan las vistas, incluyendo el registro de ventas.
"""

from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import (
    RestauranteServicio,
    ResultadoAcceso,
    ResultadoOperacion,
    ResultadoVenta,
)

__all__ = [
    "ArchivoServicio",
    "RestauranteServicio",
    "ResultadoAcceso",
    "ResultadoOperacion",
    "ResultadoVenta",
]
