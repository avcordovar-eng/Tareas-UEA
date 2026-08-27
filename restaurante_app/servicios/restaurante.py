"""Módulo que define la clase Restaurante como servicio del sistema."""

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class Restaurante:
    """Servicio encargado de administrar las colecciones y operaciones del sistema.

    Gestiona una lista de productos, una lista de usuarios y una lista de
    ventas. Todos los registros, búsquedas, actualizaciones, eliminaciones
    y consultas se realizan a través de los métodos de esta clase; main.py
    nunca manipula directamente las listas internas.
    """

    def __init__(self, nombre: str) -> None:
        self.nombre: str = nombre
        self._productos: list[Producto] = []
        self._usuarios: list[Usuario] = []
        self._ventas: list[Venta] = []

    @property
    def productos(self) -> list[Producto]:
        """Devuelve una copia de la lista interna de productos."""
        return list(self._productos)

    @property
    def usuarios(self) -> list[Usuario]:
        """Devuelve una copia de la lista interna de usuarios."""
        return list(self._usuarios)

    @property
    def ventas(self) -> list[Venta]:
        """Devuelve una copia de la lista interna de ventas."""
        return list(self._ventas)

    def cargar_productos(self, productos: list[Producto]) -> None:
        """Incorpora los productos recuperados desde el archivo JSON.

        Se evita cargar dos veces un producto cuyo código ya existe en la
        colección, manteniendo la unicidad que exige el registro normal.

        Args:
            productos: Lista de objetos Producto reconstruidos al iniciar
                la aplicación.
        """
        for producto in productos:
            if self.buscar_producto(producto.codigo) is not None:
                print(f"Advertencia: el producto con código '{producto.codigo}' "
                      f"ya existía y no se cargó nuevamente.")
                continue
            self._productos.append(producto)

    def cargar_usuarios(self, usuarios: list[Usuario]) -> None:
        """Incorpora los usuarios recuperados desde el archivo JSON.

        Args:
            usuarios: Lista de objetos Usuario reconstruidos al iniciar
                la aplicación.
        """
        for usuario in usuarios:
            if self.buscar_usuario(usuario.identificacion) is not None:
                print(f"Advertencia: el usuario con identificación '{usuario.identificacion}' "
                      f"ya existía y no se cargó nuevamente.")
                continue
            self._usuarios.append(usuario)

    def cargar_ventas(self, ventas: list[Venta]) -> None:
        """Incorpora las ventas recuperadas desde el archivo JSON.

        Args:
            ventas: Lista de objetos Venta reconstruidos al iniciar
                la aplicación.
        """
        self._ventas.extend(ventas)

    def registrar_producto(self, producto: Producto) -> bool:
        """Registra un producto evitando códigos duplicados.

        Returns:
            True si el producto se registró, False si el código ya existe.
        """
        if self.buscar_producto(producto.codigo) is not None:
            print(f"Error: Ya existe un producto con el código '{producto.codigo}'.")
            return False
        self._productos.append(producto)
        return True

    def buscar_producto(self, codigo: str) -> Producto | None:
        """Busca un producto por su código.

        Returns:
            El producto encontrado o None si no existe.
        """
        for producto in self._productos:
            if producto.codigo == codigo.strip():
                return producto
        return None

    def actualizar_producto(self, codigo: str, nombre: str,
                            categoria: str, precio: float) -> bool:
        """Actualiza los datos de un producto existente.

        Returns:
            True si se actualizó, False si el producto no existe.
        """
        producto = self.buscar_producto(codigo)
        if producto is None:
            print(f"Error: No se encontró un producto con el código '{codigo}'.")
            return False
        producto.nombre = nombre
        producto.categoria = categoria
        producto.precio = precio
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        """Elimina un producto por su código.

        Returns:
            True si se eliminó, False si el producto no existe.
        """
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        self._productos.remove(producto)
        return True

    def listar_productos(self) -> None:
        """Lista todos los productos registrados."""
        if not self._productos:
            print("No hay productos registrados.")
            return
        print(f"\n--- Productos de {self.nombre} ---")
        for i, producto in enumerate(self._productos, 1):
            print(f"{i}. {producto.nombre} ({producto.codigo}) - "
                  f"Categoría: {producto.categoria} - ${producto.precio:.2f}")

    def registrar_usuario(self, usuario: Usuario) -> bool:
        """Registra un usuario evitando identificaciones duplicadas.

        Returns:
            True si el usuario se registró, False si la identificación ya existe.
        """
        for existente in self._usuarios:
            if existente.identificacion == usuario.identificacion:
                print(f"Error: Ya existe un usuario con identificación "
                      f"'{usuario.identificacion}'.")
                return False
        self._usuarios.append(usuario)
        return True

    def listar_usuarios(self) -> None:
        """Lista todos los usuarios registrados."""
        if not self._usuarios:
            print("No hay usuarios registrados.")
            return
        print(f"\n--- Usuarios de {self.nombre} ---")
        for i, usuario in enumerate(self._usuarios, 1):
            print(f"{i}. {usuario.nombre} - Identificación: "
                  f"{usuario.identificacion} - Correo: {usuario.correo}")

    def buscar_usuario(self, identificacion: str) -> Usuario | None:
        """Busca un usuario por su identificación.

        Returns:
            El usuario encontrado o None si no existe.
        """
        for usuario in self._usuarios:
            if usuario.identificacion == identificacion.strip():
                return usuario
        return None

    def vender_producto(self, codigo_producto: str, identificacion_usuario: str,
                        cantidad: int) -> bool:
        """Realiza la venta de un producto a un usuario.

        Valida que el usuario exista, el producto exista, la cantidad sea
        válida y haya stock suficiente. Si todo es correcto, registra la
        venta, disminuye el stock y retorna True.

        Returns:
            True si la venta se realizó correctamente, False en caso contrario.
        """
        usuario = self.buscar_usuario(identificacion_usuario)
        producto = self.buscar_producto(codigo_producto)

        if usuario is None:
            print(f"Error: No se encontró un usuario con identificación "
                  f"'{identificacion_usuario}'.")
            return False

        if producto is None:
            print(f"Error: No se encontró un producto con el código "
                  f"'{codigo_producto}'.")
            return False

        if cantidad <= 0:
            print("Error: La cantidad debe ser mayor que cero.")
            return False

        if producto.stock < cantidad:
            print(f"Error: Stock insuficiente. Disponible: {producto.stock}, "
                  f"Solicitado: {cantidad}.")
            return False

        venta = Venta(usuario.identificacion, producto.codigo, cantidad)
        self._ventas.append(venta)
        producto.vender(cantidad)
        print(f"Venta realizada: {producto.nombre} x{cantidad} para "
              f"{usuario.nombre}.")
        return True

    def consultar_ventas_usuario(self, identificacion_usuario: str) -> list[Venta]:
        """Obtiene las ventas realizadas por un usuario.

        Args:
            identificacion_usuario: Identificación del usuario a consultar.

        Returns:
            Lista de ventas del usuario (puede estar vacía).
        """
        ventas_usuario: list[Venta] = []
        for venta in self._ventas:
            if venta.usuario_id == identificacion_usuario:
                ventas_usuario.append(venta)
        return ventas_usuario

    def listar_ventas_usuario(self, identificacion_usuario: str) -> None:
        """Muestra las ventas realizadas por un usuario."""
        ventas = self.consultar_ventas_usuario(identificacion_usuario)
        usuario = self.buscar_usuario(identificacion_usuario)
        if usuario is None:
            print(f"Error: No se encontró un usuario con identificación "
                  f"'{identificacion_usuario}'.")
            return
        if not ventas:
            print(f"No hay ventas registradas para {usuario.nombre}.")
            return
        print(f"\n--- Ventas de {usuario.nombre} ({identificacion_usuario}) ---")
        for venta in ventas:
            producto = self.buscar_producto(venta.producto_codigo)
            nombre_producto = producto.nombre if producto else "Producto eliminado"
            print(f"- {nombre_producto} ({venta.producto_codigo}) x{venta.cantidad}")

    def obtener_categorias(self) -> set[str]:
        """Retorna el conjunto de categorías únicas de los productos.

        El conjunto elimina automáticamente los duplicados, garantizando
        que cada categoría se presente una sola vez.

        Returns:
            Conjunto con las categorías de los productos registrados.
        """
        return {producto.categoria for producto in self._productos}
