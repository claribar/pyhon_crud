import streamlit as st
from database.db_manager import conectar_base, obtener_historial_compras, obtener_interacciones

# Función para mostrar historial de compras
def mostrar_historial_compras(cursor, cliente_id):
    st.write("### Historial de Compras")
    compras = obtener_historial_compras(cursor, cliente_id)
    if compras:
        for compra in compras:
            st.write(f"Producto: {compra[0]}, Cantidad: {compra[1]}, Precio Unitario: {compra[2]}, Total: {compra[3]}, Fecha: {compra[4]}, Método de Pago: {compra[5]}")
    else:
        st.write("No se encontraron compras para este cliente.")

# Función para mostrar interacciones
def mostrar_interacciones(cursor, cliente_id):
    st.write("### Historial de Interacciones")
    interacciones = obtener_interacciones(cursor, cliente_id)
    if interacciones:
        for interaccion in interacciones:
            st.write(f"Fecha: {interaccion[0]}, Tipo: {interaccion[1]}, Detalles: {interaccion[2]}")
    else:
        st.write("No se encontraron interacciones para este cliente.")

# Interfaz para interactuar con el cliente
def interfaz_cliente():
    st.title("Gestión de Clientes")

    cliente_id = st.number_input("Ingrese el ID del Cliente", min_value=1)

    if cliente_id:
        conn, cursor = conectar_base()
        mostrar_historial_compras(cursor, cliente_id)
        mostrar_interacciones(cursor, cliente_id)

if __name__ == '__main__':
    interfaz_cliente()
