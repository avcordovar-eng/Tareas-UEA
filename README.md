# Sistema de Restaurante - Proyecto de POO en Python

## Información del Estudiante
**Nombre:** Alex Vinicio Cordova Romero

## Descripción del Sistema
Sistema de gestión básica de productos, bebidas y clientes de un restaurante, desarrollado con Programación Orientada a Objetos en Python. El programa se ejecuta mediante un menú interactivo desde consola y demuestra la aplicación de los principios SOLID (SRP, OCP, LSP) a través de una arquitectura modular con herencia y polimorfismo.

## Estructura del Proyecto

```
restaurante_app/
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── bebida.py
│   └── cliente.py
├── servicios/
│   ├── __init__.py
│   └── restaurante.py
└── main.py
```

## Responsabilidad de cada Clase

### `modelos/producto.py` - Clase `Producto`
Clase base que representa un producto general del restaurante. Sus atributos son: código, nombre, categoría y precio. Implementa el método `mostrar_informacion()` que muestra los datos del producto en consola. Utiliza propiedades (`@property`) con validaciones para garantizar la integridad de los datos.

### `modelos/bebida.py` - Clase `Bebida`
Clase hija de `Producto` que representa una bebida. Incorpora el atributo específico `tamanio` (pequeño, mediano, grande). Sobrescribe el método `mostrar_informacion()` para incluir la información del tamaño además de los datos heredados de producto.

### `modelos/cliente.py` - Clase `Cliente`
Clase independiente que representa a un cliente registrado. Sus atributos son: identificación, nombre y correo. Implementa su propio método `mostrar_informacion()`. No hereda de `Producto` porque un cliente no es un tipo de producto.

### `servicios/restaurante.py` - Clase `Restaurante`
Clase de servicio encargada de administrar las colecciones de productos y clientes. Proporciona métodos para registrar (con validación de duplicados) y listar elementos. Aplica polimorfismo al listar productos mediante el método común `mostrar_informacion()`.

### `main.py`
Punto de entrada del programa. Contiene únicamente la interacción con el usuario (menú, solicitud de datos, creación de objetos y llamadas al servicio). No administra listas internas ni contiene lógica de negocio.

## Relación entre Producto y Bebida

`Bebida` hereda de `Producto` porque una bebida **es un** tipo de producto del restaurante. Esta relación de herencia permite:

- Reutilizar los atributos comunes (código, nombre, categoría, precio) y sus validaciones.
- Almacenar objetos `Bebida` y `Producto` en una misma lista de tipo `list[Producto]`.
- Aplicar polimorfismo: al llamar a `mostrar_informacion()` en cada elemento de la lista, cada objeto ejecuta su propia versión del método según su clase real.

## Principios SOLID Aplicados

### SRP (Single Responsibility Principle)
Cada clase tiene una única responsabilidad:
- `Producto` y `Bebida` representan datos del producto.
- `Cliente` representa datos del cliente.
- `Restaurante` administra las colecciones y operaciones.
- `main.py` maneja únicamente la interacción por consola.

### OCP (Open/Closed Principle)
El sistema está abierto para extensión pero cerrado para modificación. Se puede agregar una nueva clase hija de `Producto` (ej. `Postre`) sin modificar la clase `Producto` ni el servicio `Restaurante`. El método `listar_productos()` funciona con cualquier subtipo de `Producto`.

### LSP (Liskov Substitution Principle)
`Bebida` puede sustituir a `Producto` en cualquier contexto sin alterar el comportamiento del sistema. Se almacena en `list[Producto]`, se registra mediante `registrar_producto()` y se lista mediante `mostrar_informacion()` sin necesidad de verificar su tipo.

## Instrucciones de Ejecución

1. Asegúrese de tener Python 3.8 o superior instalado.
2. Navegue hasta la carpeta `restaurante_app/`:
   ```bash
   cd restaurante_app
   ```
3. Ejecute el programa:
   ```bash
   python main.py
   ```
4. Seleccione una opción del menú interactivo para registrar o listar productos, bebidas y clientes.

## Menú Interactivo

```
========================================
        SISTEMA DE RESTAURANTE
========================================
1. Registrar producto
2. Registrar bebida
3. Registrar cliente
----------------------------------------
4. Listar productos
5. Listar clientes
----------------------------------------
6. Salir
```

## Reflexión

Diseñar proyectos mantenibles es fundamental en el desarrollo de software porque reduce el costo de los cambios futuros y facilita la incorporación de nuevas funcionalidades. La aplicación de principios como SRP, OCP y LSP, junto con una arquitectura modular, permite que cada componente sea modificado, probado y extendido de forma independiente. En este proyecto, separar la lógica de negocio (modelos), la lógica de servicio (Restaurante) y la interacción con el usuario (main.py) hace que el sistema sea más comprensible, escalable y resistente a errores. La herencia bien aplicada (Bebida hereda de Producto) evita la duplicación de código y mantiene la coherencia del comportamiento polimórfico, mientras que evitar herencias innecesarias (Cliente no hereda de Producto) previene acoplamientos artificiales. Estas buenas prácticas, aunque incrementan ligeramente la complejidad inicial del diseño, resultan indispensables para proyectos que crecen en tamaño y requieren mantenimiento a largo plazo.
