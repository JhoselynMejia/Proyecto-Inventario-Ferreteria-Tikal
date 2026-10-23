# ============================================================
# ARCHIVO: models/usuario_model.py
# DESCRIPCIÓN: Consultas SQL para la gestión CRUD de usuarios
# ============================================================

from models.conexion import obtener_conexion

def validar_usuario(usuario, password):
    """Valida credenciales para el inicio de sesión."""
    conexion = obtener_conexion()
    if not conexion:
        return False, "Error al conectar con la base de datos MySQL."

    try:
        cursor = conexion.cursor(dictionary=True)
        sql = "SELECT * FROM usuarios WHERE usuario = %s AND password = %s AND estado = 'ACTIVO'"
        cursor.execute(sql, (usuario, password))
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()

        if resultado:
            return True, f"¡Acceso concedido! Bienvenido/a {resultado['usuario']}"
        else:
            return False, "Usuario o contraseña incorrectos, o cuenta INACTIVA."
    except Exception as e:
        return False, f"Error en la consulta: {e}"

def obtener_todos_usuarios():
    """Obtiene la lista completa de usuarios."""
    conexion = obtener_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor(dictionary=True)
        sql = "SELECT id_usuario, usuario, password, estado FROM usuarios ORDER BY id_usuario ASC"
        cursor.execute(sql)
        usuarios = cursor.fetchall()
        cursor.close()
        conexion.close()
        return usuarios
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return []

def insertar_usuario(usuario, password, estado):
    """Registra un nuevo usuario en la base de datos."""
    conexion = obtener_conexion()
    if not conexion:
        return False, "Error de conexión."
    try:
        cursor = conexion.cursor()
        sql = "INSERT INTO usuarios (usuario, password, estado) VALUES (%s, %s, %s)"
        cursor.execute(sql, (usuario, password, estado))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True, "Usuario registrado exitosamente."
    except Exception as e:
        return False, f"Error al registrar (posible usuario duplicado): {e}"

def actualizar_usuario(id_usuario, usuario, password, estado):
    """Actualiza datos de un usuario existente."""
    conexion = obtener_conexion()
    if not conexion:
        return False, "Error de conexión."
    try:
        cursor = conexion.cursor()
        sql = "UPDATE usuarios SET usuario=%s, password=%s, estado=%s WHERE id_usuario=%s"
        cursor.execute(sql, (usuario, password, estado, id_usuario))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True, "Usuario actualizado correctamente."
    except Exception as e:
        return False, f"Error al actualizar: {e}"

def eliminar_usuario(id_usuario):
    """Elimina un usuario por su ID."""
    conexion = obtener_conexion()
    if not conexion:
        return False, "Error de conexión."
    try:
        cursor = conexion.cursor()
        sql = "DELETE FROM usuarios WHERE id_usuario = %s"
        cursor.execute(sql, (id_usuario,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True, "Usuario eliminado correctamente."
    except Exception as e:
        return False, f"Error al eliminar: {e}"