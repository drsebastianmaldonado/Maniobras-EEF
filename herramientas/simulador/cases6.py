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
sp = [vs[-1] + LC + 10 + 320 * k for k in range(6)]          # el primer estímulo sale después del último QRS de la TSV
pv = [s + 28 + AHs + HV for s in sp]
vs = vs + [vs[-1] + LC]          # la última A de la TSV conduce al V antes del primer estímulo
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
sp = [vs[-1] + LC2 + 55 + 260 * k for k in range(6)]
pv = [s + 28 + AHs2 + HV for s in sp]
vs = vs + [vs[-1] + LC2]
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
sp = [vs[-1] + LC4 + 55 + 310 * k for k in range(6)]
pv = [s + 28 + AHs4 + HV4 for s in sp]
vs = vs + [vs[-1] + LC4]
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

# =====================================================================================================
# Caso 5 (TRNAV atípica rápida-lenta; LC 380 como el ECG real y Veenhuyzen 2011, VA 230, AH 105, A más precoz en el ostium del SC).
# Relaciones de Veenhuyzen 2011, fig. 3: SA > LC de estimulación (seudo A-A-V), SA−VA 150, PPI−LC 185.
SRC5 = 'caso 5: LC 380, estimulación 360 y PPI 565 de Veenhuyzen 2011 (fig. 3); el resto, ilustrativo'
LC5, VA5, AH5, SC5, SA5, PPI5 = 380, 230, 105, 360, 380, 565
HAp5 = 300                              # HA estimulando (His retrógrado 80 ms después de la espiga)
AHr5 = PPI5 - SA5 - HV                  # 150: AH del primer latido de retorno


def vop5(title, med):
    svt = [0, LC5]
    sp = [svt[-1] + 380 + SC5 * k for k in range(6)]
    A = [v + VA5 for v in svt] + [s + SA5 for s in sp]
    ret = sp[-1] + PPI5
    after = [ret, ret + LC5]
    cal = [(svt[0], svt[1], 'RVA', f'LC {LC5}'), (svt[1], svt[1] + VA5 + 2, 'CS 9-10', f'VA {VA5}'), (sp[-2], sp[-1], 'RVA', f'S-S {SC5}'),
           (sp[-1], A[-1] + 2, 'CS 9-10', f'SA {SA5}'), (sp[-1], ret + 2, 'RVA', f'PPI {PPI5}'),
           (A[-3] + 2, A[-2] + 2, 'HRA', f'A-A {SC5}'), (A[-2] + 2, A[-1] + 2, 'HRA', f'A-A {SC5}')]
    marks = []
    if med:
        cal = [c for c in cal if not c[3].startswith(('S-S', 'A-A'))]
        cal += [(svt[1] - HV, svt[1] + VA5, 'His p', f'HA {HV + VA5}'), (sp[-1] + SA5 - HAp5, A[-1], 'His p', f'HA {HAp5}'),
                (A[-1] + 2, ret - HV, 'His d', f'AH {AHr5}'), (A[0] + 2, svt[1] - HV, 'His d', f'AH {AH5}')]
        marks = [(sp[-1] + 200, 'I', f'SA − VA = {SA5} − {VA5} = {SA5 - VA5} ms'), (sp[-1] + 200, 'aVF', f'PPI − LC = {PPI5} − {LC5} = {PPI5 - LC5} ms'),
                 (sp[-1] + 200, 'V1', f'cPPI − LC = {PPI5 - LC5} − ({AHr5} − {AH5}) = {PPI5 - LC5 - AHr5 + AH5} ms · ΔHA = {HAp5} − {HV + VA5} = +{HAp5 - HV - VA5} ms')]
    return dict(win=(-100, after[-1] + 340), pxms=0.21, title=title, channels=CH6, src=SRC5,
        beats=[(v, 'n') for v in svt + after] + [(s, 'pa') for s in sp], spikes=sp,
        atr=[(a, 'conc_cs', -1) for a in A + [v + VA5 for v in after]],
        h_ante=[v - HV for v in svt + after], h_retro=[s + SA5 - HAp5 for s in sp], cal=cal, marks=marks)


S['p5_vop'] = vop5('Sobreestimulación ventricular desde el ápex del VD a 360 ms', False)
S['p5_medidas'] = vop5('Medidas sobre la sobreestimulación ventricular (ápex del VD a 360 ms): PPI, SA, AH y HA', True)


def diff5(sa, typ, title):
    svt = [0, LC5]
    sp = [svt[-1] + 380 + SC5 * k for k in range(6)]
    A = [v + VA5 for v in svt] + [s + sa for s in sp]
    ret = sp[-1] + PPI5 + (sa - SA5)
    return dict(win=(-100, ret + LC5 + 200), pxms=0.21, channels=CH6, title=title, spikes=sp, pace_ch='RVA', src=SRC5,
        beats=[(v, 'n') for v in svt] + [(s, typ) for s in sp] + [(ret, 'n'), (ret + LC5, 'n')],
        atr=[(a, 'conc_cs', -1) for a in A] + [(ret + VA5, 'conc_cs', -1), (ret + LC5 + VA5, 'conc_cs', -1)],
        h_ante=[v - HV for v in svt] + [ret - HV, ret + LC5 - HV], h_retro=[s + sa - HAp5 for s in sp],
        cal=[(svt[1], svt[1] + VA5 + 2, 'CS 9-10', f'VA {VA5}'), (sp[-1], A[-1] + 2, 'CS 9-10', f'SA {sa}'), (svt[0], svt[1], 'RVA', f'LC {LC5}')])


S['p5_diff_a'] = diff5(380, 'pa', 'A. Encarrilamiento desde el ápex del VD (360 ms)')
S['p5_diff_b'] = diff5(410, 'pb', 'B. Encarrilamiento desde la base del VD (360 ms)')

# EV con His refractario (V local del ostium del SC adelantado > 60 ms): la A no cambia.
k = 3
vs = [i * LC5 for i in range(k)]
h_exp = k * LC5 - HV
spk = h_exp - 25
A = [v + VA5 for v in vs] + [k * LC5 + VA5]
after = [k * LC5 + LC5, k * LC5 + 2 * LC5]
A += [v + VA5 for v in after]
S['p5_ehr'] = dict(win=(-80, after[-1] + 200), pxms=0.25, title='EV con His refractario durante la taquicardia', channels=CH6, src=SRC5,
    spikes=[spk], pace_ch='RVA', beats=[(v, 'n') for v in vs] + [(spk, 'pa')] + [(v, 'n') for v in after],
    atr=[(a, 'conc_cs', -1) for a in A], h_ante=[v - HV for v in vs] + [h_exp] + [v - HV for v in after],
    cal=[(A[k - 2] + 2, A[k - 1] + 2, 'CS 9-10', f'A-A {LC5}'), (A[k - 1] + 2, A[k] + 2, 'CS 9-10', f'A-A {LC5}'),
         (spk, k * LC5, 'RVA', f'EV {LC5 * k - spk} ms antes del V')],
    marks=[(spk, 'V1', 'EV'), (h_exp, 'His p', 'H')])

# Estudio basal: extraestímulo auricular; S2 10 ms más corto → el AH salta 65 ms (sin eco).
def salto5(s2, ah2, title, lab):
    sp = [0, 600, 600 + s2]
    hs = [s + 28 + a for s, a in zip(sp, [90, 90, ah2])]
    vs = [h + HV for h in hs]
    return dict(win=(-80, 1650), pxms=0.40, title=title, channels=CH6, src=SRC5,
        beats=[(v, 'n') for v in vs], aspikes=sp, apace_ch='HRA', atr=[(s + 5, 'sinus', 1) for s in sp], h_ante=hs,
        cal=[(sp[1], sp[2], 'HRA', f'S2 {s2}'), (sp[1] + 28, hs[1], 'His d', 'AH 90'), (sp[2] + 28, hs[2], 'His d', lab)])


S['p5_pre_a'] = salto5(340, 160, 'A. Extraestímulo auricular S1-S2 600-340', 'AH 160')
S['p5_pre_b'] = salto5(330, 225, 'B. S2 10 ms más corto: S1-S2 600-330', 'AH 225')

# Sobreestimulación auricular desde la AD alta a 340: AH 160 (TSV 105, ΔAH 55); al cortar, VA 230 como en la TSV.
AHs5 = 160
vs = [0, LC5]
A = [v + VA5 for v in vs]
sp = [vs[-1] + LC5 + 115 + 340 * k for k in range(5)]
pv = [s + 28 + AHs5 + HV for s in sp]
vs = vs + [vs[-1] + LC5]
vs2 = [pv[-1] + LC5]
S['p5_aop'] = dict(win=(-80, vs2[-1] + 380), pxms=0.21, title='Sobreestimulación auricular desde la AD alta a 340 ms', channels=CH6, src=SRC5,
    beats=[(v, 'n') for v in vs + pv + vs2], aspikes=sp, apace_ch='HRA',
    atr=[(a, 'conc_cs', -1) for a in A] + [(s + 5, 'sinus', 1) for s in sp] + [(v + VA5, 'conc_cs', -1) for v in [pv[-1]] + vs2],
    h_ante=[v - HV for v in vs + pv + vs2],
    cal=[(vs[0], vs[1], 'RVA', f'V-V {LC5}'), (vs[0], A[0] + 2, 'CS 9-10', f'VA {VA5}'), (A[0] + 2, vs[1] - HV, 'His d', f'AH {AH5}'), (sp[-2], sp[-1], 'HRA', 'S-S 340'),
         (pv[-2], pv[-1], 'RVA', 'V-V 340'), (sp[-1] + 28, pv[-1] - HV, 'His d', f'AH {AHs5}'), (pv[-1], pv[-1] + VA5 + 2, 'CS 9-10', f'VA {VA5}')])

# Adenosina: termina con un V (bloqueo en la vía lenta retrógrada).
vs = [0, LC5, 2 * LC5, 3 * LC5]
A = [v + VA5 for v in vs[:3]]
S['p5_ado'] = dict(win=(-80, vs[-1] + 700), pxms=0.22, title='Adenosina IV durante la taquicardia', channels=CH6, src=SRC5,
    beats=[(v, 'n') for v in vs], atr=[(a, 'conc_cs', -1) for a in A], h_ante=[v - HV for v in vs],
    cal=[(vs[0], vs[1], 'RVA', f'LC {LC5}'), (vs[1], A[1] + 2, 'CS 9-10', f'VA {VA5}')],
    marks=[(vs[3] + 120, 'aVF', 'último: V sin A')])

# Para-Hisiana en sinusal: SA 90 → 140 en el His, misma secuencia (nodal).
sp = [0, 650, 1300, 1950]
cap = [True, False, True, False]
S['p5_parahis'] = dict(win=(-80, 2300), pxms=0.32, title='Estimulación para-Hisiana en ritmo sinusal', channels=CH6, src=SRC5,
    spikes=sp, pace_ch='His p', beats=[(s + HV if c else s, 'n' if c else 'pa') for s, c in zip(sp, cap)],
    atr=[(s + (90 if c else 140), 'conc_his', -1) for s, c in zip(sp, cap)],
    cal=[(sp[0], sp[0] + 92, 'His d', 'SA 90'), (sp[1], sp[1] + 142, 'His d', 'SA 140'), (sp[2] + HV, sp[2] + HV + 95, 'RVA', 'QRS 95'), (sp[3], sp[3] + 150, 'RVA', 'QRS 150')],
    marks=[(sp[0] + 30, 'V1', 'His + V'), (sp[1] + 40, 'V1', 'solo V')])

# EA con His refractario desde el ostium del SC: el His siguiente sale a su tiempo.
hs = [i * LC5 - HV for i in range(5)]
apb = hs[2] + 10
vs = [h + HV for h in hs]
A = [v + VA5 for k2, v in enumerate(vs) if k2 != 2]
S['p5_eha'] = dict(win=(-100, vs[-1] + 250), pxms=0.25, title='EA con His refractario desde el ostium del SC', channels=CH6, src=SRC5,
    beats=[(x, 'n') for x in vs], aspikes=[apb], apace_ch='CS 9-10',
    atr=[(a, 'conc_cs', -1) for a in A] + [(apb + 4, 'conc_cs', 1)], h_ante=hs,
    cal=[(hs[1], hs[2], 'His d', f'H-H {LC5}'), (hs[2], hs[3], 'His d', f'H-H {LC5}')],
    marks=[(apb, 'V1', 'EA')])

# =====================================================================================================
# Caso 6 (PJRT; LC 300 como el ECG real, VA 190, AH 65, A más precoz en el ostium del SC).
# Relaciones de Ho 2015: PPI−LC 71, SA−VA 19, ΔHA −76 con His ortodrómico, EV-HR que retrasa la A 20, ΔAH 10.
SRC6 = 'caso 6: LC 300 como el caso; relaciones de Ho 2015; el resto, ilustrativo'
LC6, VA6, AH6, SC6, SA6, PPI6, HAp6 = 300, 190, 65, 280, 209, 371, 159


def vop6(title, med):
    svt = [i * LC6 for i in range(3)]
    sp = [svt[-1] + 230 + SC6 * k for k in range(6)]
    A = [v + VA6 for v in svt] + [s + SA6 for s in sp]
    ret = sp[-1] + PPI6
    after = [ret, ret + LC6]
    cal = [(svt[0], svt[1], 'RVA', f'LC {LC6}'), (svt[1], svt[1] + VA6 + 2, 'CS 9-10', f'VA {VA6}'), (sp[-2], sp[-1], 'RVA', f'S-S {SC6}'),
           (A[-3] + 2, A[-2] + 2, 'HRA', f'A-A {SC6}'), (sp[-1], A[-1] + 2, 'CS 9-10', f'SA {SA6}'), (sp[-1], ret + 2, 'RVA', f'PPI {PPI6}')]
    marks = []
    if med:
        cal = [c for c in cal if not c[3].startswith(('S-S', 'A-A'))]
        cal += [(svt[1] - HV, svt[1] + VA6, 'His p', f'HA {HV + VA6}'), (A[-1] - HAp6, A[-1], 'His p', f'HA {HAp6}')]
        marks = [(sp[-1] + 160, 'I', f'SA − VA = {SA6} − {VA6} = {SA6 - VA6} ms'), (sp[-1] + 160, 'aVF', f'PPI − LC = {PPI6} − {LC6} = {PPI6 - LC6} ms'),
                 (sp[-1] + 160, 'V1', f'ΔHA = {HAp6} − {HV + VA6} = −{HV + VA6 - HAp6} ms')]
    return dict(win=(-80, after[-1] + 220), pxms=0.26, title=title, channels=CH6, src=SRC6,
        beats=[(v, 'n') for v in svt + after] + [(s, 'pa') for s in sp], spikes=sp,
        atr=[(a, 'conc_cs', -1) for a in A + [v + VA6 for v in after]],
        h_ante=[v - HV for v in svt + after] + [a - HAp6 for a in A[3:]], cal=cal, marks=marks)


S['p6_vop'] = vop6('Sobreestimulación ventricular desde el ápex del VD a 280 ms', False)
S['p6_medidas'] = vop6('Medidas sobre la sobreestimulación ventricular (ápex del VD a 280 ms): PPI, SA y HA', True)


def diff6(sa, typ, title):
    svt = [0, LC6]
    sp = [560 + SC6 * k for k in range(6)]
    A = [v + VA6 for v in svt] + [s + sa for s in sp]
    ret = sp[-1] + PPI6 + (sa - SA6)
    return dict(win=(-80, ret + LC6 + 220), pxms=0.26, channels=CH6, title=title, spikes=sp, pace_ch='RVA', src=SRC6,
        beats=[(v, 'n') for v in svt] + [(s, typ) for s in sp] + [(ret, 'n'), (ret + LC6, 'n')],
        atr=[(a, 'conc_cs', -1) for a in A] + [(ret + VA6, 'conc_cs', -1), (ret + LC6 + VA6, 'conc_cs', -1)],
        h_ante=[v - HV for v in svt] + [ret - HV, ret + LC6 - HV] + [a - HAp6 for a in A[2:]],
        cal=[(svt[1], svt[1] + VA6 + 2, 'CS 9-10', f'VA {VA6}'), (sp[-1], A[-1] + 2, 'CS 9-10', f'SA {sa}'), (svt[0], svt[1], 'RVA', f'LC {LC6}')])


S['p6_diff_a'] = diff6(209, 'pa', 'A. Encarrilamiento desde el ápex del VD (280 ms)')
S['p6_diff_b'] = diff6(194, 'pb', 'B. Encarrilamiento desde la base del VD (280 ms)')

# EV con His refractario: la A siguiente se retrasa 20 ms, misma secuencia, la taquicardia sigue.
k = 3
vs = [i * LC6 for i in range(k)]
h_exp = k * LC6 - HV
A = [v + VA6 for v in vs] + [k * LC6 + VA6 + 20]
nxt = A[-1] + (LC6 - VA6)
after = [nxt, nxt + LC6]
A += [v + VA6 for v in after]
S['p6_ehr'] = dict(win=(-80, after[-1] + 200), pxms=0.30, title='EV con His refractario durante la taquicardia', channels=CH6, src=SRC6,
    spikes=[h_exp], pace_ch='RVA', beats=[(v, 'n') for v in vs] + [(h_exp, 'pa')] + [(v, 'n') for v in after],
    atr=[(a, 'conc_cs', -1) for a in A], h_ante=[v - HV for v in vs] + [h_exp] + [v - HV for v in after],
    cal=[(A[k - 2] + 2, A[k - 1] + 2, 'CS 9-10', f'A-A {LC6}'), (A[k - 1] + 2, A[k] + 2, 'CS 9-10', f'A-A {LC6 + 20}')],
    marks=[(h_exp, 'V1', 'EV'), (h_exp, 'His p', 'H')])

# Estudio basal: estimulación del VD a 500 y 400: SA 150 y 200 (decremental), concéntrica con la A precoz en el ostium del SC.
sp = [0, 500, 1000, 1400, 1800]
sas = [150, 150, 150, 200, 200]
S['p6_pre'] = dict(win=(-80, 2150), pxms=0.30, title='Estimulación ventricular en ritmo sinusal: 500 y 400 ms', channels=CH6, src=SRC6,
    spikes=sp, beats=[(s, 'pa') for s in sp], atr=[(s + a, 'conc_cs', -1) for s, a in zip(sp, sas)],
    cal=[(sp[0], sp[1], 'RVA', 'S-S 500'), (sp[1], sp[1] + 152, 'CS 9-10', 'SA 150'), (sp[2], sp[3], 'RVA', 'S-S 400'), (sp[3], sp[3] + 202, 'CS 9-10', 'SA 200')])

# Para-Hisiana en sinusal: SA 120 → 170, misma secuencia.
sp = [0, 650, 1300, 1950]
cap = [True, False, True, False]
S['p6_parahis'] = dict(win=(-80, 2300), pxms=0.32, title='Estimulación para-Hisiana en ritmo sinusal', channels=CH6, src=SRC6,
    spikes=sp, pace_ch='His p', beats=[(s + HV if c else s, 'n' if c else 'pa') for s, c in zip(sp, cap)],
    atr=[(s + (120 if c else 170), 'conc_cs', -1) for s, c in zip(sp, cap)],
    cal=[(sp[0], sp[0] + 122, 'CS 9-10', 'SA 120'), (sp[1], sp[1] + 172, 'CS 9-10', 'SA 170'), (sp[2] + HV, sp[2] + HV + 95, 'RVA', 'QRS 95'), (sp[3], sp[3] + 150, 'RVA', 'QRS 150')],
    marks=[(sp[0] + 30, 'V1', 'His + V'), (sp[1] + 40, 'V1', 'solo V')])

# Sobreestimulación auricular desde la AD alta a 280: AH 75 (TSV 65, ΔAH 10); al cortar, VA 190 como en la TSV.
AHs6 = AH6 + 10
vs = [0, LC6, 2 * LC6]
A = [v + VA6 for v in vs]
sp = [vs[-1] + LC6 + 150 + 280 * k for k in range(6)]
pv = [s + 28 + AHs6 + HV for s in sp]
vs = vs + [vs[-1] + LC6]
vs2 = [pv[-1] + LC6, pv[-1] + 2 * LC6]
S['p6_aop'] = dict(win=(-80, vs2[-1] + 220), pxms=0.24, title='Sobreestimulación auricular desde la AD alta a 280 ms', channels=CH6, src=SRC6,
    beats=[(v, 'n') for v in vs + pv + vs2], aspikes=sp, apace_ch='HRA',
    atr=[(a, 'conc_cs', -1) for a in A] + [(s + 5, 'sinus', 1) for s in sp] + [(v + VA6, 'conc_cs', -1) for v in [pv[-1]] + vs2],
    h_ante=[v - HV for v in vs + pv + vs2],
    cal=[(vs[0], vs[1], 'RVA', f'V-V {LC6}'), (vs[0], A[0] + 2, 'CS 9-10', f'VA {VA6}'), (A[1] + 2, vs[2] - HV, 'His d', f'AH {AH6}'),
         (sp[-2], sp[-1], 'HRA', 'S-S 280'), (pv[-2], pv[-1], 'RVA', 'V-V 280'), (sp[-1] + 28, pv[-1] - HV, 'His d', f'AH {AHs6}'),
         (pv[-1], pv[-1] + VA6 + 2, 'CS 9-10', f'VA {VA6}')])

# Adenosina: termina con un V (bloqueo en la vía).
vs = [0, LC6, 2 * LC6, 3 * LC6]
A = [v + VA6 for v in vs[:3]]
S['p6_ado'] = dict(win=(-80, vs[-1] + 700), pxms=0.25, title='Adenosina IV durante la taquicardia', channels=CH6, src=SRC6,
    beats=[(v, 'n') for v in vs], atr=[(a, 'conc_cs', -1) for a in A], h_ante=[v - HV for v in vs],
    cal=[(vs[0], vs[1], 'RVA', f'LC {LC6}'), (vs[1], A[1] + 2, 'CS 9-10', f'VA {VA6}')],
    marks=[(vs[3] + 120, 'aVF', 'último: V sin A')])

# EA con His refractario desde el ostium del SC: el His siguiente sale a su tiempo.
hs = [i * LC6 - HV for i in range(6)]
apb = hs[3] + 10
vs = [h + HV for h in hs]
A = [v + VA6 for k2, v in enumerate(vs) if k2 != 3]
S['p6_eha'] = dict(win=(-100, vs[-1] + 250), pxms=0.27, title='EA con His refractario desde el ostium del SC', channels=CH6, src=SRC6,
    beats=[(x, 'n') for x in vs], aspikes=[apb], apace_ch='CS 9-10',
    atr=[(a, 'conc_cs', -1) for a in A] + [(apb + 4, 'conc_cs', 1)], h_ante=hs,
    cal=[(hs[2], hs[3], 'His d', f'H-H {LC6}'), (hs[3], hs[4], 'His d', f'H-H {LC6}')],
    marks=[(apb, 'V1', 'EA')])

# =====================================================================================================
# Caso 7 (taquicardia de la unión; LC 340 como el ECG real). El foco está en el His: H → V 45 y H → A 45 (A y V simultáneos).
SRC7 = 'caso 7 (didáctico): LC 340 como el caso; el resto, ilustrativo'
LC7, SC7, SA7, PPI7, HAp7 = 340, 300, 220, 515, 100


def vop7(title, med):
    svt = [i * LC7 for i in range(3)]
    sp = [svt[-1] + 260 + SC7 * k for k in range(6)]
    A = [v for v in svt] + [s + SA7 for s in sp]
    ret = sp[-1] + PPI7
    after = [ret, ret + LC7]
    cal = [(svt[0], svt[1], 'RVA', f'LC {LC7}'), (sp[-2], sp[-1], 'RVA', f'S-S {SC7}'), (A[-3] + 2, A[-2] + 2, 'HRA', f'A-A {SC7}'),
           (sp[-1], A[-1] + 2, 'CS 9-10', f'SA {SA7}'), (sp[-1], ret + 2, 'RVA', f'PPI {PPI7}')]
    marks = [(A[-1], 'His p', 'A'), (ret - HV, 'His p', 'H')]
    if med:
        cal = [c for c in cal if not c[3].startswith(('S-S', 'A-A'))]
        cal += [(svt[1] - HV, svt[1], 'His d', f'HA {HV}'), (A[-1] - HAp7, A[-1], 'His d', f'HA {HAp7}')]
        marks = [(sp[-1] + 260, 'I', f'SA − VA = {SA7} − 0 = {SA7} ms'), (sp[-1] + 260, 'aVF', f'PPI − LC = {PPI7} − {LC7} = {PPI7 - LC7} ms'),
                 (sp[-1] + 260, 'V1', f'ΔHA = {HAp7} − {HV} = +{HAp7 - HV} ms')]
    return dict(win=(-80, after[-1] + 220), pxms=0.25, title=title, channels=CH6, src=SRC7,
        beats=[(v, 'n') for v in svt + after] + [(s, 'pa') for s in sp], spikes=sp,
        atr=[(a, 'conc_his', -1) for a in A + after], h_ante=[v - HV for v in svt + after], h_retro=[s + SA7 - HAp7 for s in sp],
        cal=cal, marks=marks)


S['p7_vop'] = vop7('Sobreestimulación ventricular desde el ápex del VD a 300 ms', False)
S['p7_medidas'] = vop7('Medidas sobre la sobreestimulación ventricular (ápex del VD a 300 ms): PPI, SA y HA', True)


def diff7(sa, typ, title):
    svt = [0, LC7]
    sp = [600 + SC7 * k for k in range(6)]
    A = svt + [s + sa for s in sp]
    ret = sp[-1] + PPI7 + (sa - SA7)
    return dict(win=(-80, ret + LC7 + 220), pxms=0.24, channels=CH6, title=title, spikes=sp, pace_ch='RVA', src=SRC7,
        beats=[(v, 'n') for v in svt] + [(s, typ) for s in sp] + [(ret, 'n'), (ret + LC7, 'n')],
        atr=[(a, 'conc_his', -1) for a in A] + [(ret, 'conc_his', -1), (ret + LC7, 'conc_his', -1)],
        h_ante=[v - HV for v in svt] + [ret - HV, ret + LC7 - HV], h_retro=[s + sa - HAp7 for s in sp],
        cal=[(sp[-1], A[-1] + 2, 'CS 9-10', f'SA {sa}'), (svt[0], svt[1], 'RVA', f'LC {LC7}')])


S['p7_diff_a'] = diff7(220, 'pa', 'A. Encarrilamiento desde el ápex del VD (300 ms)')
S['p7_diff_b'] = diff7(250, 'pb', 'B. Encarrilamiento desde la base del VD (300 ms)')

# EV con His refractario: el His y la A siguientes no cambian.
k = 3
vs = [i * LC7 for i in range(k)]
h_exp = k * LC7 - HV
after = [k * LC7 + LC7, k * LC7 + 2 * LC7]
A = vs + [k * LC7] + after
S['p7_ehr'] = dict(win=(-80, after[-1] + 200), pxms=0.30, title='EV con His refractario durante la taquicardia', channels=CH6, src=SRC7,
    spikes=[h_exp], pace_ch='RVA', beats=[(v, 'n') for v in vs] + [(h_exp, 'pa')] + [(v, 'n') for v in after],
    atr=[(a, 'conc_his', -1) for a in A], h_ante=[v - HV for v in vs] + [h_exp] + [v - HV for v in after],
    cal=[(vs[1] - HV, vs[2] - HV, 'His d', f'H-H {LC7}'), (vs[2] - HV, h_exp, 'His d', f'H-H {LC7}'), (h_exp, after[0] - HV, 'His d', f'H-H {LC7}')],
    marks=[(h_exp, 'V1', 'EV'), (h_exp, 'His p', 'H')])

# EA con His refractario (ostium del SC): el His siguiente no cambia.  EA precoz (AD alta): adelanta el His inmediato 38 ms y la taquicardia sigue.
hs = [i * LC7 - HV for i in range(7)]
vs = [h + HV for h in hs]
apb = hs[4]
S['p7_eha_a'] = dict(win=(-100, vs[-1] + 250), pxms=0.25, title='A. EA con His refractario desde el ostium del SC', channels=CH6, src=SRC7,
    beats=[(x, 'n') for x in vs], aspikes=[apb], apace_ch='CS 9-10',
    atr=[(v, 'conc_his', -1) for k2, v in enumerate(vs) if k2 != 4] + [(apb + 4, 'conc_cs', 1)], h_ante=hs,
    cal=[(hs[3], hs[4], 'His d', f'H-H {LC7}'), (hs[4], hs[5], 'His d', f'H-H {LC7}')],
    marks=[(apb, 'V1', 'EA')])
hs = [i * LC7 - HV for i in range(4)]
h_adv = 4 * LC7 - HV - 38
apb = h_adv - 125
hs += [h_adv, h_adv + LC7, h_adv + 2 * LC7]
vs = [h + HV for h in hs]
S['p7_eha_b'] = dict(win=(-100, vs[-1] + 250), pxms=0.25, title='B. EA precoz desde la AD alta', channels=CH6, src=SRC7,
    beats=[(x, 'n') for x in vs], aspikes=[apb], apace_ch='HRA',
    atr=[(v, 'conc_his', -1) for k2, v in enumerate(vs) if k2 != 4] + [(apb + 4, 'sinus', 1)], h_ante=hs,
    cal=[(hs[2], hs[3], 'His d', f'H-H {LC7}'), (hs[3], hs[4], 'His d', f'H-H {hs[4] - hs[3]}'), (hs[4], hs[5], 'His d', f'H-H {LC7}'),
         (apb, hs[4], 'His p', f'AH {hs[4] - apb - 28}')],
    marks=[(apb, 'V1', 'EA')])

# Sobreestimulación auricular desde la AD alta a 300: cada A conduce con AH 90; al cortar, el último A conduce con AH 90 (PR < RR)
# y la taquicardia retoma con H-H 340.
vs = [0, LC7]
sp = [vs[-1] + LC7 + 150 + 300 * k for k in range(6)]
pv = [s + 28 + 90 + HV for s in sp]
vs = vs + [vs[-1] + LC7]          # el latido de la unión siguiente sale antes de que conduzca el primer estímulo
vs2 = [pv[-1] + LC7, pv[-1] + 2 * LC7]
S['p7_aop'] = dict(win=(-80, vs2[-1] + 220), pxms=0.24, title='Sobreestimulación auricular desde la AD alta a 300 ms', channels=CH6, src=SRC7,
    beats=[(v, 'n') for v in vs + pv + vs2], aspikes=sp, apace_ch='HRA',
    atr=[(a, 'conc_his', -1) for a in vs[:-1]] + [(s + 5, 'sinus', 1) for s in sp] + [(v, 'conc_his', -1) for v in vs2],
    h_ante=[v - HV for v in vs + pv + vs2],
    cal=[(vs[0], vs[1], 'RVA', f'V-V {LC7}'), (sp[-2], sp[-1], 'HRA', 'S-S 300'), (pv[-2], pv[-1], 'RVA', 'V-V 300'),
         (sp[-1] + 28, pv[-1] - HV, 'His d', 'AH 90'), (pv[-1], vs2[0], 'RVA', f'V-V {LC7}')])

# Estudio basal: extraestímulo auricular sin salto del AH (S2 300 → AH 140; S2 290 → AH 150), sin eco.
def ea7(s2, ah2, title):
    sp = [0, 600, 600 + s2]
    hs = [s + 28 + a for s, a in zip(sp, [80, 80, ah2])]
    return dict(win=(-80, 1650), pxms=0.40, title=title, channels=CH6, src=SRC7,
        beats=[(h + HV, 'n') for h in hs], aspikes=sp, apace_ch='HRA', atr=[(s + 5, 'sinus', 1) for s in sp], h_ante=hs,
        cal=[(sp[1], sp[2], 'HRA', f'S2 {s2}'), (sp[1] + 28, hs[1], 'His d', 'AH 80'), (sp[2] + 28, hs[2], 'His d', f'AH {ah2}')])


S['p7_pre_a'] = ea7(300, 140, 'A. Extraestímulo auricular S1-S2 600-300')
S['p7_pre_b'] = ea7(290, 150, 'B. S2 10 ms más corto: S1-S2 600-290')

# Para-Hisiana en sinusal: SA 85 → 135, misma secuencia.
sp = [0, 650, 1300, 1950]
cap = [True, False, True, False]
S['p7_parahis'] = dict(win=(-80, 2300), pxms=0.32, title='Estimulación para-Hisiana en ritmo sinusal', channels=CH6, src=SRC7,
    spikes=sp, pace_ch='His p', beats=[(s + HV if c else s, 'n' if c else 'pa') for s, c in zip(sp, cap)],
    atr=[(s + (85 if c else 135), 'conc_his', -1) for s, c in zip(sp, cap)],
    cal=[(sp[0], sp[0] + 87, 'His d', 'SA 85'), (sp[1], sp[1] + 137, 'His d', 'SA 135'), (sp[2] + HV, sp[2] + HV + 95, 'RVA', 'QRS 95'), (sp[3], sp[3] + 150, 'RVA', 'QRS 150')],
    marks=[(sp[0] + 30, 'V1', 'His + V'), (sp[1] + 40, 'V1', 'solo V')])

# Adenosina: se enlentece (H-H 420, 470) con bloqueo VA (A sinusales disociadas) y vuelve a 340 con A y V simultáneos.
vs = [0, LC7, 2 * LC7]
for d in (420, 470, 420, 340, 340):
    vs.append(vs[-1] + d)
asin = [vs[2] + 250, vs[2] + 250 + 600]
A = vs[:3] + vs[6:]
S['p7_ado'] = dict(win=(-80, vs[-1] + 220), pxms=0.22, title='Adenosina IV durante la taquicardia', channels=CH6, src=SRC7,
    beats=[(v, 'n') for v in vs], atr=[(a, 'conc_his', -1) for a in A] + [(a, 'sinus', 1) for a in asin], h_ante=[v - HV for v in vs],
    cal=[(vs[0] - HV, vs[1] - HV, 'His d', f'H-H {LC7}'), (vs[2] - HV, vs[3] - HV, 'His d', 'H-H 420'), (vs[3] - HV, vs[4] - HV, 'His d', 'H-H 470'),
         (vs[6] - HV, vs[7] - HV, 'His d', f'H-H {LC7}')],
    marks=[(vs[3] + 60, 'aVF', 'V sin A'), (vs[4] + 60, 'aVF', 'V sin A')])

# =====================================================================================================
# Caso 8 (TV fascicular posterior; LC 420 y QRS 140 como el ECG real; ritmo sinusal disociado a 800; His 15 ms después del inicio del QRS).
SRC8 = 'caso 8: LC 420 como el caso; P1 y P2 según Liu Q 2023, Liu 2015 y Nogami 2010; el resto, ilustrativo'
LC8, CH8 = 420, ['HRA', 'His d', 'RVA']


def vop8(title, med):
    vt = [i * LC8 for i in range(3)]
    sp = [vt[-1] + 340 + 380 * k for k in range(6)]
    ret = sp[-1] + 500
    after = [ret, ret + LC8, ret + 2 * LC8]
    asin = [150, 950, 1750, 2550, 3350]
    cal = [(vt[0], vt[1], 'RVA', f'LC {LC8}'), (sp[-2], sp[-1], 'RVA', 'S-S 380'), (sp[-1], ret + 2, 'RVA', 'PPI 500')]
    marks = [(sp[-1] + 250, 'I', 'PPI − LC = 500 − 420 = 80 ms')] if med else []
    return dict(win=(-80, after[-1] + 200), pxms=0.25, title=title, channels=CH8, src=SRC8, spikes=sp,
        beats=[(v, 'rbs') for v in vt + after] + [(s, 'pa') for s in sp], atr=[(a, 'sinus', 1) for a in asin if a < after[-1]],
        h_retro=[v + 15 for v in vt + after] + [s + 120 for s in sp], cal=cal, marks=marks)


S['p8_vop'] = vop8('Sobreestimulación ventricular desde el ápex del VD a 380 ms', False)
S['p8_medidas'] = vop8('PPI después de la sobreestimulación ventricular (ápex del VD a 380 ms)', True)

# Estudio basal: estimulación ventricular en sinusal a 500 y 400: SA 140 y 190 (decremental), concéntrica.
sp = [0, 500, 1000, 1400, 1800]
sas = [140, 140, 140, 190, 190]
S['p8_pre'] = dict(win=(-80, 2150), pxms=0.30, title='Estimulación ventricular en ritmo sinusal: 500 y 400 ms', channels=CH6, src=SRC8,
    spikes=sp, beats=[(s, 'pa') for s in sp], atr=[(s + a, 'conc_his', -1) for s, a in zip(sp, sas)], h_retro=[s + a - 60 for s, a in zip(sp, sas)],
    cal=[(sp[0], sp[1], 'RVA', 'S-S 500'), (sp[1], sp[1] + 142, 'HRA', 'SA 140'), (sp[2], sp[3], 'RVA', 'S-S 400'), (sp[3], sp[3] + 192, 'HRA', 'SA 190')])

# Registro de la A y el His durante la TV: A-A 800 (sinusal), V-V 420, His 15 ms después del inicio del QRS.
vt = [i * LC8 for i in range(7)]
asin = [150, 950, 1750, 2550]
S['p8_regah'] = dict(win=(-80, vt[-1] + 200), pxms=0.30, title='Registro de la AD alta y el His durante la taquicardia', channels=CH8, src=SRC8,
    beats=[(v, 'rbs') for v in vt], atr=[(a, 'sinus', 1) for a in asin], h_retro=[v + 15 for v in vt],
    cal=[(asin[1], asin[2], 'HRA', 'A-A 800'), (vt[1], vt[2], 'RVA', f'V-V {LC8}'), (vt[4], vt[4] + 15, 'His d', 'V-H 15')],
    marks=[(vt[4] + 15, 'aVF', 'H después del inicio del QRS')])

# Sobreestimulación auricular a 380 durante la TV: el primer latido conducido es de fusión y los siguientes, angostos (AH 90, HV 45).
# Al cortar vuelve la TV.
vt = [0, LC8, 2 * LC8]
sp = [vt[-1] + 120 + 380 * k for k in range(6)]
cv = [s + 28 + 90 + HV for s in sp]
after = [cv[-1] + LC8, cv[-1] + 2 * LC8]
S['p8_aop'] = dict(win=(-80, after[-1] + 200), pxms=0.24, title='Sobreestimulación auricular desde la AD alta a 380 ms durante la taquicardia', channels=CH8, src=SRC8,
    beats=[(v, 'rbs') for v in vt + after] + [(cv[0], 'f')] + [(v, 'n') for v in cv[1:]], aspikes=sp, apace_ch='HRA',
    atr=[(150, 'sinus', 1)] + [(s + 5, 'sinus', 1) for s in sp], h_ante=[v - HV for v in cv[1:]], h_retro=[v + 15 for v in vt + after],
    cal=[(vt[0], vt[1], 'RVA', f'LC {LC8}'), (sp[-2], sp[-1], 'HRA', 'S-S 380'), (sp[-1] + 28, cv[-1] - HV, 'His d', 'AH 90'), (cv[-1] - HV, cv[-1], 'His d', 'HV 45'),
         (cv[-1], after[0], 'RVA', f'V-V {LC8}')])

# Adenosina: la TV sigue igual (LC 420).
vt = [i * LC8 for i in range(7)]
S['p8_ado'] = dict(win=(-80, vt[-1] + 200), pxms=0.27, title='Adenosina IV durante la taquicardia', channels=CH8, src=SRC8,
    beats=[(v, 'rbs') for v in vt], atr=[(a, 'sinus', 1) for a in (150, 1150, 2250)], h_retro=[v + 15 for v in vt],
    cal=[(vt[0], vt[1], 'RVA', f'LC {LC8}'), (vt[5], vt[6], 'RVA', f'LC {LC8}')])

# Mapeo del septum del VI (LV 9-10 proximal → LV 1-2 distal): P1 mesodiastólico de proximal a distal, P2 presistólico de distal a proximal.
vt = [i * LC8 for i in range(6)]
lv = ['LV 9-10', 'LV 7-8', 'LV 5-6', 'LV 3-4', 'LV 1-2']
P1V = [120, 100, 75, 55, None]
A1 = [0.42, 0.38, 0.25, 0.12, 0]
A2 = [0, 0, 0.12, 0.35, 0.62]
ext = {}
for i, n in enumerate(lv):
    ext[n] = [(v - 14 - 4 * i, A2[i], 0.7) for v in vt] if A2[i] else []
    if P1V[i]:
        ext[n] += [(v - P1V[i], A1[i], 3.2) for v in vt]
S['p8_map'] = dict(win=(-60, vt[-1] + 200), pxms=0.30, title='Mapeo del septum medio-inferior del VI durante la taquicardia', channels=['HRA', 'His d'] + lv + ['RVA'], src=SRC8,
    beats=[(v, 'rbs') for v in vt], atr=[(a, 'sinus', 1) for a in (150, 950, 1750)], h_retro=[v + 15 for v in vt], extra=ext,
    cal=[(vt[0], vt[1], 'RVA', f'LC {LC8}'), (vt[1] - 120, vt[1], 'LV 9-10', 'P1-V 120'), (vt[2] - 100, vt[2], 'LV 7-8', 'P1-V 100'),
         (vt[3] - 75, vt[3], 'LV 5-6', 'P1-V 75'), (vt[4] - 55, vt[4], 'LV 3-4', 'P1-V 55'), (vt[5] - 30, vt[5], 'LV 1-2', 'P2-V 30')])

# Caso 8: verapamilo. A, antes (LC 420, P1-P2 110, P2-V 30). B, con verapamilo: la LC y el P1-P2 se alargan (P2-V sigue en 30),
# el último P1 se bloquea antes de P2 y la TV termina; sigue el ritmo sinusal con QRS angosto.
def verap8(title, lcs, p1p2s, end):
    vt = [0]
    for lc in lcs[1:]:
        vt.append(vt[-1] + lc)
    p2 = [v - 30 for v in vt]
    p1 = [x - d for x, d in zip(p2, p1p2s)]
    ext = {'LV 1-2': [(t, 0.32, 0.8) for t in p1] + [(t, 0.55, 0.7) for t in p2]}
    beats = [(v, 'rbs') for v in vt]
    atr = [(a, 'sinus', 1) for a in (130, 930, 1730) if a < vt[-1]]
    h_ante, marks = [], []
    cal = [(vt[1], vt[2], 'RVA', f'LC {vt[2] - vt[1]}'), (p1[2], p2[2], 'LV 1-2', f'P1-P2 {p1p2s[2]}'), (p2[3], vt[3], 'LV 1-2', 'P2-V 30')]
    win = vt[-1] + 200
    if end:
        pb = vt[-1] + 330                                   # P1 bloqueado: no le sigue P2 ni QRS
        ext['LV 1-2'].append((pb, 0.32, 0.8))
        sa = [vt[-1] + 650, vt[-1] + 1450]                  # ritmo sinusal después de la terminación
        h_ante = [a + 28 + 90 for a in sa]
        beats += [(h + HV, 'n') for h in h_ante]
        atr = [(a, 'sinus', 1) for a in (130, 930, 1730, 2530) if a < vt[-1]] + [(a, 'sinus', 1) for a in sa]
        cal = [(vt[0], vt[1], 'RVA', f'LC {vt[1]}'), (vt[-2], vt[-1], 'RVA', f'LC {vt[-1] - vt[-2]}'),
               (p1[-1], p2[-1], 'LV 1-2', f'P1-P2 {p1p2s[-1]}'), (p2[-1], vt[-1], 'LV 1-2', 'P2-V 30'), (sa[0], sa[1], 'HRA', 'A-A 800')]
        marks = [(pb, 'LV 1-2', 'P1 sin P2'), (h_ante[0] + HV + 40, 'aVF', 'sinusal')]
        win = sa[1] + 400
    return dict(win=(-60, win), pxms=0.25, title=title, channels=['HRA', 'His d', 'LV 1-2', 'RVA'], src=SRC8,
        beats=beats, atr=atr, h_retro=[v + 15 for v in vt], h_ante=h_ante, extra=ext, cal=cal, marks=marks)


S['p8_verapamilo_a'] = verap8('A. Antes del verapamilo', [0, 420, 420, 420, 420, 420], [110] * 6, False)
S['p8_verapamilo_b'] = verap8('B. Verapamilo IV', [0, 440, 460, 480, 500], [120, 130, 145, 160, 175], True)

# =====================================================================================================
# Caso 9 (TRAV por vía septal lenta y decremental que imita una TRNAV atípica; LC 310 como el ECG real, VA 180, HV 42, AH 88).
# Base − ápex ΔVA −28 y ΔPPI −18 de Arias 2010. Desde el ápex PPI−LC 110 (< 125, corte del RP largo), SA−VA 70 y ΔHA −22, ilustrativos.
SRC9 = 'caso 9: LC 310 como el caso; ΔVA −28 y ΔPPI −18 de Arias 2010; el resto, ilustrativo'
LC9, VA9, HV9, AH9, SC9, SA9, PPI9, HAp9 = 310, 180, 42, 88, 295, 250, 420, 200


def vop9(title, med):
    svt = [i * LC9 for i in range(3)]
    sp = [svt[-1] + 230 + SC9 * k for k in range(6)]
    A = [v + VA9 for v in svt] + [s + SA9 for s in sp]
    ret = sp[-1] + PPI9
    after = [ret, ret + LC9]
    cal = [(svt[0], svt[1], 'RVA', f'LC {LC9}'), (svt[1], svt[1] + VA9 + 2, 'CS 9-10', f'VA {VA9}'), (sp[-2], sp[-1], 'RVA', f'S-S {SC9}'),
           (A[-3] + 2, A[-2] + 2, 'HRA', f'A-A {SC9}'), (sp[-1], A[-1] + 2, 'CS 9-10', f'SA {SA9}'), (sp[-1], ret + 2, 'RVA', f'PPI {PPI9}')]
    marks = []
    if med:
        cal = [c for c in cal if not c[3].startswith(('S-S', 'A-A'))]
        cal += [(svt[1] - HV9, svt[1] + VA9, 'His p', f'HA {HV9 + VA9}'), (A[-1] - HAp9, A[-1], 'His p', f'HA {HAp9}')]
        marks = [(sp[-1] + 160, 'I', f'SA − VA = {SA9} − {VA9} = {SA9 - VA9} ms'), (sp[-1] + 160, 'aVF', f'PPI − LC = {PPI9} − {LC9} = {PPI9 - LC9} ms'),
                 (sp[-1] + 160, 'V1', f'ΔHA = {HAp9} − {HV9 + VA9} = −{HV9 + VA9 - HAp9} ms')]
    return dict(win=(-80, after[-1] + 220), pxms=0.24, title=title, channels=CH6, src=SRC9,
        beats=[(v, 'n') for v in svt + after] + [(s, 'pa') for s in sp], spikes=sp,
        atr=[(a, 'conc_cs', -1) for a in A + [v + VA9 for v in after]],
        h_ante=[v - HV9 for v in svt + after], h_retro=[s + SA9 - HAp9 for s in sp], cal=cal, marks=marks)


S['p9_vop'] = vop9('Sobreestimulación ventricular desde el ápex del VD a 295 ms', False)
S['p9_medidas'] = vop9('Medidas sobre la sobreestimulación ventricular (ápex del VD a 295 ms): PPI, SA y HA', True)


def diff9(sa, ppi, typ, title):
    svt = [0, LC9]
    sp = [560 + SC9 * k for k in range(6)]
    A = [v + VA9 for v in svt] + [s + sa for s in sp]
    ret = sp[-1] + ppi
    return dict(win=(-80, ret + LC9 + 220), pxms=0.24, channels=CH6, title=title, spikes=sp, pace_ch='RVA', src=SRC9,
        beats=[(v, 'n') for v in svt] + [(s, typ) for s in sp] + [(ret, 'n'), (ret + LC9, 'n')],
        atr=[(a, 'conc_cs', -1) for a in A] + [(ret + VA9, 'conc_cs', -1), (ret + LC9 + VA9, 'conc_cs', -1)],
        h_ante=[v - HV9 for v in svt] + [ret - HV9, ret + LC9 - HV9], h_retro=[s + sa - HAp9 for s in sp],
        cal=[(svt[1], svt[1] + VA9 + 2, 'CS 9-10', f'VA {VA9}'), (sp[-1], A[-1] + 2, 'CS 9-10', f'SA {sa}'), (svt[0], svt[1], 'RVA', f'LC {LC9}'),
             (sp[-1], ret + 2, 'RVA', f'PPI {ppi}')])


S['p9_diff_a'] = diff9(250, 420, 'pa', 'A. Encarrilamiento desde el ápex del VD (295 ms)')
S['p9_diff_b'] = diff9(222, 402, 'pb', 'B. Encarrilamiento desde la base del VD (295 ms)')

# EV con His refractario: por el decremento de la vía, retrasa la A siguiente 20 ms, misma secuencia, la taquicardia sigue.
k = 3
vs = [i * LC9 for i in range(k)]
h_exp = k * LC9 - HV9
A = [v + VA9 for v in vs] + [k * LC9 + VA9 + 20]
nxt = A[-1] + (LC9 - VA9)
after = [nxt, nxt + LC9]
A += [v + VA9 for v in after]
S['p9_ehr'] = dict(win=(-80, after[-1] + 200), pxms=0.30, title='EV con His refractario durante la taquicardia', channels=CH6, src=SRC9,
    spikes=[h_exp], pace_ch='RVA', beats=[(v, 'n') for v in vs] + [(h_exp, 'pa')] + [(v, 'n') for v in after],
    atr=[(a, 'conc_cs', -1) for a in A], h_ante=[v - HV9 for v in vs] + [h_exp] + [v - HV9 for v in after],
    cal=[(A[k - 2] + 2, A[k - 1] + 2, 'CS 9-10', f'A-A {LC9}'), (A[k - 1] + 2, A[k] + 2, 'CS 9-10', f'A-A {LC9 + 20}')],
    marks=[(h_exp, 'V1', 'EV'), (h_exp, 'His p', 'H')])

# Estudio basal: estimulación del VD a 500 y 400: SA 150 y 190 (decremental), A más precoz en el SC proximal.
sp = [0, 500, 1000, 1400, 1800]
sas = [150, 150, 150, 190, 190]
S['p9_pre'] = dict(win=(-80, 2150), pxms=0.30, title='Estimulación ventricular en ritmo sinusal: 500 y 400 ms', channels=CH6, src=SRC9,
    spikes=sp, beats=[(s, 'pa') for s in sp], atr=[(s + a, 'conc_cs', -1) for s, a in zip(sp, sas)],
    cal=[(sp[0], sp[1], 'RVA', 'S-S 500'), (sp[1], sp[1] + 152, 'CS 9-10', 'SA 150'), (sp[2], sp[3], 'RVA', 'S-S 400'), (sp[3], sp[3] + 192, 'CS 9-10', 'SA 190')])

# Para-Hisiana en sinusal: SA 120 → 170, misma secuencia.
sp = [0, 650, 1300, 1950]
cap = [True, False, True, False]
S['p9_parahis'] = dict(win=(-80, 2300), pxms=0.32, title='Estimulación para-Hisiana en ritmo sinusal', channels=CH6, src=SRC9,
    spikes=sp, pace_ch='His p', beats=[(s + HV9 if c else s, 'n' if c else 'pa') for s, c in zip(sp, cap)],
    atr=[(s + (120 if c else 170), 'conc_cs', -1) for s, c in zip(sp, cap)],
    cal=[(sp[0], sp[0] + 122, 'CS 9-10', 'SA 120'), (sp[1], sp[1] + 172, 'CS 9-10', 'SA 170'), (sp[2] + HV9, sp[2] + HV9 + 95, 'RVA', 'QRS 95'), (sp[3], sp[3] + 150, 'RVA', 'QRS 150')],
    marks=[(sp[0] + 30, 'V1', 'His + V'), (sp[1] + 40, 'V1', 'solo V')])

# Sobreestimulación auricular desde la AD alta a 290: AH 100 (TSV 88, ΔAH 12); al cortar, VA 180 como en la TSV.
AHs9 = AH9 + 12
vs = [0, LC9, 2 * LC9]
A = [v + VA9 for v in vs]
sp = [vs[-1] + LC9 + 140 + 290 * k for k in range(6)]
pv = [s + 28 + AHs9 + HV9 for s in sp]
vs = vs + [vs[-1] + LC9]
vs2 = [pv[-1] + LC9, pv[-1] + 2 * LC9]
S['p9_aop'] = dict(win=(-80, vs2[-1] + 220), pxms=0.24, title='Sobreestimulación auricular desde la AD alta a 290 ms', channels=CH6, src=SRC9,
    beats=[(v, 'n') for v in vs + pv + vs2], aspikes=sp, apace_ch='HRA',
    atr=[(a, 'conc_cs', -1) for a in A] + [(s + 5, 'sinus', 1) for s in sp] + [(v + VA9, 'conc_cs', -1) for v in [pv[-1]] + vs2],
    h_ante=[v - HV9 for v in vs + pv + vs2],
    cal=[(vs[0], vs[1], 'RVA', f'V-V {LC9}'), (vs[0], A[0] + 2, 'CS 9-10', f'VA {VA9}'), (A[1] + 2, vs[2] - HV9, 'His d', f'AH {AH9}'),
         (sp[-2], sp[-1], 'HRA', 'S-S 290'), (pv[-2], pv[-1], 'RVA', 'V-V 290'), (sp[-1] + 28, pv[-1] - HV9, 'His d', f'AH {AHs9}'),
         (pv[-1], pv[-1] + VA9 + 2, 'CS 9-10', f'VA {VA9}')])

# Adenosina: termina con un V (bloqueo en la vía).
vs = [0, LC9, 2 * LC9, 3 * LC9]
A = [v + VA9 for v in vs[:3]]
S['p9_ado'] = dict(win=(-80, vs[-1] + 700), pxms=0.25, title='Adenosina IV durante la taquicardia', channels=CH6, src=SRC9,
    beats=[(v, 'n') for v in vs], atr=[(a, 'conc_cs', -1) for a in A], h_ante=[v - HV9 for v in vs],
    cal=[(vs[0], vs[1], 'RVA', f'LC {LC9}'), (vs[1], A[1] + 2, 'CS 9-10', f'VA {VA9}')],
    marks=[(vs[3] + 120, 'aVF', 'último: V sin A')])

# EA con His refractario desde el ostium del SC: el His siguiente sale a su tiempo.
hs = [i * LC9 - HV9 for i in range(6)]
apb = hs[3] + 10
vs = [h + HV9 for h in hs]
A = [v + VA9 for k2, v in enumerate(vs) if k2 != 3]
S['p9_eha'] = dict(win=(-100, vs[-1] + 250), pxms=0.27, title='EA con His refractario desde el ostium del SC', channels=CH6, src=SRC9,
    beats=[(x, 'n') for x in vs], aspikes=[apb], apace_ch='CS 9-10',
    atr=[(a, 'conc_cs', -1) for a in A] + [(apb + 4, 'conc_cs', 1)], h_ante=hs,
    cal=[(hs[2], hs[3], 'His d', f'H-H {LC9}'), (hs[3], hs[4], 'His d', f'H-H {LC9}')],
    marks=[(apb, 'V1', 'EA')])

# =====================================================================================================
# Caso 10 (reentrada por una vía nodoventricular; LC 390, HV 45). Conducción VA tipo Wenckebach (220 → 250 → 270 → bloqueo)
# con H-H estable. Nagashima 2020: PPI−LC 105, His ortodrómico y fusión constante. El resto, ilustrativo.
SRC10 = 'caso 10 (didáctico): LC 390 y PPI−LC 105 de Nagashima 2020; el resto, ilustrativo'
LC10 = 390
WK = [220, 250, 270, None]


def wk(vs, k0=0):
    return [v + WK[(i + k0) % 4] for i, v in enumerate(vs) if WK[(i + k0) % 4] is not None]


def vop10(title, med, ppi=495, typ='f', pace='RVA'):
    svt = [i * LC10 for i in range(3)]
    sp = [svt[-1] + 330 + 360 * k for k in range(6)]
    ret = sp[-1] + ppi
    after = [ret, ret + LC10, ret + 2 * LC10]
    A = wk(svt) + [s + 120 for s in sp[::2]] + wk(after)
    cal = [(svt[0], svt[1], 'RVA', f'LC {LC10}'), (sp[-2], sp[-1], 'RVA', 'S-S 360'), (sp[-1], ret + 2, 'RVA', f'PPI {ppi}'),
           (svt[0] - HV, svt[1] - HV, 'His d', f'H-H {LC10}'), (sp[1] - 10, sp[2] - 10, 'His d', 'H-H 360'), (sp[2] - 10, sp[3] - 10, 'His d', 'H-H 360')]
    marks = [] if med else [(sp[2] - 10, 'His p', 'H')]
    if med:
        marks = [(sp[-1] + 200, 'I', f'PPI − LC = {ppi} − {LC10} = {ppi - LC10} ms')]
    return dict(win=(-80, after[-1] + 220), pxms=0.22, title=title, channels=CH6, src=SRC10, spikes=sp, pace_ch=pace,
        beats=[(v, 'n') for v in svt + after] + [(s, typ) for s in sp], atr=[(a, 'conc_his', -1) for a in A],
        h_ante=[v - HV for v in svt + after] + [s - 10 for s in sp], cal=cal, marks=marks)


S['p10_vop'] = vop10('Sobreestimulación ventricular desde el ápex del VD a 360 ms', False)
S['p10_medidas'] = vop10('PPI después de la sobreestimulación ventricular (ápex del VD a 360 ms)', True)
S['p10_diff_a'] = vop10('A. Encarrilamiento desde el ápex del VD (360 ms)', False)
S['p10_diff_b'] = vop10('B. Encarrilamiento desde la base del VD (360 ms)', False, ppi=505, typ='pb')
for k in ('p10_diff_a', 'p10_diff_b'):
    S[k]['marks'] = []

# EV con His refractario: adelanta el His siguiente 25 ms (H-H 365) y la taquicardia sigue.
vs = [i * LC10 for i in range(4)]
h_exp = 4 * LC10 - HV
hn = h_exp + LC10 - 25
after = [hn + HV, hn + HV + LC10, hn + HV + 2 * LC10]
S['p10_ehr'] = dict(win=(-80, after[-1] + 200), pxms=0.25, title='EV con His refractario durante la taquicardia', channels=CH6, src=SRC10,
    spikes=[h_exp], pace_ch='RVA', beats=[(v, 'n') for v in vs] + [(h_exp, 'pa')] + [(v, 'n') for v in after],
    atr=[(a, 'conc_his', -1) for a in wk(vs) + wk(after, 1)], h_ante=[v - HV for v in vs] + [h_exp, hn] + [v - HV for v in after[1:]],
    cal=[(vs[2] - HV, vs[3] - HV, 'His d', f'H-H {LC10}'), (h_exp, hn, 'His d', f'H-H {LC10 - 25}'), (hn, after[1] - HV, 'His d', f'H-H {LC10}')],
    marks=[(h_exp, 'V1', 'EV'), (h_exp, 'His p', 'H')])

# Sobreestimulación auricular a 340: conduce con AH 180. En la TSV, el AH (de la A que sigue al bloqueo, VA 220, al His) es 125: ΔAH +55.
# Al cortar la taquicardia sigue (H-H 390) con el mismo Wenckebach VA.
vs = [0, LC10, 2 * LC10]
sp = [vs[-1] + LC10 + 120 + 340 * k for k in range(6)]
pv = [s + 28 + 180 + HV for s in sp]
vs = vs + [vs[-1] + LC10]          # V sin A (bloqueo VA del Wenckebach) antes de que conduzca el primer estímulo
vs2 = [pv[-1] + LC10, pv[-1] + 2 * LC10, pv[-1] + 3 * LC10]
S['p10_aop'] = dict(win=(-80, vs2[-1] + 220), pxms=0.22, title='Sobreestimulación auricular desde la AD alta a 340 ms', channels=CH6, src=SRC10,
    beats=[(v, 'n') for v in vs + pv + vs2], aspikes=sp, apace_ch='HRA',
    atr=[(a, 'conc_his', -1) for a in wk(vs)] + [(s + 5, 'sinus', 1) for s in sp] + [(a, 'conc_his', -1) for a in wk(vs2)],
    h_ante=[v - HV for v in vs + pv + vs2],
    cal=[(vs[0] + 220, vs[1] - HV, 'His d', 'AH 125'), (sp[-2], sp[-1], 'HRA', 'S-S 340'), (sp[-1] + 28, pv[-1] - HV, 'His d', 'AH 180'),
         (pv[-1] - HV, vs2[0] - HV, 'His d', f'H-H {LC10}')])

# Estudio basal: extraestímulo auricular: S2 310 → AH 150; S2 300 → AH 245 (salto de 95).
def ea10(s2, ah2, title):
    sp = [0, 600, 600 + s2]
    hs = [s + 28 + a for s, a in zip(sp, [85, 85, ah2])]
    return dict(win=(-80, 1650), pxms=0.40, title=title, channels=CH6, src=SRC10,
        beats=[(h + HV, 'n') for h in hs], aspikes=sp, apace_ch='HRA', atr=[(s + 5, 'sinus', 1) for s in sp], h_ante=hs,
        cal=[(sp[1], sp[2], 'HRA', f'S2 {s2}'), (sp[1] + 28, hs[1], 'His d', 'AH 85'), (sp[2] + 28, hs[2], 'His d', f'AH {ah2}')])


S['p10_pre_a'] = ea10(310, 150, 'A. Extraestímulo auricular S1-S2 600-310')
S['p10_pre_b'] = ea10(300, 245, 'B. S2 10 ms más corto: S1-S2 600-300')

# Para-Hisiana en sinusal: SA 85 → 135, misma secuencia.
sp = [0, 650, 1300, 1950]
cap = [True, False, True, False]
S['p10_parahis'] = dict(win=(-80, 2300), pxms=0.32, title='Estimulación para-Hisiana en ritmo sinusal', channels=CH6, src=SRC10,
    spikes=sp, pace_ch='His p', beats=[(s + HV if c else s, 'n' if c else 'pa') for s, c in zip(sp, cap)],
    atr=[(s + (85 if c else 135), 'conc_his', -1) for s, c in zip(sp, cap)],
    cal=[(sp[0], sp[0] + 87, 'His d', 'SA 85'), (sp[1], sp[1] + 137, 'His d', 'SA 135'), (sp[2] + HV, sp[2] + HV + 95, 'RVA', 'QRS 95'), (sp[3], sp[3] + 150, 'RVA', 'QRS 150')],
    marks=[(sp[0] + 30, 'V1', 'His + V'), (sp[1] + 40, 'V1', 'solo V')])

# Adenosina: la taquicardia termina sin un His después del último V; vuelve el sinusal.
vs = [i * LC10 for i in range(5)]
sa = [vs[-1] + 900, vs[-1] + 1650]
hsin = [a + 28 + 85 for a in sa]
S['p10_ado'] = dict(win=(-80, hsin[-1] + 300), pxms=0.22, title='Adenosina IV durante la taquicardia', channels=CH6, src=SRC10,
    beats=[(v, 'n') for v in vs] + [(h + HV, 'n') for h in hsin], atr=[(a, 'conc_his', -1) for a in wk(vs)] + [(a, 'sinus', 1) for a in sa],
    h_ante=[v - HV for v in vs] + hsin,
    cal=[(vs[0] - HV, vs[1] - HV, 'His d', f'H-H {LC10}'), (sa[0], sa[1], 'HRA', 'A-A 750')],
    marks=[(vs[-1] + 150, 'aVF', 'termina'), (hsin[0] + HV + 40, 'aVF', 'sinusal')])

# EA con His refractario desde el ostium del SC: el His siguiente sale a su tiempo.
hs = [i * LC10 - HV for i in range(6)]
vs = [h + HV for h in hs]
apb = hs[3] + 10
S['p10_eha'] = dict(win=(-100, vs[-1] + 250), pxms=0.25, title='EA con His refractario desde el ostium del SC', channels=CH6, src=SRC10,
    beats=[(x, 'n') for x in vs], aspikes=[apb], apace_ch='CS 9-10',
    atr=[(a, 'conc_his', -1) for a in wk(vs[:3])] + [(apb + 4, 'conc_cs', 1)] + [(a, 'conc_his', -1) for a in wk(vs[4:], 1)], h_ante=hs,
    cal=[(hs[2], hs[3], 'His d', f'H-H {LC10}'), (hs[3], hs[4], 'His d', f'H-H {LC10}')],
    marks=[(apb, 'V1', 'EA')])

# =====================================================================================================
# Caso 11 (TRAV antidrómica por una vía atriofascicular, Mahaim; LC 260 como el ECG real). AV por la vía 150, VA por el His y el nodo 110,
# His retrógrado 25 ms después del inicio del QRS. Valores ilustrativos.
SRC11 = 'caso 11 (didáctico): LC 260 como el caso; el resto, ilustrativo'
LC11, VA11 = 260, 110
CH11 = ['HRA', 'AD lat', 'His p', 'His d', 'CS 9-10', 'RVA']

# Estudio basal: estimulación ventricular en sinusal a 500 y 400: SA 140 y 190 (decremental), concéntrica: sin conducción retrógrada por la vía.
sp = [0, 500, 1000, 1400, 1800]
sas = [140, 140, 140, 190, 190]
S['p11_pre'] = dict(win=(-80, 2150), pxms=0.30, title='Estimulación ventricular en ritmo sinusal: 500 y 400 ms', channels=CH6, src=SRC11,
    spikes=sp, beats=[(s, 'pa') for s in sp], atr=[(s + a, 'conc_his', -1) for s, a in zip(sp, sas)], h_retro=[s + a - 60 for s, a in zip(sp, sas)],
    cal=[(sp[0], sp[1], 'RVA', 'S-S 500'), (sp[1], sp[1] + 142, 'HRA', 'SA 140'), (sp[2], sp[3], 'RVA', 'S-S 400'), (sp[3], sp[3] + 192, 'HRA', 'SA 190')])

# Registro de la A y el His durante la taquicardia: relación 1:1, VA 110, His 25 ms después del inicio del QRS.
vs = [i * LC11 for i in range(7)]
A = [v + VA11 for v in vs]
S['p11_regah'] = dict(win=(-80, vs[-1] + 200), pxms=0.30, title='Registro de la AD alta y el His durante la taquicardia', channels=CH11, src=SRC11,
    beats=[(v, 'lb') for v in vs], atr=[(a, 'conc_his', -1) for a in A], h_retro=[v + 25 for v in vs], extra={'AD lat': [(a + 30, 0.9, 1.0) for a in A]},
    cal=[(vs[1], vs[2], 'RVA', f'V-V {LC11}'), (A[1], A[2], 'HRA', f'A-A {LC11}'), (vs[3], A[3] + 2, 'CS 9-10', f'VA {VA11}'), (vs[4], vs[4] + 25, 'His d', 'V-H 25')],
    marks=[(vs[4] + 25, 'aVF', 'H después del inicio del QRS')])

# Sobreestimulación ventricular desde el ápex del VD a 240: la A sigue a 240; al cortar, V-A-V con la misma morfología; PPI 290.
vt = [0, LC11, 2 * LC11]
sp = [vt[-1] + 200 + 240 * k for k in range(6)]
ret = sp[-1] + 290
after = [ret, ret + LC11, ret + 2 * LC11]
A = [v + VA11 for v in vt] + [s + VA11 for s in sp] + [v + VA11 for v in after]
S['p11_vop'] = dict(win=(-80, after[-1] + 200), pxms=0.27, title='Sobreestimulación ventricular desde el ápex del VD a 240 ms', channels=CH11, src=SRC11,
    beats=[(v, 'lb') for v in vt + after] + [(s, 'pa') for s in sp], spikes=sp, atr=[(a, 'conc_his', -1) for a in A],
    h_retro=[v + 25 for v in vt + after] + [s + 30 for s in sp], extra={'AD lat': [(a + 30, 0.9, 1.0) for a in A]},
    cal=[(vt[0], vt[1], 'RVA', f'LC {LC11}'), (sp[-2], sp[-1], 'RVA', 'S-S 240'), (A[-5] + 2, A[-4] + 2, 'HRA', 'A-A 240'), (sp[-1], ret + 2, 'RVA', 'PPI 290')])

# Adenosina: termina con una A que no conduce al V (bloqueo en la vía atriofascicular).
vs = [i * LC11 for i in range(4)]
A = [v + VA11 for v in vs]
S['p11_ado'] = dict(win=(-80, A[-1] + 800), pxms=0.27, title='Adenosina IV durante la taquicardia', channels=CH11, src=SRC11,
    beats=[(v, 'lb') for v in vs], atr=[(a, 'conc_his', -1) for a in A], h_retro=[v + 25 for v in vs], extra={'AD lat': [(a + 30, 0.9, 1.0) for a in A]},
    cal=[(vs[0], vs[1], 'RVA', f'LC {LC11}'), (vs[3], A[3] + 2, 'CS 9-10', f'VA {VA11}')],
    marks=[(A[3] + 60, 'aVF', 'última: A sin V')])

# Caso 11: estimulación auricular en sinusal a 600 desde dos sitios. A, ostium del SC (cerca del nodo, lejos de la vía): QRS angosto,
# AH 80, HV 45. B, AD lateral (cerca de la vía): BRI máximo; el V llega por la vía (S-V 150) y el His por el nodo (AH 112): HV 10.
def sitio11(cs, title):
    sp = [0, 600, 1200]
    if cs:
        hs = [s + 28 + 80 for s in sp]
        beats = [(h + HV, 'n') for h in hs]
        atr = [(s + 4, 'conc_cs', 1) for s in sp]
        cal = [(sp[0], sp[1], 'CS 9-10', 'S-S 600'), (sp[1] + 28, hs[1], 'His d', 'AH 80'), (hs[1], hs[1] + HV, 'His p', f'HV {HV}')]
        pace, ext = 'CS 9-10', {'AD lat': [(s + 70, 0.8, 1.0) for s in sp]}
    else:
        hs = [s + 28 + 112 for s in sp]
        beats = [(s + 150, 'lb') for s in sp]
        atr = [(s + 5, 'right', 1) for s in sp]
        cal = [(sp[0], sp[1], 'AD lat', 'S-S 600'), (sp[1], sp[1] + 150, 'RVA', 'S-V 150'), (hs[1], sp[1] + 150, 'His p', 'HV 10')]
        pace, ext = 'AD lat', {}
    return dict(win=(-80, 1650), pxms=0.40, title=title, channels=CH11, src=SRC11, aspikes=sp, apace_ch=pace,
        beats=beats, atr=atr, h_ante=hs, extra=ext, cal=cal)


S['p11_sitio_a'] = sitio11(True, 'A. Estimulación auricular a 600 ms desde el ostium del SC')
S['p11_sitio_b'] = sitio11(False, 'B. Estimulación auricular a 600 ms desde la AD lateral')

# =====================================================================================================
# Caso 12 (TRAV antidrómica por una vía AV posterolateral derecha; LC 245 como el ECG real). A → V por la vía 85, V → A por el His y el nodo 160,
# His retrógrado 120 ms después del inicio del QRS. Valores ilustrativos.
SRC12 = 'caso 12 (didáctico): LC 245 como el caso; el resto, ilustrativo'
LC12, VA12 = 245, 160
CH12 = ['HRA', 'AD lat', 'His p', 'His d', 'CS 9-10', 'RVA']

# Estimulación auricular decremental desde la AD alta (500, 400, 350): el AV por la vía queda fijo en 95; el AH se alarga y la preexcitación es máxima.
sp = [0, 500, 900, 1250]
hs = [s + 28 + a for s, a in zip(sp, [90, 120, 160, 210])]
S['p12_adec'] = dict(win=(-80, 1600), pxms=0.40, title='Estimulación auricular decremental desde la AD alta (500, 400 y 350 ms)', channels=CH12, src=SRC12,
    beats=[(s + 95, 'lb') for s in sp], aspikes=sp, apace_ch='HRA', atr=[(s + 5, 'sinus', 1) for s in sp], h_ante=hs,
    extra={'AD lat': [(s + 30, 0.8, 1.0) for s in sp]},
    cal=[(sp[0], sp[1], 'HRA', 'S-S 500'), (sp[1], sp[1] + 95, 'RVA', 'AV 95'), (sp[2], sp[3], 'HRA', 'S-S 350'), (sp[3], sp[3] + 95, 'RVA', 'AV 95'),
         (sp[1] + 28, hs[1], 'His d', 'AH 120'), (sp[3] + 28, hs[3], 'His d', 'AH 210')])

# Estimulación auricular diferencial a 600: ostium del SC (cerca del nodo, lejos de la vía) → QRS de fusión, S-V 135;
# AD lateral (cerca de la vía) → preexcitación máxima, S-V 70.
def sitio12(cs, title):
    sp = [0, 600, 1200]
    if cs:
        hs = [s + 28 + 80 for s in sp]
        beats, atr, pace = [(s + 135, 'f') for s in sp], [(s + 4, 'conc_cs', 1) for s in sp], 'CS 9-10'
        cal = [(sp[0], sp[1], 'CS 9-10', 'S-S 600'), (sp[1], sp[1] + 135, 'RVA', 'S-V 135'), (sp[1] + 28, hs[1], 'His d', 'AH 80')]
        ext = {'AD lat': [(s + 70, 0.8, 1.0) for s in sp]}
    else:
        hs = [s + 28 + 100 for s in sp]
        beats, atr, pace = [(s + 70, 'lb') for s in sp], [(s + 5, 'right', 1) for s in sp], 'AD lat'
        cal = [(sp[0], sp[1], 'AD lat', 'S-S 600'), (sp[1], sp[1] + 70, 'RVA', 'S-V 70')]
        ext = {}
    return dict(win=(-80, 1650), pxms=0.40, title=title, channels=CH12, src=SRC12, aspikes=sp, apace_ch=pace,
        beats=beats, atr=atr, h_ante=hs, extra=ext, cal=cal)


S['p12_sitio_a'] = sitio12(True, 'A. Estimulación auricular a 600 ms desde el ostium del SC')
S['p12_sitio_b'] = sitio12(False, 'B. Estimulación auricular a 600 ms desde la AD lateral')

# Estimulación ventricular en sinusal a 500 y 400: SA 140 y 190 (decremental), concéntrica: la vía no conduce en forma retrógrada.
sp = [0, 500, 1000, 1400, 1800]
sas = [140, 140, 140, 190, 190]
S['p12_pre'] = dict(win=(-80, 2150), pxms=0.30, title='Estimulación ventricular en ritmo sinusal: 500 y 400 ms', channels=CH6, src=SRC12,
    spikes=sp, beats=[(s, 'pa') for s in sp], atr=[(s + a, 'conc_his', -1) for s, a in zip(sp, sas)], h_retro=[s + a - 60 for s, a in zip(sp, sas)],
    cal=[(sp[0], sp[1], 'RVA', 'S-S 500'), (sp[1], sp[1] + 142, 'HRA', 'SA 140'), (sp[2], sp[3], 'RVA', 'S-S 400'), (sp[3], sp[3] + 192, 'HRA', 'SA 190')])

# Registro de la A y el His durante la taquicardia: 1:1, His 120 ms después del inicio del QRS y antes de la A (VA 160), A más precoz en el His.
vs = [i * LC12 for i in range(7)]
A = [v + VA12 for v in vs]
S['p12_regah'] = dict(win=(-80, vs[-1] + 200), pxms=0.30, title='Registro de la AD alta y el His durante la taquicardia', channels=CH12, src=SRC12,
    beats=[(v, 'lb') for v in vs], atr=[(a, 'conc_his', -1) for a in A], h_retro=[v + 120 for v in vs], extra={'AD lat': [(a + 25, 0.8, 1.0) for a in A]},
    cal=[(vs[1], vs[2], 'RVA', f'V-V {LC12}'), (vs[3], A[3] + 2, 'CS 9-10', f'VA {VA12}'), (vs[4], vs[4] + 120, 'His d', 'V-H 120')],
    marks=[(vs[4] + 120, 'aVF', 'H antes de la A')])

# Sobreestimulación ventricular desde el ápex del VD a 225: la A sigue a 225; al cortar, A-V con el mismo QRS; PPI 305.
vt = [0, LC12, 2 * LC12]
sp = [vt[-1] + 190 + 225 * k for k in range(6)]
ret = sp[-1] + 305
after = [ret, ret + LC12, ret + 2 * LC12]
A = [v + VA12 for v in vt] + [s + VA12 for s in sp] + [v + VA12 for v in after]
S['p12_vop'] = dict(win=(-80, after[-1] + 200), pxms=0.27, title='Sobreestimulación ventricular desde el ápex del VD a 225 ms', channels=CH12, src=SRC12,
    beats=[(v, 'lb') for v in vt + after] + [(s, 'pa') for s in sp], spikes=sp, atr=[(a, 'conc_his', -1) for a in A],
    h_retro=[v + 120 for v in vt + after] + [s + 100 for s in sp], extra={'AD lat': [(a + 25, 0.8, 1.0) for a in A]},
    cal=[(vt[0], vt[1], 'RVA', f'LC {LC12}'), (sp[-2], sp[-1], 'RVA', 'S-S 225'), (A[-5] + 2, A[-4] + 2, 'HRA', 'A-A 225'), (sp[-1], ret + 2, 'RVA', 'PPI 305')])

# Adenosina: termina con un V (bloqueo en el nodo, brazo retrógrado).
vs = [i * LC12 for i in range(4)]
A = [v + VA12 for v in vs[:3]]
S['p12_ado'] = dict(win=(-80, vs[-1] + 700), pxms=0.27, title='Adenosina IV durante la taquicardia', channels=CH12, src=SRC12,
    beats=[(v, 'lb') for v in vs], atr=[(a, 'conc_his', -1) for a in A], h_retro=[v + 120 for v in vs], extra={'AD lat': [(a + 25, 0.8, 1.0) for a in A]},
    cal=[(vs[0], vs[1], 'RVA', f'LC {LC12}'), (vs[1], A[1] + 2, 'CS 9-10', f'VA {VA12}')],
    marks=[(vs[3] + 120, 'aVF', 'último: V sin A')])

# =====================================================================================================
# Caso 13 (doble disparo nodal; Burri 2012: A-A 896, relación P:QRS 1:2; AH1 90 y H1-H2 430 ilustrativos).
SRC13 = 'caso 13: A-A 896 y relación 1:2 de Burri 2012; el resto, ilustrativo'
CH13 = ['HRA', 'His p', 'His d', 'RVA']


def ea13(cl, doble, title):
    sp = [cl * k for k in range(4)]
    h1 = [s + 28 + 90 for s in sp]
    hs = h1 + ([h + 430 for h in h1] if doble else [])
    cal = [(sp[0], sp[1], 'HRA', f'S-S {cl}'), (sp[1] + 28, h1[1], 'His d', 'AH 90')]
    if doble:
        cal += [(h1[1], h1[1] + 430, 'His p', 'H1-H2 430')]
    return dict(win=(-80, sp[-1] + 700), pxms=0.25, title=title, channels=CH13, src=SRC13,
        beats=[(h + HV, 'n') for h in sorted(hs)], aspikes=sp, apace_ch='HRA', atr=[(s + 5, 'sinus', 1) for s in sp], h_ante=sorted(hs), cal=cal)


S['p13_pre_a'] = ea13(800, True, 'A. Estimulación de la AD alta a 800 ms')
S['p13_pre_b'] = ea13(600, False, 'B. Estimulación de la AD alta a 600 ms')

# Atropina: el sinusal se acelera (A-A 650) y cada A conduce una sola vez (AH 80): desaparece el segundo QRS.
As = [650 * k for k in range(5)]
hs = [a + 80 for a in As]
S['p13_atrop'] = dict(win=(-80, As[-1] + 500), pxms=0.22, title='Después de atropina IV', channels=CH13, src=SRC13,
    beats=[(h + HV, 'n') for h in hs], atr=[(a, 'sinus', 1) for a in As], h_ante=hs,
    cal=[(As[1], As[2], 'HRA', 'A-A 650'), (As[2], hs[2], 'His d', 'AH 80')])

# Adenosina: dos A sinusales sin His ni V (bloqueo en el nodo); después vuelve la respuesta 1:2.
As = [896 * k for k in range(5)]
cond = [0, 3, 4]
h1 = [As[i] + 90 for i in cond]
hs = sorted(h1 + [h + 430 for h in h1])
S['p13_ado'] = dict(win=(-80, As[-1] + 650), pxms=0.18, title='Adenosina IV', channels=CH13, src=SRC13,
    beats=[(h + HV, 'n') for h in hs], atr=[(a, 'sinus', 1) for a in As], h_ante=hs,
    cal=[(As[0], As[1], 'HRA', 'A-A 896'), (h1[1], h1[1] + 430, 'His p', 'H1-H2 430')],
    marks=[(As[1] + 40, 'aVF', 'A sin V'), (As[2] + 40, 'aVF', 'A sin V')])

# =====================================================================================================
# Caso 14 (PJRT en un paciente de 6 años; LC 400 como el ECG real, VA 260, AH 100, HV 40, A más precoz en el ostium del SC).
SRC14 = 'caso 14: LC 400 como el caso; el resto, ilustrativo'
H14, LC14b, VA14b, AH14b, SC14, SA14, PPI14, HAp14 = 40, 400, 260, 100, 370, 335, 515, 280


def vop14(title, med):
    svt = [i * LC14b for i in range(3)]
    sp = [svt[-1] + 300 + SC14 * k for k in range(6)]
    A = [v + VA14b for v in svt] + [s + SA14 for s in sp]
    ret = sp[-1] + PPI14
    after = [ret, ret + LC14b]
    cal = [(svt[0], svt[1], 'RVA', f'LC {LC14b}'), (svt[1], svt[1] + VA14b + 2, 'CS 9-10', f'VA {VA14b}'), (sp[-2], sp[-1], 'RVA', f'S-S {SC14}'),
           (A[-3] + 2, A[-2] + 2, 'HRA', f'A-A {SC14}'), (sp[-1], A[-1] + 2, 'CS 9-10', f'SA {SA14}'), (sp[-1], ret + 2, 'RVA', f'PPI {PPI14}')]
    marks = []
    if med:
        cal = [c for c in cal if not c[3].startswith(('S-S', 'A-A'))]
        cal += [(svt[1] - H14, svt[1] + VA14b, 'His p', f'HA {H14 + VA14b}'), (A[-1] - HAp14, A[-1], 'His p', f'HA {HAp14}')]
        marks = [(sp[-1] + 200, 'I', f'SA − VA = {SA14} − {VA14b} = {SA14 - VA14b} ms'), (sp[-1] + 200, 'aVF', f'PPI − LC = {PPI14} − {LC14b} = {PPI14 - LC14b} ms'),
                 (sp[-1] + 200, 'V1', f'ΔHA = {HAp14} − {H14 + VA14b} = −{H14 + VA14b - HAp14} ms')]
    return dict(win=(-80, after[-1] + 220), pxms=0.22, title=title, channels=CH6, src=SRC14,
        beats=[(v, 'n') for v in svt + after] + [(s, 'pa') for s in sp], spikes=sp,
        atr=[(a, 'conc_cs', -1) for a in A + [v + VA14b for v in after]],
        h_ante=[v - H14 for v in svt + after], h_retro=[s + SA14 - HAp14 for s in sp], cal=cal, marks=marks)


S['p14_vop'] = vop14('Sobreestimulación ventricular desde el ápex del VD a 370 ms', False)
S['p14_medidas'] = vop14('Medidas sobre la sobreestimulación ventricular (ápex del VD a 370 ms): PPI, SA y HA', True)


def diff14(sa, typ, title):
    svt = [0, LC14b]
    sp = [700 + SC14 * k for k in range(6)]
    A = [v + VA14b for v in svt] + [s + sa for s in sp]
    ret = sp[-1] + PPI14 + (sa - SA14)
    return dict(win=(-80, ret + LC14b + 220), pxms=0.22, channels=CH6, title=title, spikes=sp, pace_ch='RVA', src=SRC14,
        beats=[(v, 'n') for v in svt] + [(s, typ) for s in sp] + [(ret, 'n'), (ret + LC14b, 'n')],
        atr=[(a, 'conc_cs', -1) for a in A] + [(ret + VA14b, 'conc_cs', -1), (ret + LC14b + VA14b, 'conc_cs', -1)],
        h_ante=[v - H14 for v in svt] + [ret - H14, ret + LC14b - H14], h_retro=[s + sa - HAp14 for s in sp],
        cal=[(svt[1], svt[1] + VA14b + 2, 'CS 9-10', f'VA {VA14b}'), (sp[-1], A[-1] + 2, 'CS 9-10', f'SA {sa}'), (svt[0], svt[1], 'RVA', f'LC {LC14b}')])


S['p14_diff_a'] = diff14(335, 'pa', 'A. Encarrilamiento desde el ápex del VD (370 ms)')
S['p14_diff_b'] = diff14(315, 'pb', 'B. Encarrilamiento desde la base del VD (370 ms)')

# EV con His refractario: no llega a la A y la taquicardia termina; vuelve el sinusal.
vs = [i * LC14b for i in range(4)]
A = [v + VA14b for v in vs]
h_exp = vs[-1] + LC14b - H14
sp = h_exp + 10
sa = sp + 700
S['p14_ehr'] = dict(win=(-80, sa + 28 + AH14b + H14 + 250), pxms=0.25, title='EV con His refractario durante la taquicardia', channels=CH6, src=SRC14,
    beats=[(v, 'n') for v in vs] + [(sp, 'pa'), (sa + 28 + AH14b + H14, 'n')], spikes=[sp], pace_ch='RVA',
    atr=[(a, 'conc_cs', -1) for a in A] + [(sa, 'sinus', 1)], h_ante=[v - H14 for v in vs] + [h_exp, sa + 28 + AH14b],
    cal=[(vs[1], vs[2], 'RVA', f'LC {LC14b}'), (vs[2], A[2] + 2, 'CS 9-10', f'VA {VA14b}'), (A[-1], sa, 'HRA', f'A-A {sa - A[-1]}')],
    marks=[(sp, 'V1', 'EV'), (h_exp, 'His p', 'H'), (sp + 180, 'aVF', 'sin A')])

# Estudio basal: estimulación del VD a 600 y 500: SA 180 y 230 (decremental), concéntrica con la A precoz en el ostium del SC.
sp = [0, 600, 1200, 1700, 2200]
sas = [180, 180, 180, 230, 230]
S['p14_pre'] = dict(win=(-80, 2600), pxms=0.27, title='Estimulación ventricular en ritmo sinusal: 600 y 500 ms', channels=CH6, src=SRC14,
    spikes=sp, beats=[(s, 'pa') for s in sp], atr=[(s + a, 'conc_cs', -1) for s, a in zip(sp, sas)],
    cal=[(sp[0], sp[1], 'RVA', 'S-S 600'), (sp[1], sp[1] + 182, 'CS 9-10', 'SA 180'), (sp[2], sp[3], 'RVA', 'S-S 500'), (sp[3], sp[3] + 232, 'CS 9-10', 'SA 230')])

# Para-Hisiana en sinusal: SA 130 → 180, misma secuencia.
sp = [0, 700, 1400, 2100]
cap = [True, False, True, False]
S['p14_parahis'] = dict(win=(-80, 2450), pxms=0.30, title='Estimulación para-Hisiana en ritmo sinusal', channels=CH6, src=SRC14,
    spikes=sp, pace_ch='His p', beats=[(s + H14 if c else s, 'n' if c else 'pa') for s, c in zip(sp, cap)],
    atr=[(s + (130 if c else 180), 'conc_cs', -1) for s, c in zip(sp, cap)],
    cal=[(sp[0], sp[0] + 132, 'CS 9-10', 'SA 130'), (sp[1], sp[1] + 182, 'CS 9-10', 'SA 180'), (sp[2] + H14, sp[2] + H14 + 90, 'RVA', 'QRS 90'), (sp[3], sp[3] + 150, 'RVA', 'QRS 150')],
    marks=[(sp[0] + 30, 'V1', 'His + V'), (sp[1] + 40, 'V1', 'solo V')])

# Sobreestimulación auricular desde la AD alta a 370: AH 110 (TSV 100, ΔAH 10); al cortar, VA 260 como en la TSV.
vs = [0, LC14b]
A = [v + VA14b for v in vs]
sp = [vs[-1] + LC14b + 200 + 370 * k for k in range(6)]
pv = [s + 28 + 110 + H14 for s in sp]
vs = vs + [vs[-1] + LC14b]
vs2 = [pv[-1] + LC14b, pv[-1] + 2 * LC14b]
S['p14_aop'] = dict(win=(-80, vs2[-1] + 300), pxms=0.21, title='Sobreestimulación auricular desde la AD alta a 370 ms', channels=CH6, src=SRC14,
    beats=[(v, 'n') for v in vs + pv + vs2], aspikes=sp, apace_ch='HRA',
    atr=[(a, 'conc_cs', -1) for a in A] + [(s + 5, 'sinus', 1) for s in sp] + [(v + VA14b, 'conc_cs', -1) for v in [pv[-1]] + vs2],
    h_ante=[v - H14 for v in vs + pv + vs2],
    cal=[(vs[0], vs[1], 'RVA', f'V-V {LC14b}'), (vs[0], A[0] + 2, 'CS 9-10', f'VA {VA14b}'), (A[0] + 2, vs[1] - H14, 'His d', f'AH {AH14b}'),
         (sp[-2], sp[-1], 'HRA', 'S-S 370'), (pv[-2], pv[-1], 'RVA', 'V-V 370'), (sp[-1] + 28, pv[-1] - H14, 'His d', 'AH 110'),
         (pv[-1], pv[-1] + VA14b + 2, 'CS 9-10', f'VA {VA14b}')])

# Adenosina: termina con un V.
vs = [i * LC14b for i in range(4)]
A = [v + VA14b for v in vs[:3]]
S['p14_ado'] = dict(win=(-80, vs[-1] + 700), pxms=0.22, title='Adenosina IV durante la taquicardia', channels=CH6, src=SRC14,
    beats=[(v, 'n') for v in vs], atr=[(a, 'conc_cs', -1) for a in A], h_ante=[v - H14 for v in vs],
    cal=[(vs[0], vs[1], 'RVA', f'LC {LC14b}'), (vs[1], A[1] + 2, 'CS 9-10', f'VA {VA14b}')],
    marks=[(vs[3] + 120, 'aVF', 'último: V sin A')])

# EA con His refractario desde el ostium del SC: el His siguiente sale a su tiempo.
hs = [i * LC14b - H14 for i in range(6)]
apb = hs[3] + 10
vs = [h + H14 for h in hs]
A = [v + VA14b for k2, v in enumerate(vs) if k2 != 3]
S['p14_eha'] = dict(win=(-100, vs[-1] + 250), pxms=0.22, title='EA con His refractario desde el ostium del SC', channels=CH6, src=SRC14,
    beats=[(x, 'n') for x in vs], aspikes=[apb], apace_ch='CS 9-10',
    atr=[(a, 'conc_cs', -1) for a in A] + [(apb + 4, 'conc_cs', 1)], h_ante=hs,
    cal=[(hs[2], hs[3], 'His d', f'H-H {LC14b}'), (hs[3], hs[4], 'His d', f'H-H {LC14b}')],
    marks=[(apb, 'V1', 'EA')])

# =====================================================================================================
# Caso 15 (TRAV por vía lateral izquierda decremental; LC 311 del estudio real; VA 140, HV 45 ilustrativos; A más precoz en el SC 1-2).
SRC15 = 'caso 15: LC 311 del estudio real; el resto, ilustrativo'
LC15b, VA15b = 311, 140


def diff15(sa, typ, title):
    svt = [0, LC15b]
    sp = [560 + 280 * k for k in range(6)]
    A = [v + VA15b for v in svt] + [s + sa for s in sp]
    ret = sp[-1] + 371 + (sa - 200)
    return dict(win=(-80, ret + LC15b + 220), pxms=0.25, channels=CH6, title=title, spikes=sp, pace_ch='RVA', src=SRC15,
        beats=[(v, 'n') for v in svt] + [(s, typ) for s in sp] + [(ret, 'n'), (ret + LC15b, 'n')],
        atr=[(a, 'left', -1) for a in A] + [(ret + VA15b, 'left', -1), (ret + LC15b + VA15b, 'left', -1)],
        h_ante=[v - HV for v in svt] + [ret - HV, ret + LC15b - HV], h_retro=[s + 70 for s in sp],
        cal=[(svt[1], svt[1] + VA15b + 2, 'CS 1-2', f'VA {VA15b}'), (sp[-1], A[-1] + 2, 'CS 1-2', f'SA {sa}'), (svt[0], svt[1], 'RVA', f'LC {LC15b}')])


S['p15_diff_a'] = diff15(200, 'pa', 'A. Encarrilamiento desde el ápex del VD (280 ms)')
S['p15_diff_b'] = diff15(190, 'pb', 'B. Encarrilamiento desde la base del VD (280 ms)')

# EV con His refractario desde el ápex: la A siguiente no cambia (la vía está lejos del sitio de estimulación).
k = 3
vs = [i * LC15b for i in range(k)]
h_exp = k * LC15b - HV
after = [k * LC15b + LC15b, k * LC15b + 2 * LC15b]
A = [v + VA15b for v in vs] + [k * LC15b + VA15b] + [v + VA15b for v in after]
S['p15_ehr'] = dict(win=(-80, after[-1] + 200), pxms=0.30, title='EV con His refractario desde el ápex del VD', channels=CH6, src=SRC15,
    spikes=[h_exp], pace_ch='RVA', beats=[(v, 'n') for v in vs] + [(h_exp, 'pa')] + [(v, 'n') for v in after],
    atr=[(a, 'left', -1) for a in A], h_ante=[v - HV for v in vs] + [h_exp] + [v - HV for v in after],
    cal=[(A[k - 2] + 2, A[k - 1] + 2, 'CS 1-2', f'A-A {LC15b}'), (A[k - 1] + 2, A[k] + 2, 'CS 1-2', f'A-A {LC15b}')],
    marks=[(h_exp, 'V1', 'EV'), (h_exp, 'His p', 'H')])

# Para-Hisiana en sinusal: SA 85 → 135, secuencia concéntrica (nodal).
sp = [0, 650, 1300, 1950]
cap = [True, False, True, False]
S['p15_parahis'] = dict(win=(-80, 2300), pxms=0.32, title='Estimulación para-Hisiana en ritmo sinusal', channels=CH6, src=SRC15,
    spikes=sp, pace_ch='His p', beats=[(s + HV if c else s, 'n' if c else 'pa') for s, c in zip(sp, cap)],
    atr=[(s + (85 if c else 135), 'conc_his', -1) for s, c in zip(sp, cap)],
    cal=[(sp[0], sp[0] + 87, 'His d', 'SA 85'), (sp[1], sp[1] + 137, 'His d', 'SA 135'), (sp[2] + HV, sp[2] + HV + 95, 'RVA', 'QRS 95'), (sp[3], sp[3] + 150, 'RVA', 'QRS 150')],
    marks=[(sp[0] + 30, 'V1', 'His + V'), (sp[1] + 40, 'V1', 'solo V')])

# Adenosina: termina con un V (bloqueo en la vía decremental, brazo retrógrado).
vs = [i * LC15b for i in range(4)]
A = [v + VA15b for v in vs[:3]]
S['p15_ado'] = dict(win=(-80, vs[-1] + 700), pxms=0.27, title='Adenosina IV durante la taquicardia', channels=CH6, src=SRC15,
    beats=[(v, 'n') for v in vs], atr=[(a, 'left', -1) for a in A], h_ante=[v - HV for v in vs],
    cal=[(vs[0], vs[1], 'RVA', f'LC {LC15b}'), (vs[1], A[1] + 2, 'CS 1-2', f'VA {VA15b}')],
    marks=[(vs[3] + 120, 'aVF', 'último: V sin A')])

# EA con His refractario desde el ostium del SC: el His siguiente sale a su tiempo.
hs = [i * LC15b - HV for i in range(6)]
apb = hs[3] + 10
vs = [h + HV for h in hs]
A = [v + VA15b for k2, v in enumerate(vs) if k2 != 3]
S['p15_eha'] = dict(win=(-100, vs[-1] + 250), pxms=0.27, title='EA con His refractario desde el ostium del SC', channels=CH6, src=SRC15,
    beats=[(x, 'n') for x in vs], aspikes=[apb], apace_ch='CS 9-10',
    atr=[(a, 'left', -1) for a in A] + [(apb + 4, 'conc_cs', 1)], h_ante=hs,
    cal=[(hs[2], hs[3], 'His d', f'H-H {LC15b}'), (hs[3], hs[4], 'His d', f'H-H {LC15b}')],
    marks=[(apb, 'V1', 'EA')])

if __name__ == '__main__':
    for k in (sys.argv[3:] or S):
        render(S[k], f'{OUT}/{k}.svg')
        print(k)
