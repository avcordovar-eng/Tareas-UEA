# Sistema de Gestión de Restaurante (POO en Python)

**Estudiante:** Alex Vinicio Cordova Romero  
**Materia:** Programación Orientada a Objetos  
**Semestre:** 2  

---

## 1. Descripción del Sistema

Este proyecto es una implementación de consola básica en Python orientada a objetos que modela el funcionamiento interno de un restaurante. Permite gestionar:
- **Catálogo del Menú:** Adición y control de productos (platos, bebidas, postres) con nombre, precio y categoría.
- **Clientes y Mesas:** Registro de clientes, asignación de mesas y control de su consumo.
- **Consumo y Cuentas:** Capacidad de que cada cliente ordene múltiples productos y cálculo automatizado del total acumulado a pagar.

El objetivo del proyecto es evidenciar la correcta aplicación de conceptos fundamentales de POO como encapsulamiento, modelado de relaciones entre entidades, creación y llamada a constructores (`__init__`), uso de métodos especiales de representación (`__str__`), y sobre todo, la estructuración modular del código.

---

## 2. Estructura del Proyecto

El código está organizado siguiendo la estructura jerárquica obligatoria para garantizar la separación de responsabilidades:

```
restaurante_app/
│
├── modelos/
│   ├── __init__.py      # Inicializador del paquete de modelos (opcional/vacío)
│   ├── producto.py      # Clase Producto (entidad que representa platillos/bebidas)
│   └── cliente.py       # Clase Cliente (entidad con mesa, consumos y métodos de cálculo)
│
├── servicios/
│   ├── __init__.py      # Inicializador del paquete de servicios (opcional/vacío)
│   └── restaurante.py   # Clase de servicio Restaurante (controlador de lógica de negocio)
│
└── main.py              # Punto de entrada y script de demostración del sistema
```

### Detalle de Componentes:
- **`modelos/producto.py`:** Define los datos base de cada elemento en el menú.
- **`modelos/cliente.py`:** Administra el estado individual de consumo de cada comensal.
- **`servicios/restaurante.py`:** Actúa como orquestador del restaurante, agregando elementos al menú, registrando comensales y coordinando la visualización general.
- **`main.py`:** Script principal que inicializa los objetos, simula el consumo y presenta de forma ordenada los resultados en la consola.

---

## 3. Reflexión: Importancia de la Modularización y Separación de Responsabilidades

La modularización y la separación de responsabilidades (principio de responsabilidad única o *Single Responsibility Principle*) constituyen los pilares del desarrollo de software moderno y mantenible por las siguientes razones:

1. **Facilidad de Mantenimiento y Extensibilidad:** Al mantener cada entidad (como `Producto` y `Cliente`) en archivos separados dentro de una estructura lógica (`modelos/` vs `servicios/`), cualquier cambio futuro —por ejemplo, agregar impuestos a la cuenta o guardar los datos en una base de datos— se realiza de manera aislada sin alterar o desestabilizar otras partes del sistema.
2. **Reutilización de Código:** Los módulos independientes pueden ser importados en múltiples secciones de la aplicación o en otros proyectos. Por ejemplo, la clase `Producto` podría ser utilizada tanto en un servicio de inventario de cocina como en un sistema de facturación electrónica sin necesidad de duplicar su código.
3. **Legibilidad y Trabajo en Equipo:** Un proyecto modularizado permite a un desarrollador comprender rápidamente el flujo y arquitectura de la aplicación en pocos minutos. Además, facilita que varios programadores trabajen simultáneamente en diferentes archivos (por ejemplo, uno mejorando la lógica en `restaurante.py` y otro extendiendo el modelo en `cliente.py`) sin experimentar conflictos de código complejos.
4. **Facilidad para Pruebas (Testability):** Separar las clases facilita la creación de pruebas unitarias automatizadas para cada funcionalidad, garantizando que el cálculo del total de un cliente funcione perfectamente e independientemente de cómo se muestre la interfaz en consola.
