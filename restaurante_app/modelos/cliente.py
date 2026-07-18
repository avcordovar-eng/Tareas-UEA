"""Módulo que define la clase Cliente del restaurante."""


class Cliente:
    """Clase que representa un cliente registrado.

    Attributes:
        identificacion (str): Identificación única del cliente.
        nombre (str): Nombre del cliente.
        correo (str): Correo electrónico del cliente.
    """

    def __init__(self, identificacion: str, nombre: str, correo: str) -> None:
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo

    @property
    def identificacion(self) -> str:
        return self._identificacion

    @identificacion.setter
    def identificacion(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La identificación del cliente no puede estar vacía.")
        self._identificacion = valor.strip()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre del cliente no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if not valor or "@" not in valor:
            raise ValueError("El correo electrónico no es válido.")
        self._correo = valor.strip()

    def mostrar_informacion(self) -> None:
        """Muestra la información del cliente."""
        print(f"  Identificación: {self.identificacion}")
        print(f"  Nombre: {self.nombre}")
        print(f"  Correo: {self.correo}")

    def __str__(self) -> str:
        return f"{self.nombre} ({self.correo}) - ID: {self.identificacion}"

    def __repr__(self) -> str:
        return (f"Cliente(identificacion='{self.identificacion}', "
                f"nombre='{self.nombre}', correo='{self.correo}')")
