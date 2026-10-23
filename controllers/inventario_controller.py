# ============================================================
# ARCHIVO: controllers/inventario_controller.py
# DESCRIPCIÓN: Controlador de Reportería de Inventario
# ============================================================

from models.inventario_model import obtener_reporte_inventario_filtrado

def buscar_inventario_controller(codigo="", descripcion="", fecha=""):
    """
    Recibe filtros de la Vista, consulta al Modelo y calcula los KPIs.
    Retorna: (datos_tabla, total_items, total_stock, valor_total_inventario)
    """
    datos = obtener_reporte_inventario_filtrado(codigo, descripcion, fecha)
    total_items = len(datos)
    total_stock = sum(int(item["cantidad"]) for item in datos)
    valor_inventario = sum(float(item["precio"]) * int(item["cantidad"]) for item in datos)

    return datos, total_items, total_stock, valor_inventario