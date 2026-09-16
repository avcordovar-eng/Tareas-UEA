"""Módulo que define la pantalla de acceso de la aplicación."""

import tkinter as tk
from collections.abc import Callable

from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio
from ui import (
    COLOR_BORDE,
    COLOR_ERROR,
    COLOR_EXITO,
    COLOR_FONDO,
    COLOR_PANEL,
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_OSCURO,
    COLOR_TEXTO,
    COLOR_TEXTO_CLARO,
    COLOR_TEXTO_SUAVE,
    FUENTE_BASE,
    FUENTE_BOTON,
    FUENTE_PEQUENA,
    FUENTE_SUBTITULO,
    FUENTE_TITULO,
)


class LoginView(tk.Frame):
    """Pantalla de acceso simulado al sistema del restaurante.

    Solicita un usuario y una contraseña, entrega esos datos a
    RestauranteServicio y muestra el mensaje que el servicio devuelve. La
    vista no conoce las credenciales ni lee archivos: únicamente presenta
    los componentes y comunica el resultado a la aplicación.

    Args:
        master: Ventana o contenedor donde se coloca la vista.
        restaurante_servicio: Servicio que valida el acceso.
        al_ingresar: Función que la aplicación ejecuta cuando el acceso es
            correcto; recibe el usuario autenticado.
    """

    def __init__(self, master: tk.Misc, restaurante_servicio: RestauranteServicio,
                 al_ingresar: Callable[[Usuario], None]) -> None:
        super().__init__(master, bg=COLOR_FONDO)
        self._servicio: RestauranteServicio = restaurante_servicio
        self._al_ingresar: Callable[[Usuario], None] = al_ingresar

        self._usuario_var: tk.StringVar = tk.StringVar()
        self._contrasena_var: tk.StringVar = tk.StringVar()
        self._mensaje_var: tk.StringVar = tk.StringVar(value="")

        self._construir_interfaz()

    # --- CONSTRUCCIÓN DE LA INTERFAZ ---
    def _construir_interfaz(self) -> None:
        """Arma la tarjeta de acceso centrada en la ventana."""
        self.rowconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        tarjeta = tk.Frame(self, bg=COLOR_PANEL, highlightbackground=COLOR_BORDE,
                           highlightthickness=1, padx=36, pady=28)
        tarjeta.grid(row=1, column=0)
        tarjeta.columnconfigure(0, weight=1)

        tk.Label(tarjeta, text=self._servicio.nombre, font=FUENTE_TITULO,
                 bg=COLOR_PANEL, fg=COLOR_PRIMARIO).grid(row=0, column=0, sticky="w")
        tk.Label(tarjeta, text="Acceso al sistema", font=FUENTE_SUBTITULO,
                 bg=COLOR_PANEL, fg=COLOR_TEXTO_SUAVE).grid(row=1, column=0,
                                                            sticky="w", pady=(2, 16))
        tk.Frame(tarjeta, bg=COLOR_BORDE, height=1).grid(row=2, column=0,
                                                         sticky="ew", pady=(0, 18))

        tk.Label(tarjeta, text="Usuario", font=FUENTE_BASE, bg=COLOR_PANEL,
                 fg=COLOR_TEXTO).grid(row=3, column=0, sticky="w")
        self._entrada_usuario = tk.Entry(tarjeta, textvariable=self._usuario_var,
                                         font=FUENTE_BASE, width=30, relief="solid",
                                         bd=1, bg=COLOR_PANEL, fg=COLOR_TEXTO,
                                         insertbackground=COLOR_TEXTO)
        self._entrada_usuario.grid(row=4, column=0, sticky="ew", ipady=5, pady=(4, 12))

        tk.Label(tarjeta, text="Contraseña", font=FUENTE_BASE, bg=COLOR_PANEL,
                 fg=COLOR_TEXTO).grid(row=5, column=0, sticky="w")
        self._entrada_contrasena = tk.Entry(tarjeta, textvariable=self._contrasena_var,
                                            font=FUENTE_BASE, width=30, show="•",
                                            relief="solid", bd=1, bg=COLOR_PANEL,
                                            fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO)
        self._entrada_contrasena.grid(row=6, column=0, sticky="ew", ipady=5, pady=(4, 10))

        self._etiqueta_mensaje = tk.Label(tarjeta, textvariable=self._mensaje_var,
                                          font=FUENTE_PEQUENA, bg=COLOR_PANEL,
                                          fg=COLOR_ERROR, wraplength=300,
                                          justify="left", height=2, anchor="w")
        self._etiqueta_mensaje.grid(row=7, column=0, sticky="ew")

        self._boton_ingresar = tk.Button(tarjeta, text="Ingresar", font=FUENTE_BOTON,
                                         bg=COLOR_PRIMARIO, fg=COLOR_TEXTO_CLARO,
                                         activebackground=COLOR_PRIMARIO_OSCURO,
                                         activeforeground=COLOR_TEXTO_CLARO,
                                         relief="flat", cursor="hand2",
                                         command=self._intentar_ingreso)
        self._boton_ingresar.grid(row=8, column=0, sticky="ew", ipady=7, pady=(6, 14))

        tk.Label(tarjeta,
                 text="Acceso simulado con fines académicos.\n"
                      "Usuario de prueba: admin  /  Contraseña: admin123",
                 font=FUENTE_PEQUENA, bg=COLOR_PANEL, fg=COLOR_TEXTO_SUAVE,
                 justify="left").grid(row=9, column=0, sticky="w")

        # La tecla Enter equivale a presionar el botón Ingresar.
        self._entrada_usuario.bind("<Return>", self._al_presionar_enter)
        self._entrada_contrasena.bind("<Return>", self._al_presionar_enter)

    # --- ACCIONES DE LA VISTA ---
    def _al_presionar_enter(self, evento: "tk.Event[tk.Entry]") -> None:
        """Permite confirmar el acceso con la tecla Enter."""
        self._intentar_ingreso()

    def _intentar_ingreso(self) -> None:
        """Entrega las credenciales al servicio y muestra su respuesta."""
        resultado = self._servicio.validar_acceso(self._usuario_var.get(),
                                                  self._contrasena_var.get())
        if not resultado.exitoso:
            self._mostrar_mensaje(resultado.mensaje, COLOR_ERROR)
            self._entrada_contrasena.focus_set()
            return

        self._mostrar_mensaje(resultado.mensaje, COLOR_EXITO)
        self.update_idletasks()
        self._al_ingresar(resultado.usuario)

    def _mostrar_mensaje(self, texto: str, color: str) -> None:
        """Muestra un mensaje de respuesta bajo los campos de acceso."""
        self._etiqueta_mensaje.configure(fg=color)
        self._mensaje_var.set(texto)

    def limpiar(self) -> None:
        """Vacía los campos y el mensaje para un nuevo intento de acceso."""
        self._usuario_var.set("")
        self._contrasena_var.set("")
        self._mensaje_var.set("")

    def enfocar(self) -> None:
        """Coloca el cursor en el campo de usuario al mostrar la pantalla."""
        self._entrada_usuario.focus_set()
