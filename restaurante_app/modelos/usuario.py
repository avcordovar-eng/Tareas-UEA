"""Módulo que define la clase Usuario del restaurante."""


class Usuario:
    """Representa a una persona registrada para acceder al sistema.

    El modelo se adapta a la necesidad de esta etapa: además de identificar
    a la persona, guarda el nombre de acceso y la contraseña utilizados en
    la simulación de ingreso. La comparación de credenciales es una
    simulación pedagógica: la contraseña se almacena en texto plano dentro
    del JSON y no representa un mecanismo real de autenticación segura.

    Attributes:
        identificacion (str): Identificación única del usuario.
        nombre (str): Nombre completo del usuario.
        usuario (str): Nombre de acceso utilizado en la pantalla de login.
        contrasena (str): Contraseña utilizada en la simulación de acceso.
        rol (str): Rol del usuario dentro del restaurante.
    """

    def __init__(self, identificacion: str, nombre: str, usuario: str,
                 contrasena: str, rol: str = "Empleado") -> None:
        self.identificacion = identificacion
        self.nombre = nombre
        self.usuario = usuario
        self.contrasena = contrasena
        self.rol = rol

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
    def usuario(self) -> str:
        return self._usuario

    @usuario.setter
    def usuario(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre de acceso no puede estar vacío.")
        self._usuario = valor.strip()

    @property
    def contrasena(self) -> str:
        return self._contrasena

    @contrasena.setter
    def contrasena(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La contraseña no puede estar vacía.")
        self._contrasena = valor.strip()

    @property
    def rol(self) -> str:
        return self._rol

    @rol.setter
    def rol(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El rol del usuario no puede estar vacío.")
        self._rol = valor.strip()

    @property
    def contrasena_oculta(self) -> str:
        """Representación enmascarada de la contraseña para mostrarla en pantalla."""
        return "•" * len(self.contrasena)

    def credenciales_validas(self, usuario: str, contrasena: str) -> bool:
        """Comprueba si el nombre de acceso y la contraseña corresponden a este usuario.

        El nombre de acceso se compara sin distinguir mayúsculas de
        minúsculas; la contraseña se compara de forma exacta.

        Args:
            usuario: Nombre de acceso ingresado en la pantalla de login.
            contrasena: Contraseña ingresada en la pantalla de login.

        Returns:
            True si ambos datos coinciden con los del usuario, False si no.
        """
        return (self.usuario.lower() == usuario.strip().lower()
                and self.contrasena == contrasena)

    def a_diccionario(self) -> dict[str, object]:
        """Convierte el usuario a un diccionario con el formato del JSON."""
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "usuario": self.usuario,
            "contrasena": self.contrasena,
            "rol": self.rol,
        }

    @classmethod
    def desde_diccionario(cls, registro: dict[str, object]) -> "Usuario":
        """Reconstruye un objeto Usuario a partir de un diccionario.

        Args:
            registro: Diccionario con las claves identificacion, nombre,
                usuario y contrasena, y opcionalmente rol. Si falta una clave
                obligatoria se propaga un KeyError; si un valor no es válido
                se propaga un ValueError o un TypeError.

        Returns:
            Una nueva instancia de Usuario con los datos del registro.
        """
        return cls(
            identificacion=str(registro["identificacion"]),
            nombre=str(registro["nombre"]),
            usuario=str(registro["usuario"]),
            contrasena=str(registro["contrasena"]),
            rol=str(registro.get("rol", "Empleado")),
        )

    def __str__(self) -> str:
        return f"{self.nombre} ({self.usuario}) - {self.rol}"

    def __repr__(self) -> str:
        return (f"Usuario(identificacion='{self.identificacion}', "
                f"nombre='{self.nombre}', usuario='{self.usuario}', "
                f"rol='{self.rol}')")
