# Sistema de Restaurante - Proyecto de POO en Python

## Información del Estudiante
**Nombre:** Alex Vinicio Cordova Romero

## Descripción del Sistema
Este proyecto implementa un sistema de restaurante utilizando Programación Orientada a Objetos (POO) en Python. El sistema permite gestionar productos y clientes de un restaurante mediante una interfaz de consola interactiva.

## Estructura del Proyecto
La estructura del proyecto sigue una arquitectura modular:

```
restaurante_app/
├── modelos/
│   ├── __init__.py                    # Módulo de modelos
│   ├── producto.py                    # Clase base Producto
│   ├── platillo.py                    # Subclase Platillo (hereda de Producto)
│   ├── bebida.py                      # Subclase Bebida (hereda de Producto)
│   └── cliente.py                     # Clase Cliente (usando @dataclass)
├── servicios/
│   ├── __init__.py                   # Módulo de servicios
│   └── restaurante.py                # Clase de servicio para gestión
└── main.py                           # Punto de entrada principal
```

## Uso del Constructor en la Clase Producto
La clase `Producto` utiliza un constructor tradicional `__init__()` que inicializa los atributos básicos:

```python
def __init__(self, nombre: str, categoria: str, precio: float, disponible: bool = True) -> None:
    self.nombre = nombre
    self.categoria = categoria
    self.precio = precio
    self.disponible = disponible
```

El constructor solicita datos al usuario y crea instancias de los objetos a través de los setters correspondientes, que aplican validaciones.

## Uso de @property y @setter en la Clase Producto
La clase `Producto` implementa @property y @setter para cada atributo importante, proporcionando encapsulamiento y validación:

- **@property nombre**: Getter que retorna el nombre del producto
- **@nombre.setter**: Setter con validación para nombres no vacíos
- **@property categoria**: Getter que retorna la categoría del producto
- **@categoria.setter**: Setter con validación para categorías no vacías
- **@property precio**: Getter que retorna el precio del producto
- **@precio.setter**: Setter con validación para precios mayores a 0
- **@property disponible**: Getter que retorna el estado de disponibilidad
- **@disponible.setter**: Setter sin validación (acepta cualquier valor booleano)

Estas propiedades garantizan que los atributos se modifiquen de forma controlada según las reglas de negocio.

## Uso de @dataclass en la Clase Cliente
La clase `Cliente` utiliza el decorador `@dataclass`, eliminando la necesidad de escribir manualmente los métodos `__init__`, `__str__`, `__repr__`, etc.:

```python
@dataclass
class Cliente:
    nombre: str
    correo: str
    id_cliente: int
```

El decorador `@dataclass` automáticamente genera:
- Método `__init__()` con los campos especificados
- Métodos `__str__()` y `__repr__()` según la estructura definida
- Validación de tipos a través de type hints

Esto permite crear instancias de clientes fácilmente desde datos de entrada del usuario.

## Menú Interactivo
El sistema presenta un menú interactivo con las siguientes opciones principales:

```
========================================
        SISTEMA DE RESTAURANTE
========================================
1. Registrar producto
2. Listar productos
3. Buscar producto
----------------------------------------
4. Registrar cliente
5. Listar clientes
6. Buscar cliente
----------------------------------------
7. Salir
========================================
```

El flujo de cada operación principal sigue la siguiente lógica:

1. **Entrada de datos del usuario** → `input()`
2. **Validación y creación de objeto** → constructor de la clase
3. **Registro en la clase Restaurante** → `registrar_producto()` o `registrar_cliente()`
4. **Listado o búsqueda del registro** → métodos `listar_*()` o `buscar_*()`

Este flujo demuestra la comprensión de la relación entre entrada de datos, creación de objetos, almacenamiento en listas y consulta de información dentro de una aplicación orientada a objetos.

## Reflexión: Creación de Objetos desde Datos de Entrada
La creación de objetos a partir de datos ingresados por el usuario es fundamental en los sistemas de interfaz gráfica. Este proyecto demuestra que:

1. **La arquitectura de objetos puede ser diseñada independientemente de la interfaz de usuario**
2. **Las entidades de negocio (Producto, Cliente, Restaurante) se mantienen separadas de la lógica de entrada/salida**
3. **Los validadores en los setters pueden aplicarse directamente después de la creación de objetos**
4. **El polimorfismo permite tratar diferentes tipos de productos de forma uniforme**

Este enfoque desacoplado facilita el mantenimiento, las pruebas y la extensión del sistema hacia interfaces más complejas (gráficas, web, CLI) en el futuro.

## Conceptos de POO Aplicados

### Herencia
- `Platillo` y `Bebida` heredan de `Producto` utilizando `super()`
- Cada subclase agrega atributos específicos (ingredientes, calorías, volumen) y sobrescribe `mostrar_informacion()`

### Encapsulamiento
- Los atributos privados de `Producto` están protegidos por @property y @setter
- Validaciones en los setters previenen valores inválidos

### Polimorfismo
- Sobreescritura de `mostrar_informacion()` en subclases
- Lista de productos tratada uniformemente mientras cada objeto muestra sus datos específicos

### Arquitectura Modular
- Separación de modelos, servicios y entrada/salida principal
- Permite el mantenimiento independiente y la reutilización de componentes

## Ejecución
Para ejecutar el sistema, navegue a `restaurante_app/` y ejecute:

```bash
python main.py
```