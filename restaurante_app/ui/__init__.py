"""Paquete de vistas del restaurante.

Contiene las pantallas construidas con Tkinter (LoginView, MainView y las
secciones que esta última agrupa) y los recursos visuales que todas
comparten: la paleta de colores, las fuentes, los estilos de los
componentes ttk y la construcción de las tablas.

Reunir aquí esos recursos evita repetirlos en cada vista y permite
cambiar la apariencia de la aplicación desde un solo lugar.

Las vistas se importan directamente desde su módulo
(``from ui.login_view import LoginView``) para que este archivo no
dependa de ellas.
"""

from tkinter import ttk

# --- Paleta de colores ---
COLOR_FONDO: str = "#f4f1ec"
COLOR_PANEL: str = "#ffffff"
COLOR_PRIMARIO: str = "#8c2f1b"
COLOR_PRIMARIO_OSCURO: str = "#6f2415"
COLOR_ACENTO: str = "#d9a441"
COLOR_TEXTO: str = "#2e2a26"
COLOR_TEXTO_SUAVE: str = "#6b625a"
COLOR_TEXTO_CLARO: str = "#f7f3ee"
COLOR_BORDE: str = "#e0d8cd"
COLOR_ERROR: str = "#b3261e"
COLOR_EXITO: str = "#1b7a3d"
COLOR_PENDIENTE: str = "#a06a14"
COLOR_FILA_ALTERNA: str = "#faf7f2"
COLOR_FILA_DESTACADA: str = "#fdf1d6"

# --- Tipografías ---
FUENTE_TITULO: tuple[str, int, str] = ("Segoe UI", 20, "bold")
FUENTE_SUBTITULO: tuple[str, int] = ("Segoe UI", 11)
FUENTE_SECCION: tuple[str, int, str] = ("Segoe UI", 14, "bold")
FUENTE_BASE: tuple[str, int] = ("Segoe UI", 10)
FUENTE_BOTON: tuple[str, int, str] = ("Segoe UI", 10, "bold")
FUENTE_PEQUENA: tuple[str, int] = ("Segoe UI", 9)

# Descripción de una columna de tabla: clave, título, ancho y alineación.
Columna = tuple[str, str, int, str]


def configurar_estilos() -> None:
    """Define la apariencia de los componentes ttk de la aplicación.

    Se ejecuta una sola vez, desde main.py, después de crear la ventana
    principal. A partir de ese momento las vistas solo indican el estilo
    que necesitan (por ejemplo ``style="Primario.TButton"``) sin repetir
    colores ni fuentes.
    """
    estilo = ttk.Style()
    estilo.theme_use("clam")

    estilo.configure("TFrame", background=COLOR_FONDO)
    estilo.configure("Panel.TFrame", background=COLOR_PANEL)
    estilo.configure("Encabezado.TFrame", background=COLOR_PRIMARIO)

    estilo.configure("TLabel", background=COLOR_FONDO, foreground=COLOR_TEXTO,
                     font=FUENTE_BASE)
    estilo.configure("Panel.TLabel", background=COLOR_PANEL, foreground=COLOR_TEXTO,
                     font=FUENTE_BASE)
    estilo.configure("Seccion.TLabel", background=COLOR_FONDO,
                     foreground=COLOR_TEXTO, font=FUENTE_SECCION)
    estilo.configure("Resumen.TLabel", background=COLOR_FONDO,
                     foreground=COLOR_TEXTO_SUAVE, font=FUENTE_PEQUENA)

    estilo.configure("Encabezado.TLabel", background=COLOR_PRIMARIO,
                     foreground=COLOR_TEXTO_CLARO, font=FUENTE_TITULO)
    estilo.configure("EncabezadoSub.TLabel", background=COLOR_PRIMARIO,
                     foreground=COLOR_ACENTO, font=FUENTE_SUBTITULO)
    estilo.configure("Sesion.TLabel", background=COLOR_PRIMARIO,
                     foreground=COLOR_TEXTO_CLARO, font=FUENTE_BASE)
    estilo.configure("Pendiente.TLabel", background=COLOR_PANEL,
                     foreground=COLOR_PENDIENTE, font=FUENTE_SECCION)

    estilo.configure("TLabelframe", background=COLOR_PANEL,
                     bordercolor=COLOR_BORDE, relief="solid", borderwidth=1)
    estilo.configure("TLabelframe.Label", background=COLOR_PANEL,
                     foreground=COLOR_PRIMARIO, font=FUENTE_BOTON)

    estilo.configure("TEntry", fieldbackground=COLOR_PANEL, foreground=COLOR_TEXTO,
                     bordercolor=COLOR_BORDE, padding=4)
    estilo.configure("TCombobox", fieldbackground=COLOR_PANEL,
                     foreground=COLOR_TEXTO, bordercolor=COLOR_BORDE, padding=4)
    estilo.configure("TSpinbox", fieldbackground=COLOR_PANEL,
                     foreground=COLOR_TEXTO, bordercolor=COLOR_BORDE, padding=4)

    _configurar_boton(estilo, "Primario.TButton", COLOR_PRIMARIO,
                      COLOR_PRIMARIO_OSCURO, COLOR_TEXTO_CLARO)
    _configurar_boton(estilo, "Secundario.TButton", "#e9e2d8", "#dbd1c2",
                      COLOR_TEXTO)
    # El botón secundario lleva borde para distinguirse del fondo de la página.
    estilo.configure("Secundario.TButton", borderwidth=1, relief="solid",
                     bordercolor=COLOR_BORDE)
    _configurar_boton(estilo, "Peligro.TButton", "#8a1f16", "#6d1710",
                      COLOR_TEXTO_CLARO)
    _configurar_boton(estilo, "Sesion.TButton", COLOR_PRIMARIO_OSCURO,
                      COLOR_PRIMARIO_OSCURO, COLOR_TEXTO_CLARO)
    _configurar_boton(estilo, "Nav.TButton", COLOR_PANEL, COLOR_FONDO, COLOR_TEXTO)
    _configurar_boton(estilo, "NavActivo.TButton", COLOR_PRIMARIO,
                      COLOR_PRIMARIO, COLOR_TEXTO_CLARO)
    for nombre in ("Nav.TButton", "NavActivo.TButton"):
        estilo.configure(nombre, anchor="w", padding=(12, 10))

    estilo.configure("Restaurante.Treeview", background=COLOR_PANEL,
                     fieldbackground=COLOR_PANEL, foreground=COLOR_TEXTO,
                     font=FUENTE_BASE, rowheight=25, borderwidth=0)
    estilo.configure("Restaurante.Treeview.Heading", background=COLOR_FONDO,
                     foreground=COLOR_TEXTO, font=FUENTE_BOTON, relief="flat",
                     padding=6)
    estilo.map("Restaurante.Treeview",
               background=[("selected", COLOR_ACENTO)],
               foreground=[("selected", COLOR_TEXTO)])


def _configurar_boton(estilo: ttk.Style, nombre: str, fondo: str,
                      fondo_activo: str, texto: str) -> None:
    """Registra un estilo de botón con sus colores normales y de pulsación."""
    estilo.configure(nombre, background=fondo, foreground=texto,
                     font=FUENTE_BOTON, borderwidth=0, focusthickness=0,
                     padding=(14, 8))
    estilo.map(nombre,
               background=[("pressed", fondo_activo), ("active", fondo_activo)],
               foreground=[("disabled", COLOR_TEXTO_SUAVE)])


def crear_tabla(contenedor: ttk.Frame,
                columnas: tuple[Columna, ...]) -> tuple[ttk.Frame, ttk.Treeview]:
    """Crea una tabla con su barra de desplazamiento dentro de un contenedor.

    Las dos secciones que muestran información (productos y usuarios) usan
    tablas con la misma apariencia; construirlas aquí evita repetir el
    mismo armado en cada vista.

    Args:
        contenedor: Contenedor donde se coloca la tabla.
        columnas: Definición de cada columna (clave, título, ancho y
            alineación).

    Returns:
        El marco que contiene la tabla y la tabla misma.
    """
    marco = ttk.Frame(contenedor, style="Panel.TFrame")
    marco.rowconfigure(0, weight=1)
    marco.columnconfigure(0, weight=1)

    tabla = ttk.Treeview(marco, show="headings", style="Restaurante.Treeview",
                         columns=tuple(clave for clave, _, _, _ in columnas))
    for clave, titulo, ancho, alineacion in columnas:
        tabla.heading(clave, text=titulo, anchor="w")
        tabla.column(clave, width=ancho, minwidth=ancho, anchor=alineacion,
                     stretch=True)
    tabla.grid(row=0, column=0, sticky="nsew")

    tabla.tag_configure("par", background=COLOR_PANEL)
    tabla.tag_configure("impar", background=COLOR_FILA_ALTERNA)
    tabla.tag_configure("destacada", background=COLOR_FILA_DESTACADA)

    barra = ttk.Scrollbar(marco, orient="vertical", command=tabla.yview)
    barra.grid(row=0, column=1, sticky="ns")
    tabla.configure(yscrollcommand=barra.set)
    return marco, tabla


def etiqueta_fila(indice: int, destacada: bool = False) -> tuple[str]:
    """Devuelve la etiqueta de color que corresponde a una fila de la tabla."""
    if destacada:
        return ("destacada",)
    return ("par",) if indice % 2 == 0 else ("impar",)
