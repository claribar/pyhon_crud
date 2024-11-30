import sqlite3

# Crear una conexión a la base de datos (esto crea el archivo si no existe)
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# Crear una tabla
cursor.execute('CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, name TEXT)')
conn.commit()

# Verificar las tablas en la base de datos
cursor.execute('SELECT name FROM sqlite_master WHERE type="table";')
print(cursor.fetchall())  # Debería mostrar las tablas, incluida 'test'

conn.close()
