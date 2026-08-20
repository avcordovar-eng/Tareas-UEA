# Sistema de Restaurante - Proyecto de POO en Python (Semana 10)

## Información del Estudiante

**Nombre:** Alex Vinicio Cordova Romero

## Descripción del Sistema

Sistema de administración básica de productos y usuarios de un restaurante, desarrollado con Programación Orientada a Objetos en Python. El programa se ejecuta mediante un menú interactivo desde consola y administra colecciones de objetos (productos y usuarios) implementadas con las estructuras de datos fundamentales de Python: `list`, `tuple`, `dict` y `set`.

La mejora principal de la Semana 10 consiste en incorporar **persistencia de productos mediante un archivo JSON**. Antes, la colección de productos existía únicamente durante la ejecución del programa; ahora, al cerrar la aplicación los productos se conservan en `datos/productos.json` y se recuperan nuevamente al iniciar una nueva ejecución, reconstruyéndose como objetos `Producto`. Los usuarios permanecen solo en memoria durante esta semana, como se solicita en la actividad.

## Estructura del Proyecto

```
restaurante_app/
├── datos/
│   └── productos.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   └── usuario.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante.py
├── main.py
└── README.md
```

La carpeta `datos/` se utiliza únicamente como ubicación para almacenar `productos.json`. No representa una nueva capa de la arquitectura del sistema.

## Responsabilidad de cada Componente

### `modelos/producto.py` - Clase `Producto`
Entidad que representa un producto del restaurante. Sus atributos son: `codigo`, `nombre`, `categoria` y `precio`. Utiliza propiedades (`@property`) con validaciones que garantizan la integridad de los datos (campos no vacíos y precio mayor que cero). Además incorpora dos métodos para la persistencia:
- `a_diccionario()`: convierte la información del objeto a un diccionario para poder guardarla en JSON.
- `desde_diccionario(registro)`: método de clase que reconstruye un objeto `Producto` a partir de un diccionario recuperado del archivo.

### `modelos/usuario.py` - Clase `Usuario`
Entidad general que representa a una persona registrada en el sistema. Sus atributos son: `identificacion`, `nombre` y `correo`. Su información no se persiste en esta actividad.

### `servicios/restaurante.py` - Clase `Restaurante`
Servicio encargado de administrar las colecciones y operaciones del sistema. Mantiene dos listas internas: `_productos` (de tipo `list[Producto]`) y `_usuarios` (de tipo `list[Usuario]`). Proporciona los métodos de registro, búsqueda, actualización, eliminación y listado. Esta semana incorpora `cargar_productos()` para incorporar a la colección los objetos `Producto` reconstruidos desde el archivo, evitando duplicados. Todas las operaciones sobre las colecciones se realizan exclusivamente a través de sus métodos.

### `servicios/archivo_servicio.py` - Clase `ArchivoServicio`
Servicio encargado de concentrar la lectura y escritura de `datos/productos.json`:
- `cargar_productos()`: utiliza `json.load()` para recuperar los registros almacenados, valida cada registro y reconstruye los objetos `Producto`.
- `guardar_productos()`: convierte la colección de objetos `Producto` a una lista de diccionarios y la escribe mediante `json.dump()`.

Ambos métodos utilizan `with open()` y `encoding="utf-8"`, y controlan de forma específica las excepciones de acceso a archivos y de formato.

### `main.py`
Punto de arranque del programa. Coordina el menú interactivo y la interacción por consola: muestra las opciones, solicita los datos mediante `input()`, crea los objetos `Producto` y `Usuario`, y delega en el servicio `Restaurante`. Además coordina la persistencia: al iniciar crea un `ArchivoServicio`, carga los productos almacenados y los entrega al servicio `Restaurante`; después de registrar, actualizar o eliminar un producto correctamente solicita el guardado de la colección. `main.py` nunca modifica directamente las listas internas del servicio.

## Funcionamiento de datos/productos.json

`datos/productos.json` es un archivo de texto con formato JSON que almacena la colección de productos como una **lista de diccionarios**. Cada diccionario representa un producto con las claves `codigo`, `nombre`, `categoria` y `precio`:

```json
[
    {
        "codigo": "P001",
        "nombre": "Hamburguesa",
        "categoria": "Comida rápida",
        "precio": 5.5
    }
]
```

El archivo es un medio de persistencia y no reemplaza la clase `Producto`: durante la ejecución el programa continúa trabajando con objetos, y la conversión a diccionarios ocurre solo en el momento de guardar o cargar.

## Flujo de Carga

```
Inicio de la aplicación
        ↓
main.py crea ArchivoServicio
        ↓
Se intenta leer datos/productos.json
        ↓
json.load() recupera la información
        ↓
Se valida la estructura obtenida
        ↓
Cada registro válido se convierte en Producto(...)
        ↓
Los objetos se entregan al servicio Restaurante
        ↓
El menú trabaja normalmente con objetos Producto
```

## Flujo de Guardado

```
Usuario registra, actualiza o elimina un producto
        ↓
main.py solicita la operación al servicio Restaurante
        ↓
Restaurante modifica la colección en memoria
        ↓
Los objetos Producto se convierten a diccionarios
        ↓
ArchivoServicio utiliza json.dump()
        ↓
Se actualiza datos/productos.json
```

## Excepciones Controladas

- `FileNotFoundError`: si `productos.json` todavía no existe, el programa inicia normalmente con una colección vacía.
- `json.JSONDecodeError`: si el archivo existe pero su contenido no es un JSON válido, se muestra un mensaje y el programa inicia con la colección vacía.
- `PermissionError`: cuando no existen permisos suficientes para leer o escribir el archivo.
- `KeyError`: al reconstruir productos cuando un registro no contiene alguna de las claves esperadas; el registro defectuoso se ignora sin detener la aplicación.
- `ValueError` / `TypeError`: para datos inválidos, tanto en las validaciones propias de `Producto` como al reconstruir registros; se ignora el registro defectuoso y se continúa con los demás.
- `ValueError`: también se mantiene en `main.py` para impedir que precios no numéricos o campos vacíos detengan el programa.

No se utilizan capturas genéricas ni `except: pass`; cada excepción responde a una situación concreta del programa y evita que un problema esperado detenga abruptamente toda la aplicación.

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

## Comprobación de la Persistencia

Para verificar que los productos permanecen disponibles después de cerrar y volver a iniciar la aplicación, se realizó la siguiente prueba:

1. Se ejecutó `main.py`.
2. Se registraron productos mediante el menú (código, nombre, categoría y precio).
3. Se verificó que `datos/productos.json` contenía la información de los productos registrados.
4. Se cerró completamente el programa.
5. Se volvió a ejecutar `main.py`.
6. Se seleccionó la opción `5. Listar productos` y los productos anteriores aparecieron sin necesidad de volver a ingresarlos.
7. Se actualizó el precio de un producto y luego se eliminó otro.
8. Se reinició nuevamente la aplicación y se confirmó que tanto la actualización como la eliminación también se conservaron.

También se comprobó el manejo controlado de casos especiales: inicio sin el archivo, un archivo con contenido JSON inválido y registros incompletos, confirmando que en todos los casos el programa responde con un mensaje claro y continúa ejecutándose.

## Validaciones Consideradas

- Los códigos de productos no pueden repetirse.
- Las identificaciones de usuarios no pueden repetirse.
- Los campos obligatorios (código, nombre, categoría, precio, identificación, correo) no pueden estar vacíos.
- El precio debe ser un número mayor que cero.
- El correo electrónico debe contener el carácter `@`.
- Las entradas incorrectas (opciones inválidas, precios no numéricos) no detienen el programa; muestran un mensaje de error y permiten continuar.
- Un registro defectuoso o incompleto en `productos.json` se ignora sin detener innecesariamente la aplicación.

## Reflexión

La persistencia mediante JSON separa la responsabilidad del almacenamiento de la lógica de dominio: la clase `Producto` sigue siendo la representación del dominio durante toda la ejecución, el servicio `Restaurante` administra las colecciones con operaciones propias del negocio y el nuevo `ArchivoServicio` concentra exclusivamente la lectura y escritura del archivo. Este desacoplamiento permite evolucionar cada parte de forma independiente. El manejo de excepciones específicas convierte los problemas esperados de acceso a archivos (inexistencia, permisos, formato inválido o registros incompletos) en mensajes controlados en lugar de fallas abruptas, manteniendo la aplicación utilizable incluso cuando los datos externos no están en las mejores condiciones. Comprender cuándo transformar objetos a diccionarios y volver a reconstruirlos es la base para cualquier sistema que necesite conservar su estado más allá de la memoria temporal del programa.