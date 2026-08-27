# Sistema de Restaurante - Proyecto de POO en Python (Semana 11)

## Información del Estudiante

**Nombre:** Alex Vinicio Cordova Romero

## Descripción del Sistema

Sistema de administración de productos, usuarios y ventas de un restaurante, desarrollado con Programación Orientada a Objetos en Python. El programa se ejecuta mediante un menú interactivo desde consola y administra colecciones de objetos (productos, usuarios y ventas) implementadas con las estructuras de datos fundamentales de Python: `list`, `tuple`, `dict` y `set`.

La mejora principal de la Semana 11 consiste en incorporar **persistencia completa de productos, usuarios y ventas mediante archivos JSON**, y la operación de **venta** que relaciona un usuario con un producto, controla el stock disponible y registra la transacción. Ahora, al cerrar la aplicación, toda la información se conserva en `datos/productos.json`, `datos/usuarios.json` y `datos/ventas.json`, y se recupera nuevamente al iniciar una nueva ejecución, reconstruyéndose como objetos `Producto`, `Usuario` y `Venta`.

## Estructura del Proyecto

```
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante.py
├── main.py
└── README.md
```

La carpeta `datos/` se utiliza únicamente como ubicación para almacenar los archivos JSON. No representa una nueva capa de la arquitectura del sistema.

## Responsabilidad de cada Componente

### `modelos/producto.py` - Clase `Producto`
Entidad que representa un producto del restaurante. Sus atributos son: `codigo`, `nombre`, `categoria`, `precio` y `stock`. Utiliza propiedades (`@property`) con validaciones que garantizan la integridad de los datos (campos no vacíos, precio mayor que cero y stock no negativo). Incorpora el método `vender(cantidad)` que disminuye el stock validando disponibilidad. Además incorpora dos métodos para la persistencia:
- `a_diccionario()`: convierte la información del objeto a un diccionario para poder guardarla en JSON.
- `desde_diccionario(registro)`: método de clase que reconstruye un objeto `Producto` a partir de un diccionario recuperado del archivo.

### `modelos/usuario.py` - Clase `Usuario`
Entidad general que representa a una persona registrada en el sistema. Sus atributos son: `identificacion`, `nombre` y `correo`. Incorpora dos métodos para la persistencia:
- `a_diccionario()`: convierte la información del objeto a un diccionario.
- `desde_diccionario(registro)`: método de clase que reconstruye un objeto `Usuario` a partir de un diccionario.

### `modelos/venta.py` - Clase `Venta`
Nueva entidad que representa la relación entre un usuario y un producto vendido. Sus atributos son: `usuario_id` (identificación del usuario), `producto_codigo` (código del producto) y `cantidad` (unidades vendidas). Utiliza propiedades con validaciones (campos no vacíos y cantidad mayor que cero). Incorpora dos métodos para la persistencia:
- `a_diccionario()`: convierte la venta a un diccionario para JSON.
- `desde_diccionario(registro)`: reconstruye un objeto `Venta` desde un diccionario.

### `servicios/restaurante.py` - Clase `Restaurante`
Servicio encargado de administrar las colecciones y operaciones del sistema. Mantiene tres listas internas: `_productos` (`list[Producto]`), `_usuarios` (`list[Usuario]`) y `_ventas` (`list[Venta]`). Proporciona métodos de registro, búsqueda, actualización, eliminación y listado. Esta semana incorpora:
- `cargar_productos()`, `cargar_usuarios()`, `cargar_ventas()`: incorporan los objetos reconstruidos desde los archivos, evitando duplicados en productos y usuarios.
- `vender_producto(codigo_producto, identificacion_usuario, cantidad)`: valida usuario, producto, cantidad y stock; crea la `Venta`, la agrega a la colección, disminuye el stock del producto y retorna el resultado.
- `consultar_ventas_usuario(identificacion_usuario)`: recorre y filtra la colección de ventas para obtener las de un usuario específico.
- `listar_ventas_usuario(identificacion_usuario)`: muestra las ventas de un usuario con el nombre del producto y cantidad.

Todas las operaciones sobre las colecciones se realizan exclusivamente a través de sus métodos.

### `servicios/archivo_servicio.py` - Clase `ArchivoServicio`
Servicio encargado de concentrar la lectura y escritura de los tres archivos JSON:
- **Productos**: `cargar_productos()` y `guardar_productos()`.
- **Usuarios**: `cargar_usuarios()` y `guardar_usuarios()`.
- **Ventas**: `cargar_ventas()` y `guardar_ventas()`.

Todos los métodos utilizan `with open()` y `encoding="utf-8"`, y controlan de forma específica las excepciones de acceso a archivos (`FileNotFoundError`, `PermissionError`), formato (`json.JSONDecodeError`), estructura inválida, y reconstrucción (`KeyError`, `ValueError`, `TypeError`).

### `main.py`
Punto de arranque del programa. Coordina el menú interactivo y la interacción por consola: muestra las opciones, solicita los datos mediante `input()`, crea los objetos `Producto`, `Usuario` y `Venta`, y delega en el servicio `Restaurante`. Coordina la persistencia: al iniciar crea un `ArchivoServicio`, carga las tres colecciones almacenadas y las entrega al servicio `Restaurante`; después de cada operación que modifica datos (registrar/actualizar/eliminar producto, registrar usuario, realizar venta) solicita el guardado de las colecciones afectadas. `main.py` nunca modifica directamente las listas internas del servicio.

## Funcionamiento del Stock

Cada `Producto` mantiene un atributo `stock` (entero no negativo) que representa la cantidad disponible. Al realizar una venta:
1. Se valida que la cantidad solicitada sea mayor que cero.
2. Se valida que el stock actual sea suficiente (`producto.stock >= cantidad`).
3. Si ambas validaciones pasan, se llama a `producto.vender(cantidad)` que disminuye internamente el stock.
4. Se registra la `Venta` en la colección.
5. Se guardan `productos.json` (con el stock actualizado) y `ventas.json` (con la nueva venta).

Si el stock es insuficiente, la operación se rechaza sin modificar los datos.

## Relación Usuario–Producto mediante Venta

La operación principal de esta semana es la venta, que materializa la relación:
```
Usuario registrado  →  Producto existente  →  Validar cantidad y stock  →  Crear Venta(...)  →  Agregar a colección  →  Disminuir stock  →  Guardar ventas.json y productos.json
```

Una venta no es solo restar stock: queda registrada como objeto `Venta` en una colección, permitiendo consultar el historial por usuario.

## Persistencia de Productos, Usuarios y Ventas

Los tres archivos JSON funcionan como medios de persistencia:

### `productos.json`
Lista de diccionarios con claves: `codigo`, `nombre`, `categoria`, `precio`, `stock`.

### `usuarios.json`
Lista de diccionarios con claves: `identificacion`, `nombre`, `correo`.

### `ventas.json`
Lista de diccionarios con claves: `usuario_id`, `producto_codigo`, `cantidad`.

Flujo general:
```
OBJETOS → convertir_a_diccionario() → lista de diccionarios → json.dump() → archivo JSON
archivo JSON → json.load() → diccionarios → reconstrucción de objetos
```

**Guardado después de cada operación:**
- Registrar, actualizar o eliminar un producto → `guardar_productos()`.
- Registrar un usuario → `guardar_usuarios()`.
- Realizar una venta → `guardar_ventas()` y `guardar_productos()` (por el cambio de stock).

## Excepciones Controladas

- `FileNotFoundError`: si alguno de los archivos JSON no existe, la aplicación inicia con la colección correspondiente vacía.
- `json.JSONDecodeError`: si un archivo existe pero su contenido no es JSON válido, se muestra un mensaje y la colección inicia vacía.
- `PermissionError`: cuando no hay permisos para leer o escribir; se muestra mensaje y la operación falla controladamente.
- `KeyError`: al reconstruir objetos cuando un registro no contiene una clave esperada; el registro defectuoso se ignora y se continúa.
- `ValueError` / `TypeError`: para datos inválidos en reconstrucción o validaciones propias (`Producto`, `Usuario`, `Venta`); el registro se ignora y se continúa.
- `ValueError`: en `main.py` para impedir que entradas no numéricas o campos vacíos detengan el programa.

No se utilizan capturas genéricas ni `except: pass`; cada excepción responde a una situación concreta.

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
9. Vender producto
10. Consultar ventas de usuario
----------------------------------------
11. Salir
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
4. Seleccione una opción del menú. El programa continúa en ejecución hasta que el usuario selecciona la opción `11. Salir`.

## Comprobación de la Persistencia

Para verificar que productos, usuarios y ventas permanecen disponibles después de cerrar y volver a iniciar la aplicación, se realizó la siguiente prueba:

1. Se ejecutó `main.py`.
2. Se registró un usuario.
3. Se registró un producto con stock disponible.
4. Se realizó una venta (opción 9) indicando identificación, producto y cantidad.
5. Se confirmó que el stock disminuyó en `productos.json`.
6. Se verificó que `ventas.json` registró la operación.
7. Se consultaron las ventas del usuario (opción 10).
8. Se cerró completamente el programa.
9. Se volvió a ejecutar `main.py`.
10. Se confirmó que productos, usuarios y ventas fueron recuperados (listar productos, listar usuarios, consultar ventas).
11. Se intentó vender una cantidad mayor al stock disponible.
12. Se confirmó que la operación fue rechazada sin alterar los datos.

También se comprobó el manejo controlado de casos especiales: inicio sin archivos, archivos con contenido JSON inválido y registros incompletos, confirmando que en todos los casos el programa responde con un mensaje claro y continúa ejecutándose.

## Validaciones Consideradas

- Los códigos de productos no pueden repetirse.
- Las identificaciones de usuarios no pueden repetirse.
- Los campos obligatorios (código, nombre, categoría, precio, stock, identificación, correo) no pueden estar vacíos.
- El precio debe ser un número mayor que cero.
- El stock no puede ser negativo.
- La cantidad a vender debe ser mayor que cero y no superar el stock disponible.
- El correo electrónico debe contener el carácter `@`.
- Las entradas incorrectas (opciones inválidas, valores no numéricos) no detienen el programa; muestran un mensaje de error y permiten continuar.
- Un registro defectuoso o incompleto en los archivos JSON se ignora sin detener innecesariamente la aplicación.

## Reflexión

La persistencia mediante JSON separa la responsabilidad del almacenamiento de la lógica de dominio: las clases `Producto`, `Usuario` y `Venta` siguen siendo la representación del dominio durante toda la ejecución, el servicio `Restaurante` administra las colecciones con operaciones propias del negocio y el `ArchivoServicio` concentra exclusivamente la lectura y escritura de los archivos. Este desacoplamiento permite evolucionar cada parte de forma independiente.

El manejo de excepciones específicas convierte los problemas esperados de acceso a archivos (inexistencia, permisos, formato inválido o registros incompletos) en mensajes controlados en lugar de fallas abruptas, manteniendo la aplicación utilizable incluso cuando los datos externos no están en las mejores condiciones.

La operación de venta demuestra directamente el uso de colecciones para recorrer, comparar y filtrar objetos: buscar usuario y producto en sus respectivas colecciones, validar reglas de negocio, crear el objeto `Venta` que relaciona ambos, agregarlo a la colección de ventas, modificar el stock del producto y persistir los cambios. Comprender cómo los objetos se relacionan mediante referencias (ID y código) y cómo las colecciones permiten navegar esas relaciones es fundamental para modelar sistemas reales.