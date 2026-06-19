# -*- coding: utf-8 -*-
from modelos.producto import Producto
from modelos.cliente import Cliente

class Restaurante:
    """
    Clase de servicio que gestiona las operaciones generales del restaurante,
    como el menú y el registro de clientes.
    """
    def __init__(self, nombre: str):
        """
        Constructor de la clase Restaurante.
        
        :param nombre: Nombre comercial del restaurante.
        """
        self.nombre = nombre
        self.menu = []        # Catálogo de productos disponibles
        self.clientes = []    # Clientes registrados actualmente

    def agregar_al_menu(self, producto: Producto):
        """
        Agrega un nuevo producto al catálogo del menú del restaurante.
        
        :param producto: Objeto de tipo Producto.
        """
        self.menu.append(producto)

    def registrar_cliente(self, cliente: Cliente):
        """
        Registra a un cliente en el sistema para realizar el seguimiento de sus pedidos.
        
        :param cliente: Objeto de tipo Cliente.
        """
        self.clientes.append(cliente)

    def mostrar_menu(self):
        """
        Muestra en consola el catálogo de productos disponibles de manera organizada.
        """
        print("\n" + "=" * 50)
        print(f" MENU DE: {self.nombre.upper()} ".center(50, "="))
        print("=" * 50)
        if not self.menu:
            print("El menú está vacío por el momento.")
        else:
            for prod in self.menu:
                print(f" - {prod}")
        print("=" * 50)

    def mostrar_estado_clientes(self):
        """
        Muestra el consumo actual de todos los clientes registrados y el total a pagar.
        """
        print("\n" + "=" * 50)
        print(" CONSUMO ACTUAL DE CLIENTES ".center(50, "="))
        print("=" * 50)
        if not self.clientes:
            print("No hay clientes registrados en el sistema.")
        else:
            for cli in self.clientes:
                print(f"\n{cli}")
                if not cli.pedidos:
                    print("   > Sin consumos registrados.")
                else:
                    print("   Consumos:")
                    for ped in cli.pedidos:
                        print(f"     - {ped.nombre:<20} ${ped.precio:>6.2f}")
                    print(f"   {"-" * 32}")
                    print(f"   Total a pagar:       ${cli.obtener_total():>6.2f}")
        print("\n" + "=" * 50)

    def __str__(self) -> str:
        """
        Retorna la representación en formato de texto legible del restaurante.
        """
        return f"Restaurante: {self.nombre}"
