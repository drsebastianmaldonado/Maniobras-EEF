"""Corazón esquemático (OAI ~30°) con el sistema de conducción, base de los esquemas de maniobras."""
import math, random, sys
random.seed(4)

def bez(p0, p1, p2, p3, n=24):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1-t)**3*p0[0] + 3*(1-t)**2*t*p1[0] + 3*(1-t)*t**2*p2[0] + t**3*p3[0]
        y = (1-t)**3*p0[1] + 3*(1-t)**2*t*p1[1] + 3*(1-t)*t**2*p2[1] + t**3*p3[1]
        pts.append((x, y))
    return pts

def purkinje(x, y, ang, length, w, depth, out):
    """Red de Purkinje: ramas que se bifurcan y se afinan."""
    if depth == 0 or length < 6:
        return
    x2 = x + length * math.cos(ang); y2 = y + length * math.sin(ang)
    cx = (x + x2) / 2 + random.uniform(-4, 4); cy = (y + y2) / 2 + random.uniform(-4, 4)
    out.append(f'<path d="M{x:.1f},{y:.1f} Q{cx:.1f},{cy:.1f} {x2:.1f},{y2:.1f}" stroke="url(#gcs)" stroke-width="{w:.2f}" fill="none" stroke-linecap="round"/>')
    for d in (-0.45, 0.4):
        purkinje(x2, y2, ang + d + random.uniform(-0.15, 0.15), length * random.uniform(0.6, 0.78), w * 0.68, depth - 1, out)

def heart(rotulos=('nodo', 'his')):
    random.seed(4)
    o = []
    # aurículas grandes y redondeadas
    o.append('<path d="M60,200 C55,110 120,60 190,62 C250,64 285,110 288,170 C290,215 286,250 280,276 L78,282 C66,262 61,236 60,200 Z" fill="url(#gat)" stroke="#9c4f42" stroke-width="2.2"/>')
    o.append('<path d="M302,276 C296,240 296,200 304,160 C318,100 370,70 430,70 C500,70 548,118 546,190 C545,232 538,262 528,280 Z" fill="url(#gat)" stroke="#9c4f42" stroke-width="2.2"/>')
    # brillo
    o.append('<ellipse cx="150" cy="130" rx="55" ry="30" fill="#fff" opacity=".18"/><ellipse cx="420" cy="128" rx="60" ry="28" fill="#fff" opacity=".16"/>')
    # surco AV con grasa
    o.append('<path d="M70,284 C170,300 400,302 532,282" stroke="#e9d3a8" stroke-width="18" fill="none" stroke-linecap="round" opacity=".85"/>')
    o.append('<path d="M70,284 C170,300 400,302 532,282" stroke="#c9ad7d" stroke-width="1.2" fill="none" opacity=".8"/>')
    # ventrículos
    o.append('<path d="M84,292 C70,380 92,480 160,560 C200,605 245,628 284,636 C292,520 292,400 282,300 Z" fill="url(#gvd)" stroke="#9c4f42" stroke-width="2.2"/>')
    o.append('<path d="M300,300 C312,420 312,530 302,638 C385,642 470,595 516,512 C556,440 566,350 540,294 Z" fill="url(#gvi)" stroke="#9c4f42" stroke-width="2.2"/>')
    o.append('<path d="M282,300 C292,420 294,530 286,636 L302,638 C312,530 312,420 300,300 Z" fill="#a9564a" opacity=".5"/>')
    o.append('<ellipse cx="170" cy="420" rx="45" ry="80" fill="#fff" opacity=".12"/><ellipse cx="430" cy="420" rx="50" ry="90" fill="#fff" opacity=".10"/>')
    for t, x, y in (('AD', 150, 185), ('AI', 440, 185), ('VD', 150, 430), ('VI', 450, 430)):
        o.append(f'<text x="{x}" y="{y}" font-size="16" font-weight="700" fill="#5d1f16" opacity=".85">{t}</text>')
    o.append('<text x="294" y="662" font-size="11" text-anchor="middle" fill="#7a4a40">septum</text>')
    # ---- sistema de conducción ----
    cs = []
    # nodo AV compacto (forma de media luna) y extensiones
    cs.append('<path d="M250,262 C255,250 275,248 284,258 C288,266 280,274 268,273 C258,272 248,270 250,262 Z" fill="url(#gnode)" stroke="#9a7300" stroke-width="1.5"/>')
    # His penetrante
    His = bez((282, 270), (288, 282), (292, 292), (293, 308))
    cs.append('<path d="M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in His) + '" stroke="url(#gcs)" stroke-width="7" fill="none" stroke-linecap="round"/>')
    # rama derecha: cordón fino por el septum del VD y la banda moderadora
    rb = bez((290, 308), (284, 380), (270, 450), (238, 500))
    cs.append('<path d="M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in rb) + '" stroke="url(#gcs)" stroke-width="3" fill="none" stroke-linecap="round"/>')
    mb = bez((238, 500), (220, 512), (195, 518), (172, 508))
    cs.append('<path d="M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in mb) + '" stroke="url(#gcs)" stroke-width="3.4" fill="none" stroke-linecap="round"/>')
    pk = []
    purkinje(172, 508, math.radians(95), 26, 1.7, 4, pk)
    purkinje(172, 508, math.radians(-110), 26, 1.7, 4, pk)
    purkinje(238, 500, math.radians(100), 30, 1.6, 4, pk)
    # rama izquierda: abanico sobre el septum del VI con fascículos
    lb_tr = bez((295, 308), (300, 318), (306, 326), (312, 334))
    cs.append('<path d="M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in lb_tr) + '" stroke="url(#gcs)" stroke-width="5" fill="none" stroke-linecap="round"/>')
    for end, c1, c2, w in (((430, 410), (350, 350), (400, 380), 3.2),   # fascículo anterior
                           ((400, 520), (330, 400), (360, 470), 3.2)):  # fascículo posterior
        p = bez((312, 334), c1, c2, end)
        cs.append('<path d="M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in p) + f'" stroke="url(#gcs)" stroke-width="{w}" fill="none" stroke-linecap="round"/>')
    purkinje(430, 410, math.radians(-10), 36, 1.9, 4, pk)
    purkinje(430, 410, math.radians(70), 32, 1.9, 4, pk)
    purkinje(400, 520, math.radians(30), 34, 1.9, 4, pk)
    purkinje(400, 520, math.radians(110), 30, 1.9, 4, pk)
    o.append('<g opacity=".95" clip-path="url(#cv)">' + ''.join(pk) + '</g>')
    o.extend(cs)
    R = {'nodo': '<text x="210" y="252" font-size="10.5" text-anchor="end" fill="#6d4c41">nodo AV</text>',
         'his': '<text x="274" y="320" font-size="10.5" text-anchor="end" fill="#6d4c41">His</text>',
         'rd': '<text x="200" y="545" font-size="10" text-anchor="middle" fill="#6d4c41">rama derecha</text>',
         'ri': '<text x="330" y="350" font-size="10" fill="#6d4c41">rama izquierda</text>',
         'fa': '<text x="440" y="398" font-size="10" fill="#6d4c41">fascículo anterior</text>',
         'fp': '<text x="410" y="545" font-size="10" fill="#6d4c41">fascículo posterior</text>'}
    o.extend(R[k] for k in rotulos)
    return '\n'.join(o)

HEART = heart()
DEFS = '''<defs>
<radialGradient id="gat" cx="45%" cy="35%" r="75%"><stop offset="0" stop-color="#f7d4cb"/><stop offset=".6" stop-color="#e6a091"/><stop offset="1" stop-color="#c97a6b"/></radialGradient>
<radialGradient id="gvd" cx="40%" cy="38%" r="80%"><stop offset="0" stop-color="#f0b6a8"/><stop offset=".65" stop-color="#d27c6c"/><stop offset="1" stop-color="#a9554a"/></radialGradient>
<radialGradient id="gvi" cx="45%" cy="40%" r="80%"><stop offset="0" stop-color="#eaa696"/><stop offset=".65" stop-color="#c86a59"/><stop offset="1" stop-color="#9a4337"/></radialGradient>
<radialGradient id="gnode" cx="40%" cy="40%" r="70%"><stop offset="0" stop-color="#fff2b0"/><stop offset="1" stop-color="#e3b11c"/></radialGradient>
<linearGradient id="gcs" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#f7d354"/><stop offset="1" stop-color="#e2a915"/></linearGradient>
<clipPath id="cv"><path d="M96,300 C84,380 104,474 168,550 C206,594 246,616 278,624 L284,300 Z"/><path d="M302,300 C314,420 314,530 304,628 C385,632 464,588 508,508 C546,440 554,350 530,302 Z"/></clipPath>
<marker id="ab" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4.5" markerHeight="4.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1f5fbf"/></marker>
<marker id="ao" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4.5" markerHeight="4.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#ef6c00"/></marker>
<filter id="sh" x="-10%" y="-10%" width="120%" height="120%"><feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#5d1f16" flood-opacity=".25"/></filter>
<g id="heart"><g filter="url(#sh)">''' + HEART + '''</g></g>
</defs>'''

