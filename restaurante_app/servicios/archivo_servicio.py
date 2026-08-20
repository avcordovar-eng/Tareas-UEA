"""Módulo que define el servicio de persistencia de productos en JSON."""

import json
from pathlib import Path

from modelos.producto import Producto


class ArchivoServicio:
    """Servicio encargado de cargar y guardar los productos en un archivo JSON.

    Concentra toda la lectura y escritura de datos/productos.json. Durante la
    ejecución el sistema continúa trabajando con objetos Producto; este
    servicio únicamente se encarga de convertirlos a diccionarios para
    guardarlos y de reconstruirlos nuevamente al cargarlos.
    """

    def __init__(self, ruta_archivo: str | Path = "datos/productos.json") -> None:
        self.ruta_archivo: Path = Path(ruta_archivo)

    def cargar_productos(self) -> list[Producto]:
        """Recupera los productos almacenados y los convierte en objetos Producto.

        Returns:
            Lista de productos reconstruidos. Si el archivo no existe, contiene
            JSON inválido o no hay permisos de lectura, se retorna una lista
            vacía para que la aplicación pueda iniciar normalmente.
        """
        try:
            with open(self.ruta_archivo, "r", encoding="utf-8") as archivo:
                registros = json.load(archivo)
        except FileNotFoundError:
            print("No se encontró datos/productos.json; "
                  "la colección inicia vacía.")
            return []
        except json.JSONDecodeError:
            print("Error: datos/productos.json no contiene un JSON válido; "
                  "la colección inicia vacía.")
            return []
        except PermissionError:
            print("Error: no se tienen permisos para leer "
                  f"'{self.ruta_archivo}'; la colección inicia vacía.")
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
        """Convierte los productos a diccionarios y los guarda en el archivo.

        Args:
            productos: Colección de objetos Producto a persistir.

        Returns:
            True si la escritura se completó, False si hubo un problema
            de permisos u otro error de acceso al archivo.
        """
        registros: list[dict[str, object]] = [
            producto.a_diccionario() for producto in productos
        ]
        try:
            self.ruta_archivo.parent.mkdir(parents=True, exist_ok=True)
            with open(self.ruta_archivo, "w", encoding="utf-8") as archivo:
                json.dump(registros, archivo, ensure_ascii=False, indent=4)
        except PermissionError:
            print(f"Error: no se tienen permisos para escribir en "
                  f"'{self.ruta_archivo}'.")
            return False
        return True