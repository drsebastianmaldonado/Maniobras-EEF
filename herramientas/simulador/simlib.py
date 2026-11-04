"""Generador de registros de polígrafo simulados.
Cada escenario define latidos (QRS angosto, estimulado desde el ápex o la base, fusionado), activaciones auriculares
con su secuencia, His anterógrado y retrógrado, espigas y calibres. Solo se rotulan los intervalos publicados."""
import math, random

def g(t, mu, sd, a):
    return a * math.exp(-0.5 * ((t - mu) / sd) ** 2)

def dg(t, mu, sd, a):
    return -a * (t - mu) / sd * math.exp(-0.5 * ((t - mu) / sd) ** 2)

QRS = {  # (desfase, ancho, amplitud) por derivación
    'n':  {'I': [(-8, 6, 0.10), (6, 9, 0.75), (24, 7, -0.15)], 'aVF': [(-6, 6, -0.05), (8, 10, 0.70), (26, 8, -0.20)], 'V1': [(0, 7, 0.15), (16, 10, -0.80)]},
    'pa': {'I': [(20, 18, 0.55), (60, 22, 0.35)], 'aVF': [(25, 20, -0.75), (70, 24, -0.35)], 'V1': [(25, 22, -0.85), (75, 24, -0.30)]},
    'pb': {'I': [(22, 18, 0.35), (62, 22, 0.20)], 'aVF': [(25, 20, 0.80), (68, 22, 0.35)], 'V1': [(25, 22, -0.70), (72, 24, -0.25)]},
    'f':  {'I': [(6, 12, 0.60), (40, 16, 0.20)], 'aVF': [(10, 13, 0.10), (42, 16, -0.30)], 'V1': [(8, 12, 0.10), (34, 16, -0.75)]},
    'lv': {'I': [(25, 20, -0.60), (65, 22, -0.25)], 'aVF': [(25, 20, 0.45), (65, 22, 0.20)], 'V1': [(25, 20, 0.80), (65, 22, 0.35)]},
    'fl': {'I': [(6, 11, 0.30), (32, 14, -0.30)], 'aVF': [(8, 11, 0.50), (32, 14, 0.15)], 'V1': [(6, 10, 0.05), (28, 14, 0.45)]},
    'rbs': {'I': [(8, 9, 0.45), (40, 12, -0.15)], 'aVF': [(6, 8, 0.10), (28, 12, -0.70)], 'V1': [(6, 7, 0.25), (22, 8, -0.15), (52, 12, 0.70)]},
}
TWAVE = {'n': {'I': 0.18, 'aVF': 0.22, 'V1': 0.10}, 'pa': {'I': -0.20, 'aVF': 0.25, 'V1': 0.22},
         'pb': {'I': -0.15, 'aVF': -0.25, 'V1': 0.20}, 'f': {'I': 0.05, 'aVF': 0.10, 'V1': 0.15},
         'lv': {'I': 0.20, 'aVF': -0.15, 'V1': -0.20}, 'fl': {'I': 0.10, 'aVF': 0.05, 'V1': -0.05},
         'rbs': {'I': -0.10, 'aVF': 0.18, 'V1': -0.15}}

# secuencias auriculares: desfase (ms) de cada canal respecto del inicio de la activación auricular
CS_NAMES = ['CS 9-10', 'CS 7-8', 'CS 5-6', 'CS 3-4', 'CS 1-2']
SEQ = {
    'conc_cs':  {'HRA': 38, 'His': 8, 'CS': [2, 11, 20, 29, 38]},      # retrógrada, más precoz en el ostium del SC
    'conc_his': {'HRA': 30, 'His': 0, 'CS': [10, 18, 26, 34, 42]},     # retrógrada, más precoz en el His
    'cs_mid':   {'HRA': 45, 'His': 20, 'CS': [14, 6, 0, 6, 14]},       # más precoz en el SC medio
    'right':    {'HRA': 0, 'His': 22, 'CS': [32, 40, 48, 56, 64]},     # más precoz en la pared libre derecha (AD alta)
    'sinus':    {'HRA': 0, 'His': 28, 'CS': [38, 46, 54, 62, 70]},
    'left':     {'HRA': 60, 'His': 40, 'CS': [36, 28, 18, 8, 0]},       # más precoz en el SC distal (vía izquierda)
}

def render(sc, path):
    random.seed(sc.get('seed', 3))
    T0, T1 = sc['win']
    PXMS = sc.get('pxms', 0.30)
    LEFT, TOP, ROWH = 78, 26, 44
    W = int(LEFT + (T1 - T0) * PXMS + 20)
    beats = sc['beats']            # [(tiempo del inicio del QRS o espiga, tipo)]
    spikes = sc.get('spikes', [])  # tiempos de estimulación ventricular
    aspikes = sc.get('aspikes', [])  # tiempos de estimulación auricular
    extra = sc.get('extra', {})      # {canal: [(t, amplitud, ancho)]}
    atr = sc['atr']                # [(tiempo, secuencia, polaridad P en aVF: -1 retrógrada / +1 sinusal)]
    h_ante = sc.get('h_ante', [])
    h_retro = sc.get('h_retro', [])
    def v_local(t0, typ):  # momento del V local en el VD
        return t0 + (14 if typ in ('pa',) else 30 if typ in ('pb', 'lv') else 6 if typ in ('f', 'fl') else 8 if typ == 'rbs' else 2)

    def egm(t, sites, w=1.0, frac=0):
        y = 0.0
        for mu, a in sites:
            y += dg(t, mu, 2.2 * w, a) + dg(t, mu + 5 * w, 2.8 * w, -0.45 * a)
            for k in range(frac):
                y += dg(t, mu + 9 + 5 * k, 1.6, 0.25 * a * (1 if k % 2 else -1))
        return y

    def surface(t, lead):
        y = 0.0
        for t0, typ in beats:
            y += sum(g(t, t0 + m, s, a) for m, s, a in QRS[typ][lead])
            y += g(t, t0 + (210 if typ == 'n' else 260), 45 if typ == 'n' else 55, TWAVE[typ][lead])
        for ta, seq, pol in atr:
            amp = {'I': 0.04, 'aVF': 0.10 * pol, 'V1': 0.06 if pol < 0 else -0.04}[lead]
            y += g(t, ta + 30, 22, amp)
        return y

    def ch_atrial_offset(seq, name):
        s = SEQ[seq]
        if name == 'HRA': return s['HRA']
        if name.startswith('His'): return s['His']
        return s['CS'][CS_NAMES.index(name)]

    def far_v(t0, typ, extra):
        return v_local(t0, typ) + extra

    def channel(name):
        def f(t):
            y = 0.0
            if name == 'HRA':
                y += egm(t, [(ta + ch_atrial_offset(seq, 'HRA'), 0.9) for ta, seq, pol in atr])
                y += egm(t, [(far_v(t0, typ, 8), 0.12) for t0, typ in beats], w=3)
            elif name.startswith('His'):
                prox = name.endswith('p')
                y += egm(t, [(ta + ch_atrial_offset(seq, 'His'), 0.55 if prox else 0.30) for ta, seq, pol in atr], w=1.2)
                y += egm(t, [(h, 0.35 if prox else 0.6) for h in h_ante], w=0.6)
                y += egm(t, [(h, 0.18) for h in h_retro], w=0.6)
                y += egm(t, [(far_v(t0, typ, 3 if typ in ('n', 'f') else 30), 0.9 if prox else 1.2) for t0, typ in beats], w=1.8, frac=1)
            elif name.startswith('CS'):
                i = CS_NAMES.index(name)
                y += egm(t, [(ta + ch_atrial_offset(seq, name), 1.0 - 0.06 * i) for ta, seq, pol in atr], frac=1 if i in (1, 2) else 0)
                y += egm(t, [(far_v(t0, typ, 18 + 6 * i if typ in ('n', 'f') else 45 + 6 * i), 0.35) for t0, typ in beats], w=2.5)
            elif name == 'RVA':
                y += egm(t, [(v_local(t0, typ), 1.5 if typ != 'n' else 1.4) for t0, typ in beats], w=1.8, frac=1)
            elif name.startswith('LV') or name.startswith('Nodo') or name.startswith('AD '):
                y += egm(t, [(far_v(t0, typ, 4), 0.8) for t0, typ in beats], w=2.0, frac=1)
            if name in extra:
                y += egm(t, [(tt, a) for tt, a, w in extra[name]], w=extra[name][0][2] if extra[name] else 1.0)
            return y
        return f

    names = sc.get('channels', ['HRA', 'His p', 'His d'] + CS_NAMES + ['RVA'])
    channels = [('I', lambda t: surface(t, 'I'), 'surf', 26), ('aVF', lambda t: surface(t, 'aVF'), 'surf', 26),
                ('V1', lambda t: surface(t, 'V1'), 'surf', 26)] + \
               [(n, channel(n), 'icd', 14 if n.startswith('CS') else 16) for n in names]
    H = TOP + ROWH * len(channels) + 40
    X = lambda t: LEFT + (t - T0) * PXMS
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Helvetica,Arial,sans-serif">',
           f'<rect width="{W}" height="{H}" fill="#fff"/>']
    t = (T0 // 100 + 1) * 100
    while t < T1:
        out.append(f'<line x1="{X(t):.1f}" x2="{X(t):.1f}" y1="{TOP-8}" y2="{H-34}" stroke="#eef0f4" stroke-width="0.6"/>')
        t += 100
    for i, (name, fn, kind, gain) in enumerate(channels):
        y0 = TOP + ROWH * i + ROWH / 2
        pts = []
        wander = random.uniform(0, 6.28)
        for ms in range(T0, T1):
            v = fn(ms) * gain + random.gauss(0, 0.25 if kind == 'icd' else 0.18)
            if kind == 'surf':
                v += 0.8 * math.sin(ms / 900 + wander)
            for s in spikes:
                if 0 <= ms - s < 3:
                    big = name == sc.get('pace_ch', 'RVA')
                    v += (-22 if big else (-6 if kind == 'icd' else -3)) * (1 if ms - s < 2 else -0.6)
            for s in aspikes:
                if 0 <= ms - s < 3:
                    big = name == sc.get('apace_ch', 'HRA')
                    v += (-22 if big else (-5 if kind == 'icd' else -2)) * (1 if ms - s < 2 else -0.6)
            v = max(-ROWH * 0.62, min(ROWH * 0.62, v))
            pts.append(f'{X(ms):.1f},{y0 - v:.1f}')
        out.append(f'<text x="8" y="{y0+4:.1f}" font-size="10.5" font-weight="700" fill="#333">{name}</text>')
        out.append(f'<polyline fill="none" stroke="#151515" stroke-width="0.75" stroke-linejoin="round" points="{" ".join(pts)}"/>')
    rows = {n: i for i, (n, *_ ) in enumerate(channels)}
    for t1, t2, ch, label in sc.get('cal', []):
        y = TOP + ROWH * rows[ch] + 6
        out.append(f'<line x1="{X(t1):.1f}" x2="{X(t2):.1f}" y1="{y}" y2="{y}" stroke="#0a58ca" stroke-width="0.9"/>')
        for tt in (t1, t2):
            out.append(f'<line x1="{X(tt):.1f}" x2="{X(tt):.1f}" y1="{y-4}" y2="{y+4}" stroke="#0a58ca" stroke-width="0.9"/>')
        out.append(f'<text x="{(X(t1)+X(t2))/2:.1f}" y="{y-3}" font-size="9.5" text-anchor="middle" fill="#0a58ca">{label}</text>')
    for tt, ch, label in sc.get('marks', []):
        y = TOP + ROWH * rows[ch] + 8
        out.append(f'<text x="{X(tt):.1f}" y="{y}" font-size="9.5" text-anchor="middle" fill="#0a58ca">{label}</text>')
    out.append(f'<line x1="{W-20-100*PXMS:.1f}" x2="{W-20}" y1="{H-20}" y2="{H-20}" stroke="#333" stroke-width="1.2"/>')
    out.append(f'<text x="{W-20-50*PXMS:.1f}" y="{H-8}" font-size="9.5" text-anchor="middle" fill="#333">100 ms</text>')
    out.append(f'<text x="{LEFT}" y="{H-8}" font-size="9.5" fill="#666">REGISTRO SIMULADO · {sc["src"]}</text>')
    out.append('</svg>')
    open(path, 'w').write('\n'.join(out))
