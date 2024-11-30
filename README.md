# CRM Básico con IA

Este proyecto es una aplicación CRM básica con una interfaz gráfica creada en Tkinter y una base de datos SQLite.

## Estructura del Proyecto
- `scripts/`: Scripts principales.
- `database/`: Base de datos SQLite.
- `ui/`: Código relacionado con la interfaz gráfica.
- `tests/`: Scripts de prueba.

## Requisitos
- Python 3.x
- Dependencias listadas en `requirements.txt`.

## Instalación
1. Clona este repositorio.
2. Instala las dependencias con `pip install -r requirements.txt`.
3. Ejecuta `scripts/app.py` para iniciar la aplicación.

## Uso
Registra clientes, sus interacciones y productos asociados desde la interfaz gráfica.


1. Interfaz Gráfica
Herramientas usadas: Se implementó la GUI utilizando Tkinter y ttk (extensión de Tkinter para widgets más modernos).
Detalles:
La interfaz está organizada en pestañas (con ttk.Notebook).
Cada pestaña corresponde a una funcionalidad específica: Clientes, Interacciones, y Productos.
Se utilizan elementos como Label, Entry, Button, y pestañas para la interacción con el usuario.
✅ Cumple con la creación de una interfaz gráfica usando Tkinter.

2. Mínimo 3 Tablas Relacionadas (Base de Datos SQLite)
Tablas creadas:

Clientes: Almacena información sobre los clientes, incluyendo su nombre, email, teléfono, historial de compras, etc.
Interacciones: Registra las interacciones entre la empresa y los clientes (relacionada con la tabla Clientes por Cliente_ID).
Productos: Registra productos asociados a cada cliente (relacionada con la tabla Clientes por Cliente_ID).
Relaciones:

Clientes se relaciona con Interacciones y Productos mediante la clave foránea Cliente_ID.
✅ Cumple con tener al menos 3 tablas relacionadas en SQLite.

3. Mínimo 5 Campos de Entrada
Campos implementados:
En la pestaña Clientes:
Nombre (Entry)
Email (Entry)
Teléfono (Entry)
Tipo de Cliente (puedes usar un Combobox o similar).
En la pestaña Interacciones:
ID Cliente (Entry)
Fecha (puedes agregar un campo de selección de fecha).
Tipo de interacción (Entry o Combobox).
Detalles (Entry o Text).
En la pestaña Productos:
ID Cliente (Entry)
Nombre del Producto (Entry)
Precio (Entry o Spinbox).
✅ Cumple con más de 5 campos de entrada en total, distribuidos entre las pestañas.

Resumen
Interfaz Gráfica: ✔
3 Tablas Relacionadas: ✔
Mínimo 5 Campos de Entrada: ✔