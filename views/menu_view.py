# ============================================================
# ARCHIVO: views/menu_view.py
# DESCRIPCIÓN: Menú Principal en Pantalla Completa (Modo Claro)
# ============================================================

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import messagebox
from views.producto_view import VentanaProductos
from views.usuario_view import VentanaUsuarios
from views.inventario_view import VentanaInventario

class VentanaMenu(ctk.CTk):
    def __init__(self, usuario_actual="Administrador"):
        super().__init__()

        self.title("FERRETERÍA TIKAL - Menú Principal")
        self.after(0, lambda: self.state('zoomed'))
        self.configure(fg_color="#F4F6F7")

        frame_central = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=15, border_width=1, border_color="#D5D8DC")
        frame_central.pack(expand=True, padx=40, pady=40)

        self.lbl_empresa = ctk.CTkLabel(
            frame_central, 
            text="🏗️ FERRETERÍA TIKAL", 
            font=("Arial", 30, "bold"),
            text_color="#1F4E78"
        )
        self.lbl_empresa.pack(pady=(40, 5), padx=60)

        self.lbl_subtitulo = ctk.CTkLabel(
            frame_central, 
            text=f"Usuario Activo: {usuario_actual}", 
            font=("Arial", 14),
            text_color="#5D6D7E"
        )
        self.lbl_subtitulo.pack(pady=(0, 35))

        self.btn_usuarios = ctk.CTkButton(
            frame_central,
            text="1. ADMINISTRACIÓN DE USUARIOS ",
            command=self.abrir_usuarios,
            width=420,
            height=52,
            fg_color="#1F4E78",
            hover_color="#154360",
            font=("Arial", 14, "bold")
        )
        self.btn_usuarios.pack(pady=12)

        self.btn_productos = ctk.CTkButton(
            frame_central,
            text="2. GESTIÓN DE PRODUCTOS ",
            command=self.abrir_productos,
            width=420,
            height=52,
            fg_color="#1F4E78",
            hover_color="#154360",
            font=("Arial", 14, "bold")
        )
        self.btn_productos.pack(pady=12)

        self.btn_inventario = ctk.CTkButton(
            frame_central,
            text="3. INVENTARIO DE PRODUCTOS ",
            command=self.abrir_inventario,
            width=420,
            height=52,
            fg_color="#1F4E78",
            hover_color="#154360",
            font=("Arial", 14, "bold")
        )
        self.btn_inventario.pack(pady=12)

        self.btn_salir = ctk.CTkButton(
            frame_central,
            text="CERRAR SESIÓN",
            command=self.cerrar_sesion,
            width=420,
            height=45,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            font=("Arial", 13, "bold")
        )
        self.btn_salir.pack(pady=(35, 30))

    def abrir_usuarios(self):
        VentanaUsuarios(self)

    def abrir_productos(self):
        VentanaProductos(self)

    def abrir_inventario(self):
        VentanaInventario(self)

    def cerrar_sesion(self):
        if messagebox.askyesno("Confirmar", "¿Desea cerrar la sesión actual?"):
            self.destroy()

if __name__ == "__main__":
    app = VentanaMenu()
    app.mainloop()