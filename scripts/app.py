
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tkinter import Tk
from database.db_manager import conectar_base, crear_tablas, obtener_historial_compras, obtener_interacciones
from ui.gui import inicializar_gui  # Ahora solo importamos la función correctamente
from ui import styles

def iniciar_app():
    """
    Configura la conexión a la base de datos e inicia la interfaz gráfica principal.
    """
    try:
        # Configuración inicial de la base de datos
        conn, cursor = conectar_base()
        print("Conexión establecida con la base de datos.")
        
        crear_tablas(cursor)
        print("Tablas creadas o verificadas en la base de datos.")
        
        # Inicializar la GUI
        print("Iniciando la interfaz gráfica...")
        root = Tk()
        root.title("CRM Básico con IA")
        root.geometry("800x600")  # Ajusta el tamaño según lo necesario
        root.protocol("WM_DELETE_WINDOW", lambda: cerrar_conexion(root, conn))
        
        # Pasar conn y cursor a inicializar_gui
        inicializar_gui(root, conn, cursor)
        
        # Ejecutar la aplicación
        root.mainloop()

        # Cerrar la conexión a la base de datos al salir
        conn.close()
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        
def cerrar_conexion(ventana, conn):
    """
    Cierra la conexión a la base de datos y la ventana.
    """
    print("Cerrando la conexión a la base de datos...")
    conn.close()
    ventana.destroy()

if __name__ == "__main__":
    iniciar_app()
