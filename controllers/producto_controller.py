# ============================================================
# ARCHIVO: controllers/producto_controller.py
# DESCRIPCIÓN: Controlador para la lógica de negocio de productos
# ============================================================
from datetime import date
from models.producto_model import (
    obtener_todos_productos,
    insertar_producto,
    actualizar_producto,
    eliminar_producto
)

def listar_productos_controller():
    """Obtiene la lista completa de productos."""
    return obtener_todos_productos()

def registrar_producto_controller(codigo, descripcion, unidad, presentacion, precio_str, stock_str, estado):
    """Valida tipos de datos y registra un nuevo producto."""
    if not codigo or not descripcion or not precio_str:
        return False, "Por favor complete todos los campos requeridos."
    try:
        precio = float(precio_str)
    except ValueError:
        return False, "El precio debe ser un número entero o decimal válido."
    try:
        stock = int(stock_str) if stock_str else 0
    except ValueError:
        return False, "El stock debe ser un número entero válido."
        
    fecha_hoy = date.today().strftime("%Y-%m-%d")
    return insertar_producto(codigo, descripcion, unidad, presentacion, precio, stock, estado, fecha_hoy)

def actualizar_producto_controller(codigo, descripcion, unidad, presentacion, precio_str, stock_str, estado):
    """Valida los datos y actualiza un producto existente."""
    if not codigo or not descripcion or not precio_str:
        return False, "Seleccione un producto de la tabla para actualizar."
    try:
        precio = float(precio_str)
    except ValueError:
        return False, "El precio debe ser un número válido."
    try:
        stock = int(stock_str) if stock_str else 0
    except ValueError:
        return False, "El stock debe ser un número entero válido."
        
    return actualizar_producto(codigo, descripcion, unidad, presentacion, precio, stock, estado)

def eliminar_producto_controller(codigo):
    """Valida la selección y elimina un producto por su código."""
    if not codigo:
        return False, "Seleccione un producto para eliminar."
    return eliminar_producto(codigo)