"""Presentación de los casos de práctica: estudio basal e inducción (polígrafo).
Sin diagnóstico ni cuentas en los rótulos: solo mediciones crudas.
Uso: python3 cases5.py <carpeta de simlib.py> <carpeta de salida> [claves]"""
import sys
sys.path.insert(0, sys.argv[1])
from simlib import render
OUT = sys.argv[2]
HV = 45
S = {}
CH6 = ['HRA', 'His p', 'His d', 'CS 9-10', 'CS 1-2', 'RVA']


def basal(src, ah=90, hv=HV, cl=700, title='Estudio basal: ritmo sinusal', typ='n'):
    a = [0, cl, 2 * cl]
    hs = [x + 28 + ah for x in a]
    return dict(win=(-80, 2 * cl + 330), pxms=0.40, title=title, channels=CH6, src=src,
                beats=[(h + hv, typ) for h in hs], atr=[(x, 'sinus', 1) for x in a], h_ante=hs,
                cal=[(a[0], a[1], 'HRA', f'A-A {cl}'), (a[1] + 28, hs[1], 'His d', f'AH {ah}'),
                     (hs[1], hs[1] + hv, 'His p', f'HV {hv}')])


# Caso 1 (didáctico, TRNAV típica): LC 340 (como el ECG real del caso), VA 40, AH 90, HV 45.
# Inducción con S1-S2 600-300: AH 280 (salto); en la TSV el AH se acomoda a 255.
S['c1_basal'] = basal('caso 1 (didáctico): AH 90, HV 45, ilustrativo')

LC, VA = 340, 40
# A: S1-S2 600-310 → AH 220 (vía rápida, sin eco). B: S2 10 ms más corto (300) → AH 280 (+60: salto) e inducción.
spa = [0, 600, 910]
hsa = [s + 28 + a for s, a in zip(spa, [90, 90, 220])]
vsa = [h + HV for h in hsa]
S['c1_ind_a'] = dict(win=(-80, 2100), pxms=0.30, title='A. Extraestímulo auricular S1-S2 600-310', channels=CH6,
    src='caso 1 (didáctico): valores ilustrativos',
    beats=[(v, 'n') for v in vsa], aspikes=spa, apace_ch='HRA',
    atr=[(s + 5, 'sinus', 1) for s in spa], h_ante=hsa,
    cal=[(spa[1] + 28, hsa[1], 'His d', 'AH 90'), (spa[2] + 28, hsa[2], 'His d', 'AH 220'), (spa[1], spa[2], 'HRA', 'S2 310')])
sp = [0, 600, 900]
hs = [s + 28 + a for s, a in zip(sp, [90, 90, 280])]
for _ in range(5):
    hs.append(hs[-1] + LC)
vs = [h + HV for h in hs]
A_echo = [v + VA for v in vs[2:]]
S['c1_ind_b'] = dict(win=(-80, vs[-1] + 200), pxms=0.30, title='B. S2 10 ms más corto: S1-S2 600-300', channels=CH6,
    src='caso 1 (didáctico): valores ilustrativos',
    beats=[(v, 'n') for v in vs], aspikes=sp, apace_ch='HRA',
    atr=[(s + 5, 'sinus', 1) for s in sp] + [(a, 'conc_his', -1) for a in A_echo], h_ante=hs,
    cal=[(sp[1] + 28, hs[1], 'His d', 'AH 90'), (sp[2] + 28, hs[2], 'His d', 'AH 280 (+60)'),
         (sp[1], sp[2], 'HRA', 'S2 300'), (vs[4], vs[5], 'RVA', f'LC {LC}')])

# Caso 1: sobreestimulación ventricular desde el ápex a 310 (6 estímulos). A-V; SA 190, PPI 510 (PPI−LC 170, SA−VA 150).
SC, SA, PPI = 310, 190, 510
svt = [0, LC, 2 * LC]
sp = [svt[-1] + 290 + SC * k for k in range(6)]
A = [v + VA for v in svt] + [s + SA for s in sp]
ret = sp[-1] + PPI
after = [ret, ret + LC]
S['p1_vop'] = dict(win=(-80, after[-1] + 250), pxms=0.25, title='Sobreestimulación ventricular desde el ápex del VD a 310 ms', channels=CH6,
    src='caso 1 (didáctico): valores ilustrativos',
    beats=[(v, 'n') for v in svt + after] + [(s, 'pa') for s in sp], spikes=sp,
    atr=[(a, 'conc_his', -1) for a in A + [v + VA for v in after]],
    h_ante=[v - HV for v in svt + after], h_retro=[s + 120 for s in sp],
    cal=[(svt[0], svt[1], 'RVA', f'LC {LC}'), (svt[1], svt[1] + VA, 'CS 9-10', f'VA {VA}'),
         (A[-2], A[-1], 'HRA', f'A-A {SC}'), (sp[-1], A[-1] + 2, 'CS 9-10', f'SA {SA}'),
         (sp[-1], ret + 2, 'RVA', f'PPI {PPI}')])

# Caso 4 (Veenhuyzen 2011: LC 340, VA 115; con BRI funcional VA +35 y LC +30). Inducción con S1-S2 600-280:
# los primeros latidos con BRI (VA 150, LC 370), después QRS angosto (VA 115, LC 340). Secuencia excéntrica (SC distal).
CH7 = ['HRA', 'His d', 'CS 9-10', 'CS 5-6', 'CS 1-2', 'RVA']
S['c4_basal'] = basal('caso 4: AH 90, HV 45, ilustrativos')
S['c4_basal']['channels'] = CH7
S['c4_basal']['cal'] = [c if c[2] != 'His p' else (c[0], c[1], 'RVA', c[3]) for c in S['c4_basal']['cal']]
sp = [0, 600, 880]
hs = [s + 28 + a for s, a in zip(sp, [90, 90, 170])]
typ = ['n', 'n', 'lb', 'lb', 'lb', 'n', 'n', 'n']
A = []
for i in range(2, len(typ)):
    va = 150 if typ[i] == 'lb' else 115
    A.append(hs[i] + HV + va)
    if i + 1 < len(typ):
        hs.append(A[-1] + (175 if typ[i + 1] == 'lb' else 180))
vs = [h + HV for h in hs]
S['c4_ind'] = dict(win=(-80, vs[-1] + 220), pxms=0.27, title='Inducción: extraestímulo auricular (S1-S2 600-280)', channels=CH7,
    src='caso 4: LC y VA de Veenhuyzen 2011; el resto ilustrativo',
    beats=[(v, k) for v, k in zip(vs, typ)], aspikes=sp, apace_ch='HRA',
    atr=[(s + 5, 'sinus', 1) for s in sp] + [(a, 'left', -1) for a in A], h_ante=hs,
    cal=[(sp[1], sp[2], 'HRA', 'S2 280'), (sp[2] + 28, hs[2], 'His d', 'AH 170'),
         (vs[3], vs[4], 'RVA', f'LC {vs[4] - vs[3]}'), (vs[3], A[1], 'CS 1-2', f'VA {A[1] - vs[3]}'),
         (vs[6], vs[7], 'RVA', f'LC {vs[7] - vs[6]}'), (vs[6], A[4], 'CS 1-2', f'VA {A[4] - vs[6]}')])

# Caso 14 (didáctico, PJRT en un lactante): LC 300, VA 190, AH 70, HV 40. Valores ilustrativos.
HV14, VA14, AH14, LC14 = 40, 190, 70, 300
S['c14_basal'] = basal('caso 14 (didáctico): AH 70, HV 40, ilustrativos', ah=AH14, hv=HV14, cl=480)
S['c14_basal']['win'] = (-80, 2 * 480 + 330)

# Reinicio espontáneo: tres sinusales (A-A 480) y la TSV arranca sola, sin extrasístole ni cambio del AH.
a_sin = [0, 480, 960]
hs = [a + 28 + AH14 for a in a_sin]
A_ret = []
for _ in range(5):
    A_ret.append(hs[-1] + HV14 + VA14)
    hs.append(A_ret[-1] + 8 + AH14 - 8)          # en la TSV la A más precoz es la del ostium del SC
vs = [h + HV14 for h in hs]
S['c14_ind'] = dict(win=(-80, vs[-1] + 200), pxms=0.30, title='Reinicio espontáneo de la taquicardia', channels=CH6,
    src='caso 14 (didáctico): valores ilustrativos', beats=[(v, 'n') for v in vs],
    atr=[(a, 'sinus', 1) for a in a_sin] + [(a, 'conc_cs', -1) for a in A_ret], h_ante=hs,
    cal=[(a_sin[1], a_sin[2], 'HRA', 'A-A 480'), (a_sin[2] + 28, hs[2], 'His d', f'AH {AH14}'),
         (vs[2], A_ret[0] + 2, 'CS 9-10', f'VA {VA14}'), (vs[4], vs[5], 'RVA', f'LC {LC14}')])

# EV con His refractario: el estímulo cae 30 ms antes del V esperado (el His ya se activó); no hay A y la TSV termina.
vs = [i * LC14 for i in range(4)]
A = [v + VA14 for v in vs]
h_exp = vs[-1] + LC14 - HV14
sp = h_exp + 10
sin_a = sp + 620
hs = [v - HV14 for v in vs] + [h_exp, sin_a + 28 + AH14]
S['p14_ehr'] = dict(win=(-80, sin_a + 28 + AH14 + HV14 + 250), pxms=0.30, title='EV con His refractario durante la taquicardia', channels=CH6,
    src='caso 14 (didáctico): valores ilustrativos',
    beats=[(v, 'n') for v in vs] + [(sp, 'pa'), (sin_a + 28 + AH14 + HV14, 'n')], spikes=[sp],
    atr=[(a, 'conc_cs', -1) for a in A] + [(sin_a, 'sinus', 1)], h_ante=hs,
    cal=[(vs[1], vs[2], 'RVA', f'LC {LC14}'), (vs[2], A[2] + 2, 'CS 9-10', f'VA {VA14}'),
         (vs[-1], sp, 'RVA', f'V-EV {sp - vs[-1]}')],
    marks=[(sp, 'HRA', 'EV')])

# Caso 7 (didáctico, taquicardia de la unión en una lactante): LC 425 como el ECG real. A y V simultáneos.
S['c7_basal'] = basal('caso 7 (didáctico): AH 80, HV 45, ilustrativos', ah=80, cl=600)

# Inicio espontáneo: tres sinusales (A-A 600) y aparecen latidos de la unión que se aceleran (H-H 480, 450, 435, 425).
a_sin = [0, 600, 1200]
hs = [a + 28 + 80 for a in a_sin]
for d in (480, 450, 435, 425, 425):
    hs.append(hs[-1] + d)
vs = [h + HV for h in hs]
S['c7_ind'] = dict(win=(-80, vs[-1] + 220), pxms=0.28, title='Inicio de la taquicardia (espontáneo)', channels=CH6,
    src='caso 7 (didáctico): valores ilustrativos', beats=[(v, 'n') for v in vs],
    atr=[(a, 'sinus', 1) for a in a_sin] + [(v, 'conc_his', -1) for v in vs[3:]], h_ante=hs,
    cal=[(a_sin[1], a_sin[2], 'HRA', 'A-A 600'), (a_sin[2] + 28, hs[2], 'His d', 'AH 80'),
         (hs[2], hs[3], 'His p', 'H-H 480'), (hs[6], hs[7], 'His p', 'H-H 425')])

# EA durante la taquicardia (LC 425), dos paneles como la ficha:
# A. EA con His refractario desde el ostium del SC: el His siguiente no cambia.  B. EA precoz desde la AD alta: adelanta el His 38 ms y sigue.
LC7 = 425
hs = [i * LC7 - HV for i in range(7)]
vs = [h + HV for h in hs]
apb = hs[4]
S['p7_eha_a'] = dict(win=(-100, vs[-1] + 250), pxms=0.25, title='A. EA con His refractario (ostium del SC)', channels=CH6,
    src='caso 7 (didáctico): valores ilustrativos',
    beats=[(x, 'n') for x in vs], aspikes=[apb], apace_ch='CS 9-10',
    atr=[(v, 'conc_his', -1) for k, v in enumerate(vs) if k != 4] + [(apb + 4, 'conc_cs', 1)], h_ante=hs,
    cal=[(hs[3], hs[4], 'His d', f'H-H {LC7}'), (hs[4], hs[5], 'His d', f'H-H {LC7}')],
    marks=[(apb, 'V1', 'EA')])
hs = [i * LC7 - HV for i in range(4)]
h_adv = 4 * LC7 - HV - 38
apb = h_adv - 125
hs += [h_adv, h_adv + LC7, h_adv + 2 * LC7]
vs = [h + HV for h in hs]
S['p7_eha_b'] = dict(win=(-100, vs[-1] + 250), pxms=0.25, title='B. EA precoz (AD alta)', channels=CH6,
    src='caso 7 (didáctico): valores ilustrativos',
    beats=[(x, 'n') for x in vs], aspikes=[apb], apace_ch='HRA',
    atr=[(v, 'conc_his', -1) for k, v in enumerate(vs) if k != 4] + [(apb + 4, 'sinus', 1)], h_ante=hs,
    cal=[(hs[2], hs[3], 'His d', f'H-H {LC7}'), (hs[3], hs[4], 'His d', f'H-H {hs[4] - hs[3]}'), (hs[4], hs[5], 'His d', f'H-H {LC7}')],
    marks=[(apb, 'V1', 'EA')])

# Caso 8 (TV fascicular posterior, LC 420 como el ECG real): basal e inducción con extraestímulos ventriculares.
S['c8_basal'] = basal('caso 8: AH 85, HV 45, ilustrativos', ah=85, cl=800)
S['c8_basal']['win'] = (-80, 2 * 800 + 330)
LC8 = 420
sp = [0, 600, 880]                                    # S1 600 x2, S2 280 desde el ápex del VD
vt = [sp[-1] + 360 + LC8 * k for k in range(6)]
p2 = [v - 30 for v in vt]; p1 = [x - 110 for x in p2]
a_sin = [250, 1050, 1850, 2650]
S['c8_ind'] = dict(win=(-80, vt[-1] + 200), pxms=0.27, title='Inducción: extraestímulo ventricular (S1-S2 600-280)',
    channels=['HRA', 'His d', 'LV 1-2', 'RVA'], src='caso 8: valores ilustrativos',
    beats=[(s, 'pa') for s in sp] + [(v, 'rbs') for v in vt], spikes=sp,
    atr=[(a, 'sinus', 1) for a in a_sin], h_retro=[s + 120 for s in sp] + [v + 15 for v in vt],
    extra={'LV 1-2': [(t, 0.32, 0.8) for t in p1] + [(t, 0.55, 0.7) for t in p2]},
    cal=[(sp[1], sp[2], 'RVA', 'S2 280'), (vt[2], vt[3], 'RVA', f'LC {LC8}'), (a_sin[1], a_sin[2], 'HRA', 'A-A 800')])

# Caso 2 (didáctico, TRAV septal en una niña de 10 años): LC 280 como el ECG real, VA 110, AH en la TSV 125.
S['c2_basal'] = basal('caso 2 (didáctico): AH 80, HV 45, ilustrativos', ah=80, cl=650)
sp = [0, 600, 900]
hs = [s + 28 + a for s, a in zip(sp, [80, 80, 150])]
A = []
for _ in range(6):
    A.append(hs[-1] + HV + 110)
    hs.append(A[-1] + 8 + 117)                       # A más precoz en el ostium del SC
vs = [h + HV for h in hs]
S['c2_ind'] = dict(win=(-80, vs[-1] + 200), pxms=0.30, title='Inducción: extraestímulo auricular (S1-S2 600-300)', channels=CH6,
    src='caso 2 (didáctico): valores ilustrativos', beats=[(v, 'n') for v in vs], aspikes=sp, apace_ch='HRA',
    atr=[(s + 5, 'sinus', 1) for s in sp] + [(a, 'conc_cs', -1) for a in A[:-1]], h_ante=hs[:-1],
    cal=[(sp[1], sp[2], 'HRA', 'S2 300'), (sp[2] + 28, hs[2], 'His d', 'AH 150'),
         (vs[3], A[1] + 2, 'CS 9-10', 'VA 110'), (vs[5], vs[6], 'RVA', f'LC {vs[6] - vs[5]}')])
S['c2_ind']['beats'] = S['c2_ind']['beats'][:-1]
S['c2_ind']['win'] = (-80, vs[-2] + 220)

# Caso 2: encarrilamiento desde el ápex a 250 (6 estímulos). LC 280, VA 110, SA 150, PPI 360 (SA−VA 40 y PPI−LC 80 de Michaud).
LC2, VA2, SC2, SA2, PPI2 = 280, 110, 250, 150, 360
svt = [0, LC2, 2 * LC2]
sp = [svt[-1] + 230 + SC2 * k for k in range(6)]
A = [v + VA2 for v in svt] + [s + SA2 for s in sp]
ret = sp[-1] + PPI2
after = [ret, ret + LC2]
S['p2_vop'] = dict(win=(-80, after[-1] + 220), pxms=0.28, title='Encarrilamiento desde el ápex del VD a 250 ms', channels=CH6,
    src='caso 2 (didáctico): valores ilustrativos',
    beats=[(v, 'n') for v in svt + after] + [(s, 'pa') for s in sp], spikes=sp,
    atr=[(a, 'conc_cs', -1) for a in A + [v + VA2 for v in after]],
    h_ante=[v - HV for v in svt + after], h_retro=[s + 110 for s in sp],
    cal=[(svt[0], svt[1], 'RVA', f'LC {LC2}'), (svt[1], svt[1] + VA2 + 2, 'CS 9-10', f'VA {VA2}'),
         (A[-2] + 2, A[-1] + 2, 'HRA', f'A-A {SC2}'), (sp[-1], A[-1] + 2, 'CS 9-10', f'SA {SA2}'),
         (sp[-1], ret + 2, 'RVA', f'PPI {PPI2}')])

# Caso 3 (TA incesante en una niña de 2 años, LC 270 como el ECG real). Inicio espontáneo con calentamiento.
S['c3_basal'] = basal('caso 3 (didáctico): AH 80, HV 45, ilustrativos', ah=80, cl=550)
a_sin = [0, 550, 1100]
A_ta = [1100 + 340]
for d in (310, 290, 280, 270, 270, 270):
    A_ta.append(A_ta[-1] + d)
hs = [a + 28 + 80 for a in a_sin] + [a + 100 for a in A_ta]
vs = [h + HV for h in hs]
S['c3_ind'] = dict(win=(-80, vs[-1] + 200), pxms=0.30, title='Inicio de la taquicardia (espontáneo)', channels=CH6,
    src='caso 3 (didáctico): valores ilustrativos', beats=[(v, 'n') for v in vs],
    atr=[(a, 'sinus', 1) for a in a_sin] + [(a, 'cs_mid', 1) for a in A_ta], h_ante=hs,
    cal=[(a_sin[1], a_sin[2], 'HRA', 'A-A 550'), (A_ta[0], A_ta[1], 'HRA', f'A-A {A_ta[1] - A_ta[0]}'),
         (A_ta[4], A_ta[5], 'HRA', 'A-A 270'), (A_ta[5] + 20, hs[8], 'His d', 'AH 80')])

# Caso 5 (TRNAV atípica rápida-lenta, LC 460 como el ECG real). Relaciones de Veenhuyzen 2011, fig. 3:
# SA > LC de estimulación (seudo A-A-V), SA−VA 150, PPI−LC 185. VA 300, AH en la TSV 115.
LC5, VA5, SC5, SA5, PPI5 = 460, 300, 430, 450, 645
S['c5_basal'] = basal('caso 5: AH 90, HV 45, ilustrativos', ah=90, cl=750)
S['c5_basal']['win'] = (-80, 2 * 750 + 330)
# Inducción con extraestímulo ventricular S1-S2 600-320: la conducción VA salta a la vía lenta (VA 300) y empieza la TSV.
sp = [0, 600, 920]
A = [sp[0] + 120, sp[1] + 120, sp[2] + 300]
hs = []
for _ in range(4):
    hs.append(A[-1] + 115)
    A.append(hs[-1] + HV + VA5)
vs = [h + HV for h in hs]
S['c5_ind'] = dict(win=(-80, vs[-1] + 330), pxms=0.27, title='Inducción: extraestímulo ventricular (S1-S2 600-320)', channels=CH6,
    src='caso 5: valores ilustrativos', beats=[(s, 'pa') for s in sp] + [(v, 'n') for v in vs], spikes=sp,
    atr=[(a, 'conc_cs', -1) for a in A], h_ante=hs, h_retro=[s + 110 for s in sp],
    cal=[(sp[1], sp[2], 'RVA', 'S2 320'), (sp[1], A[1] + 2, 'CS 9-10', 'SA 120'), (sp[2], A[2] + 2, 'CS 9-10', 'SA 300'),
         (vs[1], vs[2], 'RVA', f'LC {LC5}'), (vs[1], A[4] + 2, 'HRA', f'VA {VA5}')])
# Encarrilamiento desde el ápex a 430 (6 estímulos): después de la última espiga hay dos A antes del V.
svt = [0, LC5]
sp = [svt[-1] + 380 + SC5 * k for k in range(6)]
A = [v + VA5 for v in svt] + [s + SA5 for s in sp]
ret = sp[-1] + PPI5
after = [ret, ret + LC5]
S['p5_vop'] = dict(win=(-100, after[-1] + 340), pxms=0.22, title='Encarrilamiento desde el ápex del VD a 430 ms', channels=CH6,
    src='caso 5: valores ilustrativos según las relaciones de Veenhuyzen 2011, fig. 3',
    beats=[(v, 'n') for v in svt + after] + [(s, 'pa') for s in sp], spikes=sp,
    atr=[(a, 'conc_cs', -1) for a in A + [v + VA5 for v in after]],
    h_ante=[v - HV for v in svt + after], h_retro=[s + 120 for s in sp],
    cal=[(svt[0], svt[1], 'RVA', f'LC {LC5}'), (svt[1], svt[1] + VA5 + 2, 'CS 9-10', f'VA {VA5}'), (sp[0], sp[1], 'RVA', f'S-S {SC5}'),
         (sp[-1], ret + 2, 'RVA', f'PPI {PPI5}'), (sp[-1], A[-1] + 2, 'CS 9-10', f'SA {SA5}'),
         (A[-3] + 38, A[-2] + 38, 'HRA', f'A-A {SC5}'), (A[-2] + 38, A[-1] + 38, 'HRA', f'A-A {SC5}')],
    marks=[(A[-2] + 38, 'His p', 'A₁'), (A[-1] + 38, 'His p', 'A₂')])

# Caso 6 (PJRT, LC 300 como el ECG real). Relaciones de Ho 2015 (PPI−LC 71, ΔVA +19, ΔHA −76, His ortodrómico).
LC6, VA6 = 300, 190
S['c6_basal'] = basal('caso 6: AH 70, HV 45, ilustrativos', ah=70, cl=600)
# Inducción con extraestímulo ventricular: la conducción VA por la vía se alarga (decremental) y empieza la TSV.
sp = [0, 600, 900]
A = [sp[0] + 150, sp[1] + 150, sp[2] + 215]
hs = []
for _ in range(5):
    hs.append(A[-1] + 8 + 57)
    A.append(hs[-1] + HV + VA6)
vs = [h + HV for h in hs]
S['c6_ind'] = dict(win=(-80, vs[-1] + 260), pxms=0.27, title='Inducción: extraestímulo ventricular (S1-S2 600-300)', channels=CH6,
    src='caso 6: valores ilustrativos', beats=[(s, 'pa') for s in sp] + [(v, 'n') for v in vs], spikes=sp,
    atr=[(a, 'conc_cs', -1) for a in A], h_ante=hs, h_retro=[s + 110 for s in sp],
    cal=[(sp[1], sp[2], 'RVA', 'S2 300'), (sp[1], A[1] + 2, 'CS 9-10', 'SA 150'), (sp[2], A[2] + 2, 'CS 9-10', 'SA 215'),
         (vs[2], vs[3], 'RVA', f'LC {LC6}'), (vs[2], A[5] + 2, 'HRA', f'VA {VA6}')])
# Encarrilamiento desde el ápex a 280 con captura ortodrómica del His (6 estímulos). VA 209, HA 159, PPI 371.
svt = [i * LC6 for i in range(3)]
sp = [svt[-1] + 280 * (k + 1) for k in range(6)]
A = [v + VA6 for v in svt] + [s + 209 for s in sp]
ret = sp[-1] + 371
after = [ret, ret + LC6]
S['p6_vop'] = dict(win=(-100, after[-1] + 300), pxms=0.25, title='Encarrilamiento desde el ápex del VD a 280 ms', channels=CH6,
    src='caso 6: valores ilustrativos según las relaciones de Ho 2015',
    beats=[(v, 'n') for v in svt + after] + [(x, 'pa') for x in sp], spikes=sp,
    atr=[(a, 'conc_cs', -1) for a in A + [v + VA6 for v in after]],
    h_ante=[v - HV for v in svt + after] + [a - 159 for a in A[3:]],
    cal=[(svt[0], svt[1], 'RVA', f'LC {LC6}'), (sp[0], sp[1], 'RVA', 'S-S 280'), (sp[-1], ret + 2, 'RVA', 'PPI 371'),
         (A[5] + 8, A[6] + 8, 'HRA', 'A-A 280'), (A[6] + 8, A[7] + 8, 'HRA', 'A-A 280'),
         (svt[2] - HV, A[2] + 8, 'His p', f'HA {HV + VA6}'), (A[-1] - 159, A[-1] + 8, 'His p', 'HA 159'),
         (svt[1], A[1] + 8, 'CS 9-10', f'VA {VA6}'), (sp[-1], A[-1] + 8, 'CS 9-10', 'SA 209')])

# Caso 12 (TRAV antidrómica por una vía derecha, LC 245 como el ECG real). Basal preexcitado e inducción con extraestímulo auricular.
a = [0, 640, 1280]
hs = [x + 28 + 85 for x in a]
S['c12_basal'] = dict(win=(-80, 1280 + 360), pxms=0.40, title='Estudio basal: ritmo sinusal', channels=['HRA', 'AD lat', 'His d', 'CS 9-10', 'RVA'],
    src='caso 12 (didáctico): valores ilustrativos', beats=[(x + 95, 'lb') for x in a], atr=[(x, 'sinus', 1) for x in a], h_ante=hs,
    extra={'AD lat': [(x + 30, 0.8, 1.0) for x in a] + [(x + 95 + 20, 0.9, 1.6) for x in a]},
    cal=[(a[0], a[1], 'HRA', 'A-A 640'), (a[1], a[1] + 95, 'HRA', 'AV 95'), (a[1] + 28, hs[1], 'His d', 'AH 85')],
    marks=[(hs[1], 'His p' if False else 'His d', '')])
S['c12_basal'].pop('marks')
sp = [0, 600, 880]
vs = [s + 95 for s in sp[:2]] + [sp[2] + 95]
A = [vs[2] + 160]
for _ in range(5):
    vs.append(A[-1] + 85)
    A.append(vs[-1] + 160)
S['c12_ind'] = dict(win=(-80, vs[-1] + 200), pxms=0.30, title='Inducción: extraestímulo auricular (S1-S2 600-280)',
    channels=['HRA', 'AD lat', 'His p', 'His d', 'CS 9-10', 'RVA'], src='caso 12 (didáctico): valores ilustrativos',
    beats=[(v, 'lb') for v in vs], aspikes=sp, apace_ch='HRA',
    atr=[(s + 5, 'sinus', 1) for s in sp] + [(x, 'conc_his', -1) for x in A[:-1]], h_ante=[s + 28 + 90 for s in sp[:2]],
    h_retro=[v + 120 for v in vs[2:]], extra={'AD lat': [(s + 30, 0.8, 1.0) for s in sp] + [(x + 25, 0.8, 1.0) for x in A[:-1]]},
    cal=[(sp[1], sp[2], 'HRA', 'S2 280'), (vs[3], vs[4], 'RVA', f'LC {vs[4] - vs[3]}'), (vs[3], A[1] + 2, 'HRA', 'VA 160')])

# Caso 11 (Mahaim, LC 260 como el ECG real). Basal sin preexcitación evidente; inducción con extraestímulo auricular.
S['c11_basal'] = basal('caso 11 (didáctico): AH 90, HV 45, ilustrativos', ah=90, cl=700)
S['c11_basal']['win'] = (-80, 2 * 700 + 330)
sp = [0, 600, 860]
hs0 = [s + 28 + 90 for s in sp[:2]]
vs = [h + HV for h in hs0] + [sp[2] + 170]
A = []
for _ in range(5):
    A.append(vs[-1] + 110)
    vs.append(A[-1] + 150)
S['c11_ind'] = dict(win=(-80, vs[-1] + 200), pxms=0.30, title='Inducción: extraestímulo auricular (S1-S2 600-260)',
    channels=['HRA', 'AD lat', 'His p', 'His d', 'CS 9-10', 'RVA'], src='caso 11 (didáctico): valores ilustrativos',
    beats=[(v, 'n') for v in vs[:2]] + [(v, 'lb') for v in vs[2:]], aspikes=sp, apace_ch='HRA',
    atr=[(s + 5, 'sinus', 1) for s in sp] + [(x, 'conc_his', -1) for x in A[:-1]], h_ante=hs0, h_retro=[v + 25 for v in vs[2:]],
    extra={'AD lat': [(s + 30, 0.8, 1.0) for s in sp] + [(x + 30, 0.8, 1.0) for x in A[:-1]]},
    cal=[(sp[1], sp[2], 'HRA', 'S2 260'), (sp[2], vs[2], 'HRA', 'AV 170'), (vs[3], vs[4], 'RVA', f'LC {vs[4] - vs[3]}'),
         (vs[3], A[1] + 2, 'CS 9-10', 'VA 110')])

# Caso 9 (TRAV por vía septal lenta y decremental, LC 310 como el ECG real). VA 180, HA 222; desde el ápex
# PPI−LC 144 (Arias 2010), SA−VA 100 y ΔHA +40 (en rango de TRNAV por el decremento; ilustrativos a esta LC).
LC9, VA9, HV9 = 310, 180, 42
S['c9_basal'] = basal('caso 9: AH 80, HV 42, ilustrativos', ah=80, hv=HV9, cl=650)
sp = [0, 600, 900]
hs = [s + 28 + a for s, a in zip(sp, [80, 80, 140])]
A = []
for _ in range(5):
    A.append(hs[-1] + HV9 + VA9)
    hs.append(A[-1] + 8 + 80)
vs = [h + HV9 for h in hs]
S['c9_ind'] = dict(win=(-80, vs[-2] + 240), pxms=0.29, title='Inducción: extraestímulo auricular (S1-S2 600-300)', channels=CH6,
    src='caso 9: valores ilustrativos', beats=[(v, 'n') for v in vs[:-1]], aspikes=sp, apace_ch='HRA',
    atr=[(s + 5, 'sinus', 1) for s in sp] + [(a, 'conc_cs', -1) for a in A[:-1]], h_ante=hs[:-1],
    cal=[(sp[1], sp[2], 'HRA', 'S2 300'), (sp[2] + 28, hs[2], 'His d', 'AH 140'), (vs[3], A[1] + 2, 'CS 9-10', f'VA {VA9}'),
         (vs[4], vs[5], 'RVA', f'LC {vs[5] - vs[4]}')])
svt = [i * LC9 for i in range(3)]
sp = [svt[-1] + 295 * (k + 1) for k in range(6)]
A = [v + VA9 for v in svt] + [s + 280 for s in sp]
ret = sp[-1] + 454
after = [ret, ret + LC9]
S['p9_vop'] = dict(win=(-100, after[-1] + 300), pxms=0.24, title='Encarrilamiento desde el ápex del VD a 295 ms', channels=CH6,
    src='caso 9: valores ilustrativos (PPI−LC de Arias 2010)',
    beats=[(v, 'n') for v in svt + after] + [(x, 'pa') for x in sp], spikes=sp,
    atr=[(a, 'conc_cs', -1) for a in A + [v + VA9 for v in after]],
    h_ante=[v - HV9 for v in svt + after], h_retro=[a - 262 for a in A[3:]],
    cal=[(svt[0], svt[1], 'RVA', f'LC {LC9}'), (sp[0], sp[1], 'RVA', 'S-S 295'), (sp[-1], ret + 2, 'RVA', 'PPI 454'),
         (A[5] + 38, A[6] + 38, 'HRA', 'A-A 295'), (A[6] + 38, A[7] + 38, 'HRA', 'A-A 295'),
         (svt[2], svt[2] + VA9 + 2, 'CS 9-10', f'VA {VA9}'), (sp[-1], A[-1] + 2, 'CS 9-10', 'SA 280'),
         (svt[1] - HV9, A[1] + 8, 'His p', f'HA {HV9 + VA9}'), (A[-1] - 262, A[-1] + 8, 'His p', 'HA 262')])

# Caso 13 (doble disparo nodal; AH1 90 y H1–H2 430 de Burri 2012). Basal y paso de 1:1 a 1:2 en sinusal.
S['c13_basal'] = basal('caso 13: AH 90, HV 45 (AH de Burri 2012)', ah=90, cl=900)
S['c13_basal']['win'] = (-80, 2 * 900 + 330)
As = [0, 900, 1800, 2700, 3600]
h1 = [a + 28 + 90 for a in As]
h2 = [h1[k] + 430 for k in (2, 3, 4)]
vs = sorted([h + HV for h in h1 + h2])
S['c13_ind'] = dict(win=(-80, As[-1] + 750), pxms=0.22, title='Ritmo sinusal al inicio del estudio',
    channels=['HRA', 'His p', 'His d', 'CS 9-10', 'RVA'], src='caso 13: AH1 90 y H1–H2 430 de Burri 2012; el resto ilustrativo',
    beats=[(v, 'n') for v in vs], atr=[(a, 'sinus', 1) for a in As], h_ante=sorted(h1 + h2),
    cal=[(As[1], As[2], 'HRA', 'A-A 900'), (As[2] + 28, h1[2], 'His d', 'AH 90'), (h1[3], h2[1], 'His d', 'H-H 430')])

# Caso 10 (vía nodoventricular con bloqueo VA tipo Wenckebach, LC 390). Basal con doble vía; inducción con salto AH.
S['c10_basal'] = basal('caso 10 (didáctico): AH 85, HV 45, ilustrativos', ah=85, cl=750)
S['c10_basal']['win'] = (-80, 2 * 750 + 330)
LC10 = 390
sp = [0, 600, 900]
hs = [s + 28 + a for s, a in zip(sp, [85, 85, 245])]
for _ in range(6):
    hs.append(hs[-1] + LC10)
vs = [h + HV for h in hs]
va = [110, 150, 175, None, 110, 150, 175]          # VA que se alarga hasta que una V no conduce a la A
A = [v + d for v, d in zip(vs[2:], va) if d is not None]
S['c10_ind'] = dict(win=(-80, vs[-1] + 200), pxms=0.25, title='Inducción: extraestímulo auricular (S1-S2 600-300)', channels=CH6,
    src='caso 10 (didáctico): valores ilustrativos', beats=[(v, 'n') for v in vs], aspikes=sp, apace_ch='HRA',
    atr=[(s + 5, 'sinus', 1) for s in sp] + [(a, 'conc_his', -1) for a in A], h_ante=hs,
    cal=[(sp[1] + 28, hs[1], 'His d', 'AH 85'), (sp[2] + 28, hs[2], 'His d', 'AH 245'), (sp[1], sp[2], 'HRA', 'S2 300'),
         (hs[4], hs[5], 'His d', f'H-H {LC10}'), (hs[5], hs[6], 'His d', f'H-H {LC10}'),
         (vs[2], A[0] + 2, 'CS 9-10', 'VA 110'), (vs[3], A[1] + 2, 'CS 9-10', 'VA 150'), (vs[4], A[2] + 2, 'CS 9-10', 'VA 175')])

# Caso 15 (TRAV por vía lateral izquierda decremental, registros reales): sobreestimulación auricular SIMULADA.
# LC 311 (real); VA 140 ilustrativo, A más precoz en el SC distal. Estimulación desde la AD alta a 280 (6 estímulos):
# al cortar, el VA del primer latido de retorno es igual al de la TSV (VA linking).
LC15, VA15 = 311, 140
vs = [0, LC15, 2 * LC15]
A = [v + VA15 for v in vs]
sp = [A[-1] + 230 + 280 * k for k in range(6)]
hs_p = [s + 28 + 150 for s in sp]
vp = [h + HV for h in hs_p]
after = [vp[-1] + LC15 * k for k in range(1, 3)]
S['p15_aop'] = dict(win=(-80, after[-1] + 260), pxms=0.25, title='Sobreestimulación auricular desde la AD alta a 280 ms', channels=CH6,
    src='caso 15: registro simulado (LC 311 del estudio real; VA 140 ilustrativo)',
    beats=[(v, 'n') for v in vs + vp + after], aspikes=sp, apace_ch='HRA',
    atr=[(a, 'left', -1) for a in A] + [(s + 5, 'sinus', 1) for s in sp] + [(v + VA15, 'left', -1) for v in [vp[-1]] + after],
    h_ante=[v - HV for v in vs] + hs_p + [v - HV for v in after],
    cal=[(vs[1], vs[2], 'RVA', f'LC {LC15}'), (vs[1], A[1] + 2, 'CS 1-2', f'VA {VA15}'), (sp[-2], sp[-1], 'HRA', 'S-S 280'),
         (vp[-1], vp[-1] + VA15 + 2, 'CS 1-2', f'VA {VA15}')])

# TRNAV típica con vía lateral izquierda espectadora (didáctico): LC 350, VA 20 concéntrico.
LCb, VAb = 350, 20
CHb = ['HRA', 'His p', 'His d', 'CS 9-10', 'CS 7-8', 'CS 5-6', 'CS 3-4', 'CS 1-2', 'RVA']
vs = [i * LCb for i in range(6)]
S['bys_a'] = dict(win=(-80, vs[-1] + 250), pxms=0.30, title='A. TRNAV típica: VA 20 ms, activación concéntrica', channels=CHb,
    src='didáctico: valores ilustrativos', beats=[(v, 'n') for v in vs], atr=[(v + VAb, 'conc_his', -1) for v in vs],
    h_ante=[v - HV for v in vs],
    cal=[(vs[1], vs[2], 'RVA', f'LC {LCb}'), (vs[2], vs[2] + VAb + 2, 'His d', f'VA {VAb}')])
# B. Sobreestimulación del VD a 320 (6 estímulos): retrógrada por la vía (excéntrica, SA 150); al cortar A-V y vuelve la concéntrica.
svt = [0, LCb]
sp = [svt[-1] + 280 + 320 * k for k in range(6)]
ret = sp[-1] + 500
after = [ret, ret + LCb]
S['bys_b'] = dict(win=(-80, after[-1] + 250), pxms=0.22, title='B. Sobreestimulación del VD a 320 ms: secuencia excéntrica durante el tren', channels=CHb,
    src='didáctico: valores ilustrativos', beats=[(v, 'n') for v in svt + after] + [(s, 'pa') for s in sp], spikes=sp,
    atr=[(v + VAb, 'conc_his', -1) for v in svt + after] + [(s + 150, 'left', -1) for s in sp],
    h_ante=[v - HV for v in svt + after], h_retro=[s + 90 for s in sp],
    cal=[(sp[-2], sp[-1], 'RVA', 'S-S 320'), (sp[-1], sp[-1] + 152, 'CS 1-2', 'SA 150'), (sp[-1], ret + 2, 'RVA', 'PPI 500')],
    marks=[(sp[-1] + 150, 'CS 9-10', 'último A (excéntrico)'), (ret + VAb, 'CS 9-10', 'A concéntrica')])
# C. EV con His refractario (95 ms antes del V esperado): adelanta la A del SC distal (fusión excéntrica) y la TSV no cambia.
vs = [i * LCb for i in range(6)]
T = vs[3]
pvc = T - 95
S['bys_c'] = dict(win=(-80, vs[-1] + 250), pxms=0.30, title='C. EV con His refractario: adelanta la A del SC distal, el His siguiente no cambia', channels=CHb,
    src='didáctico: valores ilustrativos', beats=[(v, 'n') for k, v in enumerate(vs) if k != 3] + [(pvc, 'lv')], spikes=[pvc], pace_ch='RVA',
    atr=[(v + VAb, 'conc_his', -1) for k, v in enumerate(vs) if k != 3] + [(T + 5, 'fus_l', -1)],
    h_ante=[v - HV for v in vs],
    cal=[(vs[2] - HV, vs[3] - HV, 'His d', f'H-H {LCb}'), (vs[3] - HV, vs[4] - HV, 'His d', f'H-H {LCb}'), (vs[2] + VAb + 42, T + 5, 'CS 1-2', f'A-A {T + 5 - vs[2] - VAb - 42} (−{LCb - (T + 5 - vs[2] - VAb - 42)})')],
    marks=[(pvc, 'V1', 'EV-HR'), (T + 5, 'CS 3-4', 'A del SC distal adelantada')])

# Caso 17 (registros reales) — maniobras SIMULADAS con la LC real de cada TSV.
CH17 = ['HRA', 'His d', 'His p', 'CS 1-2', 'CS 3-4', 'CS 5-6', 'CS 9-10', 'RVA']   # de distal a proximal, como en el polígrafo del autor
# TRAV por vía izquierda: LC 390 (real), VA 130 (ilustrativo), A más precoz en el SC 3-4. Encarrilamiento desde el ápex a 360:
# SA 210, PPI 490 (PPI−LC 100, SA−VA 80).
LCt, VAt = 390, 130
svt = [0, LCt]
sp = [svt[-1] + 330 + 360 * k for k in range(6)]
A = [v + VAt for v in svt] + [s + 210 for s in sp]
ret = sp[-1] + 490
after = [ret, ret + LCt]
S['c17s_vop_a'] = dict(win=(-80, after[-1] + 250), pxms=0.20, title='A. TSV 1 (LC 390): encarrilamiento desde el ápex del VD a 360 ms', channels=CH17,
    src='caso 17: registro simulado; LC 390 del estudio real, el resto ilustrativo',
    beats=[(v, 'n') for v in svt + after] + [(s, 'pa') for s in sp], spikes=sp,
    atr=[(a, 'left34', -1) for a in A + [v + VAt for v in after]], h_ante=[v - HV for v in svt + after], h_retro=[s + 110 for s in sp],
    cal=[(svt[0], svt[1], 'RVA', f'LC {LCt}'), (svt[1], svt[1] + VAt + 2, 'CS 3-4', f'VA {VAt}'), (A[-2], A[-1], 'HRA', 'A-A 360'),
         (sp[-1], A[-1] + 2, 'CS 3-4', 'SA 210'), (sp[-1], ret + 2, 'RVA', 'PPI 490')])
# TRNAV típica: LC 230 (real), VA 20 (ilustrativo), concéntrica. Encarrilamiento desde el ápex a 210: SA 170, PPI 400.
LCn, VAn = 230, 20
svt = [0, LCn, 2 * LCn]
sp = [svt[-1] + 200 + 210 * k for k in range(6)]
A = [v + VAn for v in svt] + [s + 170 for s in sp]
ret = sp[-1] + 400
after = [ret, ret + LCn, ret + 2 * LCn]
S['c17s_vop_b'] = dict(win=(-80, after[-1] + 200), pxms=0.26, title='B. TSV 2 (LC 230): encarrilamiento desde el ápex del VD a 210 ms', channels=CH17,
    src='caso 17: registro simulado; LC 230 del estudio real, el resto ilustrativo',
    beats=[(v, 'n') for v in svt + after] + [(s, 'pa') for s in sp], spikes=sp,
    atr=[(a, 'conc_his', -1) for a in A + [v + VAn for v in after]], h_ante=[v - HV for v in svt + after], h_retro=[s + 100 for s in sp],
    cal=[(svt[0], svt[1], 'RVA', f'LC {LCn}'), (svt[1], svt[1] + VAn + 2, 'His d', f'VA {VAn}'), (A[-2], A[-1], 'HRA', 'A-A 210'),
         (sp[-1], A[-1] + 2, 'CS 9-10', 'SA 170'), (sp[-1], ret + 2, 'RVA', 'PPI 400')])
# EV con His refractario en la TSV 1: adelanta la A 20 ms con la misma secuencia y resetea.
vs = [i * LCt for i in range(3)]
pvc = 3 * LCt - HV - 10
a_new = 3 * LCt + VAt - 20
nxt = a_new + (LCt - VAt)
after = [nxt, nxt + LCt]
S['c17s_ehr'] = dict(win=(-80, after[-1] + 220), pxms=0.26, title='C. TSV 1: EV con His refractario', channels=CH17,
    src='caso 17: registro simulado; LC 390 del estudio real, el resto ilustrativo',
    beats=[(v, 'n') for v in vs] + [(pvc, 'pa')] + [(v, 'n') for v in after], spikes=[pvc],
    atr=[(v + VAt, 'left34', -1) for v in vs] + [(a_new, 'left34', -1)] + [(v + VAt, 'left34', -1) for v in after],
    h_ante=[v - HV for v in vs] + [3 * LCt - HV] + [v - HV for v in after],
    cal=[(vs[1] + VAt, vs[2] + VAt, 'CS 3-4', f'A-A {LCt}'), (vs[2] + VAt, a_new, 'CS 3-4', f'A-A {LCt - 20} (−20)')],
    marks=[(pvc, 'V1', 'EV-HR')])

if __name__ == '__main__':
    for k in (sys.argv[3:] or list(S)):
        render(S[k], f'{OUT}/{k}.svg')
        print(k)
