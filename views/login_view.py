# ============================================================
# ARCHIVO: views/login_view.py
# DESCRIPCIÓN: Acceso al sistema en Pantalla Completa (Modo Claro)
# ============================================================

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import messagebox
from controllers.usuario_controller import procesar_login
from views.menu_view import VentanaMenu

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class VentanaLogin(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("FERRETERÍA TIKAL - Acceso al Sistema")
        self.after(0, lambda: self.state('zoomed')) # Pantalla Completa
        self.configure(fg_color="#EBF5FB") # Fondo gris/azul claro

        # Tarjeta Central Integrada
        frame_card = ctk.CTkFrame(
            self, 
            fg_color="#FFFFFF", 
            corner_radius=15, 
            border_width=1, 
            border_color="#D5D8DC",
            width=440, 
            height=490
        )
        frame_card.place(relx=0.5, rely=0.5, anchor="center")
        frame_card.pack_propagate(False)

        lbl_logo = ctk.CTkLabel(frame_card, text="🛠️ FERRETERÍA TIKAL", font=("Arial", 24, "bold"), text_color="#1F4E78")
        lbl_logo.pack(pady=(40, 5))

        lbl_sub = ctk.CTkLabel(frame_card, text="Control y Gestión de Inventarios", font=("Arial", 13), text_color="#5D6D7E")
        lbl_sub.pack(pady=(0, 30))

        self.entry_usuario = ctk.CTkEntry(
            frame_card, 
            placeholder_text="Nombre de usuario", 
            width=330, 
            height=45, 
            fg_color="#F8F9F9", 
            text_color="#2C3E50",
            border_color="#BDC3C7"
        )
        self.entry_usuario.pack(pady=10)

        self.entry_password = ctk.CTkEntry(
            frame_card, 
            placeholder_text="Contraseña", 
            show="*", 
            width=330, 
            height=45, 
            fg_color="#F8F9F9", 
            text_color="#2C3E50",
            border_color="#BDC3C7"
        )
        self.entry_password.pack(pady=10)

        btn_aceptar = ctk.CTkButton(
            frame_card, 
            text="INGRESAR AL SISTEMA", 
            command=self.evento_aceptar, 
            width=330, 
            height=45, 
            fg_color="#27AE60", 
            hover_color="#1E8449", 
            font=("Arial", 13, "bold")
        )
        btn_aceptar.pack(pady=(25, 10))

        btn_cancelar = ctk.CTkButton(
            frame_card, 
            text="LIMPIAR CAMPOS", 
            command=self.evento_cancelar, 
            width=330, 
            height=40, 
            fg_color="#E74C3C", 
            hover_color="#C0392B", 
            font=("Arial", 12, "bold")
        )
        btn_cancelar.pack(pady=5)

    def evento_aceptar(self):
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()

        exito, mensaje = procesar_login(usuario, password)

        if exito:
            messagebox.showinfo("Acceso Permitido", mensaje)
            self.destroy()
            app_menu = VentanaMenu(usuario_actual=usuario)
            app_menu.mainloop()
        else:
            messagebox.showerror("Error de Acceso", mensaje)

    def evento_cancelar(self):
        self.entry_usuario.delete(0, 'end')
        self.entry_password.delete(0, 'end')

if __name__ == "__main__":
    app = VentanaLogin()
    app.mainloop()