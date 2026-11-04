import sys
sys.path.insert(0, sys.argv[1])
from simlib import render
OUT = sys.argv[2]
HV = 45
S = {}

# A. Arias 2010: RP largo (vía posteroseptal lenta), encarrilamiento desde el ápex del VD.
#    TSV LC 480, VA 296, HA 338; PPI−LC 144 (PPI 624), ΔVA 142 (SA 438), ΔHA 56 (HA 394).
HVa = 42
svt = [0, 480]; sp = [900, 1365, 1830]
A = [v + 296 for v in svt] + [s + 438 for s in sp]
ret = sp[-1] + 624; after = [ret, ret + 480]
S['arias10'] = dict(win=(-120, 2900), pxms=0.26, src='intervalos de Arias 2010, figs. 1 y 2',
    beats=[(v, 'n') for v in svt + after] + [(s, 'pa') for s in sp], spikes=sp,
    atr=[(a, 'conc_cs', -1) for a in A + [v + 296 for v in after]],
    h_ante=[v - HVa for v in svt + after], h_retro=[a - 394 for a in A[2:]],
    cal=[(svt[1], svt[1] + 296 + 2, 'CS 9-10', 'VA 296'), (sp[-1], A[-1] + 2, 'CS 9-10', 'SA 438'),
         (sp[-1], ret + 2, 'RVA', 'PPI 624')],
    marks=[])

# B. Veenhuyzen 2011, fig. 5: encarrilamiento manifiesto desde el VI basal (vía lateral izquierda).
#    LC 340, estimulación 320, PPI 430, AH de retorno 240 vs 180, SA−VA −20.
VA = 115; AHs = 180
svt = [0, 340]; sp = [700, 1020, 1340]
A = [v + VA for v in svt] + [s + VA - 20 for s in sp]
h_orto = [a + AHs for a in A[2:4]]           # His ortodrómico durante la estimulación
ret_h = A[-1] + 240; ret = ret_h + HV; after = [ret, ret + 340]
S['veen11_fusion'] = dict(win=(-100, 2180), pxms=0.34, src='intervalos de Veenhuyzen 2011, fig. 5',
    beats=[(v, 'n') for v in svt + after] + [(s, 'fl') for s in sp], spikes=sp, pace_ch='CS 1-2',
    atr=[(a, 'left', -1) for a in A + [v + VA for v in after]],
    h_ante=[v - HV for v in svt] + h_orto + [ret_h, after[1] - HV],
    cal=[(0, 340, 'RVA', 'LC 340'), (sp[0], sp[1], 'RVA', 'estim. 320'), (svt[1] - HV - AHs, svt[1] - HV, 'His d', 'AH 180'),
         (A[-1] + 40, ret_h, 'His d', 'AH 240'), (sp[-1], sp[-1] + 430, 'CS 1-2', 'PPI 430')],
    marks=[(sp[0] + 10, 'V1', 'fusión'), (h_orto[0], 'His p', 'H ortodr.')])

# C. Veenhuyzen 2012, fig. 6: TRNAV típica (LC 412); EA desde el ostium del SC con His refractario retrasa el His 16 ms.
LC = 412; VA = 15
v = [0, 412, 824]
apb = 2 * LC - HV                              # en el momento del His esperado
h_next = apb + LC + 16
vs = v + [h_next + HV, h_next + HV + LC, h_next + HV + 2 * LC]
atr = [(x + VA, 'conc_his', -1) for x in v[:2]] + [(apb + 4, 'conc_cs', 1)] + [(x + VA, 'conc_his', -1) for x in vs[3:]]
S['veen12_eav'] = dict(win=(-100, 2380), pxms=0.30, src='intervalos de Veenhuyzen 2012, fig. 6',
    beats=[(x, 'n') for x in vs], aspikes=[apb], apace_ch='CS 9-10',
    atr=atr, h_ante=[x - HV for x in vs],
    cal=[(v[1] - HV, v[2] - HV, 'His d', 'H-H 412'), (v[2] - HV, h_next, 'His d', 'H-H 428 (+16)')],
    marks=[(apb, 'V1', 'EA (ostium del SC)')])

# D. Veenhuyzen 2012, fig. 7: taquicardia de la unión (LC 560); EA desde la AD alta adelanta el His inmediato 38 ms y la TSV sigue.
LC = 560
hs = [-HV, LC - HV]
h3 = 2 * LC - HV - 38
apb = h3 - 125
hs += [h3, h3 + LC, h3 + 2 * LC]
vs = [h + HV for h in hs]
atr = [(vs[0], 'conc_his', -1), (vs[1], 'conc_his', -1), (apb + 4, 'sinus', 1), (vs[3], 'conc_his', -1), (vs[4], 'conc_his', -1)]
S['veen12_jt'] = dict(win=(-100, 2360), pxms=0.30, src='intervalos de Veenhuyzen 2012, fig. 7',
    beats=[(x, 'n') for x in vs], aspikes=[apb], apace_ch='HRA',
    atr=atr, h_ante=hs,
    cal=[(hs[0], hs[1], 'His d', 'H-H 560'), (hs[1], hs[2], 'His d', 'H-H 522 (−38)'), (hs[2], hs[3], 'His d', 'H-H 560')],
    marks=[(apb, 'V1', 'EA (AD alta)')])

# E. Kaneko 2011: TRNAV rápida-lenta con conducción AV 2:1 (AH 252, HA 136 → LC 388).
LC = 388
As = [i * LC for i in range(7)]
cond = As[::2]
hs = [a + 252 for a in cond]
S['kaneko11'] = dict(win=(-100, 2550), pxms=0.28, src='intervalos de Kaneko 2011, fig. 1',
    beats=[(h + HV, 'n') for h in hs], atr=[(a, 'conc_cs', -1) for a in As], h_ante=hs,
    cal=[(As[2] + 8, hs[1], 'His d', 'AH 252'), (hs[1], As[3] + 8, 'His d', 'HA 136'), (As[3], As[4], 'HRA', 'A-A 388')],
    marks=[(As[1] + 180, 'aVF', 'A sin V')])

# F. Gardey 2021: nodos AV gemelos. Baja por el nodo superior (AH 70, HV 47) y sube por el inferior (VH 133, HA 100) → LC 350.
LC = 350
As = [i * LC for i in range(7)]
hsup = [a + 70 for a in As]
vs = [h + 47 for h in hsup]
hinf = [v + 133 for v in vs]
ext = {'Nodo sup.': [(a, 0.35, 1.2) for a in As] + [(h, 0.7, 0.6) for h in hsup],
       'Nodo inf.': [(h, 0.6, 0.6) for h in hinf] + [(h + 100, 0.9, 1.2) for h in hinf]}
S['gardey21'] = dict(win=(-60, 2300), pxms=0.30, src='intervalos de Gardey 2021, fig. 3',
    channels=['AD lateral', 'Nodo sup.', 'Nodo inf.'] + ['CS 9-10', 'CS 5-6', 'CS 1-2', 'RVA'],
    beats=[(v, 'n') for v in vs], atr=[(h + 100, 'conc_cs', -1) for h in hinf[:-1]] + [(As[0], 'conc_cs', -1)],
    extra=dict(ext, **{'AD lateral': [(h + 140, 0.9, 1.0) for h in hinf[:-1]] + [(40, 0.9, 1.0)]}),
    cal=[(As[1], hsup[1], 'Nodo sup.', 'AH 70'), (hsup[4], vs[4] + 4, 'Nodo sup.', 'HV 47'),
         (vs[2] + 4, hinf[2], 'Nodo inf.', 'VH 133'), (hinf[4], hinf[4] + 100, 'Nodo inf.', 'HA 100')])

# G. TV fascicular posterior: LC 337 y P1-V 45 (Liu Q 2023); P2 ~30 ms antes del QRS (Liu 2015); His 5–30 ms después
#    del inicio del QRS (Nogami 2010); disociación AV con ritmo sinusal independiente.
LC = 337
vs = [i * LC for i in range(7)]
lv = ['LV 9-10', 'LV 7-8', 'LV 5-6', 'LV 3-4', 'LV 1-2']
ext = {}
for i, n in enumerate(lv):  # 0 = proximal, 4 = distal
    p1 = [v - 85 + 10 * i for v in vs]          # P1: proximal → distal; P1-V 45 en el distal
    p2 = [v - 14 - 4 * i for v in vs]          # P2: distal → proximal; ~30 ms antes del QRS en el distal
    ext[n] = [(t, 0.32, 0.8) for t in p1] + [(t, 0.55, 0.7) for t in p2]
sinus = [130, 930, 1730]
S['tvf_post'] = dict(win=(-60, 2200), pxms=0.32, src='intervalos de Liu Q 2023 (LC 337, P1-V 45), Liu 2015 y Nogami 2010',
    channels=['HRA', 'His d'] + lv + ['RVA'],
    beats=[(v, 'rbs') for v in vs], atr=[(a, 'sinus', 1) for a in sinus], h_retro=[v + 15 for v in vs],
    extra=ext,
    cal=[(vs[2], vs[3], 'RVA', 'LC 337'), (vs[4] - 45, vs[4], 'LV 1-2', 'P1-V 45')],
    marks=[(vs[3] - 85, 'LV 9-10', 'P1'), (vs[3] - 30, 'LV 1-2', 'P2'), (vs[5] + 15, 'His d', 'H')])

only = sys.argv[3:] or list(S)
for k in only:
    render(S[k], f'{OUT}/{k}.svg')
    print(k)
