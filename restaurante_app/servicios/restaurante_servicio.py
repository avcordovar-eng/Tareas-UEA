"""Módulo que define el servicio principal del restaurante."""

from typing import NamedTuple

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio


class ResultadoAcceso(NamedTuple):
    """Resultado de un intento de ingreso a la aplicación.

    Permite que la vista de acceso muestre una respuesta visual sin conocer
    las reglas que la originaron.

    Attributes:
        exitoso (bool): True si las credenciales son correctas.
        mensaje (str): Texto explicativo que la vista muestra en pantalla.
        usuario (Usuario | None): Usuario autenticado, o None si falló.
    """

    exitoso: bool
    mensaje: str
    usuario: Usuario | None = None


class ResultadoOperacion(NamedTuple):
    """Resultado de una operación realizada sobre un producto.

    Permite que la vista muestre el mensaje correspondiente y, cuando la
    operación lo produce, reciba el producto afectado sin conocer las
    reglas que se aplicaron.

    Attributes:
        exitoso (bool): True si la operación se completó correctamente.
        mensaje (str): Texto explicativo que la vista muestra en pantalla.
        producto (Producto | None): Producto registrado, consultado,
            actualizado o eliminado, cuando corresponde.
    """

    exitoso: bool
    mensaje: str
    producto: Producto | None = None


class ResultadoVenta(NamedTuple):
    """Resultado de un intento de registrar una venta.

    Permite que la vista de ventas muestre el mensaje correspondiente sin
    conocer las reglas que se aplicaron para aceptar o rechazar la
    operación.

    Attributes:
        exitoso (bool): True si la venta se registró correctamente.
        mensaje (str): Texto explicativo que la vista muestra en pantalla.
        venta (Venta | None): Venta registrada, cuando la operación tuvo
            éxito.
    """

    exitoso: bool
    mensaje: str
    venta: Venta | None = None


class RestauranteServicio:
    """Servicio que concentra las operaciones sobre usuarios, productos y ventas.

    Recibe los registros leídos por ArchivoServicio, los convierte en
    objetos del dominio y expone las operaciones que necesitan las vistas:
    validar el acceso, listar usuarios, listar productos, consultar sus
    cantidades, registrar, consultar, actualizar o eliminar productos, y
    registrar y listar las ventas del restaurante.

    Aquí viven las reglas del restaurante: las vistas no manipulan las
    listas internas, no validan los datos y no conocen el origen de la
    información. Después de cada operación que modifica los productos o
    las ventas, el servicio solicita a ArchivoServicio que guarde la
    colección completa en el archivo JSON correspondiente.

    Attributes:
        nombre (str): Nombre del restaurante que se muestra en la interfaz.
    """

    def __init__(self, nombre: str, archivo_servicio: ArchivoServicio) -> None:
        self.nombre: str = nombre
        self._archivo: ArchivoServicio = archivo_servicio
        self._productos: list[Producto] = []
        self._usuarios: list[Usuario] = []
        self._ventas: list[Venta] = []
        self._productos_por_codigo: dict[str, Producto] = {}
        self._usuarios_por_id: dict[str, Usuario] = {}

    # --- CARGA DE DATOS ---
    def cargar_productos(self, registros: list[dict[str, object]]) -> int:
        """Convierte en objetos Producto los registros recibidos.

        Los registros incompletos, inválidos o con un código repetido se
        descartan e informan por consola, sin interrumpir la carga del resto.

        Args:
            registros: Lista de diccionarios entregada por ArchivoServicio.

        Returns:
            Cantidad de productos incorporados a la colección.
        """
        incorporados = 0
        for registro in registros:
            try:
                producto = Producto.desde_diccionario(registro)
            except KeyError as error:
                print(f"Advertencia: producto ignorado, falta la clave "
                      f"{error}: {registro}")
                continue
            except (ValueError, TypeError) as error:
                print(f"Advertencia: producto ignorado ({error}): {registro}")
                continue

            if producto.codigo in self._productos_por_codigo:
                print(f"Advertencia: el producto con código "
                      f"'{producto.codigo}' ya estaba cargado y se ignoró.")
                continue

            self._productos.append(producto)
            self._productos_por_codigo[producto.codigo] = producto
            incorporados += 1
        return incorporados

    def cargar_usuarios(self, registros: list[dict[str, object]]) -> int:
        """Convierte en objetos Usuario los registros recibidos.

        Args:
            registros: Lista de diccionarios entregada por ArchivoServicio.

        Returns:
            Cantidad de usuarios incorporados a la colección.
        """
        incorporados = 0
        for registro in registros:
            try:
                usuario = Usuario.desde_diccionario(registro)
            except KeyError as error:
                print(f"Advertencia: usuario ignorado, falta la clave "
                      f"{error}: {registro}")
                continue
            except (ValueError, TypeError) as error:
                print(f"Advertencia: usuario ignorado ({error}): {registro}")
                continue

            if usuario.identificacion in self._usuarios_por_id:
                print(f"Advertencia: el usuario con identificación "
                      f"'{usuario.identificacion}' ya estaba cargado y se ignoró.")
                continue

            self._usuarios.append(usuario)
            self._usuarios_por_id[usuario.identificacion] = usuario
            incorporados += 1
        return incorporados

    def cargar_ventas(self, registros: list[dict[str, object]]) -> int:
        """Convierte en objetos Venta los registros recibidos.

        Args:
            registros: Lista de diccionarios entregada por ArchivoServicio.

        Returns:
            Cantidad de ventas incorporadas a la colección.
        """
        incorporados = 0
        for registro in registros:
            try:
                venta = Venta.desde_diccionario(registro)
            except KeyError as error:
                print(f"Advertencia: venta ignorada, falta la clave "
                      f"{error}: {registro}")
                continue
            except (ValueError, TypeError) as error:
                print(f"Advertencia: venta ignorada ({error}): {registro}")
                continue

            self._ventas.append(venta)
            incorporados += 1
        return incorporados

    # --- ACCESO ---
    def validar_acceso(self, usuario: str, contrasena: str) -> ResultadoAcceso:
        """Valida las credenciales ingresadas en la pantalla de acceso.

        Concentra aquí las reglas del ingreso para que LoginView solo
        muestre el mensaje devuelto. El acceso es una simulación pedagógica
        y no un mecanismo real de autenticación segura.

        Args:
            usuario: Nombre de acceso escrito por la persona.
            contrasena: Contraseña escrita por la persona.

        Returns:
            Un ResultadoAcceso con el estado, el mensaje para la vista y,
            si el ingreso fue correcto, el usuario autenticado.
        """
        if not usuario.strip() or not contrasena.strip():
            return ResultadoAcceso(False, "Debe ingresar usuario y contraseña.")

        if not self._usuarios:
            return ResultadoAcceso(
                False, "No hay usuarios registrados para validar el acceso."
            )

        for registrado in self._usuarios:
            if registrado.credenciales_validas(usuario, contrasena):
                return ResultadoAcceso(
                    True,
                    f"Acceso concedido. Bienvenido/a, {registrado.nombre}.",
                    registrado,
                )
        return ResultadoAcceso(False, "Usuario o contraseña incorrectos.")

    # --- CONSULTAS ---
    def listar_productos(self) -> list[Producto]:
        """Devuelve una copia de la lista de productos registrados."""
        return list(self._productos)

    def listar_usuarios(self) -> list[Usuario]:
        """Devuelve una copia de la lista de usuarios registrados."""
        return list(self._usuarios)

    def buscar_producto(self, codigo: str) -> Producto | None:
        """Busca un producto por su código.

        Returns:
            El producto encontrado o None si no existe.
        """
        return self._productos_por_codigo.get(codigo.strip())

    def buscar_usuario(self, identificacion: str) -> Usuario | None:
        """Busca un usuario por su identificación.

        Returns:
            El usuario encontrado o None si no existe.
        """
        return self._usuarios_por_id.get(identificacion.strip())

    def contar_productos(self) -> int:
        """Devuelve cuántos productos distintos están registrados."""
        return len(self._productos)

    def contar_usuarios(self) -> int:
        """Devuelve cuántos usuarios están registrados."""
        return len(self._usuarios)

    def cantidad_total_productos(self) -> int:
        """Devuelve la suma de las cantidades disponibles de todos los productos."""
        return sum(producto.cantidad for producto in self._productos)

    def obtener_categorias(self) -> set[str]:
        """Devuelve el conjunto de categorías distintas de los productos."""
        return {producto.categoria for producto in self._productos}

    def listar_ventas(self) -> list[Venta]:
        """Devuelve una copia de la lista de ventas registradas."""
        return list(self._ventas)

    def contar_ventas(self) -> int:
        """Devuelve cuántas ventas están registradas."""
        return len(self._ventas)

    def listar_ventas_detalladas(self) -> list[dict[str, str]]:
        """Prepara las ventas registradas para mostrarse en la interfaz.

        Cada venta solo guarda la identificación del usuario y el código
        del producto; aquí se completan con el nombre vigente de cada uno,
        de modo que la vista reciba textos listos para la tabla sin tener
        que buscar usuarios ni productos por su cuenta. Las ventas más
        recientes aparecen primero.

        Returns:
            Lista de diccionarios con las claves fecha, usuario, producto
            y precio, listos para insertarse en la tabla de ventas.
        """
        detalles: list[dict[str, str]] = []
        for venta in reversed(self._ventas):
            usuario = self.buscar_usuario(venta.usuario_identificacion)
            producto = self.buscar_producto(venta.producto_codigo)
            detalles.append({
                "fecha": venta.fecha,
                "usuario": usuario.nombre if usuario else "Usuario eliminado",
                "producto": producto.nombre if producto else "Producto eliminado",
                "precio": f"${producto.precio:.2f}" if producto else "-",
            })
        return detalles

    # --- OPERACIONES SOBRE VENTAS ---
    def registrar_venta(self, usuario_identificacion: str,
                        producto_codigo: str) -> ResultadoVenta:
        """Registra la venta de un producto a nombre de un usuario existente.

        Valida que ambas selecciones correspondan a registros existentes
        antes de crear la venta; esta etapa no descuenta existencias ni
        calcula totales, solo deja constancia de que la operación ocurrió.

        Args:
            usuario_identificacion: Identificación del usuario seleccionado
                en la interfaz.
            producto_codigo: Código del producto seleccionado en la
                interfaz.

        Returns:
            Un ResultadoVenta con el mensaje para la vista y, si se
            registró, la venta creada.
        """
        if not usuario_identificacion.strip():
            return ResultadoVenta(False, "Seleccione un usuario para registrar la venta.")
        if not producto_codigo.strip():
            return ResultadoVenta(False, "Seleccione un producto para registrar la venta.")

        usuario = self.buscar_usuario(usuario_identificacion)
        if usuario is None:
            return ResultadoVenta(
                False,
                f"No existe un usuario con identificación '{usuario_identificacion.strip()}'.",
            )
        producto = self.buscar_producto(producto_codigo)
        if producto is None:
            return ResultadoVenta(
                False, f"No existe un producto con código '{producto_codigo.strip()}'."
            )

        venta = Venta(usuario.identificacion, producto.codigo)
        self._ventas.append(venta)

        registros = [venta.a_diccionario() for venta in self._ventas]
        if not self._archivo.guardar_ventas(registros):
            return ResultadoVenta(
                False,
                "La venta se registró, pero no se pudo guardar en ventas.json.",
                venta,
            )
        return ResultadoVenta(
            True,
            f"Venta registrada: {producto.nombre} para {usuario.nombre}.",
            venta,
        )

    # --- OPERACIONES SOBRE PRODUCTOS ---
    def registrar_producto(self, codigo: str, nombre: str, categoria: str,
                           precio: str, cantidad: str) -> ResultadoOperacion:
        """Registra un producto nuevo a partir de los datos del formulario.

        Recibe los valores como texto, tal como los escribe la persona en la
        interfaz, y es el servicio quien los interpreta y valida.

        Args:
            codigo: Código con el que se identificará el producto.
            nombre: Nombre del producto.
            categoria: Categoría a la que pertenece.
            precio: Precio unitario, en texto.
            cantidad: Cantidad disponible, en texto.

        Returns:
            Un ResultadoOperacion con el mensaje para la vista y, si se
            registró, el producto creado.
        """
        if self.buscar_producto(codigo) is not None:
            return ResultadoOperacion(
                False, f"Ya existe un producto con el código '{codigo.strip()}'."
            )
        try:
            producto = Producto(codigo, nombre, categoria,
                                self._convertir_precio(precio),
                                self._convertir_cantidad(cantidad))
        except ValueError as error:
            return ResultadoOperacion(False, str(error))

        self._productos.append(producto)
        self._productos_por_codigo[producto.codigo] = producto
        return self._persistir(
            f"Producto '{producto.nombre}' registrado correctamente.", producto
        )

    def consultar_producto(self, codigo: str) -> ResultadoOperacion:
        """Busca un producto para mostrarlo en el formulario.

        Args:
            codigo: Código del producto que se desea consultar.

        Returns:
            Un ResultadoOperacion con el producto encontrado o el motivo
            por el que no se pudo consultar.
        """
        if not codigo.strip():
            return ResultadoOperacion(
                False, "Indique el código del producto que desea consultar."
            )
        producto = self.buscar_producto(codigo)
        if producto is None:
            return ResultadoOperacion(
                False, f"No existe un producto con el código '{codigo.strip()}'."
            )
        return ResultadoOperacion(
            True, f"Producto '{producto.nombre}' cargado en el formulario.", producto
        )

    def actualizar_producto(self, codigo: str, nombre: str, categoria: str,
                            precio: str, cantidad: str) -> ResultadoOperacion:
        """Actualiza los datos de un producto existente.

        El código identifica al producto y no se modifica. Los datos nuevos
        se validan antes de aplicarlos, de modo que un valor incorrecto no
        deja el producto a medio actualizar.

        Args:
            codigo: Código del producto que se desea actualizar.
            nombre: Nombre nuevo del producto.
            categoria: Categoría nueva del producto.
            precio: Precio nuevo, en texto.
            cantidad: Cantidad nueva, en texto.

        Returns:
            Un ResultadoOperacion con el mensaje para la vista y, si se
            actualizó, el producto modificado.
        """
        if not codigo.strip():
            return ResultadoOperacion(
                False, "Indique el código del producto que desea actualizar."
            )
        producto = self.buscar_producto(codigo)
        if producto is None:
            return ResultadoOperacion(
                False, f"No existe un producto con el código '{codigo.strip()}'."
            )
        try:
            validado = Producto(producto.codigo, nombre, categoria,
                                self._convertir_precio(precio),
                                self._convertir_cantidad(cantidad))
        except ValueError as error:
            return ResultadoOperacion(False, str(error))

        producto.nombre = validado.nombre
        producto.categoria = validado.categoria
        producto.precio = validado.precio
        producto.cantidad = validado.cantidad
        return self._persistir(
            f"Producto '{producto.nombre}' actualizado correctamente.", producto
        )

    def eliminar_producto(self, codigo: str) -> ResultadoOperacion:
        """Elimina un producto de la colección.

        Args:
            codigo: Código del producto que se desea eliminar.

        Returns:
            Un ResultadoOperacion con el mensaje para la vista y, si se
            eliminó, el producto retirado de la colección.
        """
        if not codigo.strip():
            return ResultadoOperacion(
                False, "Indique el código del producto que desea eliminar."
            )
        producto = self.buscar_producto(codigo)
        if producto is None:
            return ResultadoOperacion(
                False, f"No existe un producto con el código '{codigo.strip()}'."
            )
        self._productos.remove(producto)
        self._productos_por_codigo.pop(producto.codigo, None)
        return self._persistir(
            f"Producto '{producto.nombre}' eliminado correctamente.", producto
        )

    # --- APOYO INTERNO ---
    def _persistir(self, mensaje_exito: str,
                   producto: Producto | None = None) -> ResultadoOperacion:
        """Solicita a ArchivoServicio guardar la colección de productos.

        Args:
            mensaje_exito: Mensaje que se muestra si el guardado funciona.
            producto: Producto afectado por la operación.

        Returns:
            El ResultadoOperacion que corresponde según el guardado.
        """
        registros = [producto.a_diccionario() for producto in self._productos]
        if not self._archivo.guardar_productos(registros):
            return ResultadoOperacion(
                False,
                "El cambio se aplicó, pero no se pudo guardar en productos.json.",
                producto,
            )
        return ResultadoOperacion(True, mensaje_exito, producto)

    @staticmethod
    def _convertir_precio(valor: str) -> float:
        """Convierte a número el precio escrito en el formulario.

        Raises:
            ValueError: Si el texto no representa un número.
        """
        try:
            return float(str(valor).strip().replace(",", "."))
        except ValueError:
            raise ValueError(
                "El precio debe ser un número, por ejemplo 12.50."
            ) from None

    @staticmethod
    def _convertir_cantidad(valor: str) -> int:
        """Convierte a número entero la cantidad escrita en el formulario.

        Raises:
            ValueError: Si el texto no representa un número entero.
        """
        try:
            return int(str(valor).strip())
        except ValueError:
            raise ValueError(
                "La cantidad debe ser un número entero, por ejemplo 10."
            ) from None
