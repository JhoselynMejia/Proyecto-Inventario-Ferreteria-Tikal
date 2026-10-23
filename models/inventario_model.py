# ============================================================
# ARCHIVO: models/inventario_model.py
# DESCRIPCIÓN: Modelo para consultas con filtros dinámicos (RF-04.2)
# ============================================================

from models.conexion import obtener_conexion

def obtener_reporte_inventario_filtrado(codigo="", descripcion="", fecha=""):
    """
    Consulta productos e inventarios con soporte para filtros
    por Código, Descripción, Fecha o Búsqueda Combinada.
    """
    conexion = obtener_conexion()
    if not conexion:
        return []

    try:
        cursor = conexion.cursor(dictionary=True)
        
        query = """
            SELECT 
                p.codigo,
                COALESCE(i.fecha, p.fecha_registro) AS fecha,
                p.descripcion,
                COALESCE(i.cantidad, 0) AS cantidad,
                p.presentacion,
                p.unidad_medida,
                p.precio
            FROM productos p
            LEFT JOIN inventario i ON p.codigo = i.codigo_producto
            WHERE 1=1
        """
        params = []

        if codigo.strip():
            query += " AND p.codigo LIKE %s"
            params.append(f"%{codigo.strip()}%")

        if descripcion.strip():
            query += " AND p.descripcion LIKE %s"
            params.append(f"%{descripcion.strip()}%")

        if fecha.strip():
            query += " AND (i.fecha = %s OR p.fecha_registro = %s)"
            params.append(fecha.strip())
            params.append(fecha.strip())

        query += " ORDER BY p.codigo ASC"

        cursor.execute(query, tuple(params))
        resultados = cursor.fetchall()
        cursor.close()
        conexion.close()
        return resultados
    except Exception as e:
        print(f"Error en consulta de inventario: {e}")
        return []