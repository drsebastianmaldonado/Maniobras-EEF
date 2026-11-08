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
     + front((236, 350), (205, 410), (185, 465), (174, 500))
     + front((176, 512), (210, 516), (240, 500), (270, 450), (285, 380), (291, 320), (272, 268), (230, 200))
     + note(40, 120, '1. desde la base el frente baja por el|miocardio hasta la punta del VD|2. entra a la RD por su parte distal|(banda moderadora) y sube por el His', ORANGE)
     + note(96, 548, 'entrada distal a la RD', ORANGE)
     + intbar(395, 590, [('VA base', ORANGE, 120, 0)], True, '')
     + box('VA desde la base', 'largo', False),
     'El frente entra a la RD por su parte distal y la recorre|entera hasta el His y el nodo: el VA desde la base se alarga.'),
    ('B2. TRNAV: encarrilando desde el ápex', TRNAV + spark(APEX, 'ápex del VD', -60, 35)
     + front((168, 578), (172, 520), (210, 516), (240, 500), (270, 450), (285, 380), (291, 320), (272, 268), (230, 200))
     + note(40, 120, 'el ápex está al lado de la RD distal:|el frente entra enseguida y sube por el His', '#ad1457')
     + intbar(395, 590, [('VA base', ORANGE, 120, 0), ('VA ápex', '#ad1457', 75, 0)], False, 'ΔVA > 20', 'ΔVA = base − ápex')
     + box('ΔVA > 20', 'nodo (TRNAV)', False),
     'El VA desde la base es más largo que desde el ápex:|ΔVA (base − ápex) > 20 ms.')]], LEG)}

F['vai'] = {'grid': ([[
    ('A1. Vía septal: estimulando la base', via(SEPT, 'vía septal', 14, -22) + spark(BASE_VD, 'base del VD', -95, -18)
     + front((242, 345), (290, 348), (312, 310), (316, 250), (338, 190))
     + note(40, 120, 'ritmo sinusal (sin taquicardia):|la base está al lado de la vía,|el frente llega enseguida a la A', ORANGE)
     + intbar(395, 590, [('VA base', ORANGE, 55, 0)], True, '')
     + box('VA desde la base', 'corto', False),
     'Estimulando la base el frente entra a la vía|casi sin recorrer ventrículo.'),
    ('A2. Vía septal: estimulando el ápex', via(SEPT, 'vía septal', 14, -22) + spark(APEX, 'ápex del VD', -60, 35)
     + front((180, 575), (250, 470), (296, 390), (312, 330), (316, 255), (338, 190))
     + note(40, 120, 'desde el ápex el frente recorre|el V hasta la vía: tarda más', '#ad1457')
     + intbar(395, 590, [('VA base', ORANGE, 55, 0), ('VA ápex', '#ad1457', 85, 0)], True, 'Índice VA > +10', 'índice = ápex − base')
     + box('Índice VA > +10', 'conducción por la vía'),
     'El VA desde el ápex es más largo que desde la base:|índice VA (ápex − base) > +10 ms.')],
    [('B1. Nodo: estimulando la base', spark(BASE_VD, 'base del VD', -95, -18)
     + front((236, 350), (205, 410), (185, 465), (174, 500))
     + front((176, 512), (210, 516), (240, 500), (270, 450), (285, 380), (291, 320), (272, 268), (230, 200))
     + note(40, 120, '1. el frente baja por el miocardio|hasta la punta del VD|2. entra a la RD por su parte distal|y sube por el His y el nodo', ORANGE)
     + note(96, 548, 'entrada distal a la RD', ORANGE)
     + intbar(395, 590, [('VA base', ORANGE, 120, 0)], True, '')
     + box('VA desde la base', 'largo', False),
     'Sin vía, la A solo se activa por el nodo: desde la base|el frente recorre toda la RD antes de subir.'),
    ('B2. Nodo: estimulando el ápex', spark(APEX, 'ápex del VD', -60, 35)
     + front((168, 578), (172, 520), (210, 516), (240, 500), (270, 450), (285, 380), (291, 320), (272, 268), (230, 200))
     + note(40, 120, 'el ápex está al lado de la RD distal:|el frente entra enseguida y sube por el His', '#ad1457')
     + intbar(395, 590, [('VA base', ORANGE, 120, 0), ('VA ápex', '#ad1457', 85, 0)], False, 'Índice VA ≤ +10', 'índice = ápex − base')
     + box('Índice VA ≤ +10', 'conducción por el nodo', False),
     'El VA desde el ápex es igual o más corto que desde la base:|índice VA (ápex − base) ≤ +10 ms.')]], [L_EST, L_CS])}

def tline(x, y, ev, shift, ok, tag):
    """Mini línea de tiempo A / His / V: ventana refractaria del His, EV y la A siguiente."""
    c = GREEN if ok else '#546e7a'
    s = f'<g transform="translate({x},{y})"><rect x="-38" y="-30" width="226" height="98" rx="8" fill="#fff" stroke="#bdbdbd"/>'
    rows = [('A', -4), ('His', 20), ('V', 44)]
    for lab, yy in rows:
        s += (f'<text x="-30" y="{yy + 4}" font-size="10" font-weight="700" fill="#6d4c41">{lab}</text>'
              f'<line x1="0" y1="{yy}" x2="182" y2="{yy}" stroke="#e0e0e0"/>')
    s += ('<rect x="14" y="13" width="62" height="14" rx="3" fill="#c62828" opacity=".15"/>'
          '<text x="80" y="24" font-size="9" fill="#c62828">refractario</text>'
          f'<line x1="14" y1="12" x2="14" y2="28" stroke="{BLUE}" stroke-width="3"/>'
          f'<line x1="34" y1="36" x2="34" y2="52" stroke="{BLUE}" stroke-width="3"/>')
    if ev:
        s += (f'<g transform="translate(58,44)"><circle r="7" fill="{ORANGE}"/><path d="M1,-4 L-2,1 L1,1 L-1,5" stroke="#fff" stroke-width="1.5" fill="none"/></g>'
              f'<text x="58" y="64" font-size="9" text-anchor="middle" fill="{ORANGE}" font-weight="700">EV</text>')
    if shift:
        s += (f'<line x1="150" y1="-12" x2="150" y2="4" stroke="#9e9e9e" stroke-width="2" stroke-dasharray="2 2"/>'
              f'<line x1="{150 - shift}" y1="-12" x2="{150 - shift}" y2="4" stroke="{ORANGE}" stroke-width="3"/>'
              f'<text x="{150 - shift / 2}" y="-15" font-size="9" text-anchor="middle" fill="{ORANGE}">adelantada</text>')
    else:
        s += f'<line x1="150" y1="-12" x2="150" y2="4" stroke="{BLUE}" stroke-width="3"/>'
        if ev:
            s += f'<text x="160" y="-15" font-size="9" text-anchor="middle" fill="{BLUE}">a su tiempo</text>'
    if tag:
        s += f'<text x="-30" y="-14" font-size="12.5" font-weight="700" fill="{c}">{E(tag)}</text>'
    return s + '</g>'


F['ehr'] = {'grid': ([[
    ('A1. TRAV: en taquicardia', TRAV_S + via(SEPT, 'vía septal', 14, -22)
     + solid([(272, 266), (286, 300), (294, 340)])
     + note(40, 120, 'el His se acaba de activar desde el nodo:|queda refractario unos ms', BLUE)
     + tline(395, 590, False, 0, None, '')
     + box('Momento del EV', 'justo con el His', False),
     'Se busca el momento en que el His ya se activó (refractario)|y el EV no puede entrar al sistema de conducción.'),
    ('A2. TRAV: EV con His refractario', TRAV_S + via(SEPT, 'vía septal', 14, -22) + spark(APEX, 'EV (ápex del VD)', -60, 35)
     + front((180, 575), (250, 470), (296, 390), (312, 330), (316, 255), (338, 190)) + xmark(HIS, None)
     + note(40, 120, 'el EV no puede subir por el His,|pero entra por la vía y adelanta la A', ORANGE)
     + note(120, 330, 'His refractario', RED)
     + tline(395, 590, True, 28, True, 'A adelantada')
     + box('A adelantada', 'hay vía (y conduce)'),
     'Si el EV llega a la A con el His refractario,|solo pudo hacerlo por una vía accesoria.')],
    [('B1. TRNAV: en taquicardia', TRNAV
     + solid([(276, 270), (288, 300), (296, 340)])
     + note(40, 120, 'el His se acaba de activar desde el nodo:|queda refractario unos ms', BLUE)
     + tline(395, 590, False, 0, None, '')
     + box('Momento del EV', 'justo con el His', False),
     'Mismo momento: el His ya se activó y está refractario.'),
    ('B2. TRNAV: EV con His refractario', TRNAV + spark(APEX, 'EV (ápex del VD)', -60, 35)
     + front((178, 572), (240, 460), (284, 330)) + front((190, 584), (300, 500), (362, 350)) + xmark(HIS, None)
     + note(120, 330, 'His refractario', RED)
     + note(40, 120, 'el His refractario bloquea el frente|y el anillo aísla: sin vía,|el EV no llega a la A', ORANGE)
     + tline(395, 590, True, 0, False, 'A sin cambio')
     + box('A sin cambio', 'no hay vía', False),
     'Sin vía el EV no tiene por dónde llegar a la A:|la A siguiente sale a su tiempo.')]], LEG)}

PH = (300, 322)   # catéter para-Hisiano
F['parahis'] = {'grid': ([[
    ('A1. Nodal: con captura del His', spark(PH, 'alta salida: His + V', 12, 4)
     + front((296, 314), (288, 290), (270, 262), (220, 200)) + faint((300, 335), (296, 400), (282, 460))
     + note(40, 120, 'captura del His (QRS angosto):|el impulso sube directo por el His|al nodo y a la A', '#00897b')
     + intbar(395, 590, [('+ His', '#00897b', 40, 0)], True, '')
     + box('SA corto', 'QRS angosto', False),
     'Con alta salida se capturan el His y el V:|la A se activa enseguida por el nodo.'),
    ('A2. Nodal: sin captura del His', spark(PH, 'baja salida: solo V', 12, 4)
     + front((298, 338), (262, 420), (210, 480), (178, 504))
     + front((180, 514), (212, 516), (240, 500), (270, 450), (285, 380), (291, 320), (272, 268), (230, 200))
     + note(40, 120, '1. sin el His (QRS ancho) el frente baja|por el septum hasta la RD distal|2. entra a la RD y sube por el His al nodo', ORANGE)
     + intbar(395, 590, [('+ His', '#00897b', 40, 0), ('− His', ORANGE, 105, 0)], False, 'SA se alarga', 'ΔSA ≥ ΔSH')
     + box('SA se alarga', 'conducción por el nodo', False),
     'Al perder la captura del His, la A depende del sistema|de conducción: el SA se alarga (tanto como el SH).')],
    [('B1. Vía septal: con captura del His', via(SEPT, 'vía septal', 14, -22) + spark(PH, 'alta salida: His + V', -150, 30)
     + front((306, 312), (313, 290), (316, 255), (338, 190)) + faint((294, 312), (284, 285), (268, 262))
     + note(40, 120, 'el miocardio septal capturado|está al lado de la vía:|la A se activa enseguida por la vía', '#00897b')
     + intbar(395, 590, [('+ His', '#00897b', 45, 0)], True, '')
     + box('SA corto', 'QRS angosto', False),
     'Con alta salida la A se activa por la vía (más rápida|que el nodo).'),
    ('B2. Vía septal: sin captura del His', via(SEPT, 'vía septal', 14, -22) + spark(PH, 'baja salida: solo V', -150, 30)
     + front((306, 312), (313, 290), (316, 255), (338, 190))
     + note(40, 120, 'sin el His (QRS ancho) el miocardio|septal igual llega a la vía:|la A sale al mismo tiempo', ORANGE)
     + intbar(395, 590, [('+ His', '#00897b', 45, 0), ('− His', ORANGE, 47, 0)], True, 'SA no cambia', '')
     + box('SA no cambia', 'conducción por la vía'),
     'La vía no depende del His: el SA queda igual|con y sin captura del His (respuesta extranodal).')]], [L_EST, L_PAS, L_CS])}

def ladder_a(x, y, mode, ok, tag):
    """Escalera A / V: 3 A estimuladas que conducen al V; al cortar, la A de retorno."""
    c = GREEN if ok else '#e65100'
    s = (f'<g transform="translate({x},{y})"><rect x="-38" y="-30" width="226" height="98" rx="8" fill="#fff" stroke="#bdbdbd"/>'
         '<text x="-28" y="4" font-size="12" font-weight="700" fill="#6d4c41">A</text><text x="-28" y="44" font-size="12" font-weight="700" fill="#6d4c41">V</text>'
         '<line x1="-12" y1="0" x2="182" y2="0" stroke="#bdbdbd"/><line x1="-12" y1="40" x2="182" y2="40" stroke="#bdbdbd"/>')
    for i in range(3):
        ax = 2 + 28 * i
        s += (f'<line x1="{ax}" y1="0" x2="{ax + 14}" y2="40" stroke="{ORANGE}" stroke-width="2.4"/>'
              f'<text x="{ax}" y="-6" font-size="10" text-anchor="middle" fill="{ORANGE}" font-weight="700">S</text>')
    lastv = 2 + 28 * 2 + 14
    if mode != 'none':
        s += f'<line x1="{lastv + 6}" y1="-18" x2="{lastv + 6}" y2="58" stroke="#9e9e9e" stroke-dasharray="3 3"/><text x="{lastv + 6}" y="-20" font-size="9.5" text-anchor="middle" fill="#757575">corte</text>'
    if mode == 'link':
        ra = lastv + 34
        s += (f'<line x1="{lastv}" y1="40" x2="{ra}" y2="0" stroke="{BLUE}" stroke-width="2.4" stroke-dasharray="4 3"/>'
              f'<line x1="{ra}" y1="0" x2="{ra + 18}" y2="40" stroke="{BLUE}" stroke-width="2.4"/>'
              f'<path d="M{lastv},50 v4 H{ra} v-4" stroke="#424242" fill="none"/>'
              f'<text x="{(lastv + ra) / 2}" y="64" font-size="9.5" text-anchor="middle" fill="#424242">VA = el de la TSV</text>')
    elif mode == 'free':
        ra = lastv + 62
        s += (f'<g transform="translate({ra},0)"><path d="M0,-7 L2,-2 L7,-2 L3,1 L5,6 L0,3 L-5,6 L-3,1 L-7,-2 L-2,-2 Z" fill="#fdd835" stroke="#c62828"/></g>'
              f'<line x1="{ra}" y1="0" x2="{ra + 18}" y2="40" stroke="{BLUE}" stroke-width="2.4"/>'
              f'<path d="M{lastv},50 v4 H{ra} v-4" stroke="#424242" fill="none"/>'
              f'<text x="{(lastv + ra) / 2}" y="64" font-size="9.5" text-anchor="middle" fill="#424242">VA distinto (variable)</text>')
    if tag:
        s += f'<text x="140" y="-12" font-size="12.5" font-weight="700" text-anchor="middle" fill="{c}">{E(tag)}</text>'
    return s + '</g>'


F['aop'] = {'grid': ([[
    ('A1. TRNAV o TRAV: durante la estimulación', TRNAV + spark(HRA, 'estimulación AD alta', -60, -20)
     + front((135, 132), (220, 210), (262, 250)) + front((285, 285), (292, 330), (290, 400))
     + note(40, 300, 'cada A estimulada entra al circuito|y baja al V (la TSV queda encarrilada)', ORANGE)
     + ladder_a(395, 590, 'none', True, '')
     + box('Encarrilada', 'desde la AD alta', False),
     'Estimulo la AD alta más rápido que la TSV:|cada A baja por el nodo y arrastra el V.'),
    ('A2. TRNAV o TRAV: al cortar', TRNAV
     + solid([(262, 252), (230, 210), (190, 175)]) + solid([(290, 290), (298, 350), (310, 420)])
     + note(40, 300, 'el circuito sigue girando: la A de retorno|sale "atada" al último V, con el mismo VA|que en la TSV', BLUE)
     + ladder_a(395, 590, 'link', True, 'VA linking')
     + box('VA linking', 'VA de retorno = TSV'),
     'La A de retorno depende del V (sale del circuito):|el VA del primer latido es el de la TSV.')],
    [('B1. TA: durante la estimulación', focus((150, 160), 'foco') + spark(HRA, 'estimulación AD alta', -60, -20)
     + front((135, 132), (220, 210), (262, 250)) + front((285, 285), (292, 330), (290, 400))
     + note(40, 300, 'las A estimuladas suprimen el foco|y bajan al V', ORANGE)
     + ladder_a(395, 590, 'none', True, '')
     + box('Encarrilada', 'desde la AD alta', False),
     'Mismo sitio y misma LC: las A estimuladas|bajan por el nodo al V.'),
    ('B2. TA: al cortar', focus((150, 160), 'foco')
     + circ((160, 175), (210, 220), (255, 252)) + solid([(290, 290), (298, 350), (310, 420)])
     + note(40, 300, 'la A de retorno la dispara el foco|cuando se recupera: no depende del V,|el VA no es el de la TSV', '#c62828')
     + ladder_a(395, 590, 'free', False, 'sin VA linking')
     + box('VA variable', 'taquicardia auricular', 'warn'),
     'El V no tiene cómo activar la A: el VA del primer latido|es distinto al de la TSV y cambia entre intentos.')]], LEG)}

MAHAIM = '<path d="M104,292 C120,360 142,440 172,505" stroke="#7e57c2" stroke-width="5" fill="none" stroke-linecap="round" opacity=".9"/>'
KENT_D = (88, 300)   # vía lateral derecha (Kent)
F['preex'] = {'grid': ([[
    ('A1. Mahaim: EA desde la AD lateral, LC lenta', MAHAIM + note(150, 330, 'vía atriofascicular', PURPLE) + spark(ADLAT, 'EA (AD lateral)', -60, -22)
     + front((82, 215), (100, 285), (128, 390), (168, 495)) + faint((95, 210), (200, 240), (262, 258), (288, 300))
     + note(40, 560, 'el EA baja por la vía hasta la RD distal:|QRS preexcitado tipo BRI', ORANGE)
     + intbar(395, 590, [('lenta', ORANGE, 60, 0)], True, '')
     + box('Preexcitación', 'S-delta largo', False),
     'Estimulando la AD lateral (cerca de la vía) el impulso|baja por la vía atriofascicular: QRS tipo BRI.'),
    ('A2. Mahaim: misma AD lateral, LC más rápida', MAHAIM + note(150, 330, 'vía atriofascicular', PURPLE) + spark(ADLAT, 'EA (AD lateral)', -60, -22)
     + f'<path d="{wavy((100, 285), (118, 360), (140, 440), (168, 495), 3, 6)}" stroke="{ORANGE}" stroke-width="3.6" fill="none"/>'
     + front((82, 215), (96, 270)) + faint((95, 210), (200, 240), (262, 258), (288, 300))
     + note(40, 560, 'la vía decrementa (como el nodo): el S-delta|se alarga y la preexcitación se hace máxima', ORANGE)
     + intbar(395, 590, [('lenta', ORANGE, 60, 0), ('rápida', '#ad1457', 115, 0)], True, 'decremental', 'S-delta se alarga')
     + box('S-delta se alarga', 'vía decremental (Mahaim)'),
     'Al acelerar, el S-delta se alarga: la vía atriofascicular|conduce en forma decremental.')],
    [('B1. Vía rápida: EA desde la AD lateral, LC lenta', via(KENT_D, 'vía lateral derecha', 14, -24) + spark(ADLAT, 'EA (AD lateral)', -60, -22)
     + front((82, 215), (88, 286)) + front((90, 316), (104, 380), (130, 440)) + faint((95, 210), (200, 240), (262, 258), (288, 300))
     + note(40, 560, 'el EA cruza la vía y activa enseguida|la pared libre del VD', ORANGE)
     + intbar(395, 590, [('lenta', ORANGE, 30, 0)], True, '')
     + box('Preexcitación', 'S-delta corto', False),
     'Mismo sitio: el impulso cruza la vía (tipo Kent)|y preexcita el VD.'),
    ('B2. Vía rápida: misma AD lateral, LC más rápida', via(KENT_D, 'vía lateral derecha', 14, -24) + spark(ADLAT, 'EA (AD lateral)', -60, -22)
     + front((82, 215), (88, 286)) + front((90, 316), (104, 380), (130, 440)) + faint((95, 210), (200, 240), (262, 258), (288, 300))
     + note(40, 560, 'la vía no decrementa: el S-delta no cambia', ORANGE)
     + intbar(395, 590, [('lenta', ORANGE, 30, 0), ('rápida', '#ad1457', 31, 0)], False, 'no decremental')
     + box('S-delta fijo', 'vía rápida (no Mahaim)', False),
     'Al acelerar, el S-delta queda igual: la vía conduce|en forma no decremental.')]], [L_EST, L_PAS, L_CS])}

def tline_h(x, y, ea, shift, ok, tag):
    """Línea de tiempo A / His / V para el EA con His refractario: mira el His siguiente."""
    c = GREEN if ok else '#546e7a'
    s = f'<g transform="translate({x},{y})"><rect x="-38" y="-30" width="226" height="98" rx="8" fill="#fff" stroke="#bdbdbd"/>'
    for lab, yy in [('A', -4), ('His', 20), ('V', 44)]:
        s += (f'<text x="-30" y="{yy + 4}" font-size="10" font-weight="700" fill="#6d4c41">{lab}</text>'
              f'<line x1="0" y1="{yy}" x2="182" y2="{yy}" stroke="#e0e0e0"/>')
    s += ('<rect x="14" y="13" width="62" height="14" rx="3" fill="#c62828" opacity=".15"/>'
          '<text x="80" y="24" font-size="9" fill="#c62828">refractario</text>'
          f'<line x1="16" y1="-12" x2="16" y2="4" stroke="{BLUE}" stroke-width="3"/>'
          f'<line x1="14" y1="12" x2="14" y2="28" stroke="{BLUE}" stroke-width="3"/>'
          f'<line x1="24" y1="36" x2="24" y2="52" stroke="{BLUE}" stroke-width="3"/>')
    if ea:
        s += (f'<g transform="translate(58,-4)"><circle r="7" fill="{ORANGE}"/><path d="M1,-4 L-2,1 L1,1 L-1,5" stroke="#fff" stroke-width="1.5" fill="none"/></g>'
              f'<text x="58" y="-15" font-size="9" text-anchor="middle" fill="{ORANGE}" font-weight="700">EA</text>')
    if shift:
        s += (f'<line x1="150" y1="12" x2="150" y2="28" stroke="#9e9e9e" stroke-width="2" stroke-dasharray="2 2"/>'
              f'<line x1="{150 + shift}" y1="12" x2="{150 + shift}" y2="28" stroke="{ORANGE}" stroke-width="3"/>'
              f'<text x="140" y="40" font-size="9" text-anchor="middle" fill="{ORANGE}">se adelanta o retrasa</text>')
    else:
        s += f'<line x1="150" y1="12" x2="150" y2="28" stroke="{BLUE}" stroke-width="3"/>'
        if ea:
            s += f'<text x="145" y="40" font-size="9" text-anchor="middle" fill="{BLUE}">a su tiempo</text>'
    if tag:
        s += f'<text x="186" y="-14" font-size="12.5" font-weight="700" text-anchor="end" fill="{c}">{E(tag)}</text>'
    return s + '</g>'


JFOC = (290, 296)
F['eha'] = {'grid': ([[
    ('A1. TRNAV: en taquicardia', TRNAV
     + solid([(262, 252), (230, 210), (190, 175)]) + solid([(290, 290), (298, 330)])
     + note(40, 120, 'A y His salen juntos del circuito:|el His recién activado queda refractario', BLUE)
     + tline_h(395, 590, False, 0, None, '')
     + box('Momento del EA', 'con el His refractario', False),
     'TSV con VA muy corto: se busca el momento en que|el His ya se activó (refractario).'),
    ('A2. TRNAV: EA con His refractario', TRNAV + spark(CSOS, 'EA (ostium del SC)', -110, 40)
     + front((236, 272), (246, 282), (260, 276)) + xmark(HIS, None)
     + note(40, 120, 'el EA entra en la vía lenta, que es parte|del circuito: adelanta, retrasa o termina|el His siguiente', ORANGE)
     + tline_h(395, 590, True, -22, True, 'His modificado')
     + box('His siguiente cambia', 'TRNAV'),
     'Aunque el His esté refractario, el EA alcanza el circuito|(vía lenta) y modifica el His siguiente.')],
    [('B1. Taquicardia de la unión: en taquicardia', focus(JFOC, 'foco')
     + solid([(286, 286), (262, 252), (220, 205)]) + solid([(292, 306), (298, 340)])
     + note(40, 120, 'el foco está en la unión, debajo del nodo:|activa el His y sube a la A', BLUE)
     + tline_h(395, 590, False, 0, None, '')
     + box('Momento del EA', 'con el His refractario', False),
     'Mismo VA corto: A y His salen casi juntos del foco.'),
    ('B2. Taquicardia de la unión: EA con His refractario', focus(JFOC, 'foco') + spark(CSOS, 'EA (ostium del SC)', -110, 40)
     + front((236, 272), (248, 270), (258, 264)) + xmark(NODO, None)
     + note(40, 120, 'el EA choca con la unión refractaria:|no alcanza el foco', ORANGE)
     + note(300, 240, 'unión refractaria', RED)
     + tline_h(395, 590, True, 0, False, 'His sin cambio')
     + box('His sin cambio', 'taquicardia de la unión', 'warn'),
     'El foco está debajo de la unión refractaria: el EA no lo|alcanza y el His siguiente sale a su tiempo.')]], LEG)}

RR = circ((291, 310), (285, 400), (250, 480), (200, 515)) + circ((230, 560), (300, 600), (340, 520), (320, 400), (298, 318))
def hvline(x, y, mode, ok, tag):
    """Línea de tiempo His / V durante la TV."""
    c = GREEN if ok else '#e65100' if ok is False else '#37474f'
    s = f'<g transform="translate({x},{y})"><rect x="-38" y="-30" width="226" height="98" rx="8" fill="#fff" stroke="#bdbdbd"/>'
    for lab, yy in [('His', 6), ('V', 36)]:
        s += (f'<text x="-30" y="{yy + 4}" font-size="10" font-weight="700" fill="#6d4c41">{lab}</text>'
              f'<line x1="0" y1="{yy}" x2="182" y2="{yy}" stroke="#e0e0e0"/>')
    for i in range(3):
        v = 40 + 60 * i
        h = v - 28 if mode == 'bbr' else v + 22
        s += (f'<line x1="{h}" y1="-2" x2="{h}" y2="14" stroke="{BLUE}" stroke-width="3"/>'
              f'<rect x="{v - 4}" y="28" width="8" height="16" rx="2" fill="#6d4c41"/>')
    if mode == 'bbr':
        s += '<path d="M12,50 v4 H40 v-4" stroke="#424242" fill="none"/><text x="26" y="64" font-size="9.5" text-anchor="middle" fill="#424242">HV ≥ sinusal</text>'
    else:
        s += '<text x="94" y="62" font-size="9.5" text-anchor="middle" fill="#424242">His después del V (o disociado)</text>'
    if tag:
        s += f'<text x="186" y="-14" font-size="12.5" font-weight="700" text-anchor="end" fill="{c}">{E(tag)}</text>'
    return s + '</g>'


LVC = circ((400, 450), (440, 430), (460, 470), (430, 505), (398, 488))
F['bbr'] = {'grid': ([[
    ('A1. Rama-rama: en taquicardia', RR + note(120, 440, 'baja por la|rama derecha', BLUE) + note(345, 470, 'sube por la|rama izquierda', BLUE)
     + note(40, 120, 'el circuito usa las dos ramas y el septum:|el His se activa antes de cada V', BLUE)
     + hvline(395, 590, 'bbr', None, '')
     + box('His antes de cada V', 'HV ≥ sinusal', False),
     'Macrorreentrada en el His-Purkinje: el His precede|a cada V con HV igual o mayor que en sinusal.'),
    ('A2. Rama-rama: encarrilando desde el ápex del VD', RR + spark(APEX, 'ápex del VD', -60, 35)
     + front((168, 578), (172, 525), (190, 515))
     + note(40, 120, 'el ápex está al lado de la RD distal,|que es parte del circuito: el retorno|es una vuelta al circuito', ORANGE)
     + ppibar(395, 590, 12, True, 'PPI − LC ≤ 30')
     + box('PPI − LC ≤ 30', 'rama-rama'),
     'La rama derecha está en el circuito: desde el ápex|el PPI casi no supera la LC.')],
    [('B1. TV miocárdica: en taquicardia', LVC + note(400, 420, 'circuito en el VI', BLUE) + faint((404, 444), (340, 380), (296, 316))
     + note(40, 120, 'el circuito está en el miocardio:|el His se activa en forma pasiva,|después del V o disociado', BLUE)
     + hvline(395, 590, 'tv', None, '')
     + box('His pasivo', 'no precede al V', False),
     'El His no forma parte del circuito: no predice|el VV y puede disociarse.'),
    ('B2. TV miocárdica: encarrilando desde el ápex del VD', LVC + note(400, 420, 'circuito en el VI', BLUE) + spark(APEX, 'ápex del VD', -60, 35)
     + front((178, 580), (250, 600), (330, 560), (395, 500))
     + note(40, 120, 'el circuito está lejos del ápex del VD:|el frente tiene que ir y volver|por el miocardio', ORANGE)
     + ppibar(395, 590, 58, False, 'PPI − LC > 30')
     + box('PPI − LC > 30', 'TV miocárdica', False),
     'El circuito está lejos del sitio de estimulación:|el PPI supera claramente la LC.')]], [L_TSV, L_EST, L_PAS, L_CS])}

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

TVFP = circ((330, 420), (360, 470), (395, 515)) + circ((410, 532), (442, 492), (425, 440), (365, 418))
def p1p2(x, y):
    """Mini registro del catéter septal (4 canales, prox arriba): P1 en los 3 proximales (prox → dist),
    que sigue sin corte en P2 en los 3 distales (dist → prox)."""
    s = (f'<g transform="translate({x},{y})"><rect x="-38" y="-30" width="226" height="98" rx="8" fill="#fff" stroke="#bdbdbd"/>'
         '<text x="-30" y="-10" font-size="9.5" font-weight="700" fill="#6d4c41">prox</text>'
         '<text x="-30" y="44" font-size="9.5" font-weight="700" fill="#6d4c41">dist</text>')
    ys = [-12 + 17 * i for i in range(4)]
    p1 = [(52 + 16 * i, ys[i]) for i in range(3)]            # canales 1-3
    p2 = [(136 + 5 * k, ys[3 - k]) for k in range(3)]        # canales 4 → 2, progresión sutil y presistólica
    for yy in ys:
        s += (f'<line x1="0" y1="{yy}" x2="182" y2="{yy}" stroke="#eeeeee"/>'
              f'<rect x="6" y="{yy - 6}" width="10" height="12" rx="2" fill="#6d4c41"/><rect x="164" y="{yy - 6}" width="10" height="12" rx="2" fill="#6d4c41"/>')
    for px, py in p1:
        s += f'<line x1="{px}" y1="{py - 5}" x2="{px}" y2="{py + 5}" stroke="#1565c0" stroke-width="2.8"/>'
    for px, py in p2:
        s += f'<line x1="{px}" y1="{py - 5}" x2="{px}" y2="{py + 5}" stroke="{ORANGE}" stroke-width="2.8"/>'
    s += (f'<path d="M{p1[0][0]},{p1[0][1]} L{p1[2][0]},{p1[2][1]} L{p2[0][0]},{p2[0][1]}" stroke="#1565c0" stroke-width="1.4" stroke-dasharray="3 2" fill="none"/>'
          f'<path d="M{p2[0][0]},{p2[0][1]} L{p2[2][0]},{p2[2][1]}" stroke="{ORANGE}" stroke-width="1.4" stroke-dasharray="3 2" fill="none" marker-end="url(#ao)"/>'
          f'<text x="40" y="57" font-size="9.5" fill="#1565c0" font-weight="700">P1: prox → dist</text>'
          f'<text x="158" y="-18" font-size="9.5" text-anchor="end" fill="{ORANGE}" font-weight="700">P2: dist → prox</text>'
          '<text x="11" y="57" font-size="9" text-anchor="middle" fill="#6d4c41">QRS</text><text x="169" y="57" font-size="9" text-anchor="middle" fill="#6d4c41">QRS</text>')
    return s + '</g>'


CATH = ('<path d="M318,400 L418,532" stroke="#455a64" stroke-width="4" stroke-linecap="round"/>'
        + ''.join(f'<rect x="{318 + 25 * i - 4}" y="{400 + 33 * i - 4}" width="8" height="8" fill="#212121"/>' for i in range(5)))
USC = circ((300, 315), (318, 345), (330, 330)) + circ((322, 318), (308, 300))
F['tvf'] = {'grid': ([[
    ('A1. TV fascicular posterior: el circuito', TVFP + note(448, 470, 'P2: sube|por el|fascículo|posterior', BLUE) + note(325, 470, 'P1 baja por|tejido de Purkinje|anómalo', BLUE, 'end')
     + front((400, 530), (430, 560), (470, 540))
     + note(40, 120, 'reentrada entre el fascículo posterior y|tejido de Purkinje anómalo (P1, decremental|y sensible al verapamilo); sale por el septum|inferior: BRD + eje superior', BLUE)
     + box('BRD + eje superior', 'verapamilo la termina', False),
     'El circuito está en el septum medio-inferior del VI|y sale cerca del fascículo posterior.', ('nodo', 'his', 'fp')),
    ('A2. TV fascicular posterior: qué se registra', TVFP + CATH + note(430, 400, 'catéter|multipolar|en el septum', '#455a64')
     + note(40, 120, 'en el septum medio: P1 mesodiastólico|(de proximal a distal) y P2 presistólico|(de distal a proximal)', BLUE)
     + p1p2(395, 590)
     + box('P1 + P2', 'TV fascicular posterior'),
     'P1 y P2 se activan en sentidos opuestos:|son los dos brazos del circuito.', ('nodo', 'his', 'fp'))],
    [('B1. TV fascicular septal superior: el circuito', USC + front((330, 335), (380, 380), (425, 410)) + front((325, 345), (340, 420), (390, 510)) + faint((300, 320), (288, 296))
     + note(40, 120, 'el circuito usa el fascículo septal superior,|cerca del His: baja por los dos fascículos|a la vez y da un QRS angosto', BLUE)
     + box('QRS angosto', 'parece una TSV', 'warn'),
     'La activación baja por los dos fascículos:|QRS angosto, eje normal.', ('nodo', 'his', 'fa', 'fp')),
    ('B2. TV fascicular septal superior: qué se registra', USC + faint((300, 320), (288, 296))
     + '<path d="M286,300 L322,340" stroke="#455a64" stroke-width="4" stroke-linecap="round"/>'
     + note(40, 120, 'His retrógrado y HV más corto que en sinusal;|el potencial más precoz está a ≤ 7 mm|del His izquierdo, sin P1', BLUE)
     + intbar(395, 590, [('sinusal', BLUE, 60, 0), ('TV', ORANGE, 25, 0)], True, 'HV más corto', 'el His se activa tarde (retrógrado)')
     + box('HV < sinusal', 'TV septal superior'),
     'Con QRS angosto, un HV más corto que en sinusal|descarta la TSV: es una TV fascicular.', ('nodo', 'his', 'fa', 'fp'))]], [L_TSV, L_EST, L_PAS, L_CS])}

F['tvfabl'] = (
    ('A. Ablación en P1 / P2', TVFP + focus((365, 470), 'sitio de ablación') + box('P1-P2 se alarga', 'y la TV termina'),
     'Con la TV inducible, se ablaciona en P1 (tercio apical) o|en el P2 más precoz; durante la RF el P1-P2 se alarga.', ('nodo', 'his', 'fp')),
    ('B. Línea anatómica', '<path d="M341,490 L396,458" stroke="#c62828" stroke-width="6" stroke-dasharray="2 6" stroke-linecap="round"/>'
     + note(300, 525, 'línea perpendicular al|fascículo posterior', RED) + box('TV no inducible', 'línea de 1–2 cm'),
     'Si no se induce: línea perpendicular al fascículo|posterior en el septum medio-inferior.', ('nodo', 'his', 'fp')), [L_TSV, L_CS])

def papilar(base, tip, w, leaflet):
    """Músculo papilar: masa cónica redondeada que nace de la pared del VI, con cuerdas tendinosas a la valva mitral."""
    (bx, by), (tx, ty) = base, tip
    dx, dy = tx - bx, ty - by
    n = (dx * dx + dy * dy) ** .5
    ux, uy = dx / n, dy / n          # eje base → punta
    px, py = -uy, ux                 # perpendicular
    def pt(a, b):                    # a: a lo largo del eje (0 base, 1 punta); b: lateral en múltiplos de w
        return (bx + dx * a + px * w * b, by + dy * a + py * w * b)
    P = [pt(-.05, 1.25), pt(.35, 1.05), pt(.8, .55), pt(1.0, .22), pt(1.04, 0), pt(1.0, -.22), pt(.8, -.55), pt(.35, -1.05), pt(-.05, -1.25)]
    f = lambda q: f'{q[0]:.0f},{q[1]:.0f}'
    d = (f'M{f(P[0])} C{f(P[1])} {f(P[2])} {f(P[3])} Q{f(P[4])} {f(P[5])} C{f(P[6])} {f(P[7])} {f(P[8])} '
         f'Q{f(pt(-.22, 0))} {f(P[0])} Z')
    s = (f'<defs><linearGradient id="gpm{bx}" x1="0" x2="1"><stop offset="0" stop-color="#8e3b2f"/><stop offset=".45" stop-color="#c06a58"/>'
         f'<stop offset="1" stop-color="#7d3127"/></linearGradient></defs>'
         f'<path d="{d}" fill="url(#gpm{bx})" stroke="#5d221a" stroke-width="1.4"/>')
    for k in (-.45, 0, .45):        # estrías musculares
        a0, a1 = pt(.1, k * 1.6), pt(.85, k * .6)
        s += f'<path d="M{f(a0)} L{f(a1)}" stroke="#d98f7c" stroke-width="1.2" opacity=".5"/>'
    lx0, lx1, ly = leaflet
    s += f'<path d="M{lx0},{ly} Q{(lx0 + lx1) / 2},{ly + 16} {lx1},{ly}" stroke="#e8c9a8" stroke-width="5" fill="none" stroke-linecap="round"/>'
    for i in range(6):
        cx = lx0 + (lx1 - lx0) * (i + .5) / 6
        cy = ly + 6 + 4 * (1 - abs(i - 2.5) / 2.5)
        s += f'<line x1="{tx:.0f}" y1="{ty:.0f}" x2="{cx:.0f}" y2="{cy:.0f}" stroke="#f3e5d0" stroke-width="1.1"/>'
    return s


F['pm'] = (
    ('A. Músculo papilar posteromedial', papilar((392, 590), (408, 472), 20, (380, 470, 318)) + focus((406, 492), 'foco')
     + note(478, 336, 'valva mitral|y cuerdas', '#6d4c41')
     + box('BRD + eje superior', 'QRS ancho, focal'), 'Foco en el músculo papilar posteromedial:|BRD con eje superior, no reentrante.'),
    ('B. Músculo papilar anterolateral', papilar((500, 505), (468, 412), 18, (440, 530, 316)) + focus((474, 432), 'foco')
     + note(432, 336, 'valva mitral|y cuerdas', '#6d4c41', 'end')
     + box('BRD + eje inferior', 'QRS ancho, focal'), 'Foco en el músculo papilar anterolateral:|BRD con eje inferior.'), [L_CS])

F['ma'] = (
    ('A. Anillo mitral anterolateral', focus((515, 320), 'foco') + note(470, 345, 'justo debajo del anillo', RED, 'end')
     + box('R de V1 a V6', 'S en V6, eje inferior'),
     'Foco en el anillo mitral anterolateral (lado ventricular):|R en V1, concordancia positiva, DI negativo.'),
    ('B. Anillo mitral posterior', focus((420, 322), 'foco') + note(400, 350, 'justo debajo del anillo', RED, 'end')
     + box('R de V1 a V6', 'eje superior'),
     'Foco en el anillo mitral posterior o posteroseptal|(lado ventricular): R en V1, eje superior.'), [L_CS])

OBL = '<path d="M520,262 C510,280 495,296 478,310" stroke="#7e57c2" stroke-width="7" fill="none" stroke-linecap="round"/>'
F['obl'] = (
    ('A. Estimulación ventricular', OBL + note(500, 240, 'inserción auricular', PURPLE, 'end') + note(440, 330, 'inserción|ventricular', PURPLE, 'end')
     + spark(BASE_VI, 'VI', 10, 22) + front((488, 320), (480, 310)) + front((520, 258), (500, 220), (450, 180))
     + box('A más precoz', 'en la inserción auricular'),
     'La vía oblicua cruza el anillo en diagonal: la A más precoz|marca la inserción auricular, no la ventricular.'),
    ('B. Estimulación auricular', OBL + spark(CSD, 'SC distal', -20, -20) + front((505, 266), (512, 276)) + front((478, 314), (450, 380), (420, 420))
     + box('V más precoz', 'en la inserción ventricular'),
     'Con estimulación auricular el V más precoz marca la inserción|ventricular: invertir el frente ayuda a ubicarlas.'), LEG)

SLOW = wavy((200, 250), (215, 276), (245, 282), (264, 270), 4.5, 7)
FAST = '<path d="M206,240 C228,214 256,226 266,250" stroke="#2e7d32" stroke-width="3" fill="none"/>'
F['dfire'] = (
    ('A. Por la vía rápida: H1', spark(HRA, 'A sinusal', -40, -20) + front((135, 132), (175, 190), (200, 236))
     + FAST + front((214, 236), (240, 220), (262, 244), w=3.2)
     + f'<path d="{SLOW}" stroke="#8e24aa" stroke-width="3" fill="none" opacity=".4"/>'
     + note(194, 266, 'vía lenta', '#6a1b9a', 'end') + note(236, 206, 'vía rápida', GREEN)
     + front((285, 285), (292, 320), (300, 400))
     + box('H1 – V1', 'AH corto'), 'La A conduce primero por la vía rápida:|primer His y primer V.', ('his',)),
    ('B. Por la vía lenta: H2', spark(HRA, 'la misma A', -40, -20) + front((135, 132), (175, 190), (200, 236))
     + FAST.replace('stroke-width="3"', 'stroke-width="3" opacity=".4"')
     + f'<path d="{SLOW}" stroke="#8e24aa" stroke-width="4.5" fill="none" stroke-linecap="round"/>'
     + note(194, 266, 'vía lenta', '#6a1b9a', 'end') + note(70, 330, 'recorrido tortuoso y lento:|llega al His cuando ya se recuperó', '#6a1b9a')
     + front((276, 278), (286, 292), (291, 310)) + front((292, 322), (296, 360), (300, 400))
     + box('H2 – V2', 'H1–H2 fijo (400–500 ms)'), 'La misma A baja más tarde por la vía lenta y llega al His|cuando ya se recuperó: segundo His y segundo V.', ('his',)), [L_EST, L_CS])

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
