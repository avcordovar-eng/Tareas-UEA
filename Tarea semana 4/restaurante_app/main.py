# -*- coding: utf-8 -*-
import sys
import os

# Asegurar que el directorio raíz del proyecto esté en el path de búsqueda de módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modelos.producto import Producto
from modelos.cliente import Cliente
from servicios.restaurante import Restaurante

def main():
    # 1. Instanciar el servicio principal (el restaurante)
    mi_restaurante = Restaurante("El Portal del Sabor")
    print(f"=== Iniciando el sistema para: {mi_restaurante} ===\n")

    # 2. Crear instancias de productos (platos, bebidas, postres)
    cebiche = Producto("Cebiche Mixto", 12.50, "Plato Fuerte")
    lomo = Producto("Lomo Fino a la Parrilla", 15.00, "Plato Fuerte")
    limonada = Producto("Limonada Imperial", 2.50, "Bebida")
    pilsener = Producto("Cerveza Pilsener", 3.00, "Bebida")
    tres_leches = Producto("Postre Tres Leches", 4.00, "Postre")
    empanadas = Producto("Empanadas de Viento", 3.50, "Entrada")

    # 3. Registrar los productos en el catálogo del restaurante
    mi_restaurante.agregar_al_menu(cebiche)
    mi_restaurante.agregar_al_menu(lomo)
    mi_restaurante.agregar_al_menu(limonada)
    mi_restaurante.agregar_al_menu(pilsener)
    mi_restaurante.agregar_al_menu(tres_leches)
    mi_restaurante.agregar_al_menu(empanadas)

    # 4. Crear instancias de clientes indicando nombre y mesa
    cliente1 = Cliente("Carlos Mendoza", 3)
    cliente2 = Cliente("Maria Augusta Torres", 7)
    cliente3 = Cliente("Juan Carlos Perez", 1)  # Cliente sin pedidos para demostrar manejo de casos

    # 5. Registrar los clientes en el sistema
    mi_restaurante.registrar_cliente(cliente1)
    mi_restaurante.registrar_cliente(cliente2)
    mi_restaurante.registrar_cliente(cliente3)

    # 6. Registrar pedidos consumidos por los clientes
    # Carlos Mendoza pide un Cebiche, una Pilsener y un Tres Leches
    cliente1.agregar_pedido(cebiche)
    cliente1.agregar_pedido(pilsener)
    cliente1.agregar_pedido(tres_leches)

    # María Augusta Torres pide Empanadas, un Lomo y una Limonada
    cliente2.agregar_pedido(empanadas)
    cliente2.agregar_pedido(lomo)
    cliente2.agregar_pedido(limonada)

    # 7. Mostrar la información en consola de forma ordenada
    # Mostrar el menú del restaurante
    mi_restaurante.mostrar_menu()

    # Mostrar la cuenta de los clientes registrados y sus consumos
    mi_restaurante.mostrar_estado_clientes()

if __name__ == "__main__":
    main()
