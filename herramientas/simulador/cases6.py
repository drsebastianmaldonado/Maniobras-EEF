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
S['p1_medidas'] = dict(win=(-80, after[-1] + 250), pxms=0.25, title='Medidas sobre la sobreestimulación ventricular (ápex del VD a 310 ms)',
    channels=CH6, src=SRC,
    beats=[(v, 'n') for v in svt + after] + [(s, 'pa') for s in sp], spikes=sp,
    atr=[(a, 'trnav', -1) for a in A + [v + VA for v in after]],
    h_ante=[v - HV for v in svt + after], h_retro=[s + 120 for s in sp],
    cal=[(svt[0], svt[1], 'RVA', f'LC {LC}'), (svt[1], svt[1] + VA, 'CS 9-10', f'VA {VA}'),
         (sp[-1], A[-1] + 2, 'CS 9-10', f'SA {SA}'), (sp[-1], ret + 2, 'RVA', f'PPI {PPI}')],
    marks=[(sp[-1] + 260, 'I', f'SA − VA = {SA} − {VA} = {SA - VA} ms'), (sp[-1] + 260, 'aVF', f'PPI − LC = {PPI} − {LC} = {PPI - LC} ms')])


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
    cal=[(vs[1], vs[1] + VA + 2, 'CS 9-10', f'VA {VA}'), (sp[-2], sp[-1], 'HRA', 'S-S 320'),
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

if __name__ == '__main__':
    for k in (sys.argv[3:] or S):
        render(S[k], f'{OUT}/{k}.svg')
        print(k)
