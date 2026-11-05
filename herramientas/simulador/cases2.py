import sys
sys.path.insert(0, sys.argv[1])
from simlib import render
OUT = sys.argv[2]
HV = 45
S = {}

# A. Arias 2010: RP largo (vía posteroseptal lenta), encarrilamiento desde el ápex del VD.
#    TSV LC 480, VA 296, HA 338; PPI−LC 144 (PPI 624), ΔVA 142 (SA 438), ΔHA 56 (HA 394).
#    Encarrilamiento con 6 estímulos; la LC de estimulación (465) no está publicada.
HVa = 42
LC, VA, SC = 480, 296, 465
svt = [i * LC for i in range(3)]
sp = [svt[-1] + SC * (i + 1) for i in range(6)]
A = [v + VA for v in svt] + [s + 438 for s in sp]
ret = sp[-1] + 624; after = [ret, ret + LC]
S['arias10'] = dict(win=(-100, after[-1] + 380), pxms=0.2,
    src='Arias 2010, figs. 1 y 2: LC 480, VA 296, HA 338, SA 438, HA 394, PPI 624; LC de estimulación 465 ilustrativa',
    beats=[(v, 'n') for v in svt + after] + [(x, 'pa') for x in sp], spikes=sp,
    atr=[(a, 'conc_cs', -1) for a in A + [v + VA for v in after]],
    h_ante=[v - HVa for v in svt + after], h_retro=[a - 394 for a in A[3:]],
    cal=[(svt[0], svt[1], 'RVA', 'LC 480'), (sp[0], sp[1], 'RVA', 'S-S 465'), (sp[-1], ret + 2, 'RVA', 'PPI 624'),
         (A[5] + 38, A[6] + 38, 'HRA', 'A-A 465'), (A[6] + 38, A[7] + 38, 'HRA', 'A-A 465'),
         (svt[2], svt[2] + VA + 2, 'CS 9-10', 'VA 296'), (sp[-1], A[-1] + 2, 'CS 9-10', 'SA 438'),
         (svt[1] - HVa, A[1] + 8, 'His p', 'HA 338'), (A[-1] - 394, A[-1] + 8, 'His p', 'HA 394')],
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
#    4 latidos de base antes del EA.
LC = 412; VA = 15
v = [i * LC for i in range(4)]
apb = v[3] - HV                                # en el momento del His esperado
h_next = apb + LC + 16
vs = v + [h_next + HV, h_next + HV + LC, h_next + HV + 2 * LC]
atr = [(x + VA, 'conc_his', -1) for x in v[:3]] + [(apb + 4, 'conc_cs', 1)] + [(x + VA, 'conc_his', -1) for x in vs[4:]]
S['veen12_eav'] = dict(win=(-100, vs[-1] + 300), pxms=0.27,
    src='Veenhuyzen 2012, fig. 6: TRNAV de LC 412; el EA con His refractario retrasa el His siguiente 16 ms',
    beats=[(x, 'n') for x in vs], aspikes=[apb], apace_ch='CS 9-10',
    atr=atr, h_ante=[x - HV for x in vs],
    cal=[(v[2] - HV, v[3] - HV, 'His d', 'H-H 412'), (v[3] - HV, h_next, 'His d', 'H-H 428 (+16)')],
    marks=[(apb, 'V1', 'EA (ostium del SC)'), (apb, 'His p', 'H')])

# D. Taquicardia de la unión (LC 560). Dos paneles:
#    A. EA desde el ostium del SC con His refractario: no modifica el His siguiente (criterio de Padanilam 2008; ilustrativo).
#    B. Veenhuyzen 2012, fig. 7: EA precoz desde la AD alta adelanta el His inmediato 38 ms y la TSV sigue.
LC = 560
hs = [i * LC - HV for i in range(7)]
vs = [h + HV for h in hs]
apb = hs[4]                                     # en el momento del His esperado: His refractario
atr = [(v, 'conc_his', -1) for k, v in enumerate(vs) if k != 4] + [(apb + 4, 'conc_cs', 1)]
S['veen12_jt_a'] = dict(win=(-100, vs[-1] + 250), pxms=0.22,
    title='A. EA con His refractario (ostium del SC): el His siguiente no cambia',
    src='ilustrativo según Padanilam 2008: en la taquicardia de la unión, el EA con His refractario no modifica el His siguiente',
    beats=[(x, 'n') for x in vs], aspikes=[apb], apace_ch='CS 9-10', atr=atr, h_ante=hs,
    cal=[(hs[3], hs[4], 'His d', 'H-H 560'), (hs[4], hs[5], 'His d', 'H-H 560')],
    marks=[(apb, 'V1', 'EA (ostium del SC)'), (apb, 'His p', 'H')])
hs = [i * LC - HV for i in range(4)]
h_adv = 4 * LC - HV - 38
apb = h_adv - 125
hs += [h_adv, h_adv + LC, h_adv + 2 * LC]
vs = [h + HV for h in hs]
atr = [(v, 'conc_his', -1) for k, v in enumerate(vs) if k != 4] + [(apb + 4, 'sinus', 1)]
S['veen12_jt_b'] = dict(win=(-100, vs[-1] + 250), pxms=0.22,
    title='B. EA precoz (AD alta): adelanta el His inmediato 38 ms y la taquicardia sigue',
    src='Veenhuyzen 2012, fig. 7: LC 560; el EA precoz adelanta el His inmediato 38 ms y la taquicardia continúa',
    beats=[(x, 'n') for x in vs], aspikes=[apb], apace_ch='HRA', atr=atr, h_ante=hs,
    cal=[(hs[2], hs[3], 'His d', 'H-H 560'), (hs[3], hs[4], 'His d', 'H-H 522 (−38)'), (hs[4], hs[5], 'His d', 'H-H 560')],
    marks=[(apb, 'V1', 'EA (AD alta)')])

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

# H. Burri 2012: doble disparo nodal. 134 lpm con RR levemente alternantes y relación P:QRS 1:2 (A-A ≈ 896).
#    Publicado: frecuencia, relación 1:2 y secuencia sinusal. Ilustrativos: AH1 90, H1-H2 430 (rango de Peiker 2016: 265-520).
AA = 896; AH1 = 90; H12 = 430
As = [i * AA for i in range(3)]
h1 = [a + AH1 for a in As]; h2 = [h + H12 for h in h1]
vs = sorted([h + HV for h in h1 + h2])
S['burri12'] = dict(win=(-80, 2450), pxms=0.30, src='Burri 2012 (134 lpm, P:QRS 1:2, A sinusal); AH y H1-H2 ilustrativos',
    channels=['HRA', 'His p', 'His d'],
    beats=[(v, 'n') for v in vs], atr=[(a, 'sinus', 1) for a in As], h_ante=h1 + h2,
    cal=[(As[0], As[1], 'HRA', 'A-A 896: una A cada dos V'), (vs[2], vs[4], 'V1', '2 RR = 896 (134 lpm)')],
    marks=[(h1[1], 'His d', 'H1'), (h2[1], 'His d', 'H2'), (As[1] + 30, 'aVF', 'P'), (vs[2] + 45, 'aVF', 'V1'), (vs[3] + 45, 'aVF', 'V2')])

if __name__ == '__main__':
    only = sys.argv[3:] or list(S)
    for k in only:
        render(S[k], f'{OUT}/{k}.svg')
        print(k)
