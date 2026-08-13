# Sistema de Restaurante - Proyecto de POO en Python (Semana 9)

## Información del Estudiante

**Nombre:** Alex Vinicio Cordova Romero

## Descripción del Sistema

Sistema de administración básica de productos y usuarios de un restaurante, desarrollado con Programación Orientada a Objetos en Python. El programa se ejecuta mediante un menú interactivo desde consola y administra colecciones de objetos (productos y usuarios) implementadas con las estructuras de datos fundamentales de Python: `list`, `tuple`, `dict` y `set`.

La mejora principal de esta semana consiste en pasar del manejo de objetos individuales a la administración organizada de colecciones de objetos y datos. El servicio `Restaurante` concentra todas las operaciones de registro, búsqueda, actualización, eliminación y listado, manteniendo a `main.py` únicamente como punto de interacción por consola.

## Estructura del Proyecto

```
restaurante_app/
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   └── usuario.py
├── servicios/
│   ├── __init__.py
│   └── restaurante.py
├── main.py
└── README.md
```

## Responsabilidad de cada Componente

### `modelos/producto.py` - Clase `Producto`
Entidad que representa un producto del restaurante. Sus atributos son: `codigo`, `nombre`, `categoria` y `precio`. Utiliza propiedades (`@property`) con validaciones que garantizan la integridad de los datos (campos no vacíos y precio mayor que cero). Implementa `mostrar_informacion()` y `__str__()` para su presentación.

### `modelos/usuario.py` - Clase `Usuario`
Entidad general que representa a una persona registrada en el sistema. Sus atributos son: `identificacion`, `nombre` y `correo`. Representa de forma general a los usuarios, de modo que el proyecto pueda evolucionar posteriormente hacia clientes, empleados o administradores sin necesidad de implementar todavía una jerarquía adicional. Incluye validación del correo electrónico y de campos vacíos.

### `servicios/restaurante.py` - Clase `Restaurante`
Servicio encargado de administrar las colecciones y operaciones del sistema. Mantiene dos listas internas: `_productos` (de tipo `list[Producto]`) y `_usuarios` (de tipo `list[Usuario]`). Proporciona los métodos:
- `registrar_producto()` y `registrar_usuario()`: agregan elementos evitando códigos e identificaciones duplicados.
- `buscar_producto()`: busca un producto por su código.
- `actualizar_producto()`: actualiza nombre, categoría y precio de un producto existente.
- `eliminar_producto()`: elimina un producto por su código.
- `listar_productos()` y `listar_usuarios()`: muestran todas las colecciones.
- `obtener_categorias()`: retorna las categorías únicas de los productos mediante un conjunto.

`main.py` no modifica directamente las listas internas; todas las operaciones sobre las colecciones se realizan exclusivamente a través de los métodos del servicio.

### `main.py`
Punto de arranque del programa. Coordina el menú interactivo y la interacción por consola: muestra las opciones, solicita los datos mediante `input()`, crea los objetos `Producto` y `Usuario`, y delega en el servicio `Restaurante`. Organiza las opciones mediante funciones y evita una cadena extensa de condicionales, ya que cada opción del menú se asocia con su función a través de un diccionario.

## Estructuras de Datos Aplicadas

### `list` (Lista)
- **Dónde:** `servicios/restaurante.py`.
- **Para qué:** Se utiliza para administrar las colecciones dinámicas de objetos del sistema. `Restaurante` mantiene una `list[Producto]` (`_productos`) y una `list[Usuario]` (`_usuarios`). Son colecciones dinámicas porque se agregan y eliminan elementos durante la ejecución mediante los métodos de registro, actualización y eliminación.

### `tuple` (Tupla)
- **Dónde:** `main.py`, constante `OPCIONES_MENU`.
- **Para qué:** Representa información estable que no debe modificarse durante la ejecución: las opciones disponibles del menú principal. Al ser inmutable, se garantiza que la estructura del menú permanezca fija mientras el programa se ejecuta, y se utiliza tanto para mostrar las opciones en pantalla como para organizar la salida.

### `dict` (Diccionario)
- **Dónde:** `main.py`, constante `ACCIONES_MENU`.
- **Para qué:** Establece una relación clara de clave → valor: cada opción del menú (clave, ej. `"1"` o `"2"`) se asocia con la función encargada de ejecutarla (valor). Esto evita una cadena extensa de `if/elif` y permite despachar la opción seleccionada de forma directa y ordenada.

### `set` (Conjunto)
- **Dónde:** `servicios/restaurante.py`, método `obtener_categorias()`.
- **Para qué:** Retorna las categorías únicas de los productos registrados. El conjunto elimina automáticamente los valores duplicados, garantizando que cada categoría se muestre una sola vez sin necesidad de verificaciones manuales.

## Flujo del Sistema

```
Usuario selecciona una opción
        ↓
main.py solicita o recibe los datos necesarios
        ↓
main.py utiliza el servicio Restaurante
        ↓
Restaurante procesa la operación solicitada
        ↓
Se consulta o modifica la colección correspondiente
        ↓
main.py presenta el resultado al usuario
```

## Menú Interactivo

```
========================================
        SISTEMA DE RESTAURANTE
========================================
1. Registrar producto
2. Buscar producto
3. Actualizar producto
4. Eliminar producto
5. Listar productos
----------------------------------------
6. Registrar usuario
7. Listar usuarios
----------------------------------------
8. Mostrar categorías
9. Salir
```

## Instrucciones de Ejecución

1. Asegúrese de tener Python 3.10 o superior instalado (se utilizan anotaciones de tipos con unión, como `Producto | None`).
2. Navegue hasta la carpeta `restaurante_app/`:
   ```bash
   cd restaurante_app
   ```
3. Ejecute el programa:
   ```bash
   python main.py
   ```
4. Seleccione una opción del menú para registrar, buscar, actualizar o eliminar productos; registrar o listar usuarios; o mostrar las categorías únicas. El programa continúa en ejecución hasta que el usuario selecciona la opción `9. Salir`.

## Validaciones Consideradas

- Los códigos de productos no pueden repetirse.
- Las identificaciones de usuarios no pueden repetirse.
- Los campos obligatorios (código, nombre, categoría, precio, identificación, correo) no pueden estar vacíos.
- El precio debe ser un número mayor que cero.
- El correo electrónico debe contener el carácter `@`.
- Las entradas incorrectas (opciones inválidas, precios no numéricos) no detienen el programa; muestran un mensaje de error y permiten continuar.

## Reflexión

La selección de una estructura de datos adecuada es una decisión de diseño tan importante como el propio algoritmo, porque cada estructura ofrece ventajas y limitaciones distintas según la necesidad del problema. En este proyecto, la `list` fue la opción correcta para las colecciones de productos y usuarios porque el sistema requiere agregar, recorrer y eliminar elementos de forma dinámica manteniendo el orden de inserción. La `tuple` garantizó la estabilidad de las opciones del menú al ser inmutable: el catálogo de opciones no puede modificarse accidentalmente durante la ejecución. El `dict` simplificó el despacho de acciones al asociar directamente cada opción con su función, evitando cadenas largas de condicionales y haciendo el código más legible y escalable. Finalmente, el `set` resolvió de manera elegante la necesidad de mostrar categorías únicas sin duplicados. Elegir mal una estructura puede llevar a un desempeño deficiente, código confuso o errores sutiles; por ello comprender las propiedades de cada estructura y su relación con la operación requerida es fundamental para construir soluciones claras y eficientes.