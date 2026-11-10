"""Caso 1 (TRNAV típica, LC 340 como el ECG real del caso, VA 15): registros simulados de todas las maniobras.
Valores ilustrativos, coherentes con los del caso. Los escenarios con _a y _b son dos paneles que se unen después."""
import sys
sys.path.insert(0, sys.argv[1])
from simlib import render
OUT = sys.argv[2]
HV = 45
S = {}
CH6 = ['HRA', 'His p', 'His d', 'CS 9-10', 'CS 1-2', 'RVA']
SRC = 'caso 1 (didáctico): LC 340 y VA 15 como el caso; el resto, ilustrativo'
LC, VA = 340, 15

# --- PPI − LC y SA − VA, medidos sobre la misma sobreestimulación ventricular (ápex a 310) ---
SC, SA, PPI = 310, 190, 510
svt = [0, LC, 2 * LC]
sp = [svt[-1] + 290 + SC * k for k in range(6)]
A = [v + VA for v in svt] + [s + SA for s in sp]
ret = sp[-1] + PPI
after = [ret, ret + LC]
S['p1_medidas'] = dict(win=(-80, after[-1] + 250), pxms=0.25, title='Medidas sobre la sobreestimulación ventricular (ápex del VD a 310 ms): PPI, SA y HA',
    channels=CH6, src=SRC,
    beats=[(v, 'n') for v in svt + after] + [(s, 'pa') for s in sp], spikes=sp,
    atr=[(a, 'trnav', -1) for a in A + [v + VA for v in after]],
    h_ante=[v - HV for v in svt + after], h_retro=[s + SA - 85 for s in sp],
    cal=[(svt[0], svt[1], 'RVA', f'LC {LC}'), (svt[1], svt[1] + VA, 'CS 9-10', f'VA {VA}'),
         (sp[-1], A[-1] + 2, 'CS 9-10', f'SA {SA}'), (sp[-1], ret + 2, 'RVA', f'PPI {PPI}'),
         (svt[1] - HV, svt[1] + VA, 'His p', f'HA {HV + VA}'), (sp[-1] + SA - 85, A[-1], 'His p', 'HA 85')],
    marks=[(sp[-1] + 260, 'I', f'SA − VA = {SA} − {VA} = {SA - VA} ms'), (sp[-1] + 260, 'aVF', f'PPI − LC = {PPI} − {LC} = {PPI - LC} ms'), (sp[-1] + 260, 'V1', f'ΔHA = 85 − {HV + VA} = +{85 - HV - VA} ms')])


# --- Encarrilamiento diferencial: ápex (SA 190) y base del VD (SA 225) a 310 ms ---
def diff(sa, typ, title):
    svt = [0, LC]
    sp = [600 + SC * k for k in range(6)]
    A = [v + VA for v in svt] + [s + sa for s in sp]
    ret = sp[-1] + PPI + (sa - SA)
    return dict(win=(-80, ret + LC + 250), pxms=0.22, channels=CH6, title=title, spikes=sp, pace_ch='RVA', src=SRC,
        beats=[(v, 'n') for v in svt] + [(s, typ) for s in sp] + [(ret, 'n'), (ret + LC, 'n')],
        atr=[(a, 'trnav', -1) for a in A] + [(ret + VA, 'trnav', -1), (ret + LC + VA, 'trnav', -1)],
        h_ante=[v - HV for v in svt] + [ret - HV, ret + LC - HV], h_retro=[s + 120 + (sa - SA) for s in sp],
        cal=[(svt[1], svt[1] + VA + 2, 'CS 9-10', f'VA {VA}'), (sp[-1], A[-1] + 2, 'CS 9-10', f'SA {sa}'),
             (svt[0], svt[1], 'RVA', f'LC {LC}')])


S['p1_diff_a'] = diff(190, 'pa', 'A. Encarrilamiento desde el ápex del VD (310 ms)')
S['p1_diff_b'] = diff(225, 'pb', 'B. Encarrilamiento desde la base del VD (310 ms)')

# --- Sobreestimulación auricular desde la AD alta a 320 ms: al cortar, VA del primer latido = VA de la TSV ---
AHs = 260
vs = [0, LC, 2 * LC]
A = [v + VA for v in vs]
sp = [A[-1] + 250 + 320 * k for k in range(6)]
pv = [s + 28 + AHs + HV for s in sp]
vs2 = [pv[-1] + LC, pv[-1] + 2 * LC]
S['p1_aop'] = dict(win=(-80, vs2[-1] + 250), pxms=0.22, title='Sobreestimulación auricular desde la AD alta a 320 ms', channels=CH6, src=SRC,
    beats=[(v, 'n') for v in vs + pv + vs2], aspikes=sp, apace_ch='HRA',
    atr=[(a, 'trnav', -1) for a in A] + [(s + 5, 'sinus', 1) for s in sp] + [(v + VA, 'trnav', -1) for v in [pv[-1]] + vs2],
    h_ante=[v - HV for v in vs + pv + vs2],
    cal=[(vs[1], vs[1] + VA + 2, 'CS 9-10', f'VA {VA}'), (sp[-2], sp[-1], 'HRA', 'S-S 320'), (vs[0], vs[1], 'RVA', f'V-V {LC}'), (pv[-3], pv[-2], 'RVA', 'V-V 320'), (pv[-2], pv[-1], 'RVA', 'V-V 320'),
         (pv[-1], pv[-1] + VA + 2, 'CS 9-10', f'VA {VA}'), (sp[-1] + 28, pv[-1] - HV, 'His d', f'AH {AHs}')])


# --- Estudio basal: salto del AH (el mismo de la inducción) ---
def salto(s2, ah2, title, lab, eco):
    sp = [0, 600, 600 + s2]
    hs = [s + 28 + a for s, a in zip(sp, [90, 90, ah2])]
    vs = [h + HV for h in hs]
    atr = [(s + 5, 'sinus', 1) for s in sp] + ([(vs[2] + VA, 'trnav', -1)] if eco else [])
    return dict(win=(-80, 1650), pxms=0.40, title=title, channels=CH6, src=SRC,
        beats=[(v, 'n') for v in vs], aspikes=sp, apace_ch='HRA', atr=atr, h_ante=hs,
        cal=[(sp[1], sp[2], 'HRA', f'S2 {s2}'), (sp[1] + 28, hs[1], 'His d', 'AH 90'), (sp[2] + 28, hs[2], 'His d', lab)])


S['p1_pre_a'] = salto(310, 220, 'A. Extraestímulo auricular S1-S2 600-310', 'AH 220', False)
S['p1_pre_b'] = salto(300, 280, 'B. S2 10 ms más corto: S1-S2 600-300', 'AH 280', True)


# --- Para-Hisiana en ritmo sinusal: al perder la captura del His el SA se alarga 50 ms, misma secuencia ---
def parahis():
    sp = [0, 650, 1300, 1950]
    cap = [True, False, True, False]
    beats = [(s + HV if c else s, 'n' if c else 'pa') for s, c in zip(sp, cap)]
    A = [s + (80 if c else 130) for s, c in zip(sp, cap)]
    return dict(win=(-80, 2300), pxms=0.32, title='Estimulación para-Hisiana en ritmo sinusal', channels=CH6, src=SRC,
        spikes=sp, pace_ch='His p', beats=beats, atr=[(a, 'trnav', -1) for a in A],
        cal=[(sp[0], A[0] + 2, 'HRA', 'SA 80'), (sp[1], A[1] + 2, 'HRA', 'SA 130'),
             (sp[2] + HV, sp[2] + HV + 95, 'RVA', 'QRS 95'), (sp[3], sp[3] + 150, 'RVA', 'QRS 150')],
        marks=[(sp[0] + 30, 'V1', 'His + V'), (sp[1] + 40, 'V1', 'solo V')])


S['p1_parahis'] = parahis()

# --- Adenosina: la TSV termina con una A (la última A retrógrada no conduce) ---
vs = [0, LC, 2 * LC, 3 * LC]
A = [v + VA for v in vs]
hs = [v - HV for v in vs]
S['p1_ado'] = dict(win=(-80, A[-1] + 900), pxms=0.25, title='Adenosina IV durante la taquicardia', channels=CH6, src=SRC,
    beats=[(v, 'n') for v in vs], atr=[(a, 'trnav', -1) for a in A], h_ante=hs,
    cal=[(vs[1], vs[2], 'RVA', f'LC {LC}'), (vs[3], A[3] + 2, 'CS 9-10', f'VA {VA}')],
    marks=[(A[3] + 60, 'aVF', 'última: A sin V')])

# --- EV con His refractario: no modifica la A siguiente ---
k = 3
vs = [i * LC for i in range(k)]
h_exp = k * LC - HV
spk = h_exp
A = [v + VA for v in vs] + [k * LC + VA]
after = [k * LC + LC, k * LC + 2 * LC]
A += [v + VA for v in after]
S['p1_ehr'] = dict(win=(-80, after[-1] + 200), pxms=0.30, title='EV con His refractario durante la taquicardia', channels=CH6, src=SRC,
    spikes=[spk], pace_ch='RVA', beats=[(v, 'n') for v in vs] + [(spk, 'pa')] + [(v, 'n') for v in after],
    atr=[(a, 'trnav', -1) for a in A], h_ante=[v - HV for v in vs] + [h_exp] + [v - HV for v in after],
    cal=[(A[k - 2] + 2, A[k - 1] + 2, 'CS 9-10', f'A-A {LC}'), (A[k - 1] + 2, A[k] + 2, 'CS 9-10', f'A-A {LC}')],
    marks=[(spk, 'V1', 'EV'), (h_exp, 'His p', 'H')])

# --- EA con His refractario desde el ostium del SC: el His siguiente se retrasa 14 ms ---
hs = [i * LC - HV for i in range(7)]
apb = hs[4] + 10
hs = hs[:5] + [h + 14 for h in hs[5:]]
vs = [h + HV for h in hs]
A = [v + VA for k2, v in enumerate(vs) if k2 != 4]
S['p1_eha'] = dict(win=(-100, vs[-1] + 250), pxms=0.25, title='EA con His refractario desde el ostium del SC', channels=CH6, src=SRC,
    beats=[(x, 'n') for x in vs], aspikes=[apb], apace_ch='CS 9-10',
    atr=[(a, 'trnav', -1) for a in A] + [(apb + 4, 'conc_cs', 1)], h_ante=hs,
    cal=[(hs[3], hs[4], 'His d', f'H-H {LC}'), (hs[4], hs[5], 'His d', f'H-H {LC + 14}')],
    marks=[(apb, 'V1', 'EA')])

# =====================================================================================================
# Caso 2 (TRAV por vía septal; LC 280 como el ECG real del caso, VA 110, A más precoz en el ostium del SC).
# Michaud 2001: SA−VA 40, PPI−LC 80; ΔHA −45 y EV-HR que adelanta 25 ms, ilustrativos.
SRC2 = 'caso 2 (didáctico): LC 280 y VA 110 como el caso; el resto, ilustrativo'
LC2, VA2, SC2, SA2, PPI2, HAt2, HAp2 = 280, 110, 250, 150, 360, 155, 110


def vop2(title, med):
    svt = [0, LC2, 2 * LC2]
    sp = [svt[-1] + 230 + SC2 * k for k in range(6)]
    A = [v + VA2 for v in svt] + [s + SA2 for s in sp]
    ret = sp[-1] + PPI2
    after = [ret, ret + LC2]
    cal = [(svt[0], svt[1], 'RVA', f'LC {LC2}'), (svt[1], svt[1] + VA2 + 2, 'CS 9-10', f'VA {VA2}'),
           (sp[-2], sp[-1], 'RVA', f'S-S {SC2}'), (A[-2] + 2, A[-1] + 2, 'HRA', f'A-A {SC2}'),
           (sp[-1], A[-1] + 2, 'CS 9-10', f'SA {SA2}'), (sp[-1], ret + 2, 'RVA', f'PPI {PPI2}')]
    marks = []
    if med:
        cal += [(svt[1] - HV, svt[1] + VA2, 'His p', f'HA {HAt2}'), (sp[-1] + SA2 - HAp2, A[-1], 'His p', f'HA {HAp2}')]
        marks = [(sp[-1] + 200, 'I', f'SA − VA = {SA2} − {VA2} = {SA2 - VA2} ms'), (sp[-1] + 200, 'aVF', f'PPI − LC = {PPI2} − {LC2} = {PPI2 - LC2} ms'),
                 (sp[-1] + 200, 'V1', f'ΔHA = {HAp2} − {HAt2} = {HAp2 - HAt2} ms')]
    return dict(win=(-80, after[-1] + 220), pxms=0.28, title=title, channels=CH6, src=SRC2,
        beats=[(v, 'n') for v in svt + after] + [(s, 'pa') for s in sp], spikes=sp,
        atr=[(a, 'conc_cs', -1) for a in A + [v + VA2 for v in after]],
        h_ante=[v - HV for v in svt + after], h_retro=[s + SA2 - HAp2 for s in sp], cal=cal, marks=marks)


S['p2_vop'] = vop2('Sobreestimulación ventricular desde el ápex del VD a 250 ms', False)
S['p2_medidas'] = vop2('Medidas sobre la sobreestimulación ventricular (ápex del VD a 250 ms): PPI, SA y HA', True)


def diff2(sa, typ, title):
    svt = [0, LC2]
    sp = [600 + SC2 * k for k in range(6)]
    A = [v + VA2 for v in svt] + [s + sa for s in sp]
    ret = sp[-1] + PPI2 + (sa - SA2)
    return dict(win=(-80, ret + LC2 + 220), pxms=0.24, channels=CH6, title=title, spikes=sp, pace_ch='RVA', src=SRC2,
        beats=[(v, 'n') for v in svt] + [(s, typ) for s in sp] + [(ret, 'n'), (ret + LC2, 'n')],
        atr=[(a, 'conc_cs', -1) for a in A] + [(ret + VA2, 'conc_cs', -1), (ret + LC2 + VA2, 'conc_cs', -1)],
        h_ante=[v - HV for v in svt] + [ret - HV, ret + LC2 - HV], h_retro=[s + sa - HAp2 for s in sp],
        cal=[(svt[1], svt[1] + VA2 + 2, 'CS 9-10', f'VA {VA2}'), (sp[-1], A[-1] + 2, 'CS 9-10', f'SA {sa}'), (svt[0], svt[1], 'RVA', f'LC {LC2}')])


S['p2_diff_a'] = diff2(150, 'pa', 'A. Encarrilamiento desde el ápex del VD (250 ms)')
S['p2_diff_b'] = diff2(140, 'pb', 'B. Encarrilamiento desde la base del VD (250 ms)')


def ehr2():
    k = 3
    vs = [i * LC2 for i in range(k)]
    h_exp = k * LC2 - HV
    A = [v + VA2 for v in vs] + [k * LC2 + VA2 - 25]
    nxt = A[-1] + (LC2 - VA2)
    after = [nxt, nxt + LC2]
    A += [v + VA2 for v in after]
    return dict(win=(-80, after[-1] + 200), pxms=0.30, title='EV con His refractario durante la taquicardia', channels=CH6, src=SRC2,
        spikes=[h_exp], pace_ch='RVA', beats=[(v, 'n') for v in vs] + [(h_exp, 'pa')] + [(v, 'n') for v in after],
        atr=[(a, 'conc_cs', -1) for a in A], h_ante=[v - HV for v in vs] + [h_exp] + [v - HV for v in after],
        cal=[(A[k - 2] + 2, A[k - 1] + 2, 'CS 9-10', f'A-A {LC2}'), (A[k - 1] + 2, A[k] + 2, 'CS 9-10', f'A-A {LC2 - 25}')],
        marks=[(h_exp, 'V1', 'EV'), (h_exp, 'His p', 'H')])


S['p2_ehr'] = ehr2()


def parahis2():
    sp = [0, 650, 1300, 1950]
    cap = [True, False, True, False]
    beats = [(s + HV if c else s, 'n' if c else 'pa') for s, c in zip(sp, cap)]
    A = [s + 100 for s in sp]
    return dict(win=(-80, 2300), pxms=0.32, title='Estimulación para-Hisiana en ritmo sinusal', channels=CH6, src=SRC2,
        spikes=sp, pace_ch='His p', beats=beats, atr=[(a, 'conc_cs', -1) for a in A],
        cal=[(sp[0], A[0] + 2, 'CS 9-10', 'SA 100'), (sp[1], A[1] + 2, 'CS 9-10', 'SA 100'),
             (sp[2] + HV, sp[2] + HV + 95, 'RVA', 'QRS 95'), (sp[3], sp[3] + 150, 'RVA', 'QRS 150')],
        marks=[(sp[0] + 30, 'V1', 'His + V'), (sp[1] + 40, 'V1', 'solo V')])


S['p2_parahis'] = parahis2()

# Estudio basal: estimulación del VD a 500 y 400 ms, SA 125 en los dos (no decremental), concéntrica con la A precoz en el ostium del SC.
sp = [0, 500, 1000, 1400, 1800]
S['p2_pre'] = dict(win=(-80, 2150), pxms=0.30, title='Estimulación ventricular en ritmo sinusal: 500 y 400 ms', channels=CH6, src=SRC2,
    spikes=sp, beats=[(s, 'pa') for s in sp], atr=[(s + 125, 'conc_cs', -1) for s in sp], h_retro=[s + 60 for s in sp],
    cal=[(sp[0], sp[1], 'RVA', 'S-S 500'), (sp[1], sp[1] + 127, 'CS 9-10', 'SA 125'), (sp[2], sp[3], 'RVA', 'S-S 400'), (sp[3], sp[3] + 127, 'CS 9-10', 'SA 125')])

# Sobreestimulación auricular desde la AD alta a 260 ms: al cortar, VA del primer latido = 110.
AHs2 = 150
vs = [0, LC2, 2 * LC2]
A = [v + VA2 for v in vs]
sp = [A[-1] + 200 + 260 * k for k in range(6)]
pv = [s + 28 + AHs2 + HV for s in sp]
vs2 = [pv[-1] + LC2, pv[-1] + 2 * LC2]
S['p2_aop'] = dict(win=(-80, vs2[-1] + 220), pxms=0.22, title='Sobreestimulación auricular desde la AD alta a 260 ms', channels=CH6, src=SRC2,
    beats=[(v, 'n') for v in vs + pv + vs2], aspikes=sp, apace_ch='HRA',
    atr=[(a, 'conc_cs', -1) for a in A] + [(s + 5, 'sinus', 1) for s in sp] + [(v + VA2, 'conc_cs', -1) for v in [pv[-1]] + vs2],
    h_ante=[v - HV for v in vs + pv + vs2],
    cal=[(vs[1], vs[1] + VA2 + 2, 'CS 9-10', f'VA {VA2}'), (vs[0], vs[1], 'RVA', f'V-V {LC2}'), (sp[-2], sp[-1], 'HRA', 'S-S 260'),
         (pv[-2], pv[-1], 'RVA', 'V-V 260'), (pv[-1], pv[-1] + VA2 + 2, 'CS 9-10', f'VA {VA2}')])

# Adenosina: termina con una A (bloqueo en el nodo).
vs = [0, LC2, 2 * LC2, 3 * LC2]
A = [v + VA2 for v in vs]
S['p2_ado'] = dict(win=(-80, A[-1] + 900), pxms=0.25, title='Adenosina IV durante la taquicardia', channels=CH6, src=SRC2,
    beats=[(v, 'n') for v in vs], atr=[(a, 'conc_cs', -1) for a in A], h_ante=[v - HV for v in vs],
    cal=[(vs[1], vs[2], 'RVA', f'LC {LC2}'), (vs[3], A[3] + 2, 'CS 9-10', f'VA {VA2}')],
    marks=[(A[3] + 60, 'aVF', 'última: A sin V')])

# =====================================================================================================
# Maniobras que faltaban en los casos 1 y 2: sobreestimulación desde el VI basal, EA con His refractario (caso 2)
# y mapa de activación auricular durante la taquicardia.
CHMAP = ['HRA', 'His p', 'His d', 'CS 9-10', 'CS 7-8', 'CS 5-6', 'CS 3-4', 'CS 1-2', 'RVA']


def vopvi(LCx, VAx, seq, SCx, SAx, PPIx, src, ch=CH6):
    svt = [0, LCx, 2 * LCx]
    sp = [svt[-1] + 230 + SCx * k for k in range(6)]
    A = [v + VAx for v in svt] + [s + SAx for s in sp]
    ret = sp[-1] + PPIx
    after = [ret, ret + LCx]
    return dict(win=(-80, after[-1] + 220), pxms=0.26, title=f'Sobreestimulación desde el VI basal (rama del SC) a {SCx} ms', channels=ch, src=src,
        beats=[(v, 'n') for v in svt + after] + [(s, 'lv') for s in sp], spikes=sp, pace_ch='CS 1-2',
        atr=[(a, seq, -1) for a in A + [v + VAx for v in after]], h_ante=[v - HV for v in svt + after],
        cal=[(svt[0], svt[1], 'RVA', f'LC {LCx}'), (svt[1], svt[1] + VAx + 2, 'CS 9-10', f'VA {VAx}'),
             (sp[-2], sp[-1], 'RVA', f'S-S {SCx}'), (sp[-1], A[-1] + 2, 'CS 9-10', f'SA {SAx}'), (sp[-1], ret + 2, 'RVA', f'PPI {PPIx}')])


S['p1_vopvi'] = vopvi(LC, VA, 'trnav', 310, 215, 545, SRC)
S['p2_vopvi'] = vopvi(LC2, VA2, 'conc_cs', 250, 165, 380, SRC2)


def mapa(LCx, VAx, seq, src, lab):
    vs = [i * LCx for i in range(4)]
    return dict(win=(-80, vs[-1] + 260), pxms=0.42, title='Activación auricular durante la taquicardia (AD alta, His y SC 9-10 a 1-2)',
        channels=CHMAP, src=src, beats=[(v, 'n') for v in vs], atr=[(v + VAx, seq, -1) for v in vs], h_ante=[v - HV for v in vs],
        cal=[(vs[0], vs[1], 'RVA', f'LC {LCx}'), (vs[1], vs[1] + VAx + 2, 'His d', f'VA {VAx}')])


S['p1_mapa'] = mapa(LC, VA, 'trnav', SRC, 'A más precoz en el His; el SC distal y la AD alta, 16 ms después')
S['p2_mapa'] = mapa(LC2, VA2, 'conc_cs', SRC2, 'A más precoz en el SC 9-10 (ostium); el SC distal y la AD alta, 36-38 ms después')

# Caso 2: EA con His refractario desde el ostium del SC: el His siguiente sale a su tiempo.
hs = [i * LC2 - HV for i in range(7)]
apb = hs[4] + 10
vs = [h + HV for h in hs]
A = [v + VA2 for k2, v in enumerate(vs) if k2 != 4]
S['p2_eha'] = dict(win=(-100, vs[-1] + 250), pxms=0.25, title='EA con His refractario desde el ostium del SC', channels=CH6, src=SRC2,
    beats=[(x, 'n') for x in vs], aspikes=[apb], apace_ch='CS 9-10',
    atr=[(a, 'conc_cs', -1) for a in A] + [(apb + 4, 'conc_cs', 1)], h_ante=hs,
    cal=[(hs[3], hs[4], 'His d', f'H-H {LC2}'), (hs[4], hs[5], 'His d', f'H-H {LC2}')],
    marks=[(apb, 'V1', 'EA')])

# =====================================================================================================
# Caso 3 (TA incesante en una niña de 2 años; LC 270 como el ECG real). A → His 100, HV 45 (PR 145), VA 125.
SRC3 = 'caso 3 (didáctico): LC 270 como el caso; el resto, ilustrativo'
LC3, AH3, SC3 = 270, 100, 240
VA3 = LC3 - AH3 - HV


def ta_vop(title, med, sa=120, typ='pa', pace='RVA'):
    A0 = [0, LC3, 2 * LC3]
    vs0 = [a + AH3 + HV for a in A0]
    sp = [vs0[-1] + 200 + SC3 * k for k in range(6)]
    Aret = [s + sa for s in sp]
    focal = Aret[-1] + 330
    v_after = focal + AH3 + HV
    cal = [(A0[0], A0[1], 'HRA', f'A-A {LC3}'), (sp[-2], sp[-1], 'RVA', f'S-S {SC3}'), (Aret[-2], Aret[-1], 'HRA', f'A-A {SC3}'),
           (Aret[-1], focal, 'CS 9-10', f'A-A {focal - Aret[-1]}')]
    marks = [(Aret[-1], 'His p', 'A'), (focal, 'His p', 'A'), (v_after, 'aVF', 'V')]
    if med:
        cal = [(A0[0], A0[1], 'HRA', f'A-A {LC3}'), (vs0[0], A0[1] + 2, 'CS 9-10', f'VA {VA3}'), (sp[-1], Aret[-1] + 2, 'CS 9-10', f'SA {sa}'),
               (sp[-1], v_after + 2, 'RVA', f'PPI {v_after - sp[-1]}')]
        marks = [(sp[-1] + 300, 'I', f'SA − VA = {sa} − {VA3} = {sa - VA3} ms'), (sp[-1] + 300, 'aVF', f'PPI − LC = {v_after - sp[-1]} − {LC3} = {v_after - sp[-1] - LC3} ms')]
    return dict(win=(-80, v_after + 380), pxms=0.25, channels=CH6, title=title, src=SRC3, pace_ch=pace,
        beats=[(v, 'n') for v in vs0] + [(s, typ) for s in sp] + [(v_after, 'n'), (v_after + LC3, 'n')], spikes=sp,
        atr=[(a, 'cs_mid', 1) for a in A0] + [(a, 'conc_his', -1) for a in Aret] + [(focal, 'cs_mid', 1), (focal + LC3, 'cs_mid', 1)],
        h_ante=[v - HV for v in vs0] + [v_after - HV, v_after + LC3 - HV], h_retro=[s + sa - 10 for s in sp], cal=cal, marks=marks)


S['p3_vop'] = ta_vop('Sobreestimulación ventricular desde el ápex del VD a 240 ms', False)
S['p3_medidas'] = ta_vop('Medidas sobre la sobreestimulación ventricular (ápex del VD a 240 ms): PPI y SA', True)
S['p3_diff_a'] = ta_vop('A. Encarrilamiento desde el ápex del VD (240 ms)', True, 120, 'pa')
S['p3_diff_b'] = ta_vop('B. Encarrilamiento desde la base del VD (240 ms)', True, 145, 'pb')
for k in ('p3_diff_a', 'p3_diff_b'):
    S[k]['marks'] = []

# Adenosina: bloqueo AV 2:1 transitorio y la TA sigue.
A = [i * LC3 for i in range(9)]
cond = [0, 1, 2, 4, 6, 7, 8]
hs = [A[i] + AH3 for i in cond]
S['p3_ado'] = dict(win=(-80, A[-1] + 300), pxms=0.29, channels=CH6, title='Adenosina IV durante la taquicardia', src=SRC3,
    beats=[(h + HV, 'n') for h in hs], atr=[(a, 'cs_mid', 1) for a in A], h_ante=hs,
    cal=[(A[3], A[4], 'HRA', f'A-A {LC3}')], marks=[(A[3] + 30, 'aVF', 'A sin V'), (A[5] + 30, 'aVF', 'A sin V')])

# EV con His refractario: la A siguiente no cambia.
A = [i * LC3 for i in range(7)]
hs = [a + AH3 for a in A]
vs = [h + HV for h in hs]
ev = hs[3]
S['p3_ehr'] = dict(win=(-80, vs[-1] + 200), pxms=0.30, title='EV con His refractario durante la taquicardia', channels=CH6, src=SRC3,
    spikes=[ev], pace_ch='RVA', beats=[(v, 'n') for k2, v in enumerate(vs) if k2 != 3] + [(ev, 'pa')],
    atr=[(a, 'cs_mid', 1) for a in A], h_ante=hs,
    cal=[(A[2], A[3], 'CS 9-10', f'A-A {LC3}'), (A[3], A[4], 'CS 9-10', f'A-A {LC3}')], marks=[(ev, 'V1', 'EV'), (ev, 'His p', 'H')])

# EA con His refractario desde el ostium del SC: captura la aurícula y resetea el foco: la A y el His siguientes se retrasan.
A = [i * LC3 for i in range(4)]
ea = A[3] + AH3 + 10
A2 = [ea + 300, ea + 300 + LC3, ea + 300 + 2 * LC3]
hs = [a + AH3 for a in A] + [a + AH3 for a in A2]
vs = [h + HV for h in hs]
S['p3_eha'] = dict(win=(-80, vs[-1] + 220), pxms=0.27, title='EA con His refractario desde el ostium del SC', channels=CH6, src=SRC3,
    beats=[(v, 'n') for v in vs], aspikes=[ea], apace_ch='CS 9-10',
    atr=[(a, 'cs_mid', 1) for a in A + A2] + [(ea + 4, 'conc_cs', 1)], h_ante=hs,
    cal=[(hs[2], hs[3], 'His d', f'H-H {LC3}'), (hs[3], hs[4], 'His d', f'H-H {hs[4] - hs[3]}'), (ea, A2[0], 'CS 9-10', 'A-A 300')],
    marks=[(ea, 'V1', 'EA')])


# Sobreestimulación auricular desde dos sitios: el VA del primer latido de retorno cambia.
def ta_aop(site, ch, seq, ret, title):
    A0 = [0, LC3]
    sp = [A0[-1] + 200 + 240 * k for k in range(6)]
    pv = [s + 28 + AH3 + HV for s in sp]
    focal = sp[-1] + ret
    hs = [a + AH3 for a in A0] + [s + 28 + AH3 for s in sp] + [focal + AH3, focal + LC3 + AH3]
    vs = [h + HV for h in hs]
    return dict(win=(-80, vs[-1] + 220), pxms=0.22, title=title, channels=CH6, src=SRC3, beats=[(v, 'n') for v in vs],
        aspikes=sp, apace_ch=ch, atr=[(a, 'cs_mid', 1) for a in A0] + [(s + 5, seq, 1) for s in sp] + [(focal, 'cs_mid', 1), (focal + LC3, 'cs_mid', 1)],
        h_ante=hs, cal=[(sp[-2], sp[-1], ch, 'S-S 240'), (pv[-2], pv[-1], 'RVA', 'V-V 240'), (pv[-1], focal + 2, 'CS 9-10', f'VA {focal - pv[-1]}')])


S['p3_aop_a'] = ta_aop('AD alta', 'HRA', 'sinus', 330, 'A. Sobreestimulación auricular desde la AD alta a 240 ms')
S['p3_aop_b'] = ta_aop('ostium del SC', 'CS 9-10', 'conc_cs', 290, 'B. Desde el ostium del SC a 240 ms')

# Para-Hisiana en sinusal: respuesta nodal (el SA se alarga 50 ms).
sp = [0, 650, 1300, 1950]
cap = [True, False, True, False]
S['p3_parahis'] = dict(win=(-80, 2300), pxms=0.32, title='Estimulación para-Hisiana en ritmo sinusal', channels=CH6, src=SRC3,
    spikes=sp, pace_ch='His p', beats=[(s + HV if c else s, 'n' if c else 'pa') for s, c in zip(sp, cap)],
    atr=[(s + (85 if c else 135), 'conc_his', -1) for s, c in zip(sp, cap)],
    cal=[(sp[0], sp[0] + 87, 'HRA', 'SA 85'), (sp[1], sp[1] + 137, 'HRA', 'SA 135'), (sp[2] + HV, sp[2] + HV + 95, 'RVA', 'QRS 95'), (sp[3], sp[3] + 150, 'RVA', 'QRS 150')],
    marks=[(sp[0] + 30, 'V1', 'His + V'), (sp[1] + 40, 'V1', 'solo V')])

# Estudio basal: estimulación ventricular a 500 y 400: SA 140 y 190 (decremental), concéntrica por el nodo.
sp = [0, 500, 1000, 1400, 1800]
sas = [140, 140, 140, 190, 190]
S['p3_pre'] = dict(win=(-80, 2150), pxms=0.30, title='Estimulación ventricular en ritmo sinusal: 500 y 400 ms', channels=CH6, src=SRC3,
    spikes=sp, beats=[(s, 'pa') for s in sp], atr=[(s + a, 'conc_his', -1) for s, a in zip(sp, sas)], h_retro=[s + a - 60 for s, a in zip(sp, sas)],
    cal=[(sp[0], sp[1], 'RVA', 'S-S 500'), (sp[1], sp[1] + 142, 'HRA', 'SA 140'), (sp[2], sp[3], 'RVA', 'S-S 400'), (sp[3], sp[3] + 192, 'HRA', 'SA 190')])

# =====================================================================================================
# Caso 4 (TRAV por vía lateral izquierda; LC 340 y VA 115 de Veenhuyzen 2011, A más precoz en el SC 1-2, AH 180 en la TSV).
# Desde el ápex del VD: PPI−LC 140 y cPPI−LC 120 (AH +20) como Veenhuyzen; SA−VA 120 resulta de esos valores.
SRC4 = 'caso 4: LC 340, VA 115 y PPI−LC 140 de Veenhuyzen 2011; el resto, ilustrativo'
LC4, VA4, SC4, SA4, AH4, HV4 = 340, 115, 310, 235, 180, 45
PPI4 = SA4 + AH4 + 20 + HV4          # 480: el primer retorno conduce con AH 200


def vop4(title, med):
    svt = [0, LC4, 2 * LC4]
    sp = [svt[-1] + 260 + SC4 * k for k in range(6)]
    A = [v + VA4 for v in svt] + [s + SA4 for s in sp]
    ret = sp[-1] + PPI4
    after = [ret, ret + LC4]
    cal = [(svt[0], svt[1], 'RVA', f'LC {LC4}'), (svt[1], svt[1] + VA4 + 2, 'CS 1-2', f'VA {VA4}'),
           (sp[-2], sp[-1], 'RVA', f'S-S {SC4}'), (A[-3] + 2, A[-2] + 2, 'CS 1-2', f'A-A {SC4}'),
           (sp[-1], A[-1] + 2, 'CS 1-2', f'SA {SA4}'), (sp[-1], ret + 2, 'RVA', f'PPI {PPI4}')]
    marks = []
    if med:
        cal = [c for c in cal if not c[3].startswith(('S-S', 'A-A'))]
        cal += [(svt[1] - HV4 - AH4, svt[1] - HV4, 'His d', f'AH {AH4}'), (A[-1] + 2, ret - HV4, 'His d', f'AH {AH4 + 20}')]
        marks = [(sp[-1] + 260, 'I', f'SA − VA = {SA4} − {VA4} = {SA4 - VA4} ms'),
                 (sp[-1] + 260, 'aVF', f'PPI − LC = {PPI4} − {LC4} = {PPI4 - LC4} ms'),
                 (sp[-1] + 260, 'V1', f'cPPI − LC = {PPI4 - LC4} − ({AH4 + 20} − {AH4}) = {PPI4 - LC4 - 20} ms')]
    return dict(win=(-80, after[-1] + 220), pxms=0.25, title=title, channels=CH6, src=SRC4,
        beats=[(v, 'n') for v in svt + after] + [(s, 'pa') for s in sp], spikes=sp,
        atr=[(a, 'left', -1) for a in A + [v + VA4 for v in after]],
        h_ante=[v - HV4 for v in svt + after], h_retro=[s + 70 for s in sp], cal=cal, marks=marks)


S['p4_vop'] = vop4('Sobreestimulación ventricular desde el ápex del VD a 310 ms', False)
S['p4_medidas'] = vop4('Medidas sobre la sobreestimulación ventricular (ápex del VD a 310 ms): PPI, SA y AH', True)


def diff4(sa, typ, title):
    svt = [0, LC4]
    sp = [600 + SC4 * k for k in range(6)]
    A = [v + VA4 for v in svt] + [s + sa for s in sp]
    ret = sp[-1] + PPI4 + (sa - SA4)
    return dict(win=(-80, ret + LC4 + 220), pxms=0.22, channels=CH6, title=title, spikes=sp, pace_ch='RVA', src=SRC4,
        beats=[(v, 'n') for v in svt] + [(s, typ) for s in sp] + [(ret, 'n'), (ret + LC4, 'n')],
        atr=[(a, 'left', -1) for a in A] + [(ret + VA4, 'left', -1), (ret + LC4 + VA4, 'left', -1)],
        h_ante=[v - HV4 for v in svt] + [ret - HV4, ret + LC4 - HV4], h_retro=[s + 70 + (sa - SA4) for s in sp],
        cal=[(svt[1], svt[1] + VA4 + 2, 'CS 1-2', f'VA {VA4}'), (sp[-1], A[-1] + 2, 'CS 1-2', f'SA {sa}'), (svt[0], svt[1], 'RVA', f'LC {LC4}')])


S['p4_diff_a'] = diff4(235, 'pa', 'A. Encarrilamiento desde el ápex del VD (310 ms)')
S['p4_diff_b'] = diff4(225, 'pb', 'B. Encarrilamiento desde la base del VD (310 ms)')


def ehr4(d, typ, pace, title, mark):
    k = 3
    vs = [i * LC4 for i in range(k)]
    h_exp = k * LC4 - HV4
    A = [v + VA4 for v in vs] + [k * LC4 + VA4 - d]
    nxt = A[-1] + (LC4 - VA4) if d else k * LC4 + LC4
    after = [nxt, nxt + LC4]
    A += [v + VA4 for v in after]
    return dict(win=(-80, after[-1] + 200), pxms=0.30, title=title, channels=CH6, src=SRC4,
        spikes=[h_exp], pace_ch=pace, beats=[(v, 'n') for v in vs] + [(h_exp, typ)] + [(v, 'n') for v in after],
        atr=[(a, 'left', -1) for a in A], h_ante=[v - HV4 for v in vs] + [h_exp] + [v - HV4 for v in after],
        cal=[(A[k - 2] + 2, A[k - 1] + 2, 'CS 1-2', f'A-A {LC4}'), (A[k - 1] + 2, A[k] + 2, 'CS 1-2', f'A-A {LC4 - d}')],
        marks=[(h_exp, 'V1', mark), (h_exp, 'His p', 'H')])


S['p4_ehr_a'] = ehr4(0, 'pa', 'RVA', 'A. EV con His refractario desde el ápex del VD', 'EV')
S['p4_ehr_b'] = ehr4(20, 'lv', 'CS 1-2', 'B. EV con His refractario desde el VI basal (rama del SC)', 'EV (VI)')

# Estudio basal: estimulación del VD a 500 y 400: SA 120 en los dos (no decremental), excéntrica (SC 1-2 primero).
sp = [0, 500, 1000, 1400, 1800]
S['p4_pre'] = dict(win=(-80, 2150), pxms=0.30, title='Estimulación ventricular en ritmo sinusal: 500 y 400 ms', channels=CH6, src=SRC4,
    spikes=sp, beats=[(s, 'pa') for s in sp], atr=[(s + 120, 'left', -1) for s in sp], h_retro=[s + 70 for s in sp],
    cal=[(sp[0], sp[1], 'RVA', 'S-S 500'), (sp[1], sp[1] + 122, 'CS 1-2', 'SA 120'), (sp[2], sp[3], 'RVA', 'S-S 400'), (sp[3], sp[3] + 122, 'CS 1-2', 'SA 120')])

# Para-Hisiana en sinusal: SA 85 → 135 en el His, secuencia concéntrica en los dos (la vía está lejos del sitio).
sp = [0, 650, 1300, 1950]
cap = [True, False, True, False]
S['p4_parahis'] = dict(win=(-80, 2300), pxms=0.32, title='Estimulación para-Hisiana en ritmo sinusal', channels=CH6, src=SRC4,
    spikes=sp, pace_ch='His p', beats=[(s + HV4 if c else s, 'n' if c else 'pa') for s, c in zip(sp, cap)],
    atr=[(s + (85 if c else 135), 'conc_his', -1) for s, c in zip(sp, cap)],
    cal=[(sp[0], sp[0] + 87, 'His d', 'SA 85'), (sp[1], sp[1] + 137, 'His d', 'SA 135'), (sp[2] + HV4, sp[2] + HV4 + 95, 'RVA', 'QRS 95'), (sp[3], sp[3] + 150, 'RVA', 'QRS 150')],
    marks=[(sp[0] + 30, 'V1', 'His + V'), (sp[1] + 40, 'V1', 'solo V')])

# Sobreestimulación auricular desde la AD alta a 310: V-V 310; al cortar, VA 115 como en la TSV.
AHs4 = 200
vs = [0, LC4, 2 * LC4]
A = [v + VA4 for v in vs]
sp = [A[-1] + 220 + 310 * k for k in range(6)]
pv = [s + 28 + AHs4 + HV4 for s in sp]
vs2 = [pv[-1] + LC4, pv[-1] + 2 * LC4]
S['p4_aop'] = dict(win=(-80, vs2[-1] + 220), pxms=0.22, title='Sobreestimulación auricular desde la AD alta a 310 ms', channels=CH6, src=SRC4,
    beats=[(v, 'n') for v in vs + pv + vs2], aspikes=sp, apace_ch='HRA',
    atr=[(a, 'left', -1) for a in A] + [(s + 5, 'sinus', 1) for s in sp] + [(v + VA4, 'left', -1) for v in [pv[-1]] + vs2],
    h_ante=[v - HV4 for v in vs + pv + vs2],
    cal=[(vs[1], vs[1] + VA4 + 2, 'CS 1-2', f'VA {VA4}'), (vs[0], vs[1], 'RVA', f'V-V {LC4}'), (sp[-2], sp[-1], 'HRA', 'S-S 310'),
         (pv[-2], pv[-1], 'RVA', 'V-V 310'), (pv[-1], pv[-1] + VA4 + 2, 'CS 1-2', f'VA {VA4}')])

# Adenosina: termina con una A.
vs = [0, LC4, 2 * LC4, 3 * LC4]
A = [v + VA4 for v in vs]
S['p4_ado'] = dict(win=(-80, A[-1] + 900), pxms=0.25, title='Adenosina IV durante la taquicardia', channels=CH6, src=SRC4,
    beats=[(v, 'n') for v in vs], atr=[(a, 'left', -1) for a in A], h_ante=[v - HV4 for v in vs],
    cal=[(vs[1], vs[2], 'RVA', f'LC {LC4}'), (vs[3], A[3] + 2, 'CS 1-2', f'VA {VA4}')],
    marks=[(A[3] + 60, 'aVF', 'última: A sin V')])

# EA con His refractario desde el ostium del SC: el His siguiente sale a su tiempo.
hs = [i * LC4 - HV4 for i in range(6)]
apb = hs[3] + 10
vs = [h + HV4 for h in hs]
A = [v + VA4 for k2, v in enumerate(vs) if k2 != 3]
S['p4_eha'] = dict(win=(-100, vs[-1] + 250), pxms=0.25, title='EA con His refractario desde el ostium del SC', channels=CH6, src=SRC4,
    beats=[(x, 'n') for x in vs], aspikes=[apb], apace_ch='CS 9-10',
    atr=[(a, 'left', -1) for a in A] + [(apb + 4, 'conc_cs', 1)], h_ante=hs,
    cal=[(hs[2], hs[3], 'His d', f'H-H {LC4}'), (hs[3], hs[4], 'His d', f'H-H {LC4}')],
    marks=[(apb, 'V1', 'EA')])

if __name__ == '__main__':
    for k in (sys.argv[3:] or S):
        render(S[k], f'{OUT}/{k}.svg')
        print(k)
