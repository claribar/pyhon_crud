# verificar_tablas.py
import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect("database/crm_basico.db")
cursor = conn.cursor()

# Consultar las tablas existentes
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Imprimir las tablas que existen
print("Tablas en la base de datos:", cursor.fetchall())

# Cerrar la conexión
conn.close()
