"""Módulo que define el panel principal de la aplicación.

Reúne el contenedor principal (MainView) y las secciones que este organiza
dentro de su área de contenido:

- ProductosView: formulario, acciones y tabla para gestionar los productos.
- UsuariosView: tabla de consulta de los usuarios registrados.
- VentaView: selección de usuario y producto, y registro de ventas.

Las cuatro clases son vistas: recogen lo que la persona escribe o
selecciona, piden las operaciones a RestauranteServicio y muestran lo que
el servicio responde. Ninguna de ellas abre archivos ni aplica reglas del
restaurante.
"""

import tkinter as tk
from collections.abc import Callable
from tkinter import messagebox, ttk

from modelos.usuario import Usuario
from servicios.restaurante_servicio import (
    RestauranteServicio,
    ResultadoOperacion,
    ResultadoVenta,
)
from ui import (
    COLOR_ERROR,
    COLOR_EXITO,
    COLOR_TEXTO_SUAVE,
    Columna,
    cargar_icono,
    crear_tabla,
    etiqueta_fila,
)

# Definición de las columnas de cada tabla: clave, título, ancho y alineación.
COLUMNAS_PRODUCTOS: tuple[Columna, ...] = (
    ("codigo", "Código", 90, "w"),
    ("nombre", "Nombre", 240, "w"),
    ("categoria", "Categoría", 150, "w"),
    ("precio", "Precio", 100, "e"),
    ("cantidad", "Cantidad", 100, "center"),
)

COLUMNAS_USUARIOS: tuple[Columna, ...] = (
    ("identificacion", "Identificación", 120, "w"),
    ("nombre", "Nombre", 220, "w"),
    ("usuario", "Usuario", 140, "w"),
    ("contrasena", "Contraseña", 120, "w"),
    ("rol", "Rol", 150, "w"),
)

COLUMNAS_VENTAS: tuple[Columna, ...] = (
    ("fecha", "Fecha", 150, "w"),
    ("usuario", "Usuario", 220, "w"),
    ("producto", "Producto", 240, "w"),
    ("precio", "Precio", 100, "e"),
)

CATEGORIAS_SUGERIDAS: tuple[str, ...] = (
    "Entrada", "Plato fuerte", "Bebida", "Postre", "Guarnición",
)

AYUDA_PRODUCTOS: str = ("Para consultar, actualizar o eliminar: escriba el código "
                        "o seleccione una fila de la tabla y pulse Cargar.")

AYUDA_VENTA: str = "Seleccione un usuario y un producto, y pulse Registrar venta."


def _titulo_con_icono(contenedor: tk.Misc, icono: "tk.PhotoImage | None",
                      texto: str) -> ttk.Frame:
    """Arma un pequeño contenedor con un icono junto al título de una sección.

    Quien llama debe conservar su propia referencia al icono (por ejemplo
    en ``self._icono_titulo``) mientras la etiqueta exista, ya que Tkinter
    libera la imagen si no queda ningún objeto Python que la referencie.

    Args:
        contenedor: Contenedor donde se coloca el título.
        icono: Imagen ya cargada con cargar_icono(), o None si no existe.
        texto: Texto del título de la sección.

    Returns:
        El contenedor con el icono y el texto del título.
    """
    marco = ttk.Frame(contenedor, style="TFrame")
    if icono is not None:
        ttk.Label(marco, image=icono, style="TLabel").pack(side="left", padx=(0, 8))
    ttk.Label(marco, text=texto, style="Seccion.TLabel").pack(side="left")
    return marco


class ProductosView(ttk.Frame):
    """Sección que permite registrar, consultar, actualizar y eliminar productos.

    Organiza la pantalla en zonas mediante contenedores: el formulario con
    los datos del producto, la fila de acciones, la tabla con los productos
    registrados y la barra de estado.

    La vista solo recoge lo que la persona escribe y lo entrega a
    RestauranteServicio; las validaciones, las reglas y el guardado en
    productos.json ocurren dentro del servicio. Después de cada operación
    la vista vuelve a pedir la información para mostrar el resultado.

    Args:
        master: Contenedor donde se coloca la sección.
        restaurante_servicio: Servicio que resuelve las operaciones.
    """

    def __init__(self, master: tk.Misc,
                 restaurante_servicio: RestauranteServicio) -> None:
        super().__init__(master, style="TFrame")
        self._servicio: RestauranteServicio = restaurante_servicio
        self._icono_titulo = cargar_icono("icono_productos.png")

        self._codigo_var: tk.StringVar = tk.StringVar()
        self._nombre_var: tk.StringVar = tk.StringVar()
        self._categoria_var: tk.StringVar = tk.StringVar()
        self._precio_var: tk.StringVar = tk.StringVar()
        self._cantidad_var: tk.StringVar = tk.StringVar(value="0")
        self._resumen_var: tk.StringVar = tk.StringVar(value="")
        self._mensaje_var: tk.StringVar = tk.StringVar(value="")

        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)
        self._construir_interfaz()
        self._mostrar_mensaje(AYUDA_PRODUCTOS, COLOR_TEXTO_SUAVE)

    # --- CONSTRUCCIÓN DE LA INTERFAZ ---
    def _construir_interfaz(self) -> None:
        """Arma el encabezado, el formulario, las acciones, la tabla y el estado."""
        self._construir_cabecera()
        self._construir_formulario()
        self._construir_acciones()
        self._construir_tabla()
        self._construir_barra_estado()

    def _construir_cabecera(self) -> None:
        """Crea la línea con el título de la sección y su resumen."""
        cabecera = ttk.Frame(self, style="TFrame")
        cabecera.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        cabecera.columnconfigure(1, weight=1)

        titulo = _titulo_con_icono(
            cabecera, self._icono_titulo, "Gestión de productos"
        )
        titulo.grid(row=0, column=0, sticky="w")
        ttk.Label(cabecera, textvariable=self._resumen_var,
                  style="Resumen.TLabel").grid(row=0, column=1, sticky="e",
                                               padx=(12, 0))

    def _construir_formulario(self) -> None:
        """Crea el contenedor con los campos de datos del producto."""
        formulario = ttk.Labelframe(self, text=" Datos del producto ", padding=10)
        formulario.grid(row=1, column=0, sticky="ew")
        for columna in range(3):
            formulario.columnconfigure(columna, weight=1)

        campo = self._crear_campo(formulario, "Código", 0, 0)
        ttk.Entry(campo, textvariable=self._codigo_var,
                  width=14).pack(fill="x", pady=(4, 0))

        campo = self._crear_campo(formulario, "Nombre", 0, 1)
        ttk.Entry(campo, textvariable=self._nombre_var,
                  width=28).pack(fill="x", pady=(4, 0))

        campo = self._crear_campo(formulario, "Categoría", 0, 2)
        self._combo_categoria = ttk.Combobox(campo, textvariable=self._categoria_var,
                                             values=CATEGORIAS_SUGERIDAS, width=20)
        self._combo_categoria.pack(fill="x", pady=(4, 0))

        campo = self._crear_campo(formulario, "Precio ($)", 1, 0)
        ttk.Entry(campo, textvariable=self._precio_var,
                  width=14).pack(fill="x", pady=(4, 0))

        campo = self._crear_campo(formulario, "Cantidad", 1, 1)
        ttk.Spinbox(campo, textvariable=self._cantidad_var, from_=0, to=9999,
                    width=12).pack(fill="x", pady=(4, 0))

    @staticmethod
    def _crear_campo(contenedor: ttk.Labelframe, texto: str,
                     fila: int, columna: int) -> ttk.Frame:
        """Crea un campo del formulario con su etiqueta.

        Cada campo es un contenedor propio dentro de la cuadrícula del
        formulario: la etiqueta se coloca arriba y quien llama añade debajo
        el componente de entrada que corresponda.

        Args:
            contenedor: Formulario donde se ubica el campo.
            texto: Texto de la etiqueta.
            fila: Fila de la cuadrícula del formulario.
            columna: Columna de la cuadrícula del formulario.

        Returns:
            El contenedor del campo, listo para recibir su componente.
        """
        campo = ttk.Frame(contenedor, style="Panel.TFrame")
        campo.grid(row=fila, column=columna, sticky="ew", padx=6, pady=4)
        ttk.Label(campo, text=texto, style="Panel.TLabel").pack(anchor="w")
        return campo

    def _construir_acciones(self) -> None:
        """Crea la fila de botones que solicitan las operaciones al servicio."""
        acciones = ttk.Frame(self, style="TFrame")
        acciones.grid(row=2, column=0, sticky="ew", pady=(10, 10))

        botones: tuple[tuple[str, str, Callable[[], None]], ...] = (
            ("Registrar", "Primario.TButton", self.registrar),
            ("Cargar", "Secundario.TButton", self.cargar),
            ("Actualizar", "Secundario.TButton", self.actualizar),
            ("Eliminar", "Peligro.TButton", self.eliminar),
            ("Limpiar", "Secundario.TButton", self.limpiar_formulario),
        )
        for texto, estilo, accion in botones:
            ttk.Button(acciones, text=texto, style=estilo,
                       command=accion).pack(side="left", padx=(0, 8))

    def _construir_tabla(self) -> None:
        """Crea el contenedor con la tabla de productos registrados."""
        contenedor = ttk.Labelframe(self, text=" Productos registrados ", padding=10)
        contenedor.grid(row=3, column=0, sticky="nsew")
        contenedor.rowconfigure(0, weight=1)
        contenedor.columnconfigure(0, weight=1)

        marco, self._tabla = crear_tabla(contenedor, COLUMNAS_PRODUCTOS)
        marco.grid(row=0, column=0, sticky="nsew")

    def _construir_barra_estado(self) -> None:
        """Crea la línea inferior donde se muestra la respuesta del servicio."""
        self._etiqueta_mensaje = ttk.Label(self, textvariable=self._mensaje_var,
                                           style="Resumen.TLabel", anchor="w")
        self._etiqueta_mensaje.grid(row=4, column=0, sticky="ew", pady=(8, 0))

    # --- OPERACIONES ---
    def registrar(self) -> None:
        """Pide al servicio registrar el producto escrito en el formulario."""
        resultado = self._servicio.registrar_producto(
            self._codigo_var.get(), self._nombre_var.get(),
            self._categoria_var.get(), self._precio_var.get(),
            self._cantidad_var.get(),
        )
        if resultado.exitoso:
            self.limpiar_formulario()
        self._aplicar_resultado(resultado)

    def cargar(self) -> None:
        """Pide al servicio un producto y muestra sus datos en el formulario."""
        resultado = self._servicio.consultar_producto(self._codigo_objetivo())
        if resultado.exitoso and resultado.producto is not None:
            producto = resultado.producto
            self._codigo_var.set(producto.codigo)
            self._nombre_var.set(producto.nombre)
            self._categoria_var.set(producto.categoria)
            self._precio_var.set(f"{producto.precio:.2f}")
            self._cantidad_var.set(str(producto.cantidad))
        self._aplicar_resultado(resultado)

    def actualizar(self) -> None:
        """Pide al servicio actualizar el producto con los datos del formulario."""
        resultado = self._servicio.actualizar_producto(
            self._codigo_var.get(), self._nombre_var.get(),
            self._categoria_var.get(), self._precio_var.get(),
            self._cantidad_var.get(),
        )
        self._aplicar_resultado(resultado)

    def eliminar(self) -> None:
        """Pide confirmación y solicita al servicio eliminar el producto."""
        codigo = self._codigo_objetivo()
        consulta = self._servicio.consultar_producto(codigo)
        if not consulta.exitoso or consulta.producto is None:
            self._aplicar_resultado(consulta)
            return

        confirmado = messagebox.askyesno(
            "Eliminar producto",
            f"¿Desea eliminar '{consulta.producto.nombre}' "
            f"({consulta.producto.codigo}) del restaurante?",
            parent=self,
        )
        if not confirmado:
            self._mostrar_mensaje("Eliminación cancelada.", COLOR_TEXTO_SUAVE)
            return

        resultado = self._servicio.eliminar_producto(codigo)
        if resultado.exitoso:
            self.limpiar_formulario()
        self._aplicar_resultado(resultado)

    def limpiar_formulario(self) -> None:
        """Vacía los campos para preparar un registro nuevo."""
        self._codigo_var.set("")
        self._nombre_var.set("")
        self._categoria_var.set("")
        self._precio_var.set("")
        self._cantidad_var.set("0")

    # --- ACTUALIZACIÓN DE LA INFORMACIÓN ---
    def refrescar(self) -> None:
        """Vuelve a pedir los productos al servicio y redibuja la sección."""
        self._resumen_var.set(
            f"{self._servicio.contar_productos()} productos  |  "
            f"{self._servicio.cantidad_total_productos()} unidades disponibles  |  "
            f"{len(self._servicio.obtener_categorias())} categorías"
        )
        self._tabla.delete(*self._tabla.get_children())
        for indice, producto in enumerate(self._servicio.listar_productos()):
            self._tabla.insert(
                "", "end",
                values=(producto.codigo, producto.nombre, producto.categoria,
                        f"${producto.precio:.2f}", producto.cantidad),
                tags=etiqueta_fila(indice),
            )
        self._combo_categoria.configure(values=self._categorias_disponibles())

    def _aplicar_resultado(self, resultado: ResultadoOperacion) -> None:
        """Muestra el mensaje del servicio y actualiza la información en pantalla."""
        self._mostrar_mensaje(resultado.mensaje,
                              COLOR_EXITO if resultado.exitoso else COLOR_ERROR)
        self.refrescar()

    def _mostrar_mensaje(self, texto: str, color: str) -> None:
        """Escribe un mensaje de respuesta en la barra de estado de la sección."""
        self._etiqueta_mensaje.configure(foreground=color)
        self._mensaje_var.set(texto)

    def _codigo_objetivo(self) -> str:
        """Devuelve el código a utilizar en una operación.

        Se toma el código escrito en el formulario; si está vacío, se usa
        el de la fila seleccionada en la tabla.
        """
        codigo = self._codigo_var.get().strip()
        if codigo:
            return codigo
        seleccion = self._tabla.selection()
        if seleccion:
            return str(self._tabla.item(seleccion[0], "values")[0])
        return ""

    def _categorias_disponibles(self) -> tuple[str, ...]:
        """Combina las categorías sugeridas con las ya utilizadas."""
        categorias = set(CATEGORIAS_SUGERIDAS) | self._servicio.obtener_categorias()
        return tuple(sorted(categorias))


class UsuariosView(ttk.Frame):
    """Sección que permite consultar los usuarios registrados.

    Es una sección de solo lectura: pide la información a
    RestauranteServicio y la presenta en una tabla. La fila de la persona
    que inició sesión se resalta para distinguirla del resto.

    Args:
        master: Contenedor donde se coloca la sección.
        restaurante_servicio: Servicio que entrega los usuarios.
    """

    def __init__(self, master: tk.Misc,
                 restaurante_servicio: RestauranteServicio) -> None:
        super().__init__(master, style="TFrame")
        self._servicio: RestauranteServicio = restaurante_servicio
        self._icono_titulo = cargar_icono("icono_usuarios.png")
        self._resumen_var: tk.StringVar = tk.StringVar(value="")

        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self._construir_interfaz()

    def _construir_interfaz(self) -> None:
        """Arma el encabezado de la sección y el contenedor de la tabla."""
        titulo = _titulo_con_icono(
            self, self._icono_titulo, "Usuarios registrados"
        )
        titulo.grid(row=0, column=0, sticky="w")
        ttk.Label(self, textvariable=self._resumen_var,
                  style="Resumen.TLabel").grid(row=1, column=0, sticky="w",
                                               pady=(2, 12))

        contenedor = ttk.Labelframe(self, text=" Personal con acceso al sistema ",
                                    padding=12)
        contenedor.grid(row=2, column=0, sticky="nsew")
        contenedor.rowconfigure(0, weight=1)
        contenedor.columnconfigure(0, weight=1)

        marco, self._tabla = crear_tabla(contenedor, COLUMNAS_USUARIOS)
        marco.grid(row=0, column=0, sticky="nsew")

    def refrescar(self, usuario_actual: Usuario | None = None) -> None:
        """Vuelve a pedir los usuarios al servicio y redibuja la tabla.

        Args:
            usuario_actual: Usuario con la sesión iniciada, cuya fila se
                resalta en la tabla.
        """
        self._resumen_var.set(
            f"{self._servicio.contar_usuarios()} usuarios habilitados para el "
            f"acceso al sistema  |  la fila resaltada es la sesión actual"
        )
        self._tabla.delete(*self._tabla.get_children())
        for indice, usuario in enumerate(self._servicio.listar_usuarios()):
            es_actual = (usuario_actual is not None
                         and usuario.identificacion == usuario_actual.identificacion)
            self._tabla.insert(
                "", "end",
                values=(usuario.identificacion, usuario.nombre, usuario.usuario,
                        usuario.contrasena_oculta, usuario.rol),
                tags=etiqueta_fila(indice, es_actual),
            )


class VentaView(ttk.Frame):
    """Sección que permite registrar ventas relacionando un usuario y un producto.

    Presenta dos componentes de selección —usuario y producto— y un botón
    "Registrar venta" asociado mediante ``command=`` al callback
    ``registrar_venta``. Ese callback obtiene la selección hecha en la
    interfaz, delega la operación en RestauranteServicio y actualiza la
    tabla con el resultado, evidenciando el flujo de la semana:

        botón → command= → callback → RestauranteServicio →
        persistencia en ventas.json → respuesta visual

    La vista no valida ni guarda nada por sí misma: que el usuario y el
    producto seleccionados existan, y el guardado del registro, ocurren
    dentro de RestauranteServicio.

    Args:
        master: Contenedor donde se coloca la sección.
        restaurante_servicio: Servicio que resuelve el registro de ventas.
    """

    def __init__(self, master: tk.Misc,
                 restaurante_servicio: RestauranteServicio) -> None:
        super().__init__(master, style="TFrame")
        self._servicio: RestauranteServicio = restaurante_servicio
        self._icono_titulo = cargar_icono("icono_ventas.png")
        self._icono_boton = cargar_icono("icono_registrar_venta.png")

        self._usuario_var: tk.StringVar = tk.StringVar()
        self._producto_var: tk.StringVar = tk.StringVar()
        self._resumen_var: tk.StringVar = tk.StringVar(value="")
        self._mensaje_var: tk.StringVar = tk.StringVar(value="")
        self._mapa_usuarios: dict[str, str] = {}
        self._mapa_productos: dict[str, str] = {}

        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self._construir_interfaz()
        self._mostrar_mensaje(AYUDA_VENTA, COLOR_TEXTO_SUAVE)

    # --- CONSTRUCCIÓN DE LA INTERFAZ ---
    def _construir_interfaz(self) -> None:
        """Arma el encabezado, la selección, la tabla y la barra de estado."""
        self._construir_cabecera()
        self._construir_seleccion()
        self._construir_tabla()
        self._construir_barra_estado()

    def _construir_cabecera(self) -> None:
        """Crea la línea con el título de la sección y su resumen."""
        cabecera = ttk.Frame(self, style="TFrame")
        cabecera.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        cabecera.columnconfigure(1, weight=1)

        titulo = _titulo_con_icono(
            cabecera, self._icono_titulo, "Registro de ventas"
        )
        titulo.grid(row=0, column=0, sticky="w")
        ttk.Label(cabecera, textvariable=self._resumen_var,
                  style="Resumen.TLabel").grid(row=0, column=1, sticky="e",
                                               padx=(12, 0))

    def _construir_seleccion(self) -> None:
        """Crea los componentes para seleccionar usuario y producto."""
        seleccion = ttk.Labelframe(self, text=" Nueva venta ", padding=10)
        seleccion.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        seleccion.columnconfigure(0, weight=1)
        seleccion.columnconfigure(1, weight=1)

        campo = ttk.Frame(seleccion, style="Panel.TFrame")
        campo.grid(row=0, column=0, sticky="ew", padx=6, pady=4)
        ttk.Label(campo, text="Usuario", style="Panel.TLabel").pack(anchor="w")
        self._combo_usuario = ttk.Combobox(campo, textvariable=self._usuario_var,
                                           state="readonly", width=28)
        self._combo_usuario.pack(fill="x", pady=(4, 0))

        campo = ttk.Frame(seleccion, style="Panel.TFrame")
        campo.grid(row=0, column=1, sticky="ew", padx=6, pady=4)
        ttk.Label(campo, text="Producto", style="Panel.TLabel").pack(anchor="w")
        self._combo_producto = ttk.Combobox(campo, textvariable=self._producto_var,
                                            state="readonly", width=32)
        self._combo_producto.pack(fill="x", pady=(4, 0))

        acciones = ttk.Frame(seleccion, style="Panel.TFrame")
        acciones.grid(row=1, column=0, columnspan=2, sticky="w", padx=6, pady=(10, 2))
        boton = ttk.Button(acciones, text="Registrar venta", style="Primario.TButton",
                           command=self.registrar_venta)
        if self._icono_boton is not None:
            boton.configure(image=self._icono_boton, compound="left")
        boton.pack(side="left")

    def _construir_tabla(self) -> None:
        """Crea el contenedor con la tabla de ventas registradas."""
        contenedor = ttk.Labelframe(self, text=" Ventas registradas ", padding=10)
        contenedor.grid(row=2, column=0, sticky="nsew")
        contenedor.rowconfigure(0, weight=1)
        contenedor.columnconfigure(0, weight=1)

        marco, self._tabla = crear_tabla(contenedor, COLUMNAS_VENTAS)
        marco.grid(row=0, column=0, sticky="nsew")

    def _construir_barra_estado(self) -> None:
        """Crea la línea inferior donde se muestra la respuesta del servicio."""
        self._etiqueta_mensaje = ttk.Label(self, textvariable=self._mensaje_var,
                                           style="Resumen.TLabel", anchor="w")
        self._etiqueta_mensaje.grid(row=3, column=0, sticky="ew", pady=(8, 0))

    # --- CALLBACK DE VENTA ---
    def registrar_venta(self) -> None:
        """Callback del botón "Registrar venta".

        Tkinter ejecuta este método porque el botón lo indicó mediante
        ``command=self.registrar_venta``. El callback solo interpreta la
        selección hecha en los componentes y delega la operación en
        RestauranteServicio; no decide si la venta es válida ni la guarda
        por su cuenta.
        """
        usuario_identificacion = self._mapa_usuarios.get(self._usuario_var.get(), "")
        producto_codigo = self._mapa_productos.get(self._producto_var.get(), "")
        resultado = self._servicio.registrar_venta(usuario_identificacion,
                                                    producto_codigo)
        if resultado.exitoso:
            self._usuario_var.set("")
            self._producto_var.set("")
        self._aplicar_resultado(resultado)

    # --- ACTUALIZACIÓN DE LA INFORMACIÓN ---
    def refrescar(self) -> None:
        """Actualiza las listas de selección y vuelve a pedir las ventas al servicio."""
        self._mapa_usuarios = {
            f"{usuario.identificacion} - {usuario.nombre}": usuario.identificacion
            for usuario in self._servicio.listar_usuarios()
        }
        self._mapa_productos = {
            f"{producto.codigo} - {producto.nombre} (${producto.precio:.2f})":
                producto.codigo
            for producto in self._servicio.listar_productos()
        }
        self._combo_usuario.configure(values=list(self._mapa_usuarios.keys()))
        self._combo_producto.configure(values=list(self._mapa_productos.keys()))
        if self._usuario_var.get() not in self._mapa_usuarios:
            self._usuario_var.set("")
        if self._producto_var.get() not in self._mapa_productos:
            self._producto_var.set("")

        self._resumen_var.set(f"{self._servicio.contar_ventas()} ventas registradas")
        self._tabla.delete(*self._tabla.get_children())
        for indice, detalle in enumerate(self._servicio.listar_ventas_detalladas()):
            self._tabla.insert(
                "", "end",
                values=(detalle["fecha"], detalle["usuario"], detalle["producto"],
                        detalle["precio"]),
                tags=etiqueta_fila(indice),
            )

    def _aplicar_resultado(self, resultado: ResultadoVenta) -> None:
        """Muestra el mensaje del servicio y actualiza la información en pantalla."""
        self._mostrar_mensaje(resultado.mensaje,
                              COLOR_EXITO if resultado.exitoso else COLOR_ERROR)
        self.refrescar()

    def _mostrar_mensaje(self, texto: str, color: str) -> None:
        """Escribe un mensaje de respuesta en la barra de estado de la sección."""
        self._etiqueta_mensaje.configure(foreground=color)
        self._mensaje_var.set(texto)


class MainView(ttk.Frame):
    """Panel principal que se muestra después de un acceso correcto.

    Actúa como contenedor principal de la aplicación: organiza la ventana
    en tres zonas —el encabezado con la sesión, el menú de navegación y el
    área de contenido— y coloca dentro de esa área las secciones del
    sistema: Productos, Usuarios y Ventas.

    Las secciones se crean una sola vez y comparten la misma celda del
    área de contenido; cambiar de sección consiste en traer la
    correspondiente al frente.

    Args:
        master: Ventana o contenedor donde se coloca la vista.
        restaurante_servicio: Servicio que se entrega a cada sección.
        al_cerrar_sesion: Función que la aplicación ejecuta al cerrar sesión.
    """

    def __init__(self, master: tk.Misc, restaurante_servicio: RestauranteServicio,
                 al_cerrar_sesion: Callable[[], None]) -> None:
        super().__init__(master, style="TFrame")
        self._servicio: RestauranteServicio = restaurante_servicio
        self._al_cerrar_sesion: Callable[[], None] = al_cerrar_sesion
        self._usuario: Usuario | None = None
        self._botones: dict[str, ttk.Button] = {}
        self._logo = cargar_icono("logo.png")
        self._icono_salir = cargar_icono("icono_salir.png")

        self._sesion_var: tk.StringVar = tk.StringVar(value="Sin sesión activa")

        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)
        self._construir_encabezado()
        self._construir_navegacion()
        self._construir_contenido()

    # --- CONTENEDORES PRINCIPALES ---
    def _construir_encabezado(self) -> None:
        """Crea la barra superior con el logo, la sesión y el cierre de sesión."""
        encabezado = ttk.Frame(self, style="Encabezado.TFrame", padding=(20, 12))
        encabezado.grid(row=0, column=0, columnspan=2, sticky="ew")
        encabezado.columnconfigure(0, weight=1)

        marca = ttk.Frame(encabezado, style="Encabezado.TFrame")
        marca.grid(row=0, column=0, sticky="w")
        if self._logo is not None:
            ttk.Label(marca, image=self._logo,
                      style="Encabezado.TLabel").pack(side="left", padx=(0, 10))
        titulos = ttk.Frame(marca, style="Encabezado.TFrame")
        titulos.pack(side="left")
        ttk.Label(titulos, text=self._servicio.nombre,
                  style="Encabezado.TLabel").pack(anchor="w")
        ttk.Label(titulos, text="Panel principal",
                  style="EncabezadoSub.TLabel").pack(anchor="w")

        sesion = ttk.Frame(encabezado, style="Encabezado.TFrame")
        sesion.grid(row=0, column=1, sticky="e")
        ttk.Label(sesion, textvariable=self._sesion_var,
                  style="Sesion.TLabel").pack(anchor="e")
        boton_salir = ttk.Button(sesion, text="Cerrar sesión", style="Sesion.TButton",
                                 command=self._al_cerrar_sesion)
        if self._icono_salir is not None:
            boton_salir.configure(image=self._icono_salir, compound="left")
        boton_salir.pack(anchor="e", pady=(6, 0))

    def _construir_navegacion(self) -> None:
        """Crea el menú lateral con las secciones del sistema."""
        lateral = ttk.Frame(self, style="Panel.TFrame", padding=(14, 18))
        lateral.grid(row=1, column=0, sticky="ns")

        ttk.Label(lateral, text="OPCIONES", style="Panel.TLabel",
                  foreground=COLOR_TEXTO_SUAVE).pack(anchor="w", pady=(0, 10))

        opciones: tuple[tuple[str, str, Callable[[], None]], ...] = (
            ("productos", "Productos", self.mostrar_productos),
            ("usuarios", "Usuarios", self.mostrar_usuarios),
            ("ventas", "Ventas", self.mostrar_ventas),
        )
        for clave, texto, accion in opciones:
            boton = ttk.Button(lateral, text=texto, style="Nav.TButton",
                               width=18, command=accion)
            boton.pack(fill="x", pady=3)
            self._botones[clave] = boton

    def _construir_contenido(self) -> None:
        """Crea el área de contenido y coloca dentro las secciones del sistema."""
        contenido = ttk.Frame(self, style="TFrame", padding=(20, 18))
        contenido.grid(row=1, column=1, sticky="nsew")
        contenido.rowconfigure(0, weight=1)
        contenido.columnconfigure(0, weight=1)

        self._seccion_productos = ProductosView(contenido, self._servicio)
        self._seccion_usuarios = UsuariosView(contenido, self._servicio)
        self._seccion_ventas = VentaView(contenido, self._servicio)

        # Las tres secciones comparten la misma celda del área de contenido.
        for seccion in (self._seccion_productos, self._seccion_usuarios,
                        self._seccion_ventas):
            seccion.grid(row=0, column=0, sticky="nsew")

    # --- SESIÓN ---
    def establecer_usuario(self, usuario: Usuario) -> None:
        """Registra la sesión actual y prepara el panel para esa persona.

        Args:
            usuario: Usuario autenticado por RestauranteServicio.
        """
        self._usuario = usuario
        self._sesion_var.set(f"{usuario.nombre}  |  {usuario.rol}")
        self.mostrar_productos()

    # --- NAVEGACIÓN ENTRE SECCIONES ---
    def mostrar_productos(self) -> None:
        """Muestra la sección de gestión de productos."""
        self._seccion_productos.refrescar()
        self._seccion_productos.tkraise()
        self._marcar_opcion("productos")

    def mostrar_usuarios(self) -> None:
        """Muestra la sección de consulta de usuarios."""
        self._seccion_usuarios.refrescar(self._usuario)
        self._seccion_usuarios.tkraise()
        self._marcar_opcion("usuarios")

    def mostrar_ventas(self) -> None:
        """Muestra la sección de registro de ventas."""
        self._seccion_ventas.refrescar()
        self._seccion_ventas.tkraise()
        self._marcar_opcion("ventas")

    def _marcar_opcion(self, clave: str) -> None:
        """Resalta en el menú lateral la sección que se está mostrando."""
        for nombre, boton in self._botones.items():
            boton.configure(
                style="NavActivo.TButton" if nombre == clave else "Nav.TButton"
            )
