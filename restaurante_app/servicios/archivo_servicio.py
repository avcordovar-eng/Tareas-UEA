"""Módulo que define el servicio de lectura y escritura de los datos locales."""

import json
from pathlib import Path

CARPETA_DATOS: Path = Path(__file__).resolve().parent.parent / "datos"


class ArchivoServicio:
    """Servicio encargado de leer y guardar los archivos JSON de datos/.

    Es la única clase del proyecto que abre archivos. Trabaja con los
    registros tal como están almacenados (listas de diccionarios); la
    conversión entre esos registros y los objetos del dominio es
    responsabilidad de RestauranteServicio. Las vistas nunca utilizan este
    servicio de forma directa.

    Las rutas se resuelven a partir de la ubicación del proyecto, de modo
    que la aplicación se ejecuta correctamente sin importar desde qué
    carpeta se invoque main.py.

    Attributes:
        ruta_productos (Path): Ruta del archivo de productos.
        ruta_usuarios (Path): Ruta del archivo de usuarios.
        ruta_ventas (Path): Ruta del archivo de ventas.
    """

    def __init__(self, ruta_productos: str | Path | None = None,
                 ruta_usuarios: str | Path | None = None,
                 ruta_ventas: str | Path | None = None) -> None:
        self.ruta_productos: Path = Path(
            ruta_productos if ruta_productos is not None
            else CARPETA_DATOS / "productos.json"
        )
        self.ruta_usuarios: Path = Path(
            ruta_usuarios if ruta_usuarios is not None
            else CARPETA_DATOS / "usuarios.json"
        )
        self.ruta_ventas: Path = Path(
            ruta_ventas if ruta_ventas is not None
            else CARPETA_DATOS / "ventas.json"
        )

    def leer_productos(self) -> list[dict[str, object]]:
        """Lee datos/productos.json y devuelve los registros almacenados.

        Returns:
            Lista de diccionarios con los datos de cada producto. La lista
            es vacía si el archivo no existe o no se puede interpretar.
        """
        return self._leer_json(self.ruta_productos)

    def leer_usuarios(self) -> list[dict[str, object]]:
        """Lee datos/usuarios.json y devuelve los registros almacenados.

        Returns:
            Lista de diccionarios con los datos de cada usuario. La lista
            es vacía si el archivo no existe o no se puede interpretar.
        """
        return self._leer_json(self.ruta_usuarios)

    def leer_ventas(self) -> list[dict[str, object]]:
        """Lee datos/ventas.json y devuelve los registros almacenados.

        Returns:
            Lista de diccionarios con los datos de cada venta. La lista es
            vacía si el archivo no existe o no se puede interpretar.
        """
        return self._leer_json(self.ruta_ventas)

    def guardar_productos(self, registros: list[dict[str, object]]) -> bool:
        """Guarda en datos/productos.json los registros recibidos.

        Reemplaza el contenido del archivo con la colección completa que
        entrega RestauranteServicio después de cada operación.

        Args:
            registros: Lista de diccionarios, uno por producto.

        Returns:
            True si el archivo se escribió correctamente, False si no.
        """
        try:
            self.ruta_productos.parent.mkdir(parents=True, exist_ok=True)
            with open(self.ruta_productos, "w", encoding="utf-8") as archivo:
                json.dump(registros, archivo, ensure_ascii=False, indent=4)
        except PermissionError:
            print(f"Error: no se tienen permisos para escribir en "
                  f"'{self.ruta_productos}'.")
            return False
        except OSError as error:
            print(f"Error: no se pudo guardar '{self.ruta_productos}' ({error}).")
            return False
        return True

    def guardar_ventas(self, registros: list[dict[str, object]]) -> bool:
        """Guarda en datos/ventas.json los registros recibidos.

        Reemplaza el contenido del archivo con la colección completa que
        entrega RestauranteServicio después de registrar una venta.

        Args:
            registros: Lista de diccionarios, uno por venta.

        Returns:
            True si el archivo se escribió correctamente, False si no.
        """
        try:
            self.ruta_ventas.parent.mkdir(parents=True, exist_ok=True)
            with open(self.ruta_ventas, "w", encoding="utf-8") as archivo:
                json.dump(registros, archivo, ensure_ascii=False, indent=4)
        except PermissionError:
            print(f"Error: no se tienen permisos para escribir en "
                  f"'{self.ruta_ventas}'.")
            return False
        except OSError as error:
            print(f"Error: no se pudo guardar '{self.ruta_ventas}' ({error}).")
            return False
        return True

    def _leer_json(self, ruta: Path) -> list[dict[str, object]]:
        """Abre un archivo JSON y devuelve la lista de registros que contiene.

        Los problemas de lectura no interrumpen la aplicación: se informan
        por consola como diagnóstico y se devuelve una lista vacía, de modo
        que la interfaz siempre pueda iniciarse.

        Args:
            ruta: Ruta del archivo JSON que se desea leer.

        Returns:
            Lista de diccionarios leídos del archivo, o una lista vacía.
        """
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                contenido = json.load(archivo)
        except FileNotFoundError:
            print(f"Aviso: no se encontró '{ruta}'; la colección inicia vacía.")
            return []
        except json.JSONDecodeError:
            print(f"Error: '{ruta}' no contiene un JSON válido; "
                  f"la colección inicia vacía.")
            return []
        except PermissionError:
            print(f"Error: no se tienen permisos para leer '{ruta}'; "
                  f"la colección inicia vacía.")
            return []

        if not isinstance(contenido, list):
            print(f"Error: la estructura de '{ruta}' no es una lista de "
                  f"registros; la colección inicia vacía.")
            return []

        registros: list[dict[str, object]] = []
        for registro in contenido:
            if not isinstance(registro, dict):
                print(f"Advertencia: se ignoró un registro que no es un "
                      f"diccionario en '{ruta}': {registro}")
                continue
            registros.append(registro)
        return registros
