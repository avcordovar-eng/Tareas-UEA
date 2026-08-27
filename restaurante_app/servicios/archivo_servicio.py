"""Módulo que define el servicio de persistencia en JSON."""

import json
from pathlib import Path

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class ArchivoServicio:
    """Servicio encargado de cargar y guardar productos, usuarios y ventas en archivos JSON.

    Concentra toda la lectura y escritura de datos. Durante la ejecución el
    sistema continúa trabajando con objetos; este servicio únicamente se
    encarga de convertirlos a diccionarios para guardarlos y de
    reconstruirlos nuevamente al cargarlos.
    """

    def __init__(self, ruta_productos: str | Path = "datos/productos.json",
                 ruta_usuarios: str | Path = "datos/usuarios.json",
                 ruta_ventas: str | Path = "datos/ventas.json") -> None:
        self.ruta_productos: Path = Path(ruta_productos)
        self.ruta_usuarios: Path = Path(ruta_usuarios)
        self.ruta_ventas: Path = Path(ruta_ventas)

    # --- PRODUCTOS ---
    def cargar_productos(self) -> list[Producto]:
        """Recupera los productos almacenados y los convierte en objetos Producto."""
        try:
            with open(self.ruta_productos, "r", encoding="utf-8") as archivo:
                registros = json.load(archivo)
        except FileNotFoundError:
            print("No se encontró datos/productos.json; la colección inicia vacía.")
            return []
        except json.JSONDecodeError:
            print("Error: datos/productos.json no contiene un JSON válido; "
                  "la colección inicia vacía.")
            return []
        except PermissionError:
            print(f"Error: no se tienen permisos para leer '{self.ruta_productos}'; "
                  "la colección inicia vacía.")
            return []

        if not isinstance(registros, list):
            print("Error: la estructura de datos/productos.json no es una "
                  "lista de productos; la colección inicia vacía.")
            return []

        productos: list[Producto] = []
        for registro in registros:
            try:
                producto = Producto.desde_diccionario(registro)
            except KeyError as e:
                print(f"Advertencia: se ignoró un registro incompleto "
                      f"(falta la clave {e}): {registro}")
                continue
            except (ValueError, TypeError) as e:
                print(f"Advertencia: se ignoró un registro inválido ({e}): "
                      f"{registro}")
                continue
            productos.append(producto)
        return productos

    def guardar_productos(self, productos: list[Producto]) -> bool:
        """Convierte los productos a diccionarios y los guarda en el archivo."""
        registros: list[dict[str, object]] = [
            producto.a_diccionario() for producto in productos
        ]
        try:
            self.ruta_productos.parent.mkdir(parents=True, exist_ok=True)
            with open(self.ruta_productos, "w", encoding="utf-8") as archivo:
                json.dump(registros, archivo, ensure_ascii=False, indent=4)
        except PermissionError:
            print(f"Error: no se tienen permisos para escribir en "
                  f"'{self.ruta_productos}'.")
            return False
        return True

    # --- USUARIOS ---
    def cargar_usuarios(self) -> list[Usuario]:
        """Recupera los usuarios almacenados y los convierte en objetos Usuario."""
        try:
            with open(self.ruta_usuarios, "r", encoding="utf-8") as archivo:
                registros = json.load(archivo)
        except FileNotFoundError:
            print("No se encontró datos/usuarios.json; la colección inicia vacía.")
            return []
        except json.JSONDecodeError:
            print("Error: datos/usuarios.json no contiene un JSON válido; "
                  "la colección inicia vacía.")
            return []
        except PermissionError:
            print(f"Error: no se tienen permisos para leer '{self.ruta_usuarios}'; "
                  "la colección inicia vacía.")
            return []

        if not isinstance(registros, list):
            print("Error: la estructura de datos/usuarios.json no es una "
                  "lista de usuarios; la colección inicia vacía.")
            return []

        usuarios: list[Usuario] = []
        for registro in registros:
            try:
                usuario = Usuario.desde_diccionario(registro)
            except KeyError as e:
                print(f"Advertencia: se ignoró un registro incompleto "
                      f"(falta la clave {e}): {registro}")
                continue
            except (ValueError, TypeError) as e:
                print(f"Advertencia: se ignoró un registro inválido ({e}): "
                      f"{registro}")
                continue
            usuarios.append(usuario)
        return usuarios

    def guardar_usuarios(self, usuarios: list[Usuario]) -> bool:
        """Convierte los usuarios a diccionarios y los guarda en el archivo."""
        registros: list[dict[str, object]] = [
            usuario.a_diccionario() for usuario in usuarios
        ]
        try:
            self.ruta_usuarios.parent.mkdir(parents=True, exist_ok=True)
            with open(self.ruta_usuarios, "w", encoding="utf-8") as archivo:
                json.dump(registros, archivo, ensure_ascii=False, indent=4)
        except PermissionError:
            print(f"Error: no se tienen permisos para escribir en "
                  f"'{self.ruta_usuarios}'.")
            return False
        return True

    # --- VENTAS ---
    def cargar_ventas(self) -> list[Venta]:
        """Recupera las ventas almacenadas y las convierte en objetos Venta."""
        try:
            with open(self.ruta_ventas, "r", encoding="utf-8") as archivo:
                registros = json.load(archivo)
        except FileNotFoundError:
            print("No se encontró datos/ventas.json; la colección inicia vacía.")
            return []
        except json.JSONDecodeError:
            print("Error: datos/ventas.json no contiene un JSON válido; "
                  "la colección inicia vacía.")
            return []
        except PermissionError:
            print(f"Error: no se tienen permisos para leer '{self.ruta_ventas}'; "
                  "la colección inicia vacía.")
            return []

        if not isinstance(registros, list):
            print("Error: la estructura de datos/ventas.json no es una "
                  "lista de ventas; la colección inicia vacía.")
            return []

        ventas: list[Venta] = []
        for registro in registros:
            try:
                venta = Venta.desde_diccionario(registro)
            except KeyError as e:
                print(f"Advertencia: se ignoró un registro incompleto "
                      f"(falta la clave {e}): {registro}")
                continue
            except (ValueError, TypeError) as e:
                print(f"Advertencia: se ignoró un registro inválido ({e}): "
                      f"{registro}")
                continue
            ventas.append(venta)
        return ventas

    def guardar_ventas(self, ventas: list[Venta]) -> bool:
        """Convierte las ventas a diccionarios y las guarda en el archivo."""
        registros: list[dict[str, object]] = [
            venta.a_diccionario() for venta in ventas
        ]
        try:
            self.ruta_ventas.parent.mkdir(parents=True, exist_ok=True)
            with open(self.ruta_ventas, "w", encoding="utf-8") as archivo:
                json.dump(registros, archivo, ensure_ascii=False, indent=4)
        except PermissionError:
            print(f"Error: no se tienen permisos para escribir en "
                  f"'{self.ruta_ventas}'.")
            return False
        return True