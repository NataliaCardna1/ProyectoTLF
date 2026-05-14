# ============================================================
#  buscador_patrones.py  —  Interfaz gráfica con tkinter
#  Importa el motor de motor_patrones.py
# ============================================================

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sys, os

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE, '..', 'motor'))
from motor_patrones import buscar_patrones, PATRONES, reporte

# ── Paleta de colores por tipo de patrón ──────────────────────
COLORES = {
    'Correo electrónico': '#4FC3F7',   # azul claro
    'Teléfono':           '#81C784',   # verde
    'Fecha':              '#FFB74D',   # naranja
    'URL':                '#CE93D8',   # morado
    'Placa vehicular':    '#F48FB1',   # rosa
    'Cédula / ID':        '#80DEEA',   # cyan
}

COLORES_OSCUROS = {
    'Correo electrónico': '#0277BD',
    'Teléfono':           '#2E7D32',
    'Fecha':              '#E65100',
    'URL':                '#6A1B9A',
    'Placa vehicular':    '#AD1457',
    'Cédula / ID':        '#00838F',
}


class AplicacionPatrones(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PatternLex — Búsqueda de Patrones")
        self.geometry("1100x720")
        self.minsize(800, 550)
        self.configure(bg='#1A1D27')
        self._configurar_estilos()
        self._construir_ui()
        self._insertar_texto_ejemplo()

    # ── Estilos ──────────────────────────────────────────────
    def _configurar_estilos(self):
        style = ttk.Style(self)
        style.theme_use('clam')

        style.configure('TFrame', background='#1A1D27')
        style.configure('Panel.TFrame', background='#22263A')
        style.configure('TLabel',
                         background='#1A1D27', foreground='#C9D1E8',
                         font=('Courier New', 10))
        style.configure('Title.TLabel',
                         background='#1A1D27', foreground='#00E5A0',
                         font=('Courier New', 16, 'bold'))
        style.configure('Sub.TLabel',
                         background='#1A1D27', foreground='#6B7A99',
                         font=('Courier New', 9))
        style.configure('Header.TLabel',
                         background='#22263A', foreground='#A8B4D0',
                         font=('Courier New', 9, 'bold'))
        style.configure('TCheckbutton',
                         background='#1A1D27', foreground='#C9D1E8',
                         font=('Courier New', 9))
        style.map('TCheckbutton',
                  background=[('active', '#1A1D27')],
                  foreground=[('active', '#00E5A0')])
        style.configure('Accent.TButton',
                         background='#00E5A0', foreground='#0A0D15',
                         font=('Courier New', 10, 'bold'),
                         borderwidth=0, padding=(12, 6))
        style.map('Accent.TButton',
                  background=[('active', '#00BF87'), ('pressed', '#009C6E')])
        style.configure('Ghost.TButton',
                         background='#22263A', foreground='#6B7A99',
                         font=('Courier New', 9),
                         borderwidth=1, padding=(8, 4))
        style.map('Ghost.TButton',
                  background=[('active', '#2D3350')],
                  foreground=[('active', '#A8B4D0')])
        style.configure('TNotebook', background='#1A1D27', borderwidth=0)
        style.configure('TNotebook.Tab',
                         background='#22263A', foreground='#6B7A99',
                         font=('Courier New', 9), padding=(10, 5))
        style.map('TNotebook.Tab',
                  background=[('selected', '#1A1D27')],
                  foreground=[('selected', '#00E5A0')])

    # ── UI Principal ─────────────────────────────────────────
    def _construir_ui(self):
        # Título
        cab = ttk.Frame(self, padding=(20, 14, 20, 8))
        cab.pack(fill='x')
        ttk.Label(cab, text="⬡ PatternLex", style='Title.TLabel').pack(side='left')
        ttk.Label(cab, text="Motor de búsqueda de patrones  |  Autómatas Finitos",
                  style='Sub.TLabel').pack(side='left', padx=14, pady=4)

        sep = tk.Frame(self, bg='#00E5A0', height=1)
        sep.pack(fill='x', padx=20)

        # Cuerpo principal (3 columnas)
        cuerpo = ttk.Frame(self, padding=(16, 10))
        cuerpo.pack(fill='both', expand=True)
        cuerpo.columnconfigure(0, weight=3)
        cuerpo.columnconfigure(1, weight=0)
        cuerpo.columnconfigure(2, weight=2)
        cuerpo.rowconfigure(0, weight=1)

        self._panel_texto(cuerpo)
        self._panel_controles(cuerpo)
        self._panel_resultados(cuerpo)

    # ── Panel izquierdo: editor de texto ─────────────────────
    def _panel_texto(self, padre):
        frame = ttk.Frame(padre, style='Panel.TFrame', padding=2)
        frame.grid(row=0, column=0, sticky='nsew', padx=(0,6))
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)

        barra = ttk.Frame(frame, style='Panel.TFrame', padding=(6,4))
        barra.grid(row=0, column=0, sticky='ew')
        ttk.Label(barra, text="TEXTO DE ENTRADA",
                  style='Header.TLabel').pack(side='left')
        ttk.Button(barra, text="Cargar archivo",
                   style='Ghost.TButton',
                   command=self._cargar_archivo).pack(side='right', padx=2)
        ttk.Button(barra, text="Limpiar",
                   style='Ghost.TButton',
                   command=self._limpiar_texto).pack(side='right', padx=2)

        self.text_entrada = tk.Text(
            frame,
            bg='#0D101A', fg='#C9D1E8',
            insertbackground='#00E5A0',
            selectbackground='#2D3A5A',
            font=('Courier New', 10),
            wrap='word', relief='flat',
            padx=10, pady=10,
            undo=True
        )
        self.text_entrada.grid(row=1, column=0, sticky='nsew')

        sb = ttk.Scrollbar(frame, command=self.text_entrada.yview)
        sb.grid(row=1, column=1, sticky='ns')
        self.text_entrada.configure(yscrollcommand=sb.set)

        # Barra inferior con contador
        self.lbl_chars = ttk.Label(frame, text="0 caracteres",
                                    style='Sub.TLabel', padding=(6,2))
        self.lbl_chars.grid(row=2, column=0, sticky='w')
        self.text_entrada.bind('<KeyRelease>', self._actualizar_contador)

    # ── Panel central: controles ──────────────────────────────
    def _panel_controles(self, padre):
        frame = ttk.Frame(padre, padding=(6,0))
        frame.grid(row=0, column=1, sticky='ns')

        ttk.Label(frame, text="PATRONES",
                  style='Header.TLabel').pack(pady=(0,8))

        self.vars_patron = {}
        for tipo in PATRONES:
            var = tk.BooleanVar(value=True)
            self.vars_patron[tipo] = var
            cb = ttk.Checkbutton(frame, text=tipo, variable=var)
            cb.pack(anchor='w', pady=2)

        ttk.Label(frame, text='', style='Sub.TLabel').pack(pady=4)

        ttk.Button(frame, text="▶  BUSCAR",
                   style='Accent.TButton',
                   command=self._buscar).pack(fill='x', pady=4)

        ttk.Button(frame, text="Exportar .txt",
                   style='Ghost.TButton',
                   command=self._exportar).pack(fill='x', pady=2)

        ttk.Button(frame, text="Quitar marcas",
                   style='Ghost.TButton',
                   command=self._quitar_marcas).pack(fill='x', pady=2)

        # Contador de resultados
        self.lbl_total = ttk.Label(frame, text="—", style='Sub.TLabel',
                                    wraplength=110, justify='center')
        self.lbl_total.pack(pady=8)

    # ── Panel derecho: resultados ─────────────────────────────
    def _panel_resultados(self, padre):
        frame = ttk.Frame(padre, style='Panel.TFrame', padding=2)
        frame.grid(row=0, column=2, sticky='nsew', padx=(6,0))
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)

        ttk.Label(frame, text="RESULTADOS",
                  style='Header.TLabel', padding=(6,4)).grid(row=0, column=0, sticky='w')

        self.text_resultados = tk.Text(
            frame,
            bg='#0D101A', fg='#A8B4D0',
            font=('Courier New', 9),
            wrap='none', relief='flat',
            padx=10, pady=10,
            state='disabled'
        )
        self.text_resultados.grid(row=1, column=0, sticky='nsew')

        sb_y = ttk.Scrollbar(frame, command=self.text_resultados.yview)
        sb_y.grid(row=1, column=1, sticky='ns')
        sb_x = ttk.Scrollbar(frame, orient='horizontal',
                              command=self.text_resultados.xview)
        sb_x.grid(row=2, column=0, sticky='ew')
        self.text_resultados.configure(
            yscrollcommand=sb_y.set,
            xscrollcommand=sb_x.set
        )

        # Tags de color en el panel de resultados
        for tipo, color in COLORES.items():
            self.text_resultados.tag_configure(
                f'res_{tipo}',
                foreground=color,
                font=('Courier New', 9, 'bold')
            )
        self.text_resultados.tag_configure(
            'seccion',
            foreground='#4A5568',
            font=('Courier New', 8)
        )
        self.text_resultados.tag_configure(
            'tipo_hdr',
            foreground='#6B8CDA',
            font=('Courier New', 9, 'bold')
        )

    # ── Acciones ─────────────────────────────────────────────
    def _actualizar_contador(self, *_):
        n = len(self.text_entrada.get('1.0', 'end-1c'))
        self.lbl_chars.config(text=f"{n:,} caracteres")

    def _cargar_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo de texto",
            filetypes=[("Archivos de texto", "*.txt"),
                       ("CSV", "*.csv"),
                       ("Todos", "*.*")]
        )
        if ruta:
            try:
                with open(ruta, encoding='utf-8', errors='replace') as f:
                    contenido = f.read()
                self.text_entrada.delete('1.0', 'end')
                self.text_entrada.insert('1.0', contenido)
                self._actualizar_contador()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")

    def _limpiar_texto(self):
        self.text_entrada.delete('1.0', 'end')
        self._quitar_marcas()
        self._limpiar_resultados()
        self.lbl_total.config(text="—")
        self._actualizar_contador()

    def _quitar_marcas(self):
        for tipo in PATRONES:
            self.text_entrada.tag_remove(f'mark_{tipo}', '1.0', 'end')

    def _limpiar_resultados(self):
        self.text_resultados.config(state='normal')
        self.text_resultados.delete('1.0', 'end')
        self.text_resultados.config(state='disabled')

    def _buscar(self):
        texto = self.text_entrada.get('1.0', 'end-1c')
        if not texto.strip():
            messagebox.showwarning("Sin texto", "Escribe o carga un texto primero.")
            return

        activos = [t for t, v in self.vars_patron.items() if v.get()]
        if not activos:
            messagebox.showwarning("Sin patrones", "Selecciona al menos un patrón.")
            return

        self._quitar_marcas()

        # Configurar tags de resaltado en el editor
        for tipo, color in COLORES.items():
            self.text_entrada.tag_configure(
                f'mark_{tipo}',
                background=color,
                foreground='#0A0D15',
                font=('Courier New', 10, 'bold')
            )

        resultados = buscar_patrones(texto, activos)

        # Resaltar en el editor
        for tipo, matches in resultados.items():
            for m in matches:
                ini = f"1.0 + {m['inicio']} chars"
                fin = f"1.0 + {m['fin']} chars"
                self.text_entrada.tag_add(f'mark_{tipo}', ini, fin)

        # Mostrar en panel de resultados
        self._mostrar_resultados(resultados)

        total = sum(len(v) for v in resultados.values())
        self.lbl_total.config(
            text=f"{total} coincidencias\nen {len(activos)} patrones"
        )

    def _mostrar_resultados(self, resultados):
        self.text_resultados.config(state='normal')
        self.text_resultados.delete('1.0', 'end')

        for tipo, matches in resultados.items():
            # Encabezado de sección
            self.text_resultados.insert('end',
                f"\n{'─'*38}\n", 'seccion')
            self.text_resultados.insert('end',
                f" {tipo}  ({len(matches)})\n", 'tipo_hdr')
            self.text_resultados.insert('end',
                f"{'─'*38}\n", 'seccion')

            if matches:
                for m in matches:
                    self.text_resultados.insert('end', f"  [{m['inicio']:>4}]  ")
                    self.text_resultados.insert('end',
                        f"{m['texto']}\n", f"res_{tipo}")
            else:
                self.text_resultados.insert('end',
                    "  — ninguno —\n", 'seccion')

        self.text_resultados.config(state='disabled')

    def _exportar(self):
        texto = self.text_entrada.get('1.0', 'end-1c')
        if not texto.strip():
            messagebox.showwarning("Sin texto", "No hay texto para analizar.")
            return

        activos = [t for t, v in self.vars_patron.items() if v.get()]
        resultados = buscar_patrones(texto, activos)
        informe = reporte(resultados)

        ruta = filedialog.asksaveasfilename(
            title="Guardar reporte",
            defaultextension=".txt",
            filetypes=[("Texto", "*.txt")]
        )
        if ruta:
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write(informe)
            messagebox.showinfo("Guardado", f"Reporte guardado en:\n{ruta}")

    # ── Texto de ejemplo ─────────────────────────────────────
    def _insertar_texto_ejemplo(self):
        ejemplo = """Ejemplo de texto con múltiples patrones:

Contactos:
  - juan.perez@gmail.com
  - soporte@empresa.com.co
  - info@universidad.edu.co

Teléfonos:
  - Celular: 3001234567
  - Internacional: +57 310 456 7890
  - Fijo: (601) 234-5678

Fechas importantes:
  - Nacimiento: 15/03/1995
  - Vencimiento: 2026-12-31
  - Evento: 01-07-2025

Sitios web:
  - https://www.ejemplo.com/pagina?id=42#inicio
  - http://github.com/usuario/proyecto
  - ftp://archivos.servidor.co

Placas vehiculares:
  - Carro: ABC-123
  - Moto: XYZ-45K

Cédulas:
  - 1098765432
  - 987654321
  - 123456
"""
        self.text_entrada.insert('1.0', ejemplo)
        self._actualizar_contador()


# ── Punto de entrada ──────────────────────────────────────────
if __name__ == '__main__':
    app = AplicacionPatrones()
    app.mainloop()