# ============================================================
# ARCHIVO: views/usuario_view.py
# DESCRIPCIÓN: CRUD de Usuarios en Pantalla Completa (Modo Claro)
# ============================================================

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import ttk, messagebox
from controllers.usuario_controller import (
    listar_usuarios_controller,
    registrar_usuario_controller,
    actualizar_usuario_controller,
    eliminar_usuario_controller
)

class VentanaUsuarios(ctk.CTkToplevel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.title("FERRETERÍA TIKAL - Gestión de Usuarios")
        self.after(0, lambda: self.state('zoomed')) # Pantalla Completa
        self.configure(fg_color="#F4F6F7")
        self.grab_set()

        self.id_seleccionado = None

        lbl_titulo = ctk.CTkLabel(self, text="👤 ADMINISTRACIÓN DE USUARIOS - FERRETERÍA TIKAL", font=("Arial", 22, "bold"), text_color="#1F4E78")
        lbl_titulo.pack(pady=20)

        frame_contenido = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12, border_width=1, border_color="#D5D8DC")
        frame_contenido.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        # Formulario
        frame_form = ctk.CTkFrame(frame_contenido, width=350, fg_color="#F8F9F9", corner_radius=10)
        frame_form.pack(side="left", fill="y", padx=20, pady=20)

        ctk.CTkLabel(frame_form, text="DATOS DEL USUARIO", font=("Arial", 15, "bold"), text_color="#1F4E78").pack(pady=15)

        self.txt_usuario = ctk.CTkEntry(frame_form, placeholder_text="Nombre de usuario", width=300, height=40, fg_color="#FFFFFF", text_color="#2C3E50", border_color="#BDC3C7")
        self.txt_usuario.pack(pady=10)

        self.txt_password = ctk.CTkEntry(frame_form, placeholder_text="Contraseña", show="*", width=300, height=40, fg_color="#FFFFFF", text_color="#2C3E50", border_color="#BDC3C7")
        self.txt_password.pack(pady=10)

        self.combo_estado = ctk.CTkOptionMenu(frame_form, values=["ACTIVO", "INACTIVO"], width=300, height=40, fg_color="#2980B9", button_color="#1F618D")
        self.combo_estado.pack(pady=10)

        btn_guardar = ctk.CTkButton(frame_form, text="GUARDAR USUARIO", command=self.guardar, fg_color="#27AE60", hover_color="#1E8449", width=300, height=42, font=("Arial", 12, "bold"))
        btn_guardar.pack(pady=12)

        btn_actualizar = ctk.CTkButton(frame_form, text="ACTUALIZAR", command=self.actualizar, fg_color="#2980B9", hover_color="#1F618D", width=300, height=40, font=("Arial", 12, "bold"))
        btn_actualizar.pack(pady=5)

        btn_eliminar = ctk.CTkButton(frame_form, text="ELIMINAR", command=self.eliminar, fg_color="#E74C3C", hover_color="#C0392B", width=300, height=40, font=("Arial", 12, "bold"))
        btn_eliminar.pack(pady=5)

        btn_limpiar = ctk.CTkButton(frame_form, text="LIMPIAR CAMPOS", command=self.limpiar_campos, fg_color="#7F8C8D", hover_color="#616A6B", width=300, height=40, font=("Arial", 12, "bold"))
        btn_limpiar.pack(pady=5)

        # Tabla
        frame_tabla = ctk.CTkFrame(frame_contenido, fg_color="transparent")
        frame_tabla.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", font=("Arial", 11), rowheight=32, background="#FFFFFF", fieldbackground="#FFFFFF", foreground="#2C3E50")
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#EAECEE", foreground="#1F4E78")

        self.tabla = ttk.Treeview(frame_tabla, columns=("id", "usuario", "password", "estado"), show="headings")
        self.tabla.heading("id", text="ID")
        self.tabla.heading("usuario", text="Usuario")
        self.tabla.heading("password", text="Contraseña")
        self.tabla.heading("estado", text="Estado")

        self.tabla.column("id", width=80, anchor="center")
        self.tabla.column("usuario", width=250)
        self.tabla.column("password", width=250)
        self.tabla.column("estado", width=150, anchor="center")

        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_registro)

        self.cargar_datos()

    def cargar_datos(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        usuarios = listar_usuarios_controller()
        for u in usuarios:
            self.tabla.insert("", "end", values=(u["id_usuario"], u["usuario"], u["password"], u["estado"]))

    def seleccionar_registro(self, event):
        item = self.tabla.focus()
        if not item: return
        valores = self.tabla.item(item, "values")
        if valores:
            self.limpiar_campos()
            self.id_seleccionado = valores[0]
            self.txt_usuario.insert(0, valores[1])
            self.txt_password.insert(0, valores[2])
            self.combo_estado.set(valores[3])

    # 1. GUARDAR USUARIO
    def guardar(self):
        usuario = self.txt_usuario.get().strip()
        password = self.txt_password.get().strip()
        estado = self.combo_estado.get()

        exito, msj = registrar_usuario_controller(usuario, password, estado)
        if exito:
            # messagebox.showinfo("Éxito", msj)  # Desactivado para evitar interrupciones de foco
            self.cargar_datos()
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", msj)

    # 2. ACTUALIZAR USUARIO
    def actualizar(self):
        usuario = self.txt_usuario.get().strip()
        password = self.txt_password.get().strip()
        estado = self.combo_estado.get()

        exito, msj = actualizar_usuario_controller(self.id_seleccionado, usuario, password, estado)
        if exito:
            # messagebox.showinfo("Éxito", msj)
            self.cargar_datos()
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", msj)

    # 3. ELIMINAR USUARIO
    def eliminar(self):
        if not hasattr(self, 'id_seleccionado') or not self.id_seleccionado:
            messagebox.showwarning("Atención", "Seleccione un usuario de la tabla.")
            return

        exito, msj = eliminar_usuario_controller(self.id_seleccionado)
        if exito:
            # messagebox.showinfo("Éxito", msj)
            self.cargar_datos()
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", msj)
            
    def limpiar_campos(self):
        self.id_seleccionado = None
        self.txt_usuario.delete(0, "end")
        self.txt_password.delete(0, "end")
        self.combo_estado.set("ACTIVO")

if __name__ == "__main__":
    app = ctk.CTk()
    app.withdraw()
    win = VentanaUsuarios(app)
    app.mainloop()