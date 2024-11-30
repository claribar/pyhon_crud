from tkinter import Label, Entry, Button, StringVar, ttk, Toplevel
from database.db_manager import guardar_cliente, guardar_interaccion, guardar_producto, desconectar
from tkinter import messagebox
from enums.enums import TipoCliente, TipoInteraccion  # Asegúrate de que estas enumeraciones estén definidas en este archivo
from ui.styles import aplicar_estilos
from datetime import datetime
from ui.tooltip import Tooltip  # Si usas tkintertooltip para tooltips
import re
from functools import partial

# Función para inicializar la GUI
def inicializar_gui(root, conn, cursor):
    """
    Configura la GUI, creando las pestañas de Clientes, Interacciones y Productos.
    Recibe el root (ventana principal), la conexión y el cursor de la base de datos.
    """
    # Aplicar estilos generales a la GUI
    aplicar_estilos()
    
    # Crear el contenedor de pestañas
    tab_control = ttk.Notebook(root)
    
    # Pestaña de Clientes
    tab_clientes = ttk.Frame(tab_control)
    tab_control.add(tab_clientes, text="Clientes")
    agregar_formulario(tab_clientes, conn, cursor)  # Aquí se llama al formulario de clientes
    
    # Pestaña de Interacciones
    tab_interacciones = ttk.Frame(tab_control)
    tab_control.add(tab_interacciones, text="Interacciones")
    agregar_formulario_interacciones(tab_interacciones, conn, cursor)  # Aquí se llama al formulario de interacciones
    
    # Pestaña de Productos
    tab_productos = ttk.Frame(tab_control)
    tab_control.add(tab_productos, text="Productos")
    agregar_formulario_productos(tab_productos, conn, cursor)  # Aquí se llama al formulario de productos
    
    # Mostrar las pestañas
    tab_control.pack(expand=1, fill="both")
    
    # Configurar la acción al cerrar la ventana
    root.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana(root, conn, cursor))
    
    # Iniciar la GUI
    root.mainloop()

# Función para cerrar la ventana y desconectar de la base de datos
def cerrar_ventana(root, conn, cursor):
    try:
        desconectar(conn, cursor)
        print("Conexión cerrada correctamente.")
    except Exception as e:
        print(f"Error al cerrar la conexión: {e}")
    root.quit()  # Cierra la ventana


# Función para borrar el placeholder al hacer clic en el campo
def borrar_placeholder(entry, placeholder, event=None):
    if entry.get() == placeholder:
        entry.delete(0, "end")  # Borrar el placeholder
        entry.config(fg="black")  # Cambiar el color a negro

# Función para poner el placeholder si el campo está vacío
def poner_placeholder(entry, placeholder, event=None):
    # Si el campo está vacío, poner de nuevo el placeholder
    if entry.get() == "":
        entry.insert(0, placeholder)
        entry.config(fg="grey")  # El color del placeholder debe ser gris


# Función para agregar un formulario dinámico de clientes
def agregar_formulario(tab_clientes, conn, cursor):
    campos = [
        ("Nombre", "nombre_var", "Ingrese el nombre completo del cliente."),
        ("Email", "email_var", "Ejemplo: cliente@dominio.com"),
        ("Teléfono", "telefono_var", "Ejemplo: +54 9 11 1234-5678"),
        ("Tipo de Cliente", "tipo_cliente_var", "Selecciona el tipo de cliente.")
    ]
    
    variables = {}
    
    # Crear campos de formulario dinámicamente
    for i, (etiqueta, var_nombre, placeholder) in enumerate(campos):
        Label(tab_clientes, text=f"{etiqueta}:").grid(row=i, column=0, padx=10, pady=5, sticky="w")
        variables[var_nombre] = StringVar()
        if etiqueta != "Tipo de Cliente":  # Placeholder solo para campos normales
            entry = Entry(tab_clientes, textvariable=variables[var_nombre])
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            entry.insert(0, placeholder)
            entry.config(fg="grey")  # El texto del placeholder será gris
            
            # Borrar el placeholder cuando el usuario haga clic en el campo
            entry.bind("<FocusIn>", partial(borrar_placeholder, entry, placeholder))
            
            # Volver a poner el placeholder si el campo está vacío al perder el foco
            entry.bind("<FocusOut>", partial(poner_placeholder, entry, placeholder))
            
            # Aplicar tooltip
            Tooltip(entry, f"Introduce {etiqueta.lower()}.")
        else:
            # ComboBox para "Tipo de Cliente"
            tipo_cliente_combobox = ttk.Combobox(
                tab_clientes,
                values=[e.value for e in TipoCliente],  # Opciones del enumerador
                state="readonly",
                textvariable=variables[var_nombre]
            )
            tipo_cliente_combobox.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            variables[var_nombre].set(placeholder)  # Inicializar con placeholder
            Tooltip(tipo_cliente_combobox, "Selecciona el tipo de cliente.")
    
    # Botón para guardar cliente
    ttk.Button(tab_clientes, text="Guardar Cliente", style="TButton", 
               command=lambda: on_guardar_cliente(variables, conn, cursor)).grid(row=len(campos), column=0, columnspan=2, padx=10, pady=20, sticky="nsew")

# Función para guardar cliente
def on_guardar_cliente(variables, conn, cursor):
    try:
        errores = []
        
        # Validación de cada campo
        nombre = variables["nombre_var"].get().strip()
        if not nombre or nombre == "Ingrese el nombre completo del cliente.":
            errores.append("El campo Nombre es obligatorio y no puede ser el texto sugerido.")
        
        email = variables["email_var"].get().strip()
        if not email or email == "Ejemplo: cliente@dominio.com":
            errores.append("El campo Email es obligatorio y no puede ser el texto sugerido.")
        
        telefono = variables["telefono_var"].get().strip()
        if not telefono or telefono == "Ejemplo: +54 9 11 1234-5678":
            errores.append("El campo Teléfono es obligatorio y no puede ser el texto sugerido.")
        
        tipo_cliente = variables["tipo_cliente_var"].get().strip()
        if tipo_cliente not in [e.value for e in TipoCliente]:  # Validar contra opciones válidas
            errores.append("Por favor selecciona un tipo de cliente válido.")
        
        if errores:
            messagebox.showerror("Error", "\n".join(errores))
            return
        
        # Guardar el cliente
        guardar_cliente(conn, cursor, nombre, email, telefono, tipo_cliente)
        
        messagebox.showinfo("Éxito", "Cliente guardado exitosamente.")
        clear_fields(variables)
        
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al guardar el cliente: {str(e)}")

# Función para limpiar los campos después de un envío exitoso
def clear_fields(variables):
    for var_nombre, var in variables.items():
        if var_nombre == "tipo_cliente_var":
            var.set("Selecciona el tipo de cliente.")  # Restablecer el placeholder del ComboBox
        else:
            var.set("")


# Función para agregar un formulario para interacciones
def agregar_formulario_interacciones(tab_interacciones, conn, cursor):
    """
    Configura el formulario para la gestión de interacciones.
    """
    # Etiqueta y campo de ID Cliente
    label_cliente_id = Label(tab_interacciones, text="ID Cliente:")
    label_cliente_id.grid(row=0, column=0, padx=10, pady=10)
    cliente_id_var = StringVar()
    entry_cliente_id = Entry(tab_interacciones, textvariable=cliente_id_var)
    entry_cliente_id.grid(row=0, column=1, padx=10, pady=10)

    # Etiqueta y campo de Fecha (con valor predeterminado de hoy)
    label_fecha = Label(tab_interacciones, text="Fecha (YYYY-MM-DD):")
    label_fecha.grid(row=1, column=0, padx=10, pady=10)
    fecha_var = StringVar(value=datetime.now().strftime("%Y-%m-%d"))
    entry_fecha = Entry(tab_interacciones, textvariable=fecha_var)
    entry_fecha.grid(row=1, column=1, padx=10, pady=10)

    # Etiqueta y Combobox para Tipo de Interacción
    label_tipo_interaccion = Label(tab_interacciones, text="Tipo de Interacción:")
    label_tipo_interaccion.grid(row=2, column=0, padx=10, pady=10)
    tipo_var = StringVar()
    tipo_interaccion_combobox = ttk.Combobox(tab_interacciones, values=[e.value for e in TipoInteraccion], state="readonly", textvariable=tipo_var)
    tipo_interaccion_combobox.grid(row=2, column=1, padx=10, pady=10)

    # Etiqueta y campo de Detalles
    label_detalles = Label(tab_interacciones, text="Detalles:")
    label_detalles.grid(row=3, column=0, padx=10, pady=10)
    detalles_var = StringVar()
    entry_detalles = Entry(tab_interacciones, textvariable=detalles_var)
    entry_detalles.grid(row=3, column=1, padx=10, pady=10)

    # Función que guarda la interacción
    def on_guardar_interaccion():
        cliente_id = cliente_id_var.get()
        fecha = fecha_var.get()
        tipo = tipo_var.get()
        detalles = detalles_var.get()

        # Validación de campos vacíos
        if not cliente_id or not fecha or not tipo or not detalles:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Validación de formato de fecha (simple ejemplo)
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "La fecha no tiene el formato correcto (YYYY-MM-DD).")
            return

        # Llamada para guardar la interacción
        try:
            if not guardar_interaccion(conn, cursor, cliente_id, fecha, tipo, detalles):
                messagebox.showerror("Error", "Hubo un problema al guardar la interacción.")
            else:
                messagebox.showinfo("Éxito", "Interacción guardada exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar la interacción: {str(e)}")
            conn.rollback()

  # Botón para guardar interacción
    ttk.Button(tab_interacciones, text="Guardar Interacción", command=on_guardar_interaccion).grid(row=4, column=0, columnspan=2, pady=10)

    # Botón para mostrar el historial de interacciones
    ttk.Button(tab_interacciones, text="Mostrar Historial", command=lambda: mostrar_historial(conn, cursor, cliente_id_var.get())).grid(row=5, column=0, columnspan=2, pady=10)

# Función para agregar un formulario para productos
def agregar_formulario_productos(tab_productos, conn, cursor):
    """
    Configura el formulario para la gestión de productos.
    """
    Label(tab_productos, text="Nombre del Producto:").grid(row=0, column=0, padx=10, pady=10)
    nombre_producto_var = StringVar()
    Entry(tab_productos, textvariable=nombre_producto_var).grid(row=0, column=1, padx=10, pady=10)

    Label(tab_productos, text="Precio:").grid(row=1, column=0, padx=10, pady=10)
    precio_var = StringVar()
    Entry(tab_productos, textvariable=precio_var).grid(row=1, column=1, padx=10, pady=10)

    # Función para guardar producto
    def on_guardar_producto():
        nombre_producto = nombre_producto_var.get()
        precio = precio_var.get()

        if not nombre_producto or not precio:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            if not guardar_producto(conn, cursor, nombre_producto, precio):
                messagebox.showerror("Error", "Hubo un problema al guardar el producto.")
            else:
                messagebox.showinfo("Éxito", "Producto guardado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar el producto: {str(e)}")

    ttk.Button(tab_productos, text="Guardar Producto", command=on_guardar_producto).grid(row=2, column=0, columnspan=2, pady=10)

# Función para mostrar historial de interacciones
def mostrar_historial(conn, cursor, cliente_id):
    # Mostrar el historial de interacciones de un cliente
    pass  # Aquí agregar la implementación según tu base de datos

def mostrar_historial(conn, cursor, cliente_id):
    if cliente_id:
        try:
            cursor.execute("""
                SELECT fecha, tipo_interaccion, detalles
                FROM interacciones
                WHERE cliente_id = ?
                ORDER BY fecha DESC
            """, (cliente_id,))
            historial = cursor.fetchall()

            historial_ventana = Toplevel()
            historial_ventana.title(f"Historial de Interacciones de Cliente {cliente_id}")

            if historial:
                historial_texto = '\n'.join([f"{interaccion[0]} - {interaccion[1]}: {interaccion[2]}" for interaccion in historial])
            else:
                historial_texto = f"No se encontraron interacciones para el cliente {cliente_id}."

            Label(historial_ventana, text=historial_texto, padx=10, pady=10).pack()
            ttk.Button(historial_ventana, text="Cerrar", command=historial_ventana.destroy).pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error de Base de Datos", f"Hubo un error al obtener el historial: {str(e)}")

