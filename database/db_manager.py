import sqlite3
import re
import datetime
from enums.enums import TipoCliente, TipoInteraccion
from tkinter import messagebox
import os

def conectar_base():
    db_path = "database/crm_basico.db"
    if not os.path.exists(os.path.dirname(db_path)):
        os.makedirs(os.path.dirname(db_path))
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn, cursor

# def conectar_db():
    """Conectar a la base de datos SQLite."""
    conn = sqlite3.connect('crm.db')
    cursor = conn.cursor()
    return conn, cursor

def desconectar(conn, cursor):
    """
    Cierra la conexión a la base de datos y el cursor.
    """
    try:
        cursor.close()
        conn.close()
        print("Conexión a la base de datos cerrada correctamente.")
    except Exception as e:
        print(f"Error al cerrar la conexión: {e}")


def verificar_conexion(conn):
    if conn is None:
        messagebox.showerror("Error de Conexión", "No se pudo establecer conexión con la base de datos.")
        return False
    return True

def crear_tablas(cursor):
    """
    Crea las tablas necesarias en la base de datos si no existen.
    """
    # Crear la tabla de Clientes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Clientes (
            ID INTEGER PRIMARY KEY AUTOINCREMENT, 
            Nombre VARCHAR(255),
            Email VARCHAR(255),
            Telefono VARCHAR(15),
            Tipo_Cliente VARCHAR(50),
            Ultima_Interaccion DATE
        )
    """)

    # Crear el índice en Email para búsquedas rápidas
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_email ON Clientes (Email)
    """)

    # Crear la tabla de Interacciones
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Interacciones (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Cliente_ID INTEGER,
        Fecha DATE,
        Tipo TEXT,
        Detalles TEXT,
        FOREIGN KEY (Cliente_ID) REFERENCES Clientes(ID) ON DELETE CASCADE
    )
    """)
    # Crear el índice en Cliente_ID para búsquedas rápidas en Interacciones
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_cliente_id_interacciones ON Interacciones (Cliente_ID)
    """)

    # Crear la tabla de Productos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Productos (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT NOT NULL,
        Precio DECIMAL(10, 2) NOT NULL
    )
    """)
    # Crear el índice en Nombre para búsquedas rápidas en Productos
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_producto_nombre ON Productos (Nombre)
    """)

    # Crear la tabla de Historial de Compras
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Historial_Compras (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Cliente_ID INTEGER,
        Fecha DATE,
        Producto_ID INTEGER,
        Cantidad INTEGER,
        Precio_Unitario DECIMAL(10, 2),
        Total DECIMAL(10, 2),
        Metodo_Pago VARCHAR(50),
        FOREIGN KEY (Cliente_ID) REFERENCES Clientes(ID) ON DELETE CASCADE,
        FOREIGN KEY (Producto_ID) REFERENCES Productos(ID) ON DELETE CASCADE
    )
    """)
    # Crear los índices en las columnas clave para mejorar la búsqueda en Historial_Compras
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_cliente_id_historial_compras ON Historial_Compras (Cliente_ID)
    """)
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_producto_id_historial_compras ON Historial_Compras (Producto_ID)
    """)
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_historial_fecha ON Historial_Compras (Fecha)
    """)



def validar_campos_no_vacios(nombre, email, telefono, tipo_cliente):
    """Valida que los campos no estén vacíos."""
    return bool(nombre) and bool(email) and bool(telefono) and bool(tipo_cliente)

def validar_email(email):
    """Valida si el correo electrónico tiene un formato correcto."""
    # Puedes usar una expresión regular para validar el correo
    return "@" in email and "." in email

def validar_telefono(telefono):
    """Valida si el teléfono tiene 10 dígitos."""
    return telefono.isdigit() and len(telefono) == 10

def validar_tipo_cliente(tipo_cliente):
    """Valida que el tipo de cliente sea válido."""
    tipos_validos = ['Regular', 'Premium', 'VIP']  # Cambia según tus necesidades
    return tipo_cliente in tipos_validos

def validar_campos_no_vacios(nombre, email, telefono, tipo_cliente):
    """Valida que los campos no estén vacíos."""
    return bool(nombre) and bool(email) and bool(telefono) and bool(tipo_cliente)

def validar_email(email):
    """Valida si el correo electrónico tiene un formato correcto."""
    return "@" in email and "." in email

def validar_telefono(telefono):
    """Valida si el teléfono tiene 10 dígitos."""
    return telefono.isdigit() and len(telefono) == 10

def validar_tipo_cliente(tipo_cliente):
    """Valida que el tipo de cliente sea válido."""
    tipos_validos = ['Regular', 'Premium', 'VIP']  # Cambia según tus necesidades
    return tipo_cliente in tipos_validos

def guardar_cliente(conn, cursor, nombre, email, telefono, tipo_cliente):
    """
    Guarda un cliente en la base de datos y obtiene el ID generado automáticamente.
    """
    # Validar que los campos no estén vacíos
    if not validar_campos_no_vacios(nombre, email, telefono, tipo_cliente):
        messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
        return None

    # Validaciones específicas
    if not validar_email(email):
        messagebox.showwarning("Advertencia", "El correo electrónico no es válido.")
        return None

    if not validar_telefono(telefono):
        messagebox.showwarning("Advertencia", "El número de teléfono debe contener 10 dígitos.")
        return None

    if not validar_tipo_cliente(tipo_cliente):
        messagebox.showwarning("Advertencia", f"El tipo de cliente '{tipo_cliente}' no es válido.")
        return None

    try:
        # Insertar cliente en la base de datos
        cursor.execute("""
            INSERT INTO clientes (nombre, email, telefono, tipo_cliente, Ultima_Interaccion)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, email, telefono, tipo_cliente, None))  # Inicialmente sin interacción
        conn.commit()

        # Obtener el ID generado
        cliente_id = cursor.lastrowid

        # Mostrar mensaje de éxito
        messagebox.showinfo("Éxito", f"El cliente fue guardado correctamente con ID: {cliente_id}.")
        return cliente_id

    except Exception as e:
        # En caso de error, hacer rollback y mostrar mensaje de error
        conn.rollback()
        print(f"Error al guardar cliente: {e}")
        messagebox.showerror("Error", f"Hubo un problema al guardar el cliente: {e}")
        return None



def guardar_producto(conn, cursor, nombre_producto, precio):
    """
    Guarda un nuevo producto en la base de datos después de validar los campos.
    """
    # Validar que los campos no estén vacíos
    if not nombre_producto or not precio:
        messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
        return

    try:
        # Verificar que el precio es un número válido
        precio = float(precio)
    except ValueError:
        messagebox.showwarning("Advertencia", "El precio debe ser un número válido.")
        return

    # Insertar producto en la base de datos
    try:
        cursor.execute("""INSERT INTO productos (nombre, precio) VALUES (?, ?)""", (nombre_producto, precio))
        conn.commit()
        messagebox.showinfo("Éxito", "El producto fue guardado correctamente.")
    except Exception as e:
        print(f"Error al guardar producto: {e}")
        messagebox.showerror("Error", "Hubo un problema al guardar el producto.")



def guardar_compra(conn, cursor, cliente_id, fecha, producto_nombre, cantidad, precio_unitario, metodo_pago):
    try:
        # Obtener el ID del producto a partir del nombre
        cursor.execute("SELECT ID FROM Productos WHERE Nombre = ?", (producto_nombre,))
        producto_id = cursor.fetchone()
        
        if producto_id is None:
            messagebox.showwarning("Advertencia", f"Producto '{producto_nombre}' no encontrado.")
            return False
        
        producto_id = producto_id[0]  # Obtenemos el ID del producto
        
        # Calcular el total de la compra
        total = cantidad * precio_unitario
        
        # Insertar la compra en la tabla Historial_Compras
        query = """
        INSERT INTO Historial_Compras (Cliente_ID, Fecha, Producto_ID, Cantidad, Precio_Unitario, Total, Metodo_Pago)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (cliente_id, fecha, producto_id, cantidad, precio_unitario, total, metodo_pago))
        conn.commit()
        messagebox.showinfo("Éxito", "Compra guardada exitosamente.")
        return True
    except Exception as e:
        print(f"Error al guardar compra: {e}")
        messagebox.showerror("Error", "Hubo un problema al guardar la compra.")
        return False


def guardar_interaccion(conn, cursor, cliente_id, fecha, tipo, detalles):
    """
    Guarda una nueva interacción y actualiza la fecha de la última interacción en la tabla Clientes.
    """
    try:
        # Insertar la nueva interacción en la tabla Interacciones
        cursor.execute("""
        INSERT INTO Interacciones (Cliente_ID, Fecha, Tipo, Detalles)
        VALUES (?, ?, ?, ?)
        """, (cliente_id, fecha, tipo, detalles))
        
        # Después de insertar la nueva interacción, obtener la fecha de la última interacción
        cursor.execute("""
        SELECT MAX(Fecha) FROM Interacciones WHERE Cliente_ID = ?
        """, (cliente_id,))
        ultima_fecha = cursor.fetchone()[0]

        # Actualizar el campo Ultima_Interaccion en la tabla Clientes con la fecha más reciente
        cursor.execute("""
        UPDATE Clientes
        SET Ultima_Interaccion = ?
        WHERE ID = ?
        """, (ultima_fecha, cliente_id))
        
        conn.commit()
        messagebox.showinfo("Éxito", "Interacción guardada y última interacción actualizada.")
        return True
    except Exception as e:
        print(f"Error al guardar interacción: {e}")
        messagebox.showerror("Error", "Hubo un problema al guardar la interacción.")
        return False


def obtener_historial_compras(cursor, cliente_id):
    """
    Recupera el historial de compras de un cliente.
    """
    cursor.execute("""
    SELECT Productos.Nombre, Historial_Compras.Cantidad, Historial_Compras.Precio_Unitario, 
           Historial_Compras.Total, Historial_Compras.Fecha, Historial_Compras.Metodo_Pago
    FROM Historial_Compras
    INNER JOIN Productos ON Historial_Compras.Producto_ID = Productos.ID
    WHERE Historial_Compras.Cliente_ID = ?
    ORDER BY Historial_Compras.Fecha DESC
    """, (cliente_id,))
    
    compras = cursor.fetchall()
    if compras:
        for compra in compras:
            print(f"Producto: {compra[0]}, Cantidad: {compra[1]}, Precio Unitario: {compra[2]}, Total: {compra[3]}, Fecha: {compra[4]}, Método de Pago: {compra[5]}")
    else:
        print("No se encontraron compras para este cliente.")

def obtener_interacciones(cursor, cliente_id):
    """
    Recupera las interacciones de un cliente.
    """
    cursor.execute("""
    SELECT Fecha, Tipo, Detalles
    FROM Interacciones
    WHERE Cliente_ID = ?
    ORDER BY Fecha DESC
    """, (cliente_id,))
    
    interacciones = cursor.fetchall()
    if interacciones:
        for interaccion in interacciones:
            print(f"Fecha: {interaccion[0]}, Tipo: {interaccion[1]}, Detalles: {interaccion[2]}")
    else:
        print("No se encontraron interacciones para este cliente.")
