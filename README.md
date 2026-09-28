# Restaurante App — Manejo de eventos: ventas, botones y callbacks (Tkinter/ttk)

Aplicación de escritorio para la gestión de un restaurante. Parte de la versión con
componentes y contenedores construida en la Semana 14 y la amplía con el tema de la
**Semana 15: fundamentos del manejo de eventos**.

La aplicación inicia en una pantalla de acceso simulada y, tras una validación
correcta, muestra un panel principal con tres secciones: **Productos** (registrar,
cargar/consultar, actualizar y eliminar), **Usuarios** (consulta) y, nueva en esta
etapa, **Ventas**: seleccionar un usuario y un producto existentes y registrar la
operación mediante un botón conectado a un callback.

---

## Propósito de esta etapa

- Comprender el fundamento básico del manejo de eventos en Tkinter: un botón asociado
  mediante `command=` dispara un **callback**, y ese callback coordina una operación
  sin concentrar en la interfaz la lógica del sistema.
- Incorporar una venta como caso práctico: relaciona un usuario existente con un
  producto existente y dos componentes de selección (`ttk.Combobox`).
- Mantener las validaciones y la persistencia de la venta dentro de
  `RestauranteServicio`, igual que ya ocurre con productos y con el acceso.
- Incorporar la carpeta `assets/` con un logotipo e iconos propios, usados en el
  login, el encabezado, los títulos de sección y los botones principales.
- Conservar íntegras las funciones de las semanas anteriores: acceso, navegación,
  gestión de productos y consulta de usuarios.

---

## Estructura del proyecto

```
Repositorio
├── restaurante_app/
│   ├── datos/
│   │   ├── productos.json        Productos del restaurante
│   │   ├── usuarios.json         Usuarios habilitados para el acceso
│   │   └── ventas.json           Ventas registradas (nuevo)
│   ├── modelos/
│   │   ├── __init__.py
│   │   ├── producto.py           Clase Producto
│   │   ├── usuario.py            Clase Usuario
│   │   └── venta.py              Clase Venta (nuevo)
│   ├── servicios/
│   │   ├── __init__.py
│   │   ├── archivo_servicio.py   Lectura y escritura de los tres archivos JSON
│   │   └── restaurante_servicio.py  Reglas y operaciones del restaurante
│   ├── ui/
│   │   ├── __init__.py           Paleta, estilos ttk, tablas y carga de iconos
│   │   ├── login_view.py         Pantalla de acceso, ahora con el logo
│   │   └── main_view.py          Panel principal y sus secciones
│   ├── assets/                   Logo e iconos (nuevo, obligatorio esta semana)
│   │   ├── logo.png
│   │   ├── icono_productos.png
│   │   ├── icono_usuarios.png
│   │   ├── icono_ventas.png
│   │   ├── icono_registrar_venta.png
│   │   └── icono_salir.png
│   └── main.py                   Punto de entrada y cambio entre vistas
└── README.md
```

Se conserva la arquitectura modular de las semanas anteriores. `main_view.py` reúne el
contenedor principal (`MainView`) y las tres secciones que este organiza dentro de su
área de contenido: `ProductosView`, `UsuariosView` y la nueva `VentaView`.

### Responsabilidad de cada parte

| Elemento | Responsabilidad |
|---|---|
| `modelos/producto.py` | Representa un producto: código, nombre, categoría, precio y cantidad. |
| `modelos/usuario.py` | Representa un usuario: identificación, nombre, usuario de acceso, contraseña y rol. |
| `modelos/venta.py` | Representa una venta: relaciona la identificación de un usuario con el código de un producto y guarda la fecha de la operación. |
| `servicios/archivo_servicio.py` | Única clase que abre archivos: lee y guarda `productos.json`, `usuarios.json` y `ventas.json`. |
| `servicios/restaurante_servicio.py` | Convierte los registros en objetos, valida el acceso, ejecuta las operaciones sobre productos y **registra y lista las ventas**, solicitando el guardado después de cada cambio. |
| `ui/login_view.py` | Pantalla de acceso con el logo, sus campos, mensajes y botón de ingreso. |
| `ui/main_view.py` | `MainView` (encabezado con logo, navegación y contenido); `ProductosView`; `UsuariosView`; `VentaView` (selección de usuario y producto, botón "Registrar venta" y tabla de ventas). |
| `ui/__init__.py` | Recursos visuales compartidos y `cargar_icono()`, que lee los archivos de `assets/`. |
| `main.py` | Prepara los servicios, crea la única ventana de Tkinter, asigna su icono y controla el cambio entre acceso y panel principal. |

---

## El fundamento de eventos: botón → command= → callback → servicio

La sección de Ventas es donde se evidencia el tema de la semana:

```
Usuario selecciona un Usuario y un Producto (ttk.Combobox)
                    ↓
Usuario pulsa "Registrar venta"
                    ↓
El botón lo indica con command=self.registrar_venta   (VentaView, ui/main_view.py)
                    ↓
Tkinter ejecuta el callback registrar_venta()
                    ↓
El callback lee la selección y llama a
RestauranteServicio.registrar_venta(usuario_identificacion, producto_codigo)
                    ↓
El servicio valida que ambos existan, crea la Venta
y pide a ArchivoServicio que la guarde en ventas.json
                    ↓
El callback recibe el ResultadoVenta y llama a refrescar():
la tabla, el resumen y los selectores se actualizan,
y el mensaje del servicio se muestra en la barra de estado
```

El botón se conecta con `command=self.registrar_venta` (una referencia a la función,
no `self.registrar_venta()`, que la ejecutaría de inmediato al construir la interfaz).
El callback (`VentaView.registrar_venta`) **no valida ni guarda nada por sí mismo**:
solo traduce la selección de los componentes a los identificadores que
`RestauranteServicio.registrar_venta()` necesita, y muestra el resultado.

No se usa `bind()`, doble clic ni eventos de teclado o mouse para esta operación: los
`ttk.Combobox` en modo `readonly` y el botón con `command=` bastan para cubrir el
fundamento de la semana.

---

## Componentes y contenedores utilizados

### Contenedores

| Contenedor | Dónde se usa | Para qué |
|---|---|---|
| `ttk.Frame` | Encabezado, menú lateral, área de contenido, cada sección, filas de selección/acciones | Separar la ventana en zonas |
| `ttk.Labelframe` | "Datos del producto", "Productos registrados", "Personal con acceso al sistema", "Nueva venta", "Ventas registradas" | Delimitar con un título los bloques de formulario e información |
| `tk.Frame` | Tarjeta de acceso y encabezado de `LoginView` | Agrupar y centrar el logo y los campos de ingreso |

### Componentes (incorporados o ampliados esta semana)

| Componente | Dónde se usa | Para qué |
|---|---|---|
| `ttk.Combobox` (`state="readonly"`) | Selección de usuario y de producto en Ventas | Elegir un registro existente sin escritura libre |
| `ttk.Button` con `image=` y `compound="left"` | "Registrar venta", "Cerrar sesión" | Combinar icono y texto en un mismo botón |
| `ttk.Treeview` + `ttk.Scrollbar` | Tabla de ventas (fecha, usuario, producto, precio) | Mostrar el historial, con la más reciente primero |
| `tk.PhotoImage` (vía `cargar_icono()`) | Logo y los cinco iconos de `assets/` | Incorporar recursos visuales sin depender de librerías externas |
| `tk.StringVar` | Selección de usuario y de producto | Enlazar los combobox con el callback |

---

## Recursos visuales (`assets/`, obligatorio esta semana)

Se incorporó el logotipo del restaurante (un plato con cubiertos cruzados) y cinco
iconos, generados como parte de este trabajo:

| Archivo | Uso en la interfaz |
|---|---|
| `logo.png` | Icono de la ventana, encabezado de `LoginView` y encabezado de `MainView` |
| `icono_productos.png` | Junto al título "Gestión de productos" |
| `icono_usuarios.png` | Junto al título "Usuarios registrados" |
| `icono_ventas.png` | Junto al título "Registro de ventas" |
| `icono_registrar_venta.png` | Dentro del botón "Registrar venta" |
| `icono_salir.png` | Dentro del botón "Cerrar sesión" |

Los archivos se generaron con Pillow como herramienta de construcción, pero **la
aplicación no depende de Pillow**: los carga en tiempo de ejecución con
`tkinter.PhotoImage`, que lee PNG de forma nativa desde Tk 8.6. Si un icono llegara a
faltar, `cargar_icono()` devuelve `None` y la interfaz simplemente omite la imagen sin
interrumpirse.

---

## Operaciones sobre productos (de la Semana 14, sin cambios)

| Botón | Qué hace | Método del servicio |
|---|---|---|
| **Registrar** | Crea un producto con los datos del formulario | `registrar_producto()` |
| **Cargar** | Busca un producto por su código y lo muestra en el formulario | `consultar_producto()` |
| **Actualizar** | Cambia nombre, categoría, precio y cantidad del producto indicado | `actualizar_producto()` |
| **Eliminar** | Retira el producto de la colección, previa confirmación | `eliminar_producto()` |
| **Limpiar** | Vacía el formulario | (solo interfaz) |

---

## Persistencia

`RestauranteServicio` recibe `ArchivoServicio` como dependencia desde `main.py`. Tras
registrar una venta, el servicio convierte toda la colección de ventas en registros y
pide a `ArchivoServicio.guardar_ventas()` que los escriba en `datos/ventas.json`. La
misma relación ya existía para productos.

Las vistas no abren archivos en ningún caso: `ArchivoServicio` es la única clase del
proyecto que usa `open()`.

Reglas que aplica `RestauranteServicio.registrar_venta()`:

- debe seleccionarse un usuario y un producto (no puede estar vacío);
- el usuario indicado debe existir;
- el producto indicado debe existir;
- si el usuario y el producto existen, se crea la venta con la fecha y hora actuales
  y se guarda de inmediato.

Esta etapa registra la relación usuario–producto–fecha; no descuenta existencias del
producto ni calcula totales, para mantener el alcance en el fundamento de eventos que
pide la semana.

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

Las rutas de los archivos JSON y de `assets/` se resuelven a partir de la ubicación del
proyecto, de modo que la aplicación funciona sin importar desde qué carpeta se invoque.

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
| 2 | El acceso y la navegación siguen funcionando | ✔ |
| 3 | Usuarios y Productos mantienen sus funciones previas | ✔ |
| 4 | Existe una sección visible de Ventas | ✔ |
| 5 | Puede seleccionarse un usuario registrado | ✔ |
| 6 | Puede seleccionarse un producto registrado | ✔ |
| 7 | Se registra una venta mediante el botón correspondiente | ✔ |
| 8 | El botón usa `command=` para ejecutar el callback | ✔ |
| 9 | El callback delega el registro en `RestauranteServicio` | ✔ |
| 10 | La nueva venta se guarda en `ventas.json` | ✔ |
| 11 | La venta aparece en la tabla de la interfaz | ✔ |
| 12 | Las ventas se recuperan al cerrar y volver a ejecutar la aplicación | ✔ |
| 13 | No quedan nombres ni mensajes de "libro" o "biblioteca" | ✔ |
| 14 | La interfaz mantiene una apariencia clara y consistente | ✔ |

---

## Funcionalidades pendientes

- El registro de ventas no descuenta existencias del producto vendido ni calcula
  totales o facturación: esta etapa se limita a la relación usuario–producto–fecha.
- Registro de usuarios desde la interfaz: la sección de usuarios sigue siendo de solo
  consulta.
- Guardado de `usuarios.json`: en esta etapa ese archivo únicamente se lee.
