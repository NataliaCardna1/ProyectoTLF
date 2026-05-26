# ============================================================
#  main.py  —  Aplicación principal - PatternLex
#  Integra buscador de patrones y validador de formulario
#  Punto de entrada único para el proyecto
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Configurar rutas de importación
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, 'motor'))
sys.path.insert(0, os.path.join(BASE, 'busqueda'))
sys.path.insert(0, os.path.join(BASE, 'validacion'))

from motor_patrones import buscar_patrones, PATRONES, reporte


# ──────────────────────────────────────────────────────────────
#  Aplicación Principal — Menú de opciones
# ──────────────────────────────────────────────────────────────

class AplicacionPrincipal(tk.Tk):
    """Interfaz principal que ofrece acceso a todas las funcionalidades."""
    
    def __init__(self):
        super().__init__()
        self.title("PatternLex — Plataforma Integrada de Patrones")
        self.geometry("700x550")
        self.minsize(600, 450)
        self.configure(bg='#1A1D27')
        self.resizable(True, True)
        
        self._configurar_estilos()
        self._construir_interfaz()
        
    def _configurar_estilos(self):
        """Configuración de estilos para la interfaz."""
        style = ttk.Style(self)
        style.theme_use('clam')
        
        # Colores personalizados
        style.configure('TFrame', background='#1A1D27')
        style.configure('Title.TLabel',
                       background='#1A1D27', foreground='#00E5A0',
                       font=('Courier New', 20, 'bold'))
        style.configure('Subtitle.TLabel',
                       background='#1A1D27', foreground='#6B7A99',
                       font=('Courier New', 11))
        style.configure('Description.TLabel',
                       background='#22263A', foreground='#A8B4D0',
                       font=('Courier New', 9))
        style.configure('Card.TFrame', background='#22263A', relief='flat')
        style.configure('MainButton.TButton',
                       background='#00E5A0', foreground='#0A0D15',
                       font=('Courier New', 11, 'bold'),
                       padding=(15, 10), borderwidth=0)
        style.map('MainButton.TButton',
                 background=[('active', '#00BF87'), ('pressed', '#009C6E')])
        style.configure('SecondaryButton.TButton',
                       background='#2D3A5A', foreground='#00E5A0',
                       font=('Courier New', 10),
                       padding=(10, 8), borderwidth=1)
        style.map('SecondaryButton.TButton',
                 background=[('active', '#3A4A70'), ('pressed', '#2A3A60')])
    
    def _construir_interfaz(self):
        """Construye la interfaz principal."""
        # Frame principal con padding
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # ─── Encabezado ───
        header = ttk.Frame(main_frame)
        header.pack(fill='x', pady=(0, 30))
        
        ttk.Label(header, text="⬡ PatternLex",
                 style='Title.TLabel').pack(side='left')
        ttk.Label(header, text="v1.0  |  Plataforma de Análisis de Patrones",
                 style='Subtitle.TLabel').pack(side='left', padx=15)
        
        # ─── Descripción ───
        desc_frame = ttk.Frame(main_frame, style='Card.TFrame')
        desc_frame.pack(fill='x', pady=(0, 25))
        
        desc = ("Herramienta profesional para búsqueda y validación de patrones.\n"
                "Implementada con Autómatas Finitos Deterministas (AFD).\n"
                "Teoría de Lenguajes Formales — Procesamiento de Texto.")
        
        ttk.Label(desc_frame, text=desc, style='Description.TLabel',
                 justify='center', wraplength=500).pack(padx=15, pady=12)
        
        # ─── Opciones principales ───
        opciones_frame = ttk.Frame(main_frame)
        opciones_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        # Opción 1: Buscador
        self._crear_tarjeta_opcion(
            opciones_frame,
            "🔍 BUSCADOR DE PATRONES",
            "Busca múltiples patrones en texto\n(correos, teléfonos, fechas, URLs, etc.)",
            self._abrir_buscador,
            0
        )
        
        # Opción 2: Validador
        self._crear_tarjeta_opcion(
            opciones_frame,
            "✓ VALIDADOR DE FORMULARIO",
            "Valida campos de formulario en tiempo real\n(correo, contraseña, teléfono, fecha)",
            self._abrir_validador,
            1
        )
        
        # Opción 3: Demostración
        self._crear_tarjeta_opcion(
            opciones_frame,
            "▶ DEMOSTRACIÓN",
            "Ejecuta una demostración rápida\ncon texto de ejemplo",
            self._ejecutar_demo,
            2
        )
        
        # ─── Pie de página ───
        pie_frame = ttk.Frame(main_frame)
        pie_frame.pack(fill='x', side='bottom')
        
        ttk.Button(pie_frame, text="Salir", style='SecondaryButton.TButton',
                  command=self.quit).pack(side='right')
        ttk.Label(pie_frame, text="PatternLex © 2026  |  Teoría de Lenguajes Formales",
                 style='Subtitle.TLabel', foreground='#4A5568').pack(side='left')
    
    def _crear_tarjeta_opcion(self, padre, titulo, descripcion, comando, indice):
        """Crea una tarjeta de opción con título, descripción y botón."""
        card = ttk.Frame(padre, style='Card.TFrame')
        card.pack(fill='x', pady=8)
        
        contenido = ttk.Frame(card)
        contenido.pack(fill='both', expand=True, padx=15, pady=12)
        
        ttk.Label(contenido, text=titulo,
                 font=('Courier New', 12, 'bold'),
                 foreground='#00E5A0', background='#22263A').pack(anchor='w', pady=(0, 5))
        
        ttk.Label(contenido, text=descripcion,
                 style='Description.TLabel',
                 justify='left', wraplength=400).pack(anchor='w', fill='x')
        
        btn_frame = ttk.Frame(card)
        btn_frame.pack(fill='x', padx=15, pady=(8, 12))
        
        ttk.Button(btn_frame, text="Abrir", style='MainButton.TButton',
                  command=comando).pack(side='right')
    
    def _abrir_buscador(self):
        """Abre la aplicación de búsqueda de patrones."""
        try:
            from buscador_patrones import AplicacionPatrones
            app = AplicacionPatrones()
            self.withdraw()  # Oculta la ventana principal
            app.protocol("WM_DELETE_WINDOW", lambda: self._cerrar_ventana(app))
            app.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el buscador:\n{e}")
    
    def _abrir_validador(self):
        """Abre la aplicación de validación de formulario."""
        try:
            from validador_formulario import AplicacionValidador
            app = AplicacionValidador()
            self.withdraw()  # Oculta la ventana principal
            app.protocol("WM_DELETE_WINDOW", lambda: self._cerrar_ventana(app))
            app.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el validador:\n{e}")
    
    def _cerrar_ventana(self, ventana):
        """Maneja el cierre de ventanas secundarias."""
        ventana.destroy()
        self.deiconify()  # Muestra la ventana principal nuevamente
    
    def _ejecutar_demo(self):
        """Ejecuta una demostración rápida del motor."""
        texto_demo = """
        TEXTO DE DEMOSTRACIÓN - PatternLex
        
        Información de contacto:
        • Email: juan.perez@ejemplo.com
        • Teléfono: 3001234567
        • Celular internacional: +57 310 456 7890
        
        Datos importantes:
        • Cédula: 1098765432
        • Fecha de nacimiento: 15/03/1995
        • Vencimiento: 2026-12-31
        
        Recursos web:
        • Sitio: https://www.ejemplo.com/pagina?id=42
        • Repositorio: https://github.com/usuario/proyecto
        
        Vehículos:
        • Placa carro: ABC-123
        • Placa moto: XYZ-45K
        """
        
        # Ejecutar búsqueda
        resultados = buscar_patrones(texto_demo)
        informe = reporte(resultados)
        
        # Mostrar resultado en una ventana nueva
        demo_win = tk.Toplevel(self)
        demo_win.title("Demostración - PatternLex")
        demo_win.geometry("800x600")
        demo_win.configure(bg='#1A1D27')
        
        # Frame con título
        title_frame = ttk.Frame(demo_win)
        title_frame.pack(fill='x', padx=15, pady=10)
        ttk.Label(title_frame, text="Análisis de Ejemplo",
                 font=('Courier New', 14, 'bold'),
                 foreground='#00E5A0', background='#1A1D27').pack(side='left')
        
        # Text widget para mostrar resultados
        text_widget = tk.Text(
            demo_win,
            bg='#0D101A', fg='#A8B4D0',
            font=('Courier New', 9),
            wrap='word', relief='flat',
            padx=10, pady=10
        )
        text_widget.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Mostrar informe
        text_widget.insert('1.0', informe)
        text_widget.config(state='disabled')
        
        # Frame de botones
        btn_frame = ttk.Frame(demo_win)
        btn_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        def copiar_al_portapapeles():
            self.clipboard_clear()
            self.clipboard_append(informe)
            messagebox.showinfo("Copiado", "Reporte copiado al portapapeles")
        
        ttk.Button(btn_frame, text="Copiar", style='SecondaryButton.TButton',
                  command=copiar_al_portapapeles).pack(side='right', padx=5)
        ttk.Button(btn_frame, text="Cerrar", style='SecondaryButton.TButton',
                  command=demo_win.destroy).pack(side='right')


# ──────────────────────────────────────────────────────────────
#  Punto de entrada
# ──────────────────────────────────────────────────────────────

if __name__ == '__main__':
    app = AplicacionPrincipal()
    app.mainloop()
