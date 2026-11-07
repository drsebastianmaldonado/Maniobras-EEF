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
sp = [0, 600, 900]
hs = [s + 28 + a for s, a in zip(sp, [90, 90, 280])]
for _ in range(5):
    hs.append(hs[-1] + LC)
vs = [h + HV for h in hs]
A_echo = [v + VA for v in vs[2:]]
S['c1_ind'] = dict(win=(-80, vs[-1] + 200), pxms=0.30, title='Inducción: extraestímulo auricular (S1-S2 600-300)', channels=CH6,
    src='caso 1 (didáctico): valores ilustrativos',
    beats=[(v, 'n') for v in vs], aspikes=sp, apace_ch='HRA',
    atr=[(s + 5, 'sinus', 1) for s in sp] + [(a, 'conc_his', -1) for a in A_echo], h_ante=hs,
    cal=[(sp[1] + 28, hs[1], 'His d', 'AH 90'), (sp[2] + 28, hs[2], 'His d', 'AH 280'),
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

if __name__ == '__main__':
    for k in (sys.argv[3:] or list(S)):
        render(S[k], f'{OUT}/{k}.svg')
        print(k)
