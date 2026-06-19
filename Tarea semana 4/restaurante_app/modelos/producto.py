# -*- coding: utf-8 -*-

class Producto:
    """
    Clase que representa un producto disponible en el menú del restaurante.
    """
    def __init__(self, nombre: str, precio: float, categoria: str):
        """
        Constructor de la clase Producto.
        
        :param nombre: Nombre del plato, bebida o postre.
        :param precio: Precio de venta del producto.
        :param categoria: Categoría a la que pertenece (Entrada, Plato Fuerte, Bebida, Postre, etc.).
        """
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria

    def __str__(self) -> str:
        """
        Retorna la representación en formato de texto legible del producto.
        """
        return f"[{self.categoria}] {self.nombre} - ${self.precio:.2f}"
