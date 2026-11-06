"""ECG de 12 derivaciones simulado: un latido sinusal y una EV, por derivación.
Morfologías ilustrativas según la descripción de cada artículo (no calcadas de ninguna figura).
Uso: python3 ecg12.py <carpeta de simlib.py> <carpeta de salida> [claves]"""
import math, random, sys
sys.path.insert(0, sys.argv[1])
from simlib import g
OUT = sys.argv[2]

LEADS = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']

# QRS sinusal normal (desfase, ancho, amplitud) y T
SIN = {'I': [(10, 8, 0.7)], 'II': [(10, 8, 1.0)], 'III': [(10, 8, 0.4)], 'aVR': [(10, 8, -0.8)], 'aVL': [(10, 8, 0.25)],
       'aVF': [(10, 8, 0.7)], 'V1': [(4, 6, 0.2), (20, 9, -0.9)], 'V2': [(6, 7, 0.4), (22, 9, -1.0)],
       'V3': [(8, 8, 0.7), (24, 9, -0.7)], 'V4': [(10, 8, 1.1), (26, 8, -0.4)], 'V5': [(10, 8, 1.1), (26, 8, -0.2)],
       'V6': [(10, 8, 0.9), (26, 8, -0.1)]}
SIN_T = {'I': 0.2, 'II': 0.3, 'III': 0.1, 'aVR': -0.25, 'aVL': 0.08, 'aVF': 0.2, 'V1': 0.05, 'V2': 0.3,
         'V3': 0.35, 'V4': 0.3, 'V5': 0.25, 'V6': 0.2}

# EV del músculo papilar posteromedial (Doppalapudi 2008, Yamada 2010): BRD, eje superior, QRS ~150 ms,
# transición tardía (S en V5-V6).
PM = {'I': [(30, 18, 0.55)], 'II': [(30, 20, -0.7)], 'III': [(32, 20, -1.1)], 'aVR': [(30, 18, 0.15)],
      'aVL': [(30, 18, 0.75)], 'aVF': [(32, 20, -0.95)], 'V1': [(40, 26, 1.0)], 'V2': [(40, 24, 0.9)],
      'V3': [(30, 18, 0.7), (75, 20, -0.4)], 'V4': [(25, 16, 0.5), (70, 22, -0.7)],
      'V5': [(20, 12, 0.3), (65, 24, -0.9)], 'V6': [(18, 10, 0.2), (60, 24, -0.9)]}
# EV del anillo mitral anterolateral (Tada 2005): R en V1 (transición en V1), concordancia positiva con S en V6,
# eje inferior, DI negativo, muesca tardía en las inferiores (pared libre), QRS ~154 ms.
MA = {'I': [(35, 22, -0.6)], 'II': [(30, 20, 0.9), (85, 8, 0.25)], 'III': [(32, 22, 1.2), (88, 8, 0.3)],
      'aVR': [(32, 20, -0.5)], 'aVL': [(34, 22, -0.85)], 'aVF': [(31, 21, 1.05), (86, 8, 0.28)],
      'V1': [(40, 26, 1.0)], 'V2': [(40, 26, 1.1)], 'V3': [(40, 26, 1.1)], 'V4': [(40, 26, 1.0)],
      'V5': [(38, 24, 0.85), (95, 14, -0.2)], 'V6': [(36, 22, 0.6), (90, 16, -0.35)]}

ECGS = {
    'pm_ecg': dict(ev=PM, title='ECG de 12 derivaciones: latido sinusal y EV del músculo papilar posteromedial',
                   src='ilustrativo según Doppalapudi 2008 y Yamada 2010: BRD, eje superior, QRS ~150 ms, S en V5-V6',
                   qrs=150),
    'ma_ecg': dict(ev=MA, title='ECG de 12 derivaciones: latido sinusal y EV del anillo mitral anterolateral',
                   src='ilustrativo según Tada 2005: R en V1, concordancia positiva con S en V6, eje inferior, DI negativo, QRS ~154 ms',
                   qrs=154),
}


def render(key, sc, path):
    random.seed(7)
    T0, T1, PX = -80, 1500, 0.36
    sinus, ev = 100, 820
    LEFT, TOP, ROWH = 60, 48, 46
    W = int(LEFT + (T1 - T0) * PX + 20)
    H = TOP + ROWH * len(LEADS) + 46
    X = lambda t: LEFT + (t - T0) * PX
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Helvetica,Arial,sans-serif">',
           f'<rect width="{W}" height="{H}" fill="#fff"/>',
           f'<text x="8" y="17" font-size="11.5" font-weight="700" fill="#0a58ca">{sc["title"]}</text>']
    t = (T0 // 100 + 1) * 100
    while t < T1:
        out.append(f'<line x1="{X(t):.1f}" x2="{X(t):.1f}" y1="{TOP - 6}" y2="{H - 40}" stroke="#eef0f4" stroke-width="0.6"/>')
        t += 100
    for i, L in enumerate(LEADS):
        y0 = TOP + ROWH * i + ROWH / 2
        pts = []
        evq = sc['ev'][L]
        main = max(evq, key=lambda q: abs(q[2]))[2]
        for ms in range(T0, T1):
            v = g(ms, sinus - 70, 16, 0.12 if L not in ('aVR',) else -0.1)          # onda P sinusal
            v += sum(g(ms, sinus + m, s, a) for m, s, a in SIN[L])
            v += g(ms, sinus + 230, 45, SIN_T[L])
            v += sum(g(ms, ev + m, s, a) for m, s, a in evq)
            v += g(ms, ev + 280, 60, -0.35 * (1 if main > 0 else -1))               # T discordante de la EV
            v = v * 17 + random.gauss(0, 0.15)
            pts.append(f'{X(ms):.1f},{y0 - v:.1f}')
        out.append(f'<text x="8" y="{y0 + 4:.1f}" font-size="10.5" font-weight="700" fill="#333">{L}</text>')
        out.append(f'<polyline fill="none" stroke="#151515" stroke-width="0.8" stroke-linejoin="round" points="{" ".join(pts)}"/>')
    yq = TOP + ROWH * 1 + 8
    out.append(f'<line x1="{X(ev):.1f}" x2="{X(ev + sc["qrs"]):.1f}" y1="{yq}" y2="{yq}" stroke="#0a58ca" stroke-width="0.9"/>')
    for tt in (ev, ev + sc['qrs']):
        out.append(f'<line x1="{X(tt):.1f}" x2="{X(tt):.1f}" y1="{yq - 4}" y2="{yq + 4}" stroke="#0a58ca" stroke-width="0.9"/>')
    out.append(f'<text x="{X(ev + sc["qrs"] / 2):.1f}" y="{yq - 3}" font-size="9.5" text-anchor="middle" fill="#0a58ca">QRS {sc["qrs"]}</text>')
    out.append(f'<text x="{X(sinus):.1f}" y="{TOP - 8}" font-size="9.5" text-anchor="middle" fill="#0a58ca">sinusal</text>')
    out.append(f'<text x="{X(ev + 40):.1f}" y="{TOP - 8}" font-size="9.5" text-anchor="middle" fill="#0a58ca">EV</text>')
    out.append(f'<line x1="{W - 20 - 100 * PX:.1f}" x2="{W - 20}" y1="{H - 34}" y2="{H - 34}" stroke="#333" stroke-width="1.2"/>')
    out.append(f'<text x="{W - 20 - 50 * PX:.1f}" y="{H - 22}" font-size="9.5" text-anchor="middle" fill="#333">100 ms</text>')
    out.append(f'<text x="{LEFT}" y="{H - 8}" font-size="9.5" fill="#666">REGISTRO SIMULADO · {sc["src"]}</text>')
    out.append('</svg>')
    open(path, 'w').write('\n'.join(out))


if __name__ == '__main__':
    for k in (sys.argv[3:] or list(ECGS)):
        render(k, ECGS[k], f'{OUT}/{k}.svg')
        print(k)
