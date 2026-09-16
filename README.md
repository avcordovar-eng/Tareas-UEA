# Restaurante App — Interfaz con componentes y contenedores (Tkinter/ttk)

Aplicación de escritorio para la gestión de un restaurante. Parte de la versión
gráfica construida en la Semana 13 y la amplía con el tema de la **Semana 14:
componentes y contenedores**.

La aplicación inicia en una pantalla de acceso simulada y, tras una validación
correcta, muestra un panel principal organizado en zonas: navegación, formulario,
acciones e información. Desde ese panel se consultan los usuarios registrados y se
gestionan los productos del restaurante: registrar, cargar/consultar, actualizar y
eliminar, con persistencia en `datos/productos.json`.

---

## Propósito de esta etapa

- Aplicar **componentes y contenedores** de Tkinter/ttk para organizar la interfaz
  en zonas con una responsabilidad clara.
- Usar los gestores de geometría (`grid`, `pack`, `place`) de forma coherente,
  manteniendo una jerarquía ordenada entre ventana, contenedores y componentes.
- Incorporar las operaciones sobre productos desde la interfaz mediante botones con
  `command=`, sin manejo avanzado de eventos.
- Mantener las reglas y validaciones dentro de `RestauranteServicio`: las vistas
  recogen datos, muestran resultados y no deciden nada por su cuenta.
- Conservar la persistencia en `productos.json` a través de `ArchivoServicio`.

---

## Estructura del proyecto

```
Repositorio
├── restaurante_app/
│   ├── datos/
│   │   ├── productos.json        Productos del restaurante (se actualiza al operar)
│   │   └── usuarios.json         Usuarios habilitados para el acceso
│   ├── modelos/
│   │   ├── __init__.py
│   │   ├── producto.py           Clase Producto
│   │   └── usuario.py            Clase Usuario
│   ├── servicios/
│   │   ├── __init__.py
│   │   ├── archivo_servicio.py   Lectura y escritura de los archivos JSON
│   │   └── restaurante_servicio.py  Reglas y operaciones del restaurante
│   ├── ui/
│   │   ├── __init__.py           Paleta, fuentes, estilos ttk y armado de tablas
│   │   ├── login_view.py         Pantalla de acceso
│   │   └── main_view.py          Panel principal y sus secciones
│   └── main.py                   Punto de entrada y cambio entre vistas
└── README.md
```

Se conserva la arquitectura modular de la semana anterior, sin archivos nuevos.
`main_view.py` reúne el contenedor principal (`MainView`) y las dos secciones que este
organiza dentro de su área de contenido: `ProductosView` y `UsuariosView`.

### Responsabilidad de cada parte

| Elemento | Responsabilidad |
|---|---|
| `modelos/producto.py` | Representa un producto: código, nombre, categoría, precio y cantidad, validando sus datos en las propiedades. |
| `modelos/usuario.py` | Representa un usuario: identificación, nombre, usuario de acceso, contraseña y rol. |
| `servicios/archivo_servicio.py` | Única clase que abre archivos: lee `productos.json` y `usuarios.json`, y guarda `productos.json`. |
| `servicios/restaurante_servicio.py` | Convierte los registros en objetos, valida el acceso, resuelve las consultas y ejecuta las operaciones sobre productos, solicitando el guardado después de cada cambio. |
| `ui/login_view.py` | Pantalla de acceso con sus campos, mensajes y botón de ingreso. |
| `ui/main_view.py` | `MainView`: encabezado con la sesión, menú de navegación y área de contenido. `ProductosView`: formulario, botones de acción, tabla y barra de estado. `UsuariosView`: tabla de consulta con la sesión actual resaltada. |
| `ui/__init__.py` | Recursos visuales compartidos: colores, fuentes, estilos ttk y construcción de las tablas. |
| `main.py` | Prepara los servicios, crea la única ventana de Tkinter, registra los estilos y controla el cambio entre acceso y panel principal. |

---

## Componentes y contenedores utilizados

### Contenedores

| Contenedor | Dónde se usa | Para qué |
|---|---|---|
| `ttk.Frame` | Encabezado, menú lateral, área de contenido, cada sección, fila de acciones y cada campo del formulario | Separar la ventana en zonas y agrupar los componentes de cada una |
| `ttk.Labelframe` | "Datos del producto", "Productos registrados", "Personal con acceso al sistema", "Registro de ventas" | Delimitar con un título los bloques de formulario y de información |
| `tk.Frame` | Tarjeta de acceso en `LoginView` | Agrupar y centrar los campos de ingreso |

La jerarquía es: ventana (`Tk`) → vista (`LoginView` / `MainView`) → contenedores de
zona → contenedores de campo → componentes.

### Componentes

| Componente | Dónde se usa | Para qué |
|---|---|---|
| `ttk.Entry` | Código, nombre y precio | Capturar texto libre |
| `ttk.Combobox` | Categoría | Elegir una categoría existente o escribir una nueva |
| `ttk.Spinbox` | Cantidad | Fijar un número entero con incremento y límites (0 a 9999) |
| `ttk.Button` | Acciones de producto, navegación y cierre de sesión | Solicitar operaciones mediante `command=` |
| `ttk.Treeview` + `ttk.Scrollbar` | Tablas de productos y usuarios | Presentar los registros en columnas con desplazamiento |
| `ttk.Label` | Títulos, resúmenes, etiquetas de campo y barra de estado | Mostrar información y respuestas |
| `tk.StringVar` | Todos los campos | Enlazar los componentes con los datos del formulario |
| `messagebox.askyesno` | Botón Eliminar | Confirmar una acción que no se puede deshacer |

### Gestores de geometría

- **`grid`**: estructura de la ventana (encabezado, menú y contenido), cuadrícula del
  formulario y disposición de las secciones.
- **`pack`**: elementos que se apilan o se alinean en fila, como los botones de
  acción, los del menú lateral y la etiqueta sobre cada campo.
- **`place`**: centrado del aviso de la sección Ventas dentro de su contenedor.

---

## Mejoras realizadas en la interfaz

- El panel principal quedó dividido en zonas claras: **encabezado** con la sesión,
  **menú de navegación** a la izquierda y **área de contenido** a la derecha.
- Cada sección del sistema es ahora un contenedor independiente que se muestra u
  oculta dentro de la misma área de contenido.
- La sección de productos separa visualmente el **formulario**, las **acciones** y la
  **tabla de registros**.
- Se añadió una **barra de estado** al pie de la sección de productos: muestra una
  ayuda al inicio y, después de cada operación, el mensaje que devuelve el servicio,
  en verde si la operación se completó y en rojo si no.
- Los botones tienen jerarquía visual: acción principal (Registrar), acciones
  secundarias (Cargar, Actualizar, Limpiar) y acción destructiva (Eliminar).
- El menú lateral resalta la sección que se está mostrando.
- La apariencia se unificó mediante estilos ttk definidos en un solo lugar.
- El tamaño de la ventana se ajustó para que la aplicación entre completa en pantallas
  de 1366×768.

---

## Operaciones implementadas sobre productos

| Botón | Qué hace | Método del servicio |
|---|---|---|
| **Registrar** | Crea un producto con los datos del formulario | `registrar_producto()` |
| **Cargar** | Busca un producto por su código y muestra sus datos en el formulario | `consultar_producto()` |
| **Actualizar** | Cambia nombre, categoría, precio y cantidad del producto indicado | `actualizar_producto()` |
| **Eliminar** | Retira el producto de la colección, previa confirmación | `eliminar_producto()` |
| **Limpiar** | Vacía el formulario para empezar un registro nuevo | (solo interfaz) |

El identificador del proyecto es el **código del producto** (por ejemplo `P001`). Para
consultar, actualizar o eliminar se escribe ese código; si el campo está vacío, se usa
el código de la fila seleccionada en la tabla.

Validaciones que aplica `RestauranteServicio` y que la interfaz solo muestra:

- código, nombre y categoría no pueden estar vacíos;
- el código no puede repetirse al registrar;
- el precio debe ser un número mayor que cero (acepta coma o punto decimal);
- la cantidad debe ser un número entero no negativo;
- para actualizar, consultar o eliminar, el código debe corresponder a un producto
  existente.

Después de cada operación la interfaz vuelve a pedir la información al servicio y
redibuja la tabla, el resumen y las categorías disponibles.

---

## Persistencia

`RestauranteServicio` recibe `ArchivoServicio` como dependencia desde `main.py`. Tras
cada registro, actualización o eliminación, el servicio convierte la colección en
registros y solicita su guardado en `datos/productos.json`. Si el archivo no se puede
escribir, la interfaz lo informa en la barra de estado.

Las vistas no abren archivos en ningún caso: `ArchivoServicio` es la única clase del
proyecto que usa `open()`.

```
Botón  →  ProductosView  →  RestauranteServicio  →  ArchivoServicio  →  productos.json
                                    ↓
                      la vista vuelve a pedir los datos y se redibuja
```

---

## Ejecución

**Requisitos:** Python 3.10 o superior con Tkinter (incluido en la instalación estándar
de Python para Windows). No se necesitan librerías externas.

```bash
cd restaurante_app
python main.py
```

También puede ejecutarse desde la raíz del repositorio:

```bash
python restaurante_app/main.py
```

Las rutas de los archivos JSON se resuelven a partir de la ubicación del proyecto, de
modo que la aplicación funciona sin importar desde qué carpeta se la invoque.

### Credenciales de prueba

El acceso es una **simulación pedagógica**: las contraseñas se guardan en texto plano
dentro de `datos/usuarios.json` y no representan autenticación segura.

| Usuario | Contraseña | Rol |
|---|---|---|
| `admin` | `admin123` | Administrador |
| `jperez` | `juan456` | Mesero |
| `mlopez` | `maria789` | Cajera |
| `crios` | `carla321` | Chef |

---

## Comprobación de funcionamiento

| # | Comprobación | Resultado |
|---|---|---|
| 1 | `main.py` inicia sin errores | ✔ |
| 2 | El acceso con usuario y contraseña sigue funcionando | ✔ |
| 3 | La interfaz principal se muestra tras el acceso | ✔ |
| 4 | La sección Usuarios permite consultar la información registrada | ✔ |
| 5 | La sección Productos presenta el formulario organizado con contenedores | ✔ |
| 6 | Un producto nuevo aparece en la tabla y en el resumen | ✔ |
| 7 | Cargar por código muestra el producto en el formulario | ✔ |
| 8 | Al actualizar, los cambios se conservan | ✔ |
| 9 | Al eliminar, el producto deja de aparecer | ✔ |
| 10 | Los cambios se mantienen al cerrar y volver a ejecutar la aplicación | ✔ |
| 11 | Las vistas solicitan las operaciones a `RestauranteServicio` y no tocan los JSON | ✔ |
| 12 | La navegación y los controles resultan claros | ✔ |

---

## Funcionalidades pendientes

Se identifican como pendientes porque todavía no están desarrolladas gráficamente:

- **Ventas**: el registro de ventas mantiene su opción en el menú con el aviso
  correspondiente y se incorporará en las próximas semanas.
- Registro de usuarios desde la interfaz: la sección de usuarios es de solo consulta.
- Guardado de `usuarios.json`: en esta etapa ese archivo únicamente se lee.
