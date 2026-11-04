"""Registros simulados para las fichas que no tenían imagen.
Los valores publicados se rotulan como tales; el resto es ilustrativo y la leyenda lo aclara.
Algunos escenarios tienen dos paneles (A y B) que png.js renderiza por separado y se unen después."""
import sys
sys.path.insert(0, sys.argv[1])
from simlib import render
OUT = sys.argv[2]
HV = 45
S = {}
CH6 = ['HRA', 'His p', 'His d', 'CS 9-10', 'CS 1-2', 'RVA']

# 1. Estudio basal: salto AH con extraestímulos auriculares (doble fisiología nodal). Valores ilustrativos.
def salto(s2, ah2, title, cal2):
    sp = [0, 600, 600 + s2]
    ah = [90, 90, ah2]
    hs = [s + 28 + a for s, a in zip(sp, ah)]
    return dict(win=(-80, 1450), pxms=0.42, title=title, channels=CH6,
        src='valores ilustrativos (salto AH ≥ 50 ms = doble vía nodal; Knight 2000)',
        beats=[(h + HV, 'n') for h in hs], aspikes=sp, apace_ch='HRA',
        atr=[(s + 5, 'sinus', 1) for s in sp], h_ante=hs,
        cal=[(sp[0], sp[1], 'HRA', 'S1 600'), (sp[1], sp[2], 'HRA', f'S2 {s2}'), (sp[2] + 28, hs[2], 'His d', cal2)])
S['pre_salto_a'] = salto(310, 170, 'A. S1-S2 600-310 ms', 'AH 170')
S['pre_salto_b'] = salto(300, 270, 'B. S1-S2 600-300 ms: el AH salta 100 ms (vía lenta)', 'AH 270')

# 2. Adenosina: TRNAV típica que termina en una A (bloqueo AV). Ilustrativo.
LC = 380
vs = [0, 380]
A = [50, 430]                       # VA 50, AH 285
h2 = A[1] + 330                     # el AH se alarga con la adenosina
vs.append(h2 + HV); A.append(vs[-1] + 50)   # último latido: la A retrógrada no conduce
sin_a = A[-1] + 1000
S['ado_term'] = dict(win=(-80, 2050), pxms=0.36, channels=CH6,
    src='ilustrativo: TRNAV típica que termina con adenosina en una A (bloqueo AV)',
    beats=[(v, 'n') for v in vs] + [(sin_a + 28 + 90 + HV, 'n')],
    atr=[(a, 'conc_his', -1) for a in A] + [(sin_a, 'sinus', 1)],
    h_ante=[v - HV for v in vs] + [sin_a + 28 + 90],
    cal=[(vs[0], vs[1], 'RVA', 'LC 380'), (A[1] + 0, h2, 'His d', 'AH se alarga')],
    marks=[(A[-1] + 70, 'His p', 'termina en A'), (sin_a, 'V1', 'sinusal')])

# 3. SA−VA: TRAV posteroseptal (Michaud 2001): estimulación del ápex a 440, SA−VA 40, PPI−LC 80. LC 470 y VA 120 ilustrativos.
LC, VA = 470, 120
svt = [0, LC]; sp = [800, 1240, 1680]
A = [v + VA for v in svt] + [s + VA + 40 for s in sp]
ret = sp[-1] + LC + 80; after = [ret, ret + LC]
S['michaud01'] = dict(win=(-80, 2750), pxms=0.27, channels=['HRA', 'His p', 'His d'] + ['CS 9-10', 'CS 5-6', 'CS 1-2', 'RVA'],
    src='Michaud 2001: estimulación del ápex a 440, SA−VA 40 y PPI−LC 80 (TRAV posteroseptal); LC 470 y VA 120 ilustrativos',
    beats=[(v, 'n') for v in svt + after] + [(s, 'pa') for s in sp], spikes=sp,
    atr=[(a, 'conc_cs', -1) for a in A + [v + VA for v in after]],
    h_ante=[v - HV for v in svt + after],
    cal=[(svt[1], svt[1] + VA + 2, 'CS 9-10', 'VA'), (sp[-1], A[-1] + 2, 'CS 9-10', 'SA'), (sp[-1], ret + 2, 'RVA', 'PPI'),
         (sp[0], sp[1], 'RVA', 'estim. 440')],
    marks=[(sp[1] + 200, 'I', 'SA − VA 40 · PPI − LC 80 → TRAV')])

# 4. Para-Hisiana (Veenhuyzen 2012, fig. 3): con vía para-Hisiana el SA no cambia al perder la captura del His;
#    después de la ablación se alarga 61 ms. SA 90 ilustrativo.
def parahis(sa_nc, title, lab):
    sp = [0, 600, 1200, 1800]
    cap = [True, False, True, False]
    beats = [(s + HV if c else s, 'n' if c else 'pa') for s, c in zip(sp, cap)]
    A = [s + (90 if c else sa_nc) for s, c in zip(sp, cap)]
    return dict(win=(-80, 2150), pxms=0.34, title=title, channels=['HRA', 'His p', 'His d', 'CS 9-10', 'CS 1-2', 'RVA'],
        src='Veenhuyzen 2012, fig. 3 (Δ 61 ms publicado); SA 90 ilustrativo', spikes=sp, pace_ch='His p',
        beats=beats, atr=[(a, 'conc_his', -1) for a in A],
        cal=[(sp[0], A[0] + 2, 'His d', 'SA (H+V)'), (sp[1], A[1] + 2, 'His d', lab)],
        marks=[(sp[0] + 30, 'V1', 'captura del His'), (sp[1] + 40, 'V1', 'solo V')])
S['parahis_a'] = parahis(90, 'A. Con la vía: el SA no cambia al perder la captura del His (respuesta extranodal)', 'SA igual')
S['parahis_b'] = parahis(151, 'B. Después de ablacionar la vía: el SA se alarga 61 ms (respuesta nodal)', 'SA + 61')

# 5. Sobreestimulación auricular (Veenhuyzen 2012, fig. 5): TRNAV de LC 350, estimulación de la AD a 340;
#    PR > RR durante la estimulación (vía lenta) y VA del último latido igual al de la TSV (VA linking). AH 255 y VA 50 ilustrativos.
VA, AH = 50, 255
vs = [0, 350, 700]
A = [vs[0] + VA, vs[1] + VA]
sp = [600, 940, 1280, 1620]
pv = [s + 28 + 330 + HV for s in sp]
vs += pv
lastA = pv[-1] + VA
vs += [lastA + AH + HV, lastA + AH + HV + 350]
A += [s + 5 for s in sp]
atr = [(a, 'conc_his', -1) for a in A[:2]] + [(a, 'sinus', 1) for a in A[2:]] + [(lastA, 'conc_his', -1), (vs[-2] + VA, 'conc_his', -1), (vs[-1] + VA, 'conc_his', -1)]
S['veen12_aop'] = dict(win=(-80, 2800), pxms=0.27, channels=CH6,
    src='Veenhuyzen 2012, fig. 5: LC 350, estimulación de la AD a 340 (publicados); AH y VA ilustrativos',
    beats=[(v, 'n') for v in vs], aspikes=sp, apace_ch='HRA', atr=atr, h_ante=[v - HV for v in vs],
    cal=[(vs[0], vs[1], 'RVA', 'LC 350'), (sp[1], sp[2], 'HRA', 'estim. 340'), (vs[0], A[0] + 2, 'CS 9-10', 'VA'), (pv[-1], lastA + 2, 'CS 9-10', 'VA igual')],
    marks=[(sp[2] + 200, 'His p', 'PR > RR: vía lenta'), (lastA + 60, 'His p', 'VA linking')])

# 6. Rama-rama (Cáceres 1989): HV 80 durante la TV, disociación AV, His → rama derecha → V. LC 300 ilustrativa.
LC = 300
vs = [i * LC for i in range(8)]
sin_a = [150, 950, 1750]
S['caceres89'] = dict(win=(-80, 2150), pxms=0.34, channels=['HRA', 'His d', 'RB', 'RVA'],
    src='Cáceres 1989: HV 80 ms y disociación AV (publicados); LC 300 y H-RB ilustrativos',
    beats=[(v, 'lb') for v in vs], atr=[(a, 'sinus', 1) for a in sin_a], h_ante=[v - 80 for v in vs],
    extra={'RB': [(v - 50, 0.8, 0.6) for v in vs] + [(v + 20, 0.5, 2.0) for v in vs]},
    cal=[(vs[3] - 80, vs[3], 'His d', 'HV 80'), (vs[1], vs[2], 'RVA', 'LC 300')],
    marks=[(vs[5] - 80, 'His d', 'H'), (vs[5] - 50, 'RB', 'RB'), (sin_a[1] + 30, 'aVF', 'A disociada')])

# 7. Músculo papilar posteromedial (Doppalapudi 2008): EV con BRD y eje superior, QRS ancho; en el sitio de origen
#    el V local precede al QRS sin potencial de Purkinje previo. Tiempos ilustrativos.
sin = [0, 900]
pvc = 1420
S['pm_doppa'] = dict(win=(-100, 1800), pxms=0.42, channels=['His d', 'Abl d', 'Abl p', 'RVA'],
    src='ilustrativo según Doppalapudi 2008: BRD con eje superior, QRS 136–170 ms, sin potencial de Purkinje previo',
    beats=[(s + 160, 'n') for s in sin] + [(pvc, 'pm')], atr=[(s, 'sinus', 1) for s in sin], h_ante=[s + 115 for s in sin],
    extra={'Abl d': [(s + 160 + 35, 0.9, 1.4) for s in sin] + [(pvc - 22, 1.3, 1.6)],
           'Abl p': [(s + 160 + 42, 0.8, 1.4) for s in sin] + [(pvc - 10, 1.1, 1.6)]},
    cal=[(pvc - 22, pvc, 'Abl d', 'V local −22')],
    marks=[(pvc + 60, 'I', 'EV: BRD, eje superior'), (pvc - 30, 'Abl p', 'sin potencial de Purkinje previo')])

# 8. Anillo mitral anterolateral (Tada 2005): R en V1 (transición en V1), eje inferior, QRS ~154 ms.
#    En el anillo, A pequeña y V grande; V local precoz. Tiempos ilustrativos.
S['tada05'] = dict(win=(-100, 1800), pxms=0.42, channels=['His d', 'CS 1-2', 'Abl d', 'RVA'],
    src='ilustrativo según Tada 2005: transición en V1, eje inferior, QRS ~154 ms; electrograma auricular pequeño en el anillo',
    beats=[(s + 160, 'n') for s in sin] + [(pvc, 'mal')], atr=[(s, 'sinus', 1) for s in sin], h_ante=[s + 115 for s in sin],
    extra={'Abl d': [(s + 70, 0.25, 1.0) for s in sin] + [(s + 160 + 45, 1.0, 1.4) for s in sin] + [(pvc - 25, 1.4, 1.6)]},
    cal=[(pvc - 25, pvc, 'Abl d', 'V local −25')],
    marks=[(pvc + 60, 'I', 'EV: R en V1, eje inferior'), (sin[1] + 70, 'Abl d', 'A pequeña, V grande')])

# 9. Vía oblicua (Jackman 1988): durante una TRAV por vía lateral izquierda, catéter ortogonal sobre la vía:
#    V, potencial de la vía y A. Tiempos ilustrativos.
LC, VA = 340, 115
vs = [i * LC for i in range(5)]
S['jackman88'] = dict(win=(-60, 1600), pxms=0.48, channels=['HRA', 'His d', 'CS 9-10', 'CS 5-6', 'CS 1-2', 'Abl d', 'RVA'],
    src='ilustrativo según Jackman 1988: potencial de la vía entre el V y la A con un catéter orientado sobre el anillo',
    beats=[(v, 'n') for v in vs], atr=[(v + VA, 'left', -1) for v in vs], h_ante=[v - HV for v in vs],
    extra={'Abl d': [(v + 35, 0.9, 1.4) for v in vs] + [(v + 80, 0.55, 0.5) for v in vs] + [(v + VA + 2, 1.0, 1.0) for v in vs]},
    marks=[(vs[2] + 80, 'Abl d', 'potencial de la vía'), (vs[2] + VA, 'CS 1-2', 'A más precoz')])

if __name__ == '__main__':
    only = sys.argv[3:] or list(S)
    for k in only:
        render(S[k], f'{OUT}/{k}.svg')
        print(k)
