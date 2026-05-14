# ============================================================
#  motor_patrones.py  —  Motor de búsqueda de patrones
#  Implementado SIN usar el módulo 're' de Python
#  Teoría de Lenguajes Formales — Autómatas Finitos Deterministas
# ============================================================

# ──────────────────────────────────────────────────────────────
#  BLOQUE 1: Funciones auxiliares (reemplazan operaciones de re)
# ──────────────────────────────────────────────────────────────

def es_digito(c):
    return '0' <= c <= '9'

def es_letra(c):
    return ('a' <= c <= 'z') or ('A' <= c <= 'Z')

def es_alfanum(c):
    return es_letra(c) or es_digito(c)

def es_hex(c):
    return es_digito(c) or ('a' <= c <= 'f') or ('A' <= c <= 'F')

def es_espacio(c):
    return c in (' ', '\t', '\n', '\r')

def es_punto(c):
    return c == '.'

def esta_en(c, chars):
    """Verifica si c está en el string de caracteres permitidos."""
    return c in chars


# ──────────────────────────────────────────────────────────────
#  BLOQUE 2: AFD para cada patrón
#  Cada función intenta hacer match desde la posición 'inicio'
#  y retorna (True, fin) si hay match, o (False, -1) si no.
# ──────────────────────────────────────────────────────────────

def afd_correo(texto, inicio):
    """
    AFD para correos electrónicos.
    Patrón: usuario@dominio.tld
    usuario: letras, dígitos, puntos, guiones, guión_bajo
    dominio: letras, dígitos, guiones
    tld:     2-6 letras
    """
    i = inicio
    n = len(texto)

    # Estado 0 → 1: al menos un carácter válido en usuario
    if i >= n or not (es_alfanum(texto[i]) or texto[i] in '._-'):
        return False, -1
    while i < n and (es_alfanum(texto[i]) or texto[i] in '._-'):
        i += 1

    # Estado 1 → 2: arroba obligatoria
    if i >= n or texto[i] != '@':
        return False, -1
    i += 1

    # Estado 2 → 3: al menos un carácter de dominio
    if i >= n or not (es_alfanum(texto[i]) or texto[i] == '-'):
        return False, -1
    while i < n and (es_alfanum(texto[i]) or texto[i] == '-'):
        i += 1

    # Estado 3 → 4: punto obligatorio
    if i >= n or texto[i] != '.':
        return False, -1
    i += 1

    # Estado 4 → 5: TLD (2-6 letras), puede tener sub-dominios
    fin_valido = -1
    while i < n and es_letra(texto[i]):
        i += 1
        largo_tld = i - (inicio)  # aproximación
        if 2 <= (i - (i - (i - inicio))):
            pass
        fin_valido = i

        # sub-dominio adicional (p.ej. .co.uk)
        if i < n and texto[i] == '.' and i + 1 < n and es_letra(texto[i+1]):
            i += 1
        else:
            break

    if fin_valido == -1 or (fin_valido - inicio) < 5:
        return False, -1
    return True, fin_valido


def afd_correo_v2(texto, inicio):
    """Versión corregida y más robusta del AFD de correo."""
    i = inicio
    n = len(texto)

    # Parte local: user.name_-123
    if i >= n or not (es_alfanum(texto[i]) or texto[i] in '_-'):
        return False, -1
    while i < n and (es_alfanum(texto[i]) or texto[i] in '._-+'):
        i += 1
    parte_local_fin = i

    if parte_local_fin == inicio:
        return False, -1

    # @
    if i >= n or texto[i] != '@':
        return False, -1
    i += 1

    # Dominio
    dom_inicio = i
    if i >= n or not (es_alfanum(texto[i]) or texto[i] == '-'):
        return False, -1
    while i < n and (es_alfanum(texto[i]) or texto[i] == '-'):
        i += 1
    if i == dom_inicio:
        return False, -1

    # Punto + TLD (puede repetirse para sub-dominios)
    fin_valido = -1
    while i < n and texto[i] == '.':
        i += 1
        tld_inicio = i
        while i < n and es_letra(texto[i]):
            i += 1
        largo = i - tld_inicio
        if 2 <= largo <= 6:
            fin_valido = i
        else:
            break

    if fin_valido == -1:
        return False, -1
    return True, fin_valido


def afd_telefono(texto, inicio):
    """
    AFD para números telefónicos colombianos e internacionales.
    Formatos aceptados:
      3001234567         (10 dígitos, celular colombiano)
      +57 300 123 4567   (con código país)
      (601) 2345678      (fijo Bogotá)
      601-234-5678       (con guiones)
    """
    i = inicio
    n = len(texto)

    # Prefijo internacional opcional: +57
    if i < n and texto[i] == '+':
        i += 1
        if i >= n or not es_digito(texto[i]):
            return False, -1
        while i < n and es_digito(texto[i]):
            i += 1
        # espacio opcional después del código país
        if i < n and texto[i] == ' ':
            i += 1

    # Paréntesis opcionales (indicativo)
    tiene_paren = False
    if i < n and texto[i] == '(':
        tiene_paren = True
        i += 1
        ind_inicio = i
        while i < n and es_digito(texto[i]):
            i += 1
        if i - ind_inicio < 2 or i >= n or texto[i] != ')':
            return False, -1
        i += 1  # cerrar paréntesis
        if i < n and texto[i] == ' ':
            i += 1

    # Dígitos con separadores opcionales (espacios o guiones)
    digitos = 0
    inicio_digitos = i
    while i < n and (es_digito(texto[i]) or texto[i] in ' -'):
        if es_digito(texto[i]):
            digitos += 1
        elif texto[i] in ' -':
            # separador solo válido entre dígitos
            if i + 1 >= n or not es_digito(texto[i+1]):
                break
        i += 1

    # Validar cantidad de dígitos (7 a 12)
    if not (7 <= digitos <= 12):
        return False, -1

    return True, i


def afd_fecha(texto, inicio):
    """
    AFD para fechas.
    Formatos: DD/MM/AAAA  DD-MM-AAAA  AAAA/MM/DD  AAAA-MM-DD
    """
    i = inicio
    n = len(texto)

    def leer_num(pos, largo_min, largo_max):
        j = pos
        while j < n and es_digito(texto[j]):
            j += 1
        largo = j - pos
        if largo_min <= largo <= largo_max:
            return int(texto[pos:j]), j
        return None, pos

    # Intentar AAAA-MM-DD o AAAA/MM/DD
    año, j = leer_num(i, 4, 4)
    if año is not None and j < n and texto[j] in '-/':
        sep = texto[j]; j += 1
        mes, j2 = leer_num(j, 1, 2)
        if mes is not None and j2 < n and texto[j2] == sep:
            j2 += 1
            dia, j3 = leer_num(j2, 1, 2)
            if dia is not None:
                if 1 <= mes <= 12 and 1 <= dia <= 31:
                    return True, j3

    # Intentar DD/MM/AAAA o DD-MM-AAAA
    dia, j = leer_num(i, 1, 2)
    if dia is not None and j < n and texto[j] in '-/':
        sep = texto[j]; j += 1
        mes, j2 = leer_num(j, 1, 2)
        if mes is not None and j2 < n and texto[j2] == sep:
            j2 += 1
            año, j3 = leer_num(j2, 4, 4)
            if año is not None:
                if 1 <= mes <= 12 and 1 <= dia <= 31:
                    return True, j3

    return False, -1


def afd_url(texto, inicio):
    """
    AFD para URLs.
    Formato: scheme://[usuario@]host[:puerto][/ruta][?query][#frag]
    Schemes: http, https, ftp
    """
    i = inicio
    n = len(texto)

    # Scheme: http | https | ftp
    for scheme in ('https://', 'http://', 'ftp://'):
        if texto[i:i+len(scheme)].lower() == scheme:
            i += len(scheme)
            break
    else:
        return False, -1

    # Host: letras, dígitos, guiones, puntos
    if i >= n or not (es_alfanum(texto[i]) or texto[i] == '-'):
        return False, -1
    while i < n and (es_alfanum(texto[i]) or texto[i] in '.-'):
        i += 1
    host_fin = i

    if host_fin == (i - (i - inicio)):
        return False, -1

    # Puerto opcional
    if i < n and texto[i] == ':':
        i += 1
        if i >= n or not es_digito(texto[i]):
            i -= 1  # retroceder, puede ser ruta
        else:
            while i < n and es_digito(texto[i]):
                i += 1

    # Ruta, query, fragmento opcionales
    chars_url = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~:/?#[]@!$&\'()*+,;=%')
    while i < n and texto[i] in chars_url:
        i += 1

    if i == inicio:
        return False, -1
    return True, i


def afd_placa(texto, inicio):
    """
    AFD para placas vehiculares colombianas.
    Formato antiguo: AAA-000  (3 letras + guión + 3 dígitos)
    Formato motos:   AAA-00A  (3 letras + guión + 2 dígitos + 1 letra)
    """
    i = inicio
    n = len(texto)

    # 3 letras
    if i + 2 >= n:
        return False, -1
    if not (es_letra(texto[i]) and es_letra(texto[i+1]) and es_letra(texto[i+2])):
        return False, -1
    i += 3

    # Guión o espacio
    if i >= n or texto[i] not in '-':
        return False, -1
    i += 1

    # 3 dígitos (carro) o 2 dígitos + 1 letra (moto)
    if i + 1 >= n:
        return False, -1

    if es_digito(texto[i]) and es_digito(texto[i+1]):
        i += 2
        if i < n and es_digito(texto[i]):   # carro: 3er dígito
            i += 1
            return True, i
        elif i < n and es_letra(texto[i]):  # moto: letra final
            i += 1
            return True, i
        else:
            return False, -1

    return False, -1


def afd_cedula(texto, inicio):
    """
    AFD para cédulas colombianas (6-10 dígitos).
    """
    i = inicio
    n = len(texto)
    if i >= n or not es_digito(texto[i]):
        return False, -1
    while i < n and es_digito(texto[i]):
        i += 1
    largo = i - inicio
    if 6 <= largo <= 10:
        return True, i
    return False, -1


# ──────────────────────────────────────────────────────────────
#  BLOQUE 3: Motor de búsqueda — escanea todo el texto
# ──────────────────────────────────────────────────────────────

PATRONES = {
    'Correo electrónico': afd_correo_v2,
    'Teléfono':           afd_telefono,
    'Fecha':              afd_fecha,
    'URL':                afd_url,
    'Placa vehicular':    afd_placa,
    'Cédula / ID':        afd_cedula,
}

def buscar_patrones(texto, patrones_activos=None):
    """
    Escanea el texto buscando todos los patrones activos.
    Retorna dict: {tipo: [lista de coincidencias]}
    """
    if patrones_activos is None:
        patrones_activos = list(PATRONES.keys())

    resultados = {tipo: [] for tipo in patrones_activos}
    n = len(texto)

    for tipo in patrones_activos:
        afd = PATRONES[tipo]
        i = 0
        while i < n:
            # No iniciar en medio de una palabra (para IDs y cédulas)
            if tipo == 'Cédula / ID' and i > 0 and es_alfanum(texto[i-1]):
                i += 1
                continue

            ok, fin = afd(texto, i)
            if ok:
                # Verificar que no termine en medio de una palabra
                if fin < n and (es_alfanum(texto[fin]) or texto[fin] in '._-@'):
                    i += 1
                    continue
                coincidencia = texto[i:fin]
                if coincidencia.strip():
                    resultados[tipo].append({
                        'texto': coincidencia,
                        'inicio': i,
                        'fin': fin
                    })
                i = fin  # saltar lo que ya se procesó
            else:
                i += 1

    return resultados


# ──────────────────────────────────────────────────────────────
#  BLOQUE 4: Utilidad de reporte
# ──────────────────────────────────────────────────────────────

def reporte(resultados):
    total = sum(len(v) for v in resultados.values())
    lineas = [f"\n{'='*55}", f"  REPORTE DE PATRONES ENCONTRADOS  ({total} total)", f"{'='*55}"]
    for tipo, matches in resultados.items():
        lineas.append(f"\n▸ {tipo} ({len(matches)} encontrados):")
        if matches:
            for m in matches:
                lineas.append(f"    [{m['inicio']:>4}:{m['fin']:<4}]  {m['texto']}")
        else:
            lineas.append("    — ninguno —")
    lineas.append(f"\n{'='*55}\n")
    return '\n'.join(lineas)


# ──────────────────────────────────────────────────────────────
#  PRUEBA RÁPIDA (ejecutar directamente)
# ──────────────────────────────────────────────────────────────

if __name__ == '__main__':
    texto_prueba = """
    Contacto: juan.perez@gmail.com y soporte@empresa.com.co
    Celular: 3001234567 o +57 310 456 7890
    Fijo: (601) 234-5678
    Nacimiento: 15/03/1995  —  Vence: 2026-12-31
    Sitio web: https://www.ejemplo.com/pagina?id=42#seccion
    Repositorio: http://github.com/usuario/proyecto
    Placa carro: ABC-123   Moto: XYZ-45K
    Cédula: 1098765432   ID corto: 123456
    """
    resultados = buscar_patrones(texto_prueba)
    print(reporte(resultados))