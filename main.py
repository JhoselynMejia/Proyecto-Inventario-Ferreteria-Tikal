# ============================================================
# ARCHIVO: main.py
# DESCRIPCIÓN: Punto de inicio del sistema Ferretería Tikal
# ============================================================

from views.login_view import VentanaLogin

if __name__ == "__main__":
    app = VentanaLogin()
    app.mainloop()