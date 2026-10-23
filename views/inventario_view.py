# ============================================================
# ARCHIVO: views/inventario_view.py
# DESCRIPCIÓN: Vista de Reportería con Filtros Avanzados (RF-04)
# ============================================================

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import ttk
from controllers.inventario_controller import buscar_inventario_controller

class VentanaInventario(ctk.CTkToplevel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.title("FERRETERÍA TIKAL - Reportería de Inventario")
        self.after(0, lambda: self.state('zoomed'))
        self.configure(fg_color="#F4F6F7")
        self.grab_set()

        lbl_titulo = ctk.CTkLabel(self, text="📊 INVENTARIO Y CONTROL DE STOCK - FERRETERÍA TIKAL", font=("Arial", 22, "bold"), text_color="#1F4E78")
        lbl_titulo.pack(pady=15)

        # --- PANEL DE FILTROS Y BÚSQUEDA (RF-04.2 / RF-04.3) ---
        frame_filtros = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=10, border_width=1, border_color="#D5D8DC")
        frame_filtros.pack(fill="x", padx=30, pady=(0, 15))

        ctk.CTkLabel(frame_filtros, text="FILTROS DE BÚSQUEDA:", font=("Arial", 12, "bold"), text_color="#1F4E78").pack(anchor="w", padx=15, pady=(10, 5))

        frame_inputs = ctk.CTkFrame(frame_filtros, fg_color="transparent")
        frame_inputs.pack(fill="x", padx=15, pady=(0, 10))

        self.txt_filtro_codigo = ctk.CTkEntry(frame_inputs, placeholder_text="Código (ej: FER-001)", width=180, height=35)
        self.txt_filtro_codigo.pack(side="left", padx=(0, 10))

        self.txt_filtro_desc = ctk.CTkEntry(frame_inputs, placeholder_text="Descripción / Producto", width=250, height=35)
        self.txt_filtro_desc.pack(side="left", padx=10)

        self.txt_filtro_fecha = ctk.CTkEntry(frame_inputs, placeholder_text="Fecha (YYYY-MM-DD)", width=180, height=35)
        self.txt_filtro_fecha.pack(side="left", padx=10)

        btn_buscar = ctk.CTkButton(frame_inputs, text="🔍 BUSCAR", command=self.ejecutar_busqueda, fg_color="#1F4E78", hover_color="#154360", width=120, height=35, font=("Arial", 11, "bold"))
        btn_buscar.pack(side="left", padx=10)

        btn_limpiar = ctk.CTkButton(frame_inputs, text="🧹 LIMPIAR", command=self.limpiar_filtros, fg_color="#7F8C8D", hover_color="#616A6B", width=110, height=35, font=("Arial", 11, "bold"))
        btn_limpiar.pack(side="left", padx=5)

        btn_cancelar = ctk.CTkButton(frame_inputs, text="❌ CANCELAR", command=self.destroy, fg_color="#E74C3C", hover_color="#C0392B", width=110, height=35, font=("Arial", 11, "bold"))
        btn_cancelar.pack(side="left", padx=5)

        # --- TARJETAS INFORMATIVAS (KPIs) ---
        frame_kpi = ctk.CTkFrame(self, fg_color="transparent")
        frame_kpi.pack(fill="x", padx=30, pady=(0, 10))

        self.card_total_prod = ctk.CTkFrame(frame_kpi, fg_color="#1F4E78", corner_radius=10, height=80)
        self.card_total_prod.pack(side="left", expand=True, fill="both", padx=10)
        self.lbl_kpi_prod = ctk.CTkLabel(self.card_total_prod, text="Total Ítems\n0", font=("Arial", 13, "bold"), text_color="white")
        self.lbl_kpi_prod.pack(pady=15)

        self.card_total_stock = ctk.CTkFrame(frame_kpi, fg_color="#27AE60", corner_radius=10, height=80)
        self.card_total_stock.pack(side="left", expand=True, fill="both", padx=10)
        self.lbl_kpi_stock = ctk.CTkLabel(self.card_total_stock, text="Unidades en Stock\n0", font=("Arial", 13, "bold"), text_color="white")
        self.lbl_kpi_stock.pack(pady=15)

        self.card_valor = ctk.CTkFrame(frame_kpi, fg_color="#D35400", corner_radius=10, height=80)
        self.card_valor.pack(side="left", expand=True, fill="both", padx=10)
        self.lbl_kpi_valor = ctk.CTkLabel(self.card_valor, text="Valor Total Inventario\nQ0.00", font=("Arial", 13, "bold"), text_color="white")
        self.lbl_kpi_valor.pack(pady=15)

        # --- TABLA SEGÚN RF-04.1 (7 COLUMNAS EXACTAS) ---
        frame_tabla = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=10, border_width=1, border_color="#D5D8DC")
        frame_tabla.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", font=("Arial", 10), rowheight=28, background="#FFFFFF", fieldbackground="#FFFFFF", foreground="#2C3E50")
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#EAECEE", foreground="#1F4E78")

        self.tabla = ttk.Treeview(
            frame_tabla, 
            columns=("codigo", "fecha", "descripcion", "cantidad", "presentacion", "unidad", "precio"), 
            show="headings"
        )

        self.tabla.heading("codigo", text="CÓDIGO")
        self.tabla.heading("fecha", text="FECHA")
        self.tabla.heading("descripcion", text="DESCRIPCIÓN")
        self.tabla.heading("cantidad", text="CANTIDAD")
        self.tabla.heading("presentacion", text="PRESENTACIÓN")
        self.tabla.heading("unidad", text="UNIDAD MEDIDA")
        self.tabla.heading("precio", text="PRECIO")

        self.tabla.column("codigo", width=100, anchor="center")
        self.tabla.column("fecha", width=110, anchor="center")
        self.tabla.column("descripcion", width=280)
        self.tabla.column("cantidad", width=100, anchor="center")
        self.tabla.column("presentacion", width=120, anchor="center")
        self.tabla.column("unidad", width=120, anchor="center")
        self.tabla.column("precio", width=110, anchor="center")

        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

        # Carga inicial sin filtro (RF-04.2 punto 1)
        self.ejecutar_busqueda()

    def ejecutar_busqueda(self):
        cod = self.txt_filtro_codigo.get().strip()
        desc = self.txt_filtro_desc.get().strip()
        fec = self.txt_filtro_fecha.get().strip()

        datos, total_items, total_stock, valor_inventario = buscar_inventario_controller(cod, desc, fec)

        for row in self.tabla.get_children():
            self.tabla.delete(row)

        for item in datos:
            precio_f = float(item["precio"])
            self.tabla.insert("", "end", values=(
                item["codigo"],
                str(item["fecha"]),
                item["descripcion"],
                item["cantidad"],
                item["presentacion"],
                item["unidad_medida"],
                f"Q{precio_f:.2f}"
            ))

        self.lbl_kpi_prod.configure(text=f"Total Ítems\n{total_items}")
        self.lbl_kpi_stock.configure(text=f"Stock Total Acumulado\n{total_stock}")
        self.lbl_kpi_valor.configure(text=f"Valor Total Inventario\nQ{valor_inventario:,.2f}")

    def limpiar_filtros(self):
        self.txt_filtro_codigo.delete(0, "end")
        self.txt_filtro_desc.delete(0, "end")
        self.txt_filtro_fecha.delete(0, "end")
        self.ejecutar_busqueda()

if __name__ == "__main__":
    app = ctk.CTk()
    app.withdraw()
    win = VentanaInventario(app)
    app.mainloop()