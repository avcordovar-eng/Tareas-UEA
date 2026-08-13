"""Módulo que define la clase Usuario del restaurante."""


class Usuario:
    """Clase que representa a una persona registrada en el sistema.

    Representa de forma general a los usuarios, de modo que el proyecto
    pueda evolucionar posteriormente hacia distintos tipos de usuario sin
    necesidad de implementar todavía una jerarquía adicional.

    Attributes:
        identificacion (str): Identificación única del usuario.
        nombre (str): Nombre del usuario.
        correo (str): Correo electrónico del usuario.
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
            raise ValueError("La identificación del usuario no puede estar vacía.")
        self._identificacion = valor.strip()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre del usuario no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if not valor or "@" not in valor:
            raise ValueError("El correo electrónico del usuario no es válido.")
        self._correo = valor.strip()

    def mostrar_informacion(self) -> None:
        """Muestra la información del usuario."""
        print(f"  Identificación: {self.identificacion}")
        print(f"  Nombre: {self.nombre}")
        print(f"  Correo: {self.correo}")

    def __str__(self) -> str:
        return f"{self.nombre} ({self.correo}) - ID: {self.identificacion}"

    def __repr__(self) -> str:
        return (f"Usuario(identificacion='{self.identificacion}', "
                f"nombre='{self.nombre}', correo='{self.correo}')")
