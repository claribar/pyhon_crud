from tkinter import ttk

def aplicar_estilos():
    # Crear una instancia de estilo
    style = ttk.Style()

    # Configuración de los botones
    style.configure("TButton",
                    padding=6,
                    relief="flat",
                    background="#4CAF50",
                    foreground="white",
                    font=("Helvetica", 12, "bold"))

    # Configuración para otras posibles necesidades
    # Puedes agregar más configuraciones de estilo aquí según sea necesario.

    # Configuración para otros widgets (ejemplo, Entry, Label)
    style.configure("TLabel",
                    background="#f0f0f0",  # Color de fondo para los Labels
                    font=("Helvetica", 12))
    
    style.configure("TEntry",
                    padding=6,
                    font=("Helvetica", 12),
                    fieldbackground="#ffffff",
                    background="#ffffff")  # Fondo de los Entry
    
    style.configure("TFrame",
                    background="#f0f0f0")  # Fondo de los Frames

    # Puedes agregar más widgets y sus estilos si es necesario
