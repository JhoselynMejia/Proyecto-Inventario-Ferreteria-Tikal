# ============================================================
# ARCHIVO: controllers/usuario_controller.py
# DESCRIPCIÓN: Controlador para la lógica de negocio de usuarios
# ============================================================

from models.usuario_model import (
    validar_usuario,
    obtener_todos_usuarios,
    insertar_usuario,
    actualizar_usuario,
    eliminar_usuario
)

def procesar_login(usuario, password):
    """Valida los campos e invoca al modelo de autenticación."""
    if not usuario or not password:
        return False, "Por favor complete todos los campos."
    return validar_usuario(usuario, password)

def listar_usuarios_controller():
    """Obtiene el listado de usuarios desde el modelo."""
    return obtener_todos_usuarios()

def registrar_usuario_controller(usuario, password, estado):
    """Valida los datos y llama al modelo para registrar un usuario."""
    if not usuario or not password:
        return False, "Complete los campos de usuario y contraseña."
    return insertar_usuario(usuario, password, estado)

def actualizar_usuario_controller(id_usuario, usuario, password, estado):
    """Valida la selección y actualiza los datos del usuario."""
    if not id_usuario:
        return False, "Seleccione un usuario de la tabla para actualizar."
    if not usuario or not password:
        return False, "Complete todos los campos requeridos."
    return actualizar_usuario(id_usuario, usuario, password, estado)

def eliminar_usuario_controller(id_usuario):
    """Gestiona la eliminación de un usuario por su ID."""
    if not id_usuario:
        return False, "Seleccione un usuario de la tabla para eliminar."
    return eliminar_usuario(id_usuario)