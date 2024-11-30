from enum import Enum
# Definir el Enum para el tipo de cliente
class TipoCliente(Enum):
    REGULAR = "Regular"
    VIP = "VIP"
    NUEVO = "Nuevo"

class TipoInteraccion(Enum):
    CONSULTA = "Consulta"
    COMPRA = "Compra"
    SOPORTE = "Soporte"
