# ============================================================
# ARCHIVO: models/producto_model.py
# DESCRIPCIÓN: Consultas SQL para la tabla 'productos' en MySQL
# ============================================================
from models.conexion import obtener_conexion

def obtener_todos_productos():
    """Obtiene la lista de todos los productos de Ferretería Tikal."""
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor(dictionary=True)
        sql = "SELECT codigo, descripcion, unidad_medida, presentacion, precio, stock, estado FROM productos ORDER BY codigo ASC"
        cursor.execute(sql)
        productos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return productos
    except Exception as e:
        print(f"Error al obtener productos: {e}")
        return []

def insertar_producto(codigo, descripcion, unidad, presentacion, precio, stock, estado, fecha_registro):
    """Inserta un nuevo producto registrando el stock en la base de datos."""
    conexion = obtener_conexion()
    if not conexion:
        return False, "Error de conexión con la base de datos."
    try:
        cursor = conexion.cursor()
        sql = """
            INSERT INTO productos (codigo, descripcion, unidad_medida, presentacion, precio, stock, estado, fecha_registro)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (codigo, descripcion, unidad, presentacion, precio, stock, estado, fecha_registro))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True, "Producto registrado correctamente en la base de datos."
    except Exception as e:
        return False, f"Error al guardar: {e}"

def actualizar_producto(codigo, descripcion, unidad, presentacion, precio, stock, estado):
    """Actualiza los datos y el stock de un producto existente."""
    conexion = obtener_conexion()
    if not conexion:
        return False, "Error de conexión con la base de datos."
    try:
        cursor = conexion.cursor()
        sql = """
            UPDATE productos 
            SET descripcion=%s, unidad_medida=%s, presentacion=%s, precio=%s, stock=%s, estado=%s 
            WHERE codigo=%s
        """
        cursor.execute(sql, (descripcion, unidad, presentacion, precio, stock, estado, codigo))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True, "Producto actualizado correctamente."
    except Exception as e:
        return False, f"Error al actualizar: {e}"

def eliminar_producto(codigo):
    """Elimina un producto de MySQL según su código."""
    conexion = obtener_conexion()
    if not conexion:
        return False, "Error de conexión con la base de datos."
    try:
        cursor = conexion.cursor()
        sql = "DELETE FROM productos WHERE codigo = %s"
        cursor.execute(sql, (codigo,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True, "Producto eliminado correctamente."
    except Exception as e:
        return False, f"Error al eliminar: {e}"