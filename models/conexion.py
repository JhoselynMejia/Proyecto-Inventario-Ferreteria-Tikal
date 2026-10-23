import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    """
    Función que establece y devuelve la conexión a la base de datos MySQL.
    Aplica bloques try-except para gestionar errores de conexión de forma segura.
    """
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",              # Tu usuario de MySQL (por defecto es root)
            password="12345", # CAMBIA ESTO por tu contraseña real de MySQL Workbench
            database="empresa_db"
        )
        
        if conexion.is_connected():
            return conexion

    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
        return None
# Prueba rápida de ejecución
if __name__ == "__main__":
    con = obtener_conexion()
    if con:
        print("¡Conexión a MySQL exitosa de forma correcta!")
        con.close()
    else:
        print("No se pudo establecer la conexión. Revisa tu usuario/contraseña.")