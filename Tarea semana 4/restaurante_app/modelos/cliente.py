# -*- coding: utf-8 -*-
from modelos.producto import Producto

class Cliente:
    """
    Clase que representa un cliente en el restaurante.
    """
    def __init__(self, nombre: str, mesa: int):
        """
        Constructor de la clase Cliente.
        
        :param nombre: Nombre completo del cliente.
        :param mesa: Número de mesa asignada al cliente.
        """
        self.nombre = nombre
        self.mesa = mesa
        self.pedidos = []  # Lista que contendrá los productos ordenados

    def agregar_pedido(self, producto: Producto):
        """
        Agrega un producto a la lista de consumo del cliente.
        
        :param producto: Objeto de la clase Producto.
        """
        self.pedidos.append(producto)

    def obtener_total(self) -> float:
        """
        Calcula la suma total de los precios de los productos ordenados.
        
        :return: Total acumulado a pagar.
        """
        return sum(producto.precio for producto in self.pedidos)

    def __str__(self) -> str:
        """
        Retorna la representación en formato de texto legible del cliente.
        """
        return f"Cliente: {self.nombre} (Mesa {self.mesa})"
