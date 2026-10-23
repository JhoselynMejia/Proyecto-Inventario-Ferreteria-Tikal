# ============================================================
# ARCHIVO: views/producto_view.py
# DESCRIPCIÓN: CRUD de Productos en Pantalla Completa (Modo Claro)
# ============================================================
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import customtkinter as ctk
from tkinter import ttk, messagebox
from controllers.producto_controller import (
    listar_productos_controller,
    registrar_producto_controller,
    actualizar_producto_controller,
    eliminar_producto_controller
)

class VentanaProductos(ctk.CTkToplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("FERRETERÍA TIKAL - Gestión de Productos")
        self.after(0, lambda: self.state('zoomed'))
        self.configure(fg_color="#F4F6F7")
        self.grab_set()

        lbl_titulo = ctk.CTkLabel(self, text="📦 CATÁLOGO DE PRODUCTOS - FERRETERÍA TIKAL", font=("Arial", 22, "bold"), text_color="#1F4E78")
        lbl_titulo.pack(pady=20)

        frame_contenido = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12, border_width=1, border_color="#D5D8DC")
        frame_contenido.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        frame_form = ctk.CTkFrame(frame_contenido, width=350, fg_color="#F8F9F9", corner_radius=10)
        frame_form.pack(side="left", fill="y", padx=20, pady=20)

        ctk.CTkLabel(frame_form, text="DATOS DEL PRODUCTO", font=("Arial", 15, "bold"), text_color="#1F4E78").pack(pady=15)

        self.txt_codigo = ctk.CTkEntry(frame_form, placeholder_text="Código (ej: FER-005)", width=300, height=38, fg_color="#FFFFFF", text_color="#2C3E50", border_color="#BDC3C7")
        self.txt_codigo.pack(pady=6)

        self.txt_descripcion = ctk.CTkEntry(frame_form, placeholder_text="Descripción / Artículo", width=300, height=38, fg_color="#FFFFFF", text_color="#2C3E50", border_color="#BDC3C7")
        self.txt_descripcion.pack(pady=6)

        self.combo_unidad = ctk.CTkOptionMenu(frame_form, values=["Sacos", "Libras", "Quintales", "Galones", "Unidades", "Metros"], width=300, height=38, fg_color="#2980B9", button_color="#1F618D")
        self.combo_unidad.pack(pady=6)

        self.combo_presentacion = ctk.CTkOptionMenu(frame_form, values=["Saco", "Bolsa", "Atado", "Cubeta", "Caja", "Pieza", "Rollo"], width=300, height=38, fg_color="#2980B9", button_color="#1F618D")
        self.combo_presentacion.pack(pady=6)

        self.txt_precio = ctk.CTkEntry(frame_form, placeholder_text="Precio (Q)", width=300, height=38, fg_color="#FFFFFF", text_color="#2C3E50", border_color="#BDC3C7")
        self.txt_precio.pack(pady=6)

        self.txt_stock = ctk.CTkEntry(frame_form, placeholder_text="Stock Inicial", width=300, height=38, fg_color="#FFFFFF", text_color="#2C3E50", border_color="#BDC3C7")
        self.txt_stock.pack(pady=6)

        self.combo_estado = ctk.CTkOptionMenu(frame_form, values=["Activo", "Inactivo"], width=300, height=38, fg_color="#2980B9", button_color="#1F618D")
        self.combo_estado.pack(pady=6)

        btn_guardar = ctk.CTkButton(frame_form, text="GUARDAR", command=self.guardar, fg_color="#27AE60", hover_color="#1E8449", width=300, height=40, font=("Arial", 12, "bold"))
        btn_guardar.pack(pady=10)

        btn_actualizar = ctk.CTkButton(frame_form, text="ACTUALIZAR", command=self.actualizar, fg_color="#2980B9", hover_color="#1F618D", width=300, height=38, font=("Arial", 12, "bold"))
        btn_actualizar.pack(pady=4)

        btn_eliminar = ctk.CTkButton(frame_form, text="ELIMINAR", command=self.eliminar, fg_color="#E74C3C", hover_color="#C0392B", width=300, height=38, font=("Arial", 12, "bold"))
        btn_eliminar.pack(pady=4)

        btn_limpiar = ctk.CTkButton(frame_form, text="LIMPIAR CAMPOS", command=self.limpiar_campos, fg_color="#7F8C8D", hover_color="#616A6B", width=300, height=38, font=("Arial", 12, "bold"))
        btn_limpiar.pack(pady=4)

        frame_tabla = ctk.CTkFrame(frame_contenido, fg_color="transparent")
        frame_tabla.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", font=("Arial", 11), rowheight=30, background="#FFFFFF", fieldbackground="#FFFFFF", foreground="#2C3E50")
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#EAECEE", foreground="#1F4E78")

        self.tabla = ttk.Treeview(frame_tabla, columns=("codigo", "descripcion", "unidad", "presentacion", "precio", "stock", "estado"), show="headings")
        self.tabla.heading("codigo", text="Código")
        self.tabla.heading("descripcion", text="Descripción")
        self.tabla.heading("unidad", text="Unidad")
        self.tabla.heading("presentacion", text="Presentación")
        self.tabla.heading("precio", text="Precio (Q)")
        self.tabla.heading("stock", text="Stock")
        self.tabla.heading("estado", text="Estado")

        self.tabla.column("codigo", width=100, anchor="center")
        self.tabla.column("descripcion", width=250)
        self.tabla.column("unidad", width=90, anchor="center")
        self.tabla.column("presentacion", width=110, anchor="center")
        self.tabla.column("precio", width=90, anchor="center")
        self.tabla.column("stock", width=80, anchor="center")
        self.tabla.column("estado", width=90, anchor="center")

        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_registro)
        self.cargar_datos()

    def cargar_datos(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        productos = listar_productos_controller()
        for prod in productos:
            if isinstance(prod, dict):
                codigo = prod.get("codigo", "")
                descripcion = prod.get("descripcion", "")
                unidad = prod.get("unidad_medida") or prod.get("unidad", "")
                presentacion = prod.get("presentacion", "")
                precio_raw = prod.get("precio", 0)
                precio_fmt = f"Q{float(precio_raw):.2f}" if precio_raw is not None else "Q0.00"
                stock = prod.get("stock", 0)
                estado = prod.get("estado", "")
                self.tabla.insert("", "end", values=(codigo, descripcion, unidad, presentacion, precio_fmt, stock, estado))
            else:
                self.tabla.insert("", "end", values=prod)

    def seleccionar_registro(self, event):
        item = self.tabla.focus()
        if not item:
            return
        valores = self.tabla.item(item, "values")
        if valores:
            self.limpiar_campos()
            self.txt_codigo.insert(0, valores[0])
            self.txt_descripcion.insert(0, valores[1])
            self.combo_unidad.set(valores[2])
            self.combo_presentacion.set(valores[3])
            precio_limpio = str(valores[4]).replace("Q", "").strip()
            self.txt_precio.insert(0, precio_limpio)
            self.txt_stock.insert(0, valores[5])
            self.combo_estado.set(valores[6])

    def guardar(self):
        codigo = self.txt_codigo.get().strip()
        descripcion = self.txt_descripcion.get().strip()
        unidad = self.combo_unidad.get()
        presentacion = self.combo_presentacion.get()
        precio_str = self.txt_precio.get().strip()
        stock_str = self.txt_stock.get().strip()
        estado = self.combo_estado.get()

        exito, msj = registrar_producto_controller(codigo, descripcion, unidad, presentacion, precio_str, stock_str, estado)
        if exito:
            self.cargar_datos()
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", msj)

    def actualizar(self):
        codigo = self.txt_codigo.get().strip()
        descripcion = self.txt_descripcion.get().strip()
        unidad = self.combo_unidad.get()
        presentacion = self.combo_presentacion.get()
        precio_str = self.txt_precio.get().strip()
        stock_str = self.txt_stock.get().strip()
        estado = self.combo_estado.get()

        if not codigo:
            messagebox.showwarning("Atención", "Seleccione un producto de la tabla para actualizar.")
            return

        exito, msj = actualizar_producto_controller(codigo, descripcion, unidad, presentacion, precio_str, stock_str, estado)
        if exito:
            self.cargar_datos()
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", msj)

    def eliminar(self):
        codigo = self.txt_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Atención", "Seleccione un producto para eliminar.")
            return

        if messagebox.askyesno("Confirmación", f"¿Desea eliminar el producto {codigo}?"):
            exito, msj = eliminar_producto_controller(codigo)
            if exito:
                self.cargar_datos()
                self.limpiar_campos()
            else:
                messagebox.showerror("Error", msj)

    def limpiar_campos(self):
        self.txt_codigo.delete(0, "end")
        self.txt_descripcion.delete(0, "end")
        self.txt_precio.delete(0, "end")
        self.txt_stock.delete(0, "end")
        self.combo_unidad.set("Sacos")
        self.combo_presentacion.set("Saco")
        self.combo_estado.set("Activo")

if __name__ == "__main__":
    app = ctk.CTk()
    app.withdraw()
    win = VentanaProductos(app)
    app.mainloop()