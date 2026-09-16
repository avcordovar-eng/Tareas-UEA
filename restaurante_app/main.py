#!/usr/bin/env python3
"""Punto de entrada de la aplicación gráfica restaurante_app.

Responsabilidades de este archivo:

1. Preparar los servicios: ArchivoServicio lee los datos locales y
   RestauranteServicio los convierte en objetos.
2. Crear una única ventana principal de Tkinter.
3. Entregar el servicio como dependencia a las vistas LoginView y MainView.
4. Controlar el cambio entre la pantalla de acceso y el panel principal
   dentro de esa misma ventana.

No contiene reglas del restaurante ni lectura de archivos: solo conecta
las piezas y ejecuta un único mainloop().
"""

import tkinter as tk

from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui import COLOR_FONDO, configurar_estilos
from ui.login_view import LoginView
from ui.main_view import MainView

NOMBRE_RESTAURANTE: str = "Restaurante El Buen Sabor"
ANCHO_VENTANA: int = 1060
ALTO_VENTANA: int = 640


class AplicacionRestaurante:
    """Coordina la ventana principal y el cambio entre las vistas.

    Crea LoginView y MainView una sola vez sobre la misma ventana y las
    superpone en la misma celda: mostrar una u otra consiste en traerla al
    frente, de modo que la aplicación conserva una única ventana y un
    único ciclo de ejecución.

    Args:
        ventana: Ventana principal de Tkinter creada en main().
        restaurante_servicio: Servicio que se entrega a ambas vistas.
    """

    def __init__(self, ventana: tk.Tk,
                 restaurante_servicio: RestauranteServicio) -> None:
        self.ventana: tk.Tk = ventana
        self._servicio: RestauranteServicio = restaurante_servicio

        self._configurar_ventana()

        self._login_view = LoginView(ventana, restaurante_servicio,
                                     self.mostrar_principal)
        self._main_view = MainView(ventana, restaurante_servicio,
                                   self.cerrar_sesion)
        for vista in (self._main_view, self._login_view):
            vista.grid(row=0, column=0, sticky="nsew")

        self.mostrar_login()

    def _configurar_ventana(self) -> None:
        """Define los estilos, el título, el tamaño y la posición de la ventana.

        Los estilos se registran antes de construir las vistas, porque los
        componentes ttk necesitan que su estilo exista al crearse.
        """
        configurar_estilos()
        self.ventana.title(f"{self._servicio.nombre} - Sistema de gestión")
        self.ventana.configure(bg=COLOR_FONDO)
        self.ventana.minsize(960, 580)
        self.ventana.rowconfigure(0, weight=1)
        self.ventana.columnconfigure(0, weight=1)

        posicion_x = (self.ventana.winfo_screenwidth() - ANCHO_VENTANA) // 2
        posicion_y = (self.ventana.winfo_screenheight() - ALTO_VENTANA) // 3
        self.ventana.geometry(
            f"{ANCHO_VENTANA}x{ALTO_VENTANA}+{max(posicion_x, 0)}+{max(posicion_y, 0)}"
        )

    def mostrar_login(self) -> None:
        """Muestra la pantalla de acceso con los campos vacíos."""
        self._login_view.limpiar()
        self._login_view.tkraise()
        self._login_view.enfocar()

    def mostrar_principal(self, usuario: Usuario) -> None:
        """Muestra el panel principal con la sesión de la persona autenticada.

        Args:
            usuario: Usuario que LoginView obtuvo del servicio al validar
                correctamente las credenciales.
        """
        self._main_view.establecer_usuario(usuario)
        self._main_view.tkraise()

    def cerrar_sesion(self) -> None:
        """Regresa a la pantalla de acceso sin cerrar la ventana principal."""
        self.mostrar_login()


def preparar_servicio() -> RestauranteServicio:
    """Crea los servicios y carga en memoria los datos locales.

    ArchivoServicio se entrega a RestauranteServicio como dependencia: así
    el servicio puede guardar los productos después de cada operación sin
    que las vistas intervengan en la persistencia.

    Returns:
        El RestauranteServicio listo para entregarse a las vistas.
    """
    archivo_servicio = ArchivoServicio()
    restaurante_servicio = RestauranteServicio(NOMBRE_RESTAURANTE, archivo_servicio)

    productos_cargados = restaurante_servicio.cargar_productos(
        archivo_servicio.leer_productos()
    )
    usuarios_cargados = restaurante_servicio.cargar_usuarios(
        archivo_servicio.leer_usuarios()
    )
    print(f"Datos cargados: {productos_cargados} productos y "
          f"{usuarios_cargados} usuarios.")
    return restaurante_servicio


def main() -> None:
    """Prepara las dependencias, inicia la interfaz y ejecuta la aplicación."""
    restaurante_servicio = preparar_servicio()
    ventana = tk.Tk()
    AplicacionRestaurante(ventana, restaurante_servicio)
    ventana.mainloop()


if __name__ == "__main__":
    main()
