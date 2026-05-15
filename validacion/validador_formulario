# ============================================================
#  validador_formulario.py  —  Formulario con validación
#  Validación en tiempo real + bloqueo al enviar
#  SIN usar librería 're' — AFDs implementados a mano
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
import sys, os

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE, '..', 'motor'))
from motor_patrones import afd_correo_v2, afd_telefono, afd_fecha


# ──────────────────────────────────────────────────────────────
#  AFDs adicionales para validación de formulario
#  (no están en el motor de búsqueda, son específicos de campos)
# ──────────────────────────────────────────────────────────────

def validar_correo(texto):
    """Valida que TODO el texto sea un correo válido."""
    texto = texto.strip()
    if not texto:
        return False, "El correo es obligatorio"
    ok, fin = afd_correo_v2(texto, 0)
    if ok and fin == len(texto):
        return True, "✓ Correo válido"
    return False, "Formato inválido  (ej: usuario@dominio.com)"


def validar_contrasena(texto):
    """
    AFD para contraseña segura:
    - Mínimo 8 caracteres
    - Al menos una mayúscula
    - Al menos una minúscula
    - Al menos un dígito
    - Al menos un carácter especial: !@#$%^&*()_+-=[]{}|
    """
    ESPECIALES = set('!@#$%^&*()_+-=[]{}|;:,.<>?/')

    if len(texto) < 8:
        return False, f"Mínimo 8 caracteres  (tienes {len(texto)})"

    tiene_may = False
    tiene_min = False
    tiene_dig = False
    tiene_esp = False

    for c in texto:
        if 'A' <= c <= 'Z':
            tiene_may = True
        elif 'a' <= c <= 'z':
            tiene_min = True
        elif '0' <= c <= '9':
            tiene_dig = True
        elif c in ESPECIALES:
            tiene_esp = True

    if not tiene_may:
        return False, "Debe tener al menos una mayúscula"
    if not tiene_min:
        return False, "Debe tener al menos una minúscula"
    if not tiene_dig:
        return False, "Debe tener al menos un número"
    if not tiene_esp:
        return False, "Debe tener al menos un carácter especial (!@#...)"

    # Calcular nivel de seguridad
    largo = len(texto)
    if largo >= 16:
        nivel = "Muy fuerte"
    elif largo >= 12:
        nivel = "Fuerte"
    else:
        nivel = "Aceptable"
    return True, f"✓ Contraseña {nivel}"


def validar_telefono(texto):
    """Valida que TODO el texto sea un teléfono válido."""
    texto = texto.strip()
    if not texto:
        return False, "El teléfono es obligatorio"
    ok, fin = afd_telefono(texto, 0)
    if ok and fin == len(texto):
        return True, "✓ Teléfono válido"
    return False, "Formato inválido  (ej: 3001234567 o +57 300 123 4567)"


def validar_fecha(texto):
    """Valida que TODO el texto sea una fecha válida."""
    texto = texto.strip()
    if not texto:
        return False, "La fecha es obligatoria"
    ok, fin = afd_fecha(texto, 0)
    if ok and fin == len(texto):
        return True, "✓ Fecha válida"
    return False, "Formato inválido  (ej: 15/03/1995 o 1995-03-15)"


# ──────────────────────────────────────────────────────────────
#  Barra de seguridad para contraseña
# ──────────────────────────────────────────────────────────────

def nivel_seguridad(texto):
    """Retorna (nivel 0-4, color) según fortaleza."""
    if not texto:
        return 0, '#2A3347'
    puntos = 0
    ESPECIALES = set('!@#$%^&*()_+-=[]{}|;:,.<>?/')
    if len(texto) >= 8:   puntos += 1
    if len(texto) >= 12:  puntos += 1
    if any('A' <= c <= 'Z' for c in texto) and any('a' <= c <= 'z' for c in texto): puntos += 1
    if any('0' <= c <= '9' for c in texto): puntos += 1
    if any(c in ESPECIALES for c in texto): puntos += 1
    colores = ['#2A3347', '#FF6B6B', '#FFB340', '#FFD700', '#00E5A0']
    return min(puntos, 4), colores[min(puntos, 4)]


# ──────────────────────────────────────────────────────────────
#  Clase principal — Formulario
# ──────────────────────────────────────────────────────────────

class FormularioValidacion(tk.Tk):

    CAMPOS = [
        ('correo',     'Correo electrónico',  'usuario@dominio.com',    False),
        ('contrasena', 'Contraseña',          'Mín. 8 chars, 1 may, 1 núm, 1 especial', True),
        ('telefono',   'Teléfono',            '3001234567 o +57 300...',False),
        ('fecha',      'Fecha de nacimiento', 'DD/MM/AAAA o AAAA-MM-DD',False),
    ]

    VALIDADORES = {
        'correo':     validar_correo,
        'contrasena': validar_contrasena,
        'telefono':   validar_telefono,
        'fecha':      validar_fecha,
    }

    def __init__(self):
        super().__init__()
        self.title("PatternLex — Validación de Formulario")
        self.geometry("560x620")
        self.resizable(False, False)
        self.configure(bg='#1A1D27')
        self._vars = {}
        self._estados = {}   # True/False por campo
        self._configurar_estilos()
        self._construir_ui()

    # ── Estilos ──────────────────────────────────────────────
    def _configurar_estilos(self):
        s = ttk.Style(self)
        s.theme_use('clam')
        s.configure('TFrame', background='#1A1D27')
        s.configure('Card.TFrame', background='#22263A')
        s.configure('TLabel',
                    background='#1A1D27', foreground='#C9D1E8',
                    font=('Courier New', 10))
        s.configure('Title.TLabel',
                    background='#1A1D27', foreground='#00E5A0',
                    font=('Courier New', 16, 'bold'))
        s.configure('Sub.TLabel',
                    background='#1A1D27', foreground='#6B7A99',
                    font=('Courier New', 9))
        s.configure('Campo.TLabel',
                    background='#22263A', foreground='#A8B4D0',
                    font=('Courier New', 9, 'bold'))
        s.configure('Hint.TLabel',
                    background='#22263A', foreground='#4A5568',
                    font=('Courier New', 8))
        s.configure('OK.TLabel',
                    background='#22263A', foreground='#00E5A0',
                    font=('Courier New', 8))
        s.configure('Error.TLabel',
                    background='#22263A', foreground='#FF6B6B',
                    font=('Courier New', 8))
        s.configure('Accent.TButton',
                    background='#00E5A0', foreground='#0A0D15',
                    font=('Courier New', 10, 'bold'),
                    borderwidth=0, padding=(12, 8))
        s.map('Accent.TButton',
              background=[('active', '#00BF87'), ('pressed', '#009C6E')])
        s.configure('Ghost.TButton',
                    background='#22263A', foreground='#6B7A99',
                    font=('Courier New', 9),
                    borderwidth=1, padding=(8, 5))
        s.map('Ghost.TButton',
              background=[('active', '#2D3350')],
              foreground=[('active', '#A8B4D0')])

    # ── UI ───────────────────────────────────────────────────
    def _construir_ui(self):
        # Encabezado
        cab = ttk.Frame(self, padding=(28, 20, 28, 8))
        cab.pack(fill='x')
        ttk.Label(cab, text="⬡ PatternLex",
                  style='Title.TLabel').pack(anchor='w')
        ttk.Label(cab, text="Validación de formulario en tiempo real",
                  style='Sub.TLabel').pack(anchor='w', pady=(2,0))

        sep = tk.Frame(self, bg='#00E5A0', height=1)
        sep.pack(fill='x', padx=28)

        # Tarjeta principal
        card = ttk.Frame(self, style='Card.TFrame', padding=(24, 20))
        card.pack(fill='both', expand=True, padx=28, pady=16)

        for key, etiqueta, placeholder, es_pass in self.CAMPOS:
            self._crear_campo(card, key, etiqueta, placeholder, es_pass)

        # Barra de seguridad de contraseña
        self._barra_frame = ttk.Frame(card, style='Card.TFrame')
        self._barra_frame.pack(fill='x', pady=(0, 8))
        ttk.Label(self._barra_frame, text="Seguridad:",
                  style='Hint.TLabel').pack(side='left')
        self._barras = []
        barra_cont = ttk.Frame(self._barra_frame, style='Card.TFrame')
        barra_cont.pack(side='left', padx=6)
        for _ in range(4):
            seg = tk.Frame(barra_cont, bg='#2A3347',
                           width=42, height=6)
            seg.pack(side='left', padx=2)
            seg.pack_propagate(False)
            self._barras.append(seg)

        # Botones
        btns = ttk.Frame(card, style='Card.TFrame')
        btns.pack(fill='x', pady=(12, 0))
        ttk.Button(btns, text="Limpiar",
                   style='Ghost.TButton',
                   command=self._limpiar).pack(side='left')
        ttk.Button(btns, text="Enviar formulario ▶",
                   style='Accent.TButton',
                   command=self._enviar).pack(side='right')

        # Resumen de estado
        self._lbl_resumen = ttk.Label(card, text="",
                                       style='Hint.TLabel',
                                       padding=(0, 8))
        self._lbl_resumen.pack(anchor='w')

    def _crear_campo(self, padre, key, etiqueta, placeholder, es_pass):
        # Etiqueta
        ttk.Label(padre, text=etiqueta.upper(),
                  style='Campo.TLabel').pack(anchor='w', pady=(10, 2))

        # Entrada
        var = tk.StringVar()
        self._vars[key] = var
        self._estados[key] = False

        entrada = tk.Entry(
            padre,
            textvariable=var,
            bg='#0D101A', fg='#C9D1E8',
            insertbackground='#00E5A0',
            selectbackground='#2D3A5A',
            font=('Courier New', 10),
            relief='flat',
            bd=0,
            highlightthickness=1,
            highlightbackground='#2A3347',
            highlightcolor='#00E5A0',
            show='•' if es_pass else '',
        )
        entrada.pack(fill='x', ipady=6)
        setattr(self, f'_entrada_{key}', entrada)

        # Mostrar/ocultar contraseña
        if es_pass:
            self._mostrar_pass = tk.BooleanVar(value=False)
            chk = tk.Checkbutton(
                padre,
                text="Mostrar contraseña",
                variable=self._mostrar_pass,
                bg='#22263A', fg='#4A5568',
                selectcolor='#0D101A',
                activebackground='#22263A',
                activeforeground='#6B7A99',
                font=('Courier New', 8),
                bd=0,
                command=lambda e=entrada: self._toggle_pass(e)
            )
            chk.pack(anchor='e')

        # Mensaje de estado (hint/ok/error)
        lbl_msg = ttk.Label(padre, text=placeholder,
                             style='Hint.TLabel')
        lbl_msg.pack(anchor='w', pady=(1, 0))
        setattr(self, f'_msg_{key}', lbl_msg)

        # Línea separadora del campo
        tk.Frame(padre, bg='#2A3347', height=1).pack(fill='x', pady=(4,0))

        # Bind validación en tiempo real
        var.trace_add('write', lambda *_,
                      k=key, lbl=lbl_msg, e=entrada: self._validar_campo(k, lbl, e))

    # ── Lógica de validación ─────────────────────────────────
    def _validar_campo(self, key, lbl, entrada):
        texto = self._vars[key].get()
        ok, msg = self.VALIDADORES[key](texto)
        self._estados[key] = ok

        if not texto:
            lbl.configure(style='Hint.TLabel')
            entrada.configure(highlightbackground='#2A3347')
        elif ok:
            lbl.configure(style='OK.TLabel')
            entrada.configure(highlightbackground='#00E5A0')
        else:
            lbl.configure(style='Error.TLabel')
            entrada.configure(highlightbackground='#FF6B6B')

        lbl.configure(text=msg if texto else self._placeholder(key))

        # Actualizar barra de seguridad si es contraseña
        if key == 'contrasena':
            self._actualizar_barra(texto)

        # Actualizar resumen
        self._actualizar_resumen()

    def _placeholder(self, key):
        for k, _, ph, _ in self.CAMPOS:
            if k == key:
                return ph
        return ''

    def _actualizar_barra(self, texto):
        nivel, _ = nivel_seguridad(texto)
        colores_nivel = ['#2A3347', '#FF6B6B', '#FFB340', '#FFD700', '#00E5A0']
        for i, barra in enumerate(self._barras):
            color = colores_nivel[nivel] if i < nivel else '#2A3347'
            barra.configure(bg=color)

    def _actualizar_resumen(self):
        total = len(self._estados)
        ok = sum(1 for v in self._estados.values() if v)
        if ok == 0:
            self._lbl_resumen.configure(text="", style='Hint.TLabel')
        elif ok == total:
            self._lbl_resumen.configure(
                text=f"✓ Todos los campos son válidos ({ok}/{total})",
                style='OK.TLabel')
        else:
            self._lbl_resumen.configure(
                text=f"  {ok}/{total} campos válidos",
                style='Hint.TLabel')

    def _toggle_pass(self, entrada):
        entrada.configure(show='' if self._mostrar_pass.get() else '•')

    # ── Acciones ─────────────────────────────────────────────
    def _enviar(self):
        # Re-validar todos al enviar
        for key, _, _, _ in self.CAMPOS:
            lbl = getattr(self, f'_msg_{key}')
            entrada = getattr(self, f'_entrada_{key}')
            self._validar_campo(key, lbl, entrada)

        invalidos = [k for k, v in self._estados.items() if not v]

        if invalidos:
            nombres = {
                'correo': 'Correo', 'contrasena': 'Contraseña',
                'telefono': 'Teléfono', 'fecha': 'Fecha'
            }
            lista = ', '.join(nombres[k] for k in invalidos)
            messagebox.showerror(
                "Formulario incompleto",
                f"Corrige los siguientes campos:\n\n• {lista.replace(', ', chr(10)+'• ')}"
            )
        else:
            datos = {k: self._vars[k].get() for k in self._vars}
            messagebox.showinfo(
                "✓ Formulario enviado",
                f"Datos registrados correctamente:\n\n"
                f"Correo:    {datos['correo']}\n"
                f"Teléfono:  {datos['telefono']}\n"
                f"Fecha:     {datos['fecha']}\n"
                f"Contraseña: {'•' * len(datos['contrasena'])}"
            )

    def _limpiar(self):
        for key in self._vars:
            self._vars[key].set('')
            self._estados[key] = False
            lbl = getattr(self, f'_msg_{key}')
            entrada = getattr(self, f'_entrada_{key}')
            lbl.configure(text=self._placeholder(key), style='Hint.TLabel')
            entrada.configure(highlightbackground='#2A3347')
        self._actualizar_barra('')
        self._lbl_resumen.configure(text='')


# ── Punto de entrada ─────────────────────────────────────────
if __name__ == '__main__':
    app = FormularioValidacion()
    app.mainloop()