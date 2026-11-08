"""Esquemas de maniobras sobre el corazón de corazon.py (OAI ~30°): dos paneles por ficha.
Uso: python3 esquemas.py <carpeta de salida> [claves]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from corazon import heart

OUT = sys.argv[1]
E = lambda s: s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
BLUE, ORANGE, RED, PURPLE, GREEN = '#1f5fbf', '#ef6c00', '#c62828', '#6a3fb5', '#2e7d32'

# Puntos de referencia (coordenadas del panel)
NODO, HIS = (268, 262), (293, 308)
SEPT = (313, 285)                  # vía septal (posteroseptal)
LAT = (527, 284)                   # vía lateral izquierda
APEX, BASE_VD, BASE_VI = (165, 590), (232, 335), (495, 330)
HRA, CSOS, CSD, ADLAT = (125, 120), (240, 270), (500, 262), (78, 205)
A_BOX = (388, 100)


def smooth(pts):
    """Curva suave (Catmull-Rom) por los puntos."""
    d = f'M{pts[0][0]},{pts[0][1]}'
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f' C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]},{p2[1]}'
    return d


def wavy(p0, p1, p2, p3, amp=5, waves=6, off=0, n=90):
    """Trayecto tortuoso (vía lenta): bezier con ondulación perpendicular. off desplaza en paralelo."""
    import math
    pts = []
    for i in range(n + 1):
        u = i / n
        x = (1-u)**3*p0[0] + 3*(1-u)**2*u*p1[0] + 3*(1-u)*u**2*p2[0] + u**3*p3[0]
        y = (1-u)**3*p0[1] + 3*(1-u)**2*u*p1[1] + 3*(1-u)*u**2*p2[1] + u**3*p3[1]
        dx = -3*(1-u)**2*p0[0] + 3*(1-u)**2*p1[0] - 6*(1-u)*u*p1[0] + 6*(1-u)*u*p2[0] - 3*u**2*p2[0] + 3*u**2*p3[0]
        dy = -3*(1-u)**2*p0[1] + 3*(1-u)**2*p1[1] - 6*(1-u)*u*p1[1] + 6*(1-u)*u*p2[1] - 3*u**2*p2[1] + 3*u**2*p3[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        w = amp * math.sin(2 * math.pi * waves * u) * math.sin(math.pi * u) ** 0.5 + off
        pts.append((x + nx * w, y + ny * w))
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)


def circ(*pts):        # circuito de la taquicardia (azul punteado)
    return f'<path d="{smooth(pts)}" stroke="{BLUE}" stroke-width="3" fill="none" marker-end="url(#ab)" stroke-dasharray="6 4"/>'


def front(*pts, w=3.8):  # frente estimulado (naranja)
    return f'<path d="{smooth(pts)}" stroke="{ORANGE}" stroke-width="{w}" fill="none" marker-end="url(#ao)"/>'


def faint(*pts):         # conducción pasiva o espectadora (gris)
    return f'<path d="{smooth(pts)}" stroke="#78909c" stroke-width="2.6" fill="none" marker-end="url(#ag)" stroke-dasharray="3 4"/>'


def spark(p, label=None, dx=-45, dy=35):
    s = (f'<g transform="translate({p[0]},{p[1]})"><circle r="10" fill="{ORANGE}" stroke="#fff" stroke-width="2.5"/>'
         f'<path d="M1,-6 L-3,1 L1,1 L-1,7" stroke="#fff" stroke-width="2" fill="none" stroke-linejoin="round"/></g>')
    if label:
        s += f'<text x="{p[0] + dx}" y="{p[1] + dy}" font-size="12.5" font-weight="700" fill="{ORANGE}">{label}</text>'
    return s


def focus(p, label='foco'):
    x, y = p
    return (f'<g transform="translate({x},{y})"><path d="M0,-13 L4,-4 L13,-4 L6,2 L9,12 L0,6 L-9,12 L-6,2 L-13,-4 L-4,-4 Z" fill="#fdd835" stroke="#c62828" stroke-width="1.8"/></g>'
            f'<text x="{x + 16}" y="{y + 4}" font-size="11" font-weight="700" fill="#c62828">{label}</text>')


def xmark(p, label=None, dx=-22, dy=42):
    s = (f'<g transform="translate({p[0]},{p[1]})"><circle r="12" fill="#fff" stroke="{RED}" stroke-width="2.5"/>'
         f'<path d="M-7,-7 L7,7 M7,-7 L-7,7" stroke="{RED}" stroke-width="3"/></g>')
    if label:
        s += f'<text x="{p[0] + dx}" y="{p[1] + dy}" font-size="10.5" text-anchor="end" fill="{RED}">{label}</text>'
    return s


def via(p, label=None, h=30, lx=14, ly=-14):
    s = f'<rect x="{p[0] - 7}" y="{p[1] - h / 2}" width="14" height="{h}" rx="4" fill="#7e57c2" stroke="#4527a0" stroke-width="1.5"/>'
    if label:
        s += f'<text x="{p[0] + lx}" y="{p[1] + ly}" font-size="10.5" fill="#4527a0">{label}</text>'
    return s


def note(x, y, txt, color=ORANGE, anchor='start'):
    return ''.join(f'<text x="{x}" y="{y + 14 * i}" font-size="10.5" text-anchor="{anchor}" fill="{color}">{l}</text>'
                   for i, l in enumerate(E(txt).split('|')))


def box(t1, t2, ok=True, p=A_BOX):
    f, s, c = ('#e8f5e9', GREEN, '#1b5e20') if ok is True else ('#fff3e0', '#e65100', '#bf360c') if ok == 'warn' else ('#eceff1', '#546e7a', '#37474f')
    return (f'<g transform="translate({p[0]},{p[1]})"><rect x="0" y="-18" width="180" height="44" rx="8" fill="{f}" stroke="{s}" stroke-width="1.5"/>'
            f'<text x="90" y="0" font-size="13" font-weight="700" text-anchor="middle" fill="{c}">{E(t1)}</text>'
            f'<text x="90" y="17" font-size="11.5" text-anchor="middle" fill="{c}">{E(t2)}</text></g>')


DEFS = '''<defs>
<marker id="ab" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4.5" markerHeight="4.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1f5fbf"/></marker>
<marker id="ao" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4.5" markerHeight="4.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#ef6c00"/></marker>
<marker id="ag" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4.5" markerHeight="4.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#78909c"/></marker>
<radialGradient id="gat" cx="45%" cy="35%" r="75%"><stop offset="0" stop-color="#f7d4cb"/><stop offset=".6" stop-color="#e6a091"/><stop offset="1" stop-color="#c97a6b"/></radialGradient>
<radialGradient id="gvd" cx="40%" cy="38%" r="80%"><stop offset="0" stop-color="#f0b6a8"/><stop offset=".65" stop-color="#d27c6c"/><stop offset="1" stop-color="#a9554a"/></radialGradient>
<radialGradient id="gvi" cx="45%" cy="40%" r="80%"><stop offset="0" stop-color="#eaa696"/><stop offset=".65" stop-color="#c86a59"/><stop offset="1" stop-color="#9a4337"/></radialGradient>
<radialGradient id="gnode" cx="40%" cy="40%" r="70%"><stop offset="0" stop-color="#fff2b0"/><stop offset="1" stop-color="#e3b11c"/></radialGradient>
<linearGradient id="gcs" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#f7d354"/><stop offset="1" stop-color="#e2a915"/></linearGradient>
<clipPath id="cv"><path d="M96,300 C84,380 104,474 168,550 C206,594 246,616 278,624 L284,300 Z"/><path d="M302,300 C314,420 314,530 304,628 C385,632 464,588 508,508 C546,440 554,350 530,302 Z"/></clipPath>
<filter id="sh" x="-10%" y="-10%" width="120%" height="120%"><feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#5d1f16" flood-opacity=".25"/></filter>
</defs>'''


def panel(x, title, body, cap, rot=('nodo', 'his'), y=70):
    return (f'<g transform="translate({x},{y})"><text x="300" y="0" font-size="18" font-weight="700" text-anchor="middle" fill="#0a58ca">{E(title)}</text>'
            f'<g filter="url(#sh)">{heart(tuple(r for r in rot if r != "sin_nodo"), "sin_nodo" not in rot)}</g>{body}'
            + ''.join(f'<text x="300" y="{690 + 20 * i}" font-size="14" text-anchor="middle" fill="#333">{l}</text>' for i, l in enumerate(E(cap).split('|')))
            + '</g>')


def figure(*args):
    *ps, legend = args
    W = 600 * len(ps)
    leg = ''.join(f'<text x="{x}" y="24" fill="{c}">{t}</text>' for x, c, t in legend)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 800" width="{W}" height="800" font-family="Helvetica,Arial,sans-serif">'
            '<style>text{paint-order:stroke;stroke:#fff;stroke-width:3.5px;stroke-linejoin:round}</style>'
            f'{DEFS}<rect width="{W}" height="800" fill="#fff"/><g font-size="12" fill="#555"><text x="20" y="24">OAI ~30°</text>{leg}</g>'
            + ''.join(panel(600 * i, *p) for i, p in enumerate(ps))
            + ''.join(f'<line x1="{600 * i}" y1="50" x2="{600 * i}" y2="790" stroke="#e0e0e0"/>' for i in range(1, len(ps)))
            + '</svg>')


def grid_figure(rows, legend, row_titles=()):
    """Varias filas de paneles (cada fila, una secuencia que se lee de izquierda a derecha)."""
    n = max(len(r) for r in rows)
    W, H = 600 * n, 830 * len(rows)
    leg = ''.join(f'<text x="{x}" y="24" fill="{c}">{t}</text>' for x, c, t in legend)
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Helvetica,Arial,sans-serif">'
         '<style>text{paint-order:stroke;stroke:#fff;stroke-width:3.5px;stroke-linejoin:round}</style>'
         f'{DEFS}<rect width="{W}" height="{H}" fill="#fff"/><g font-size="12" fill="#555"><text x="20" y="24">OAI ~30°</text>{leg}</g>')
    for i, r in enumerate(rows):
        y0 = 830 * i
        if i:
            s += f'<line x1="20" y1="{y0 + 5}" x2="{W - 20}" y2="{y0 + 5}" stroke="#bdbdbd" stroke-width="2"/>'
        for j, p in enumerate(r):
            s += panel(600 * j, *p, y=y0 + 85)
            if j:
                s += (f'<line x1="{600 * j}" y1="{y0 + 60}" x2="{600 * j}" y2="{y0 + 820}" stroke="#e0e0e0"/>'
                      f'<path d="M{600 * j - 16},{y0 + 400} l26,14 l-26,14 z" fill="#90a4ae"/>')
    return s + '</svg>'


L_TSV = (120, BLUE, '- - circuito de la taquicardia')
L_EST = (340, ORANGE, '— frente estimulado')
L_PAS = (500, '#78909c', '··· conducción pasiva')
L_CS = (690, '#b8860b', '— sistema de conducción')
LEG = [L_TSV, L_EST, L_CS]

# circuitos típicos
TRAV_S = circ((262, 245), (258, 280), (286, 316)) + circ((306, 350), (313, 320), (313, 284)) + circ((312, 262), (296, 236), (272, 248))
TRNAV = circ((246, 262), (238, 236), (264, 228)) + circ((278, 232), (294, 248), (278, 268))
TRAV_L = (circ((262, 245), (270, 285), (292, 316)) + circ((330, 360), (440, 360), (515, 320)) + circ((527, 296), (527, 276))
          + circ((515, 250), (420, 235), (300, 236), (276, 248)))

F = {}

F['basal'] = (
    ('A. VA ≤ 70 ms (TRNAV típica)', TRNAV + front((268, 262), (240, 200), (190, 140), w=3) + front((285, 285), (292, 320), (300, 420), w=3)
     + note(120, 120, 'A y V salen juntos|del nodo', BLUE) + box('VA septal ≤ 70 ms', 'excluye la TRAV'),
     'A y V se activan casi a la vez desde el circuito:|el impulso no necesita recorrer el ventrículo.'),
    ('B. Activación en serie (TRAV por vía lateral izq.)', TRAV_L + via(LAT, 'vía lateral', lx=-70, ly=-22)
     + note(440, 210, 'A más precoz|en el SC distal', BLUE) + box('Activación en serie', 'VA > 70 ms'),
     'El impulso recorre el VI y sube por la vía: V y A se activan|en serie (VA > 70); la A más precoz está en el SC distal.'), LEG)

F['pre'] = (
    ('A. Salto del AH (doble vía nodal)', spark(HRA, 'S2 auricular (AD alta)', -60, -20) + front((135, 132), (175, 190), (200, 236))
     + '<path d="M206,240 C228,214 256,226 266,250" stroke="#2e7d32" stroke-width="3" fill="none"/>'
     + f'<path d="{wavy((204, 248), (110, 262), (200, 286), (262, 270), 4, 6)}" stroke="#7f1d1d" stroke-width="6" fill="none" stroke-linecap="round"/>'
     + f'<path d="{wavy((204, 248), (110, 262), (200, 286), (262, 270), 4, 6)}" stroke="{ORANGE}" stroke-width="3" fill="none" stroke-linecap="round"/>'
     + note(96, 250, 'vía lenta', '#7f1d1d') + note(292, 262, 'nodo AV', '#6d4c41')
     + xmark((236, 226), 'vía rápida refractaria', 150, -16) + front((276, 278), (286, 292), (291, 310))
     + note(80, 360, 'baja por la vía lenta:|AH salta ≥ 50 ms', ORANGE) + box('Salto del AH', 'doble fisiología nodal'),
     'El S2 encuentra la vía rápida refractaria y baja por la lenta:|el AH salta y puede aparecer el eco.', ('his',)),
    ('B. Conducción VA por la vía', spark(APEX, 'estimulación del VD') + via(LAT, 'vía lateral', lx=-70, ly=-22)
     + front((180, 575), (330, 470), (470, 380), (525, 300)) + front((527, 270), (480, 210), (420, 180))
     + faint((175, 560), (260, 420), (290, 320), (270, 262)) + box('A excéntrica', 'no decremental: vía', True),
     'Estimulando el ventrículo la A más precoz sale por la vía|(SC distal) y no se alarga con la frecuencia.'), [L_EST, L_PAS, L_CS])

F['ado'] = (
    ('A. TRNAV: termina', TRNAV
     + '<ellipse cx="150" cy="185" rx="70" ry="55" fill="#64b5f6" opacity="0.3"/><ellipse cx="380" cy="200" rx="70" ry="55" fill="#64b5f6" opacity="0.3"/>'
     + f'<path d="{smooth([(252, 238), (215, 205), (180, 192)])}" stroke="{BLUE}" stroke-width="4" fill="none" marker-end="url(#ab)"/>'
     + f'<path d="{smooth([(288, 236), (330, 215), (375, 205)])}" stroke="{BLUE}" stroke-width="4" fill="none" marker-end="url(#ab)"/>'
     + note(70, 145, '1. último latido: el circuito|activa la A (A final)', BLUE)
     + xmark((283, 286), None) + note(318, 330, '2. bloqueo anterógrado|en el nodo: no baja al V', RED)
     + box('Termina', 'con una A (bloqueo AV)', True),
     'El nodo es parte del circuito: la adenosina lo bloquea|y la taquicardia termina (excluye la TA si termina en A).'),
    ('B. TRAV (vía lateral izq.): termina', TRAV_L + via(LAT, 'vía lateral', lx=-70, ly=-22)
     + '<ellipse cx="150" cy="185" rx="70" ry="55" fill="#64b5f6" opacity="0.3"/><ellipse cx="380" cy="200" rx="70" ry="55" fill="#64b5f6" opacity="0.3"/>'
     + f'<path d="{smooth([(527, 262), (470, 205), (400, 190)])}" stroke="{BLUE}" stroke-width="4" fill="none" marker-end="url(#ab)"/>'
     + f'<path d="{smooth([(360, 185), (270, 170), (185, 185)])}" stroke="{BLUE}" stroke-width="4" fill="none" marker-end="url(#ab)"/>'
     + note(70, 145, '1. último latido: sube por la vía|y activa la A (A final)', BLUE)
     + xmark((283, 286), None) + note(140, 330, '2. bloqueo anterógrado|en el nodo: no baja al V', RED, 'start')
     + box('Termina', 'con una A (bloqueo AV)', True),
     'El nodo es el brazo anterógrado del circuito: la A llega|por la vía, el nodo bloqueado no la conduce y termina.'),
    ('C. TA: sigue con bloqueo AV', focus((140, 150), 'foco auricular') + circ((150, 165), (200, 210), (250, 250)) + xmark(NODO) + note(320, 232, 'bloqueo AV', RED)
     + note(330, 380, 'el V no participa', '#546e7a') + box('La TA sigue', 'con bloqueo AV', 'warn'),
     'El nodo no forma parte del mecanismo:|el foco auricular sigue disparando con bloqueo AV.'), LEG)

def ladder(x, y, after, tag, ok):
    """Mini diagrama en escalera: 3 V estimulados que arrastran la A y lo que pasa al cortar."""
    c = GREEN if ok else '#e65100'
    s = (f'<g transform="translate({x},{y})"><rect x="-38" y="-30" width="226" height="98" rx="8" fill="#fff" stroke="#bdbdbd"/>'
         '<text x="-28" y="4" font-size="12" font-weight="700" fill="#6d4c41">A</text><text x="-28" y="44" font-size="12" font-weight="700" fill="#6d4c41">V</text>'
         '<line x1="-12" y1="0" x2="180" y2="0" stroke="#bdbdbd"/><line x1="-12" y1="40" x2="180" y2="40" stroke="#bdbdbd"/>')
    for i in range(3):
        vx = 4 + 30 * i
        s += (f'<line x1="{vx}" y1="40" x2="{vx + 10}" y2="0" stroke="{ORANGE}" stroke-width="2.4"/>'
              f'<text x="{vx}" y="56" font-size="10" text-anchor="middle" fill="{ORANGE}" font-weight="700">S</text>')
    s += '<line x1="84" y1="-18" x2="84" y2="58" stroke="#9e9e9e" stroke-dasharray="3 3"/><text x="84" y="-20" font-size="9.5" text-anchor="middle" fill="#757575">corte</text>'
    for kind, ax, vx in after:
        if kind == 'AV':
            s += f'<line x1="{ax}" y1="0" x2="{vx}" y2="40" stroke="{BLUE}" stroke-width="2.4"/>'
        else:
            s += (f'<g transform="translate({ax},0)"><path d="M0,-7 L2,-2 L7,-2 L3,1 L5,6 L0,3 L-5,6 L-3,1 L-7,-2 L-2,-2 Z" fill="#fdd835" stroke="#c62828"/></g>'
                  f'<line x1="{ax}" y1="0" x2="{vx}" y2="40" stroke="{BLUE}" stroke-width="2.4"/>')
    s += f'<text x="140" y="-12" font-size="13" font-weight="700" text-anchor="middle" fill="{c}">{E(tag)}</text></g>'
    return s


F['vop'] = {'grid': ([[
    ('A1. TRNAV o TRAV: durante la estimulación', TRNAV + spark(APEX, 'sobreestimulación del VD', -60, 35)
     + front((175, 575), (250, 430), (288, 320), (268, 270), (220, 190))
     + note(40, 120, 'estimulo el VD más rápido que la TSV:|cada V sube por el circuito y arrastra una A', ORANGE)
     + ladder(395, 590, [], '', True)
     + box('Las A siguen al V', 'se aceleran a la LC estimulada', False),
     'Cada estímulo ventricular entra al circuito y activa la A:|la taquicardia queda encarrilada.'),
    ('A2. TRNAV o TRAV: al cortar', TRNAV
     + '<ellipse cx="150" cy="185" rx="70" ry="55" fill="#64b5f6" opacity="0.3"/>'
     + note(40, 120, 'la última A arrastrada|queda dentro del circuito', BLUE)
     + f'<path d="{smooth([(290, 290), (304, 360), (330, 440)])}" stroke="{BLUE}" stroke-width="4" fill="none" marker-end="url(#ab)"/>'
     + note(338, 400, 'el circuito sigue girando|y baja: sale un V', BLUE)
     + ladder(395, 590, [('AV', 70, 112)], 'A-V', True)
     + box('A-V', 'excluye la TA'),
     'La última A vuelve a bajar por el mismo circuito|y sale un V: respuesta A-V.')],
    [('B1. TA: durante la estimulación', focus((140, 150), 'foco') + spark(APEX, 'sobreestimulación del VD', -60, 35)
     + front((175, 575), (250, 430), (288, 320), (268, 270), (220, 190))
     + note(40, 105, 'cada V sube por el nodo|y arrastra una A', ORANGE)
     + ladder(395, 590, [], '', True)
     + box('Las A siguen al V', 'se aceleran a la LC estimulada', False),
     'Las A se activan desde el V a través del nodo;|el foco queda reseteado por esas A.'),
    ('B2. TA: al cortar', focus((140, 150), 'foco')
     + note(40, 105, 'la última A arrastrada no tiene|circuito: no vuelve a bajar', '#546e7a')
     + circ((150, 165), (200, 215), (250, 250))
     + note(40, 222, 'el foco dispara|otra A', '#c62828')
     + f'<path d="{smooth([(290, 290), (304, 360), (330, 440)])}" stroke="{BLUE}" stroke-width="4" fill="none" marker-end="url(#ab)"/>'
     + note(338, 400, 'recién esa A|baja al V', BLUE)
     + ladder(395, 590, [('AAV', 108, 140)], 'A-A-V', False)
     + box('A-A-V', 'taquicardia auricular', 'warn'),
     'Después de la última A arrastrada el foco dispara|otra A antes del V: respuesta A-A-V.')]], LEG)}

def intbar(x, y, rows, ok, tag, extra_label=''):
    """Barras de intervalos, cada una de un solo color con su largo total.
    rows = [(rótulo, color, base, extra)]: largo = base + extra.
    Con dos filas marca la diferencia entre las dos con líneas punteadas y un corchete."""
    c = GREEN if ok else '#e65100'
    s = f'<g transform="translate({x},{y})"><rect x="-38" y="-30" width="226" height="98" rx="8" fill="#fff" stroke="#bdbdbd"/>'
    ends = []
    for i, (lab, col, base, extra) in enumerate(rows):
        yy = -6 + 34 * i
        L = base + extra
        ends.append(22 + L)
        s += (f'<text x="-28" y="{yy + 10}" font-size="10" font-weight="700" fill="{col}">{E(lab)}</text>'
              f'<rect x="22" y="{yy}" width="{L}" height="12" rx="3" fill="{col}" opacity=".85"/>')
    if len(ends) == 2 and abs(ends[0] - ends[1]) > 3:
        a, b = sorted(ends)
        s += (f'<line x1="{ends[0]}" y1="-8" x2="{ends[0]}" y2="44" stroke="#616161" stroke-dasharray="3 3"/>'
              f'<path d="M{a},48 v4 H{b} v-4" stroke="#616161" fill="none"/>'
              f'<text x="{min((a + b) / 2, 105)}" y="64" font-size="10" text-anchor="middle" fill="#424242">{E(extra_label)}</text>')
    if tag:
        s += f'<text x="94" y="-14" font-size="12.5" font-weight="700" text-anchor="middle" fill="{c}">{E(tag)}</text>'
    return s + '</g>'


def solid(pts, color=BLUE, mk='ab'):
    return f'<path d="{smooth(pts)}" stroke="{color}" stroke-width="4" fill="none" marker-end="url(#{mk})"/>'


def ppibar(x, y, extra, ok, tag):
    return intbar(x, y, [('LC', BLUE, 100, 0), ('PPI', ORANGE, 100, extra)], ok, tag, 'PPI − LC: ida + vuelta')


LOOP_TRAV = (f'<path d="{smooth([(250, 348), (296, 352), (318, 318), (316, 262), (292, 236), (262, 244), (270, 300), (262, 336)])}" '
             f'stroke="{BLUE}" stroke-width="4" fill="none" marker-end="url(#ab)"/>')

F['ppi'] = {'grid': ([[
    ('A1. TRAV: durante el encarrilamiento', TRAV_S + via(SEPT, 'vía septal', 14, -22) + spark(APEX, 'estímulo en el VD', -60, 35)
     + front((180, 575), (250, 470), (292, 395), (304, 360))
     + note(40, 120, 'el V es parte del circuito: el frente|llega por el miocardio y entra al circuito', ORANGE)
     + box('Encarrilada', 'la TSV sigue a la LC estimulada', False),
     'Estimulo el VD algo más rápido que la TSV:|el frente entra al circuito por el ventrículo.'),
    ('A2. TRAV: al cortar (retorno)', TRAV_S + via(SEPT, 'vía septal', 14, -22) + spark(APEX, None)
     + faint((180, 575), (250, 470), (292, 395), (300, 362))
     + LOOP_TRAV
     + f'<path d="{smooth([(262, 345), (240, 420), (210, 500), (186, 566)])}" stroke="{ORANGE}" stroke-width="4" fill="none" marker-end="url(#ao)"/>'
     + note(40, 120, 'el retorno es una vuelta al circuito|(V → vía → A → nodo → V) más una ida|y vuelta corta por el miocardio del VD', BLUE)
     + ppibar(395, 590, 15, True, 'PPI − LC < 115')
     + box('PPI − LC < 115', 'el V está en el circuito'),
     'El primer latido de retorno tarda lo mismo que una vuelta|del circuito: PPI ≈ LC.')],
    [('B1. TRNAV: durante el encarrilamiento', TRNAV + spark(APEX, 'estímulo en el VD', -60, 35)
     + front((175, 575), (255, 430), (288, 320), (280, 275))
     + note(40, 120, 'el V está fuera del circuito:|el frente sube por el His hasta el nodo', ORANGE)
     + box('Encarrilada', 'la TSV sigue a la LC estimulada', False),
     'El estímulo tiene que recorrer el V y el His|para llegar al circuito en el nodo.'),
    ('B2. TRNAV: al cortar (retorno)', TRNAV + spark(APEX, None)
     + faint((175, 575), (255, 430), (285, 320), (276, 280))
     + note(40, 120, '1. ida: VD → His → nodo', '#546e7a')
     + note(40, 150, '2. una vuelta al circuito', BLUE)
     + f'<path d="{smooth([(296, 300), (300, 420), (250, 520), (192, 572)])}" stroke="{ORANGE}" stroke-width="4" fill="none" marker-end="url(#ao)"/>'
     + note(300, 470, '3. vuelta: nodo → His → VD', ORANGE)
     + ppibar(395, 590, 60, False, 'PPI − LC > 115')
     + box('PPI − LC > 115', 'el V está lejos del circuito', False),
     'El retorno suma la ida y la vuelta entre el VD y el nodo|a la vuelta del circuito: PPI mucho mayor que la LC.')]], LEG)}

F['sava'] = {'grid': ([[
    ('A1. TRAV: en taquicardia (VA)', TRAV_S + via(SEPT, 'vía septal', 14, -22)
     + solid([(306, 352), (314, 300), (318, 240), (340, 190)])
     + note(40, 120, 'VA: el V septal sube por la vía|y activa la A', BLUE)
     + intbar(395, 590, [('VA', BLUE, 70, 0)], True, '')
     + box('VA de la TSV', 'V → vía → A', False),
     'En la TSV la A se activa desde el V a través de la vía.'),
    ('A2. TRAV: estimulando el VD (SA)', TRAV_S + via(SEPT, 'vía septal', 14, -22) + spark(APEX, 'estímulo en el VD', -60, 35)
     + front((180, 575), (250, 470), (296, 390), (312, 330), (316, 260), (338, 190))
     + note(40, 120, 'SA: ápex → miocardio → vía → A|es el mismo camino que en la TSV|más el trayecto ápex → base', ORANGE)
     + intbar(395, 590, [('VA', BLUE, 70, 0), ('SA', ORANGE, 70, 25)], True, 'SA − VA < 85', 'SA − VA: ápex → base')
     + box('SA − VA < 85', 'vía en el circuito'),
     'Estimulando el V la A llega por la misma vía:|el SA es apenas mayor que el VA.')],
    [('B1. TRNAV: en taquicardia (VA)', TRNAV
     + solid([(262, 252), (230, 210), (190, 175)]) + solid([(290, 290), (298, 350), (310, 420)])
     + note(40, 120, 'VA: A y V salen juntos del nodo,|en paralelo', BLUE)
     + intbar(395, 590, [('VA', BLUE, 20, 0)], True, '')
     + box('VA de la TSV', 'muy corto (≤ 70 ms)', False),
     'En la TSV la A y el V se activan casi a la vez|desde el circuito en el nodo.'),
    ('B2. TRNAV: estimulando el VD (SA)', TRNAV + spark(APEX, 'estímulo en el VD', -60, 35)
     + front((175, 575), (255, 430), (290, 320), (270, 270), (230, 200))
     + note(40, 120, 'SA: ápex → His → nodo → A|ahora la A se activa en serie', ORANGE)
     + intbar(395, 590, [('VA', BLUE, 20, 0), ('SA', ORANGE, 20, 120)], False, 'SA − VA > 85', 'SA − VA: ápex → His → nodo')
     + box('SA − VA > 85', 'TRNAV', False),
     'Estimulando el V la A espera el ascenso por el His y el nodo:|el SA es mucho mayor que el VA.')]], LEG)}

F['dha'] = {'grid': ([[
    ('A1. TRAV: en taquicardia (HA)', TRAV_S + via(SEPT, 'vía septal', 14, -22)
     + solid([(290, 300), (300, 345)]) + solid([(310, 352), (316, 300), (320, 240), (340, 190)])
     + note(40, 120, 'HA: His → V → vía → A|His y A se activan en serie', BLUE)
     + intbar(395, 590, [('HA TSV', BLUE, 110, 0)], True, '')
     + box('HA de la TSV', 'largo (en serie)', False),
     'En la TSV el impulso baja por el His, recorre el V|y sube por la vía: el HA incluye todo ese trayecto.'),
    ('A2. TRAV: estimulando el VD (HA)', TRAV_S + via(SEPT, 'vía septal', 14, -22) + spark(APEX, 'estímulo en el VD', -60, 35)
     + front((180, 575), (250, 470), (296, 390), (312, 330), (316, 260), (338, 190))
     + front((182, 560), (240, 450), (275, 370), (288, 318))
     + note(40, 120, 'desde el V el frente llega al His|y a la vía a la vez: en paralelo', ORANGE)
     + intbar(395, 590, [('HA TSV', BLUE, 110, 0), ('HA est.', ORANGE, 45, 0)], True, 'ΔHA < 0', 'ΔHA: se acorta')
     + box('ΔHA < 0', 'HA estimulado más corto'),
     'Estimulando el V, His y A se activan en paralelo:|el HA se acorta (ΔHA negativo).')],
    [('B1. TRNAV: en taquicardia (HA)', TRNAV
     + solid([(262, 252), (230, 210), (190, 175)]) + solid([(290, 290), (298, 330)])
     + note(40, 120, 'His y A salen juntos del nodo:|en paralelo', BLUE)
     + intbar(395, 590, [('HA TSV', BLUE, 30, 0)], True, '')
     + box('HA de la TSV', 'corto (en paralelo)', False),
     'En la TSV el His y la A se activan casi a la vez|desde el circuito en el nodo.'),
    ('B2. TRNAV: estimulando el VD (HA)', TRNAV + spark(APEX, 'estímulo en el VD', -60, 35)
     + front((175, 575), (255, 430), (290, 320), (270, 268), (230, 200))
     + note(40, 120, 'estimulando: primero el His,|después el nodo y la A (en serie)', ORANGE)
     + intbar(395, 590, [('HA TSV', BLUE, 30, 0), ('HA est.', ORANGE, 110, 0)], False, 'ΔHA > 0', 'ΔHA: se alarga')
     + box('ΔHA > 0', 'HA estimulado más largo', False),
     'Estimulando el V, el His y la A se activan en serie:|el HA se alarga (ΔHA positivo).')]], LEG)}

def hisinset(x, y, down, ok, tag):
    """Mini catéter de His: orden de activación proximal/distal."""
    c = GREEN if ok else '#e65100' if ok is False else '#37474f'
    col = BLUE if ok is None else ORANGE
    s = (f'<g transform="translate({x},{y})"><rect x="-38" y="-30" width="226" height="98" rx="8" fill="#fff" stroke="#bdbdbd"/>'
         '<line x1="10" y1="-4" x2="10" y2="56" stroke="#9e9e9e" stroke-width="5" stroke-linecap="round"/>'
         '<rect x="4" y="2" width="12" height="7" fill="#424242"/><rect x="4" y="40" width="12" height="7" fill="#424242"/>'
         '<text x="-28" y="9" font-size="10" font-weight="700" fill="#6d4c41">His p</text>'
         '<text x="-28" y="47" font-size="10" font-weight="700" fill="#6d4c41">His d</text>')
    if down:
        s += (f'<path d="M30,4 V42" stroke="{col}" stroke-width="3" marker-end="url(#{"ab" if ok is None else "ao"})"/>'
              f'<text x="44" y="20" font-size="10.5" fill="#424242">proximal → distal</text>'
              f'<text x="44" y="34" font-size="10.5" fill="#424242">(anterógrado)</text>')
    else:
        s += (f'<path d="M30,44 V6" stroke="{col}" stroke-width="3" marker-end="url(#ao)"/>'
              f'<text x="44" y="20" font-size="10.5" fill="#424242">distal → proximal</text>'
              f'<text x="44" y="34" font-size="10.5" fill="#424242">(retrógrado)</text>')
    if tag:
        s += f'<text x="94" y="-14" font-size="12.5" font-weight="700" text-anchor="middle" fill="{c}">{E(tag)}</text>'
    return s + '</g>'


F['hisorto'] = {'grid': ([[
    ('A1. TRAV: en taquicardia', TRAV_S + via(SEPT, 'vía septal', 14, -22)
     + solid([(272, 266), (286, 300), (294, 340)])
     + note(40, 120, 'el impulso baja del nodo al His:|el His se activa de arriba hacia abajo', BLUE)
     + hisinset(395, 590, True, None, '')
     + box('His en la TSV', 'anterógrado', False),
     'En la TSV el His se activa desde el nodo,|en sentido anterógrado (proximal → distal).'),
    ('A2. TRAV: estimulando el VD', TRAV_S + via(SEPT, 'vía septal', 14, -22) + spark(APEX, 'estímulo en el VD', -60, 35)
     + front((180, 575), (250, 470), (296, 390), (312, 330), (313, 255)) + front((300, 236), (276, 246), (284, 280), (292, 304))
     + note(40, 120, 'el frente sube por la vía, pasa por la A|y baja por el nodo: el His se activa|igual que en la TSV', ORANGE)
     + hisinset(395, 590, True, True, 'His ortodrómico')
     + box('His ortodrómico', 'la vía participa'),
     'El V está en el circuito: el estímulo recorre el circuito|y llega al His desde arriba, como en la TSV.')],
    [('B1. TRNAV: en taquicardia', TRNAV
     + solid([(276, 270), (288, 300), (296, 340)])
     + note(40, 120, 'el impulso sale del nodo hacia el His:|el His se activa de arriba hacia abajo', BLUE)
     + hisinset(395, 590, True, None, '')
     + box('His en la TSV', 'anterógrado', False),
     'En la TSV el His se activa desde el circuito en el nodo,|en sentido anterógrado (proximal → distal).'),
    ('B2. TRNAV: estimulando el VD', TRNAV + spark(APEX, 'estímulo en el VD', -60, 35)
     + front((175, 575), (255, 430), (290, 330), (286, 280))
     + note(40, 120, 'el frente sube por la rama y el His|hacia el nodo: el His se activa|de abajo hacia arriba', ORANGE)
     + hisinset(395, 590, False, False, 'His antidrómico')
     + box('His antidrómico', 'el V no está en el circuito', False),
     'El V está fuera del circuito: el frente llega al His desde abajo,|en sentido retrógrado (al revés que en la TSV).')]], LEG)}

F['diff'] = {'grid': ([[
    ('A1. TRAV: encarrilando desde la base', TRAV_S + via(SEPT, 'vía septal', 14, -22) + spark(BASE_VD, 'base del VD', -95, -18)
     + front((242, 345), (290, 348), (312, 310), (318, 245), (340, 190))
     + note(40, 120, 'la base está cerca de la vía:|el frente llega enseguida a la A', ORANGE)
     + intbar(395, 590, [('VA base', ORANGE, 55, 0)], True, '')
     + box('VA desde la base', 'corto', False),
     'Encarrilando desde la base el frente entra a la vía|casi sin recorrer ventrículo.'),
    ('A2. TRAV: encarrilando desde el ápex', TRAV_S + via(SEPT, 'vía septal', 14, -22) + spark(APEX, 'ápex del VD', -60, 35)
     + front((180, 575), (250, 470), (296, 390), (312, 330), (318, 255), (340, 190))
     + note(40, 120, 'desde el ápex el frente recorre el V|hasta la vía: tarda igual o más', '#ad1457')
     + intbar(395, 590, [('VA base', ORANGE, 55, 0), ('VA ápex', '#ad1457', 72, 0)], True, 'ΔVA ≤ 20', 'ΔVA = base − ápex')
     + box('ΔVA ≤ 20', 'vía (TRAV)'),
     'El VA desde la base es igual o más corto que desde el ápex:|ΔVA (base − ápex) ≤ 20 ms.')],
    [('B1. TRNAV: encarrilando desde la base', TRNAV + spark(BASE_VD, 'base del VD', -95, -18)
     + front((240, 348), (248, 420), (272, 452), (290, 380), (290, 320), (270, 268), (230, 200))
     + note(40, 120, 'desde la base el frente baja hasta|la red de Purkinje y recién sube|por el His al nodo', ORANGE)
     + intbar(395, 590, [('VA base', ORANGE, 120, 0)], True, '')
     + box('VA desde la base', 'largo', False),
     'La base tiene poca red de Purkinje: el frente tarda|en entrar al sistema de conducción y llegar al nodo.'),
    ('B2. TRNAV: encarrilando desde el ápex', TRNAV + spark(APEX, 'ápex del VD', -60, 35)
     + front((175, 575), (255, 430), (290, 320), (270, 268), (230, 200))
     + note(40, 120, 'desde el ápex el frente entra enseguida|a la rama derecha y sube por el His', '#ad1457')
     + intbar(395, 590, [('VA base', ORANGE, 120, 0), ('VA ápex', '#ad1457', 75, 0)], False, 'ΔVA > 20', 'ΔVA = base − ápex')
     + box('ΔVA > 20', 'nodo (TRNAV)', False),
     'El VA desde la base es más largo que desde el ápex:|ΔVA (base − ápex) > 20 ms.')]], LEG)}

F['vai'] = (
    ('A. Índice VA > +10 (vía)', via(SEPT, 'vía septal', 14, -22) + spark(BASE_VD, 'base', -40, -18) + spark(APEX, 'ápex')
     + front((242, 342), (295, 318), (313, 290), (313, 250), (330, 190)) + faint((178, 575), (260, 450), (300, 340))
     + box('VA ápex > VA base', 'conducción por la vía'),
     'En ritmo sinusal, desde la base el frente llega antes a la vía:|el VA desde el ápex es más largo.'),
    ('B. Índice VA < +10 (nodo)', spark(BASE_VD, 'base', -40, -18) + spark(APEX, 'ápex')
     + front((178, 575), (240, 470), (288, 320), (270, 262), (220, 200)) + faint((242, 345), (262, 380), (285, 330))
     + box('VA ápex ≤ VA base', 'conducción por el nodo', False),
     'Desde el ápex el frente entra a la red de Purkinje y sube|por el His: el VA es igual o más corto que desde la base.'), [L_EST, L_PAS, L_CS])

F['ehr'] = (
    ('A. TRAV por vía septal', TRAV_S + via(SEPT, 'vía posteroseptal', 14, -16) + spark(APEX, 'EV (ápex del VD)')
     + front((175, 575), (240, 470), (306, 352)) + front((313, 270), (330, 190), (382, 128)) + xmark(HIS, 'His refractario')
     + box('A adelantada', 'misma secuencia'),
     'La EV sube por el miocardio, entra por la vía|y adelanta la A: la vía forma parte del circuito.'),
    ('B. TRNAV', TRNAV + note(320, 232, 'circuito en el nodo', BLUE) + spark(APEX, 'EV (ápex del VD)')
     + front((178, 572), (240, 460), (290, 326)) + front((190, 584), (300, 500), (362, 350)) + note(372, 452, 'el anillo aísla:|no hay otra entrada')
     + xmark(HIS, 'His refractario') + box('A sin cambio', 'llega a su tiempo', False),
     'El His refractario bloquea el frente y no hay vía:|la EV no llega al nodo ni a la aurícula.'), LEG)

F['parahis'] = (
    ('A. Respuesta nodal', spark((300, 320), 'para-Hisiana', 10, 0) + front((296, 316), (288, 290), (270, 262), (220, 200))
     + faint((304, 330), (360, 430), (420, 470)) + note(330, 380, 'con captura del His: SA corto|sin captura: SA se alarga', ORANGE)
     + box('SA se alarga', 'al perder el His: nodo', False),
     'La conducción retrógrada depende del His: al perder|la captura del His, el SA se alarga (≥ el aumento del SH).'),
    ('B. Respuesta extranodal', via(SEPT, 'vía septal', 14, -22) + spark((300, 320), 'para-Hisiana', 10, 22)
     + front((305, 312), (313, 290), (313, 255), (330, 190)) + note(330, 150, 'SA igual con y|sin captura del His', ORANGE)
     + box('SA no cambia', 'al perder el His: vía'),
     'El miocardio septal llega a la vía igual con o sin el His:|el SA no cambia (vía septal).'), [L_EST, L_PAS, L_CS])

F['aop'] = (
    ('A. VA linking (TRNAV o TRAV)', TRNAV + spark(HRA, 'sobreestimulación auricular', -60, -20)
     + front((135, 132), (220, 210), (262, 250)) + front((285, 285), (292, 330), (290, 400)) + faint((262, 250), (230, 200), (180, 160))
     + note(330, 420, 'el retorno: A después|del V a VA fijo', ORANGE) + box('VA linking', 'VA de retorno fijo'),
     'El último A estimulado entra al circuito; la A de retorno|depende del V: el VA del retorno es el de la TSV.'),
    ('B. Sin VA linking (TA)', focus((150, 160), 'foco') + spark(CSOS, 'sobreestimulación auricular', -70, 50)
     + front((240, 270), (210, 230), (170, 180)) + circ((160, 175), (200, 215), (250, 250))
     + note(330, 420, 'la A de retorno sale del foco:|VA variable', BLUE) + box('VA variable', '> 14 ms entre sitios', 'warn'),
     'La A de retorno depende del foco, no del V:|el VA cambia según el sitio de estimulación.'), LEG)

MAHAIM = '<path d="M104,292 C120,360 142,440 172,505" stroke="#7e57c2" stroke-width="5" fill="none" stroke-linecap="round" opacity=".9"/>'
F['preex'] = (
    ('A. EA desde la pared libre del AD', MAHAIM + note(150, 330, 'vía atriofascicular', PURPLE) + spark(ADLAT, 'EA (AD lateral)', -60, -22)
     + front((82, 215), (100, 285), (128, 390), (168, 495)) + xmark(HIS, 'unión refractaria')
     + box('V adelantado', 'mismo QRS: Mahaim'),
     'El EA entra por la vía atriofascicular (AD lateral)|y adelanta el V aun con la unión refractaria.'),
    ('B. EA desde el septum', MAHAIM + spark(CSOS, 'EA (septum)', -140, 40)
     + front((240, 270), (262, 268), (282, 290)) + xmark(HIS, 'unión refractaria')
     + box('V sin cambio', 'el septum está lejos de la vía', False),
     'Desde el septum el EA choca con la unión refractaria|y no llega a la vía: el V no cambia.'), LEG)

F['eha'] = (
    ('A. TRNAV: modifica el His', TRNAV + spark(CSOS, 'EA (ostium del SC)', -110, 40) + front((236, 272), (246, 280), (262, 272))
     + xmark(HIS, 'His refractario') + note(330, 232, 'entra en la vía lenta', ORANGE) + box('His siguiente', 'se retrasa o adelanta'),
     'El EA entra en la vía lenta, que es parte del circuito:|retrasa, adelanta o termina el His siguiente.'),
    ('B. Taquicardia de la unión', focus((290, 296), 'foco') + spark(CSOS, 'EA (ostium del SC)', -110, 40)
     + front((236, 272), (250, 270), (262, 264)) + xmark(NODO) + note(320, 232, 'unión refractaria', RED)
     + box('His sin cambio', 'el foco está debajo', 'warn'),
     'El foco está en la unión, debajo de la aurícula:|el EA no lo alcanza y el His siguiente no cambia.'), LEG)

RR = circ((291, 310), (285, 400), (250, 480), (200, 515)) + circ((230, 560), (300, 600), (340, 520), (320, 400), (298, 318))
F['bbr'] = (
    ('A. Reentrada rama-rama', RR + note(120, 440, 'baja por la|rama derecha', BLUE) + note(350, 560, 'sube por la|rama izquierda', BLUE)
     + box('HV ≥ sinusal', 'el His precede a cada V'),
     'El circuito usa las dos ramas y el septum:|el His se activa antes de cada V (HV ≥ sinusal).'),
    ('B. TV miocárdica', focus((420, 480), 'circuito en el VI') + faint((410, 470), (340, 380), (296, 316))
     + box('His pasivo', 'el VV cambia antes que el HH', 'warn'),
     'El circuito está en el miocardio: el His se activa|en forma pasiva y no predice el VV.'), [L_TSV, L_PAS, L_CS])

def _nodo(x, y):
    return f'<path d="M{x-18},{y} C{x-13},{y-12} {x+7},{y-14} {x+16},{y-4} C{x+20},{y+4} {x+12},{y+12} {x},{y+11} C{x-10},{y+10} {x-20},{y+8} {x-18},{y} Z" fill="url(#gnode)" stroke="#9a7300" stroke-width="1.5"/>'
# nodo anterosuperior y posteroinferior en la AD, cada uno con su His, unidos al septum (cabestrillo de Mönckeberg)
TWIN = ('<path d="M246,186 C268,215 286,260 293,308" stroke="url(#gcs)" stroke-width="6" fill="none" stroke-linecap="round"/>'
        '<path d="M232,268 C255,282 278,292 293,308" stroke="url(#gcs)" stroke-width="6" fill="none" stroke-linecap="round"/>'
        + _nodo(238, 180) + _nodo(222, 264))
TWL = note(225, 152, 'nodo anterosuperior', '#6d4c41') + note(130, 300, 'nodo posteroinferior', '#6d4c41')
F['twin'] = (
    ('A. Dos nodos AV', TWIN + TWL + box('Dos His separados', 'cada uno con su QRS'),
     'En la heterotaxia o el canal AV malalineado hay dos nodos en la AD,|uno anterosuperior y otro posteroinferior, cada uno con su His.', ('sin_nodo',)),
    ('B. Taquicardia entre los dos nodos', TWIN + TWL + circ((246, 192), (270, 240), (288, 296)) + circ((282, 304), (256, 286), (230, 276))
     + circ((214, 256), (220, 220), (234, 194))
     + box('Reentrada', 'baja por uno, sube por el otro'),
     'El circuito baja por un sistema de conducción y sube|por el otro (taquicardia por nodos gemelos).', ('sin_nodo',)), [L_TSV, L_CS])

TVFP = circ((330, 420), (360, 470), (395, 515)) + circ((405, 530), (380, 470), (345, 430))
F['tvf'] = (
    ('A. TV fascicular posterior', TVFP + note(410, 470, 'P1 baja por|el falso tendón', BLUE) + note(310, 470, 'P2: sube por el|fascículo posterior', BLUE, 'end')
     + box('BRD + eje superior', 'P1 y P2 en el septum medio'), 'Reentrada entre el fascículo posterior y tejido de Purkinje|anómalo (P1): sensible al verapamilo.', ('nodo', 'his', 'fp')),
    ('B. TV fascicular septal superior', circ((300, 315), (318, 345), (330, 330)) + circ((322, 318), (308, 300)) + faint((300, 320), (288, 296))
     + box('QRS angosto', 'His retrógrado, HV corto', 'warn'), 'El circuito usa el fascículo septal superior cerca del His:|baja por los dos fascículos y da un QRS angosto.', ('nodo', 'his', 'fa', 'fp')), [L_TSV, L_PAS, L_CS])

F['tvfabl'] = (
    ('A. Ablación en P1 / P2', TVFP + focus((365, 470), 'sitio de ablación') + box('P1-P2 se alarga', 'y la TV termina'),
     'Con la TV inducible, se ablaciona en P1 (tercio apical) o|en el P2 más precoz; durante la RF el P1-P2 se alarga.', ('nodo', 'his', 'fp')),
    ('B. Línea anatómica', '<path d="M330,470 L420,500" stroke="#c62828" stroke-width="6" stroke-dasharray="2 6" stroke-linecap="round"/>'
     + note(330, 520, 'línea en el septum|medio-inferior', RED) + box('TV no inducible', 'línea de 1–2 cm'),
     'Si no se induce: línea perpendicular al fascículo|posterior en el septum medio-inferior.', ('nodo', 'his', 'fp')), [L_TSV, L_CS])

F['pm'] = (
    ('A. Músculo papilar posteromedial', '<ellipse cx="400" cy="540" rx="20" ry="34" fill="#b85a4b" stroke="#7b2f24"/>' + focus((400, 540), 'foco')
     + box('BRD + eje superior', 'QRS ancho, focal'), 'Foco en el músculo papilar posteromedial:|BRD con eje superior, no reentrante.'),
    ('B. Músculo papilar anterolateral', '<ellipse cx="470" cy="430" rx="18" ry="32" fill="#b85a4b" stroke="#7b2f24"/>' + focus((470, 430), 'foco')
     + box('BRD + eje inferior', 'QRS ancho, focal'), 'Foco en el músculo papilar anterolateral:|BRD con eje inferior.'), [L_CS])

F['ma'] = (
    ('A. Anillo mitral anterolateral', focus((520, 290), 'foco') + box('R de V1 a V6', 'S en V6, eje inferior'),
     'Foco en el anillo mitral anterolateral:|R en V1, concordancia positiva, DI negativo.'),
    ('B. Anillo mitral posterior', focus((420, 296), 'foco') + box('R de V1 a V6', 'eje superior'),
     'Foco en el anillo mitral posterior o posteroseptal:|R en V1, eje superior.'), [L_CS])

OBL = '<path d="M520,262 C510,280 495,296 478,310" stroke="#7e57c2" stroke-width="7" fill="none" stroke-linecap="round"/>'
F['obl'] = (
    ('A. Estimulación ventricular', OBL + note(500, 240, 'inserción auricular', PURPLE, 'end') + note(440, 330, 'inserción|ventricular', PURPLE, 'end')
     + spark(BASE_VI, 'VI', 10, 22) + front((488, 320), (480, 310)) + front((520, 258), (500, 220), (450, 180))
     + box('A más precoz', 'en la inserción auricular'),
     'La vía oblicua cruza el anillo en diagonal: la A más precoz|marca la inserción auricular, no la ventricular.'),
    ('B. Estimulación auricular', OBL + spark(CSD, 'SC distal', -20, -20) + front((505, 266), (512, 276)) + front((478, 314), (450, 380), (420, 420))
     + box('V más precoz', 'en la inserción ventricular'),
     'Con estimulación auricular el V más precoz marca la inserción|ventricular: invertir el frente ayuda a ubicarlas.'), LEG)

F['dfire'] = (
    ('A. Por la vía rápida: H1', spark(HRA, 'A sinusal', -40, -20) + front((140, 140), (220, 210), (258, 248))
     + '<path d="M240,252 C246,236 262,236 270,250" stroke="#2e7d32" stroke-width="3" fill="none"/>' + front((285, 285), (292, 320), (300, 400))
     + box('H1 – V1', 'AH corto'), 'La A conduce primero por la vía rápida:|primer His y primer V.'),
    ('B. Por la vía lenta: H2', spark(HRA, 'la misma A', -40, -20)
     + front((140, 140), (200, 200), (236, 262)) + '<path d="M240,268 C244,290 266,292 274,272" stroke="#b71c1c" stroke-width="3" fill="none"/>' + front((285, 285), (292, 320), (300, 400))
     + box('H2 – V2', 'H1–H2 fijo (400–500 ms)'), 'La misma A baja más tarde por la vía lenta y llega al His|cuando ya se recuperó: segundo His y segundo V.'), [L_EST, L_CS])

F['conc'] = (
    ('A. Encarrilamiento oculto', TRAV_S + via(SEPT, 'vía', 14, -22) + spark(BASE_VD, 'estímulo', -60, -18)
     + front((242, 342), (300, 330), (308, 340)) + note(330, 420, 'ortodrómico: sigue el circuito|antidrómico: choca dentro', ORANGE)
     + box('Fusión oculta', 'el QRS no cambia'),
     'El frente ortodrómico entra al circuito y lo acelera;|el antidrómico choca con el de la taquicardia.'),
    ('B. Encarrilamiento manifiesto (fusión)', TRAV_S + via(SEPT, 'vía', 14, -22) + spark(APEX, 'estímulo')
     + front((178, 575), (240, 470), (300, 380)) + note(320, 470, 'el antidrómico choca|en el miocardio', ORANGE)
     + box('QRS de fusión', 'el V está en el circuito'),
     'Si el choque ocurre en el miocardio, el QRS es intermedio|(fusión): prueba que el ventrículo está en el circuito.'), LEG)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for k in (sys.argv[2:] or list(F)):
        svg = grid_figure(*F[k]['grid']) if isinstance(F[k], dict) else figure(*F[k])
        open(os.path.join(OUT, k + '.svg'), 'w').write(svg)
        print(k)
