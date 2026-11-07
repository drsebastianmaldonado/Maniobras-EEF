"""Registros simulados para los resultados clave del modo práctica.
Los intervalos de los hallazgos del caso se respetan; lo que no está en el caso es ilustrativo y la leyenda lo aclara.
Los escenarios con _a y _b son dos paneles que se unen después."""
import sys
sys.path.insert(0, sys.argv[1])
from simlib import render
OUT = sys.argv[2]
HV = 45
S = {}
CH = ['HRA', 'His p', 'His d', 'CS 9-10', 'CS 5-6', 'CS 1-2', 'RVA']


def ehr(LC, VA, seq, d, k_spike=3, early=0, typ='pa', pace='RVA', n_after=2, title=None, src='', lab=None, mark='EV-HR'):
    """TSV 1:1; EV con His refractario en el ciclo k. d > 0 adelanta la A, d < 0 la retrasa, 0 = sin efecto."""
    vs = [i * LC for i in range(k_spike)]
    h_exp = k_spike * LC - HV
    sp = h_exp - early                      # early = cuánto antes del His esperado
    A = [v + VA for v in vs]
    a_new = k_spike * LC + VA - d
    A.append(a_new)
    nxt = a_new + (LC - VA) if d else k_spike * LC + LC
    after = [nxt + i * LC for i in range(n_after)]
    A += [v + VA for v in after]
    beats = [(v, 'n') for v in vs] + [(sp, typ)] + [(v, 'n') for v in after]
    h = [v - HV for v in vs] + [h_exp] + [v - HV for v in after]
    cal = [(A[k_spike - 2] + 2, A[k_spike - 1] + 2, 'CS 9-10', f'A-A {LC}'), (A[k_spike - 1] + 2, a_new + 2, 'CS 9-10', lab or f'A-A {LC - d}')]
    return dict(win=(-80, after[-1] + 200), pxms=0.30, channels=CH, title=title, src=src, spikes=[sp], pace_ch=pace,
                beats=beats, atr=[(a, seq, -1) for a in A], h_ante=h, cal=cal,
                marks=[(sp, 'V1', mark), (h_exp, 'His p', 'H')])


# Caso 2: TRAV septal, LC 280 (como el ECG real del caso), VA 110; EV-HR adelanta la A 25 ms.
S['p2_ehr'] = ehr(280, 110, 'conc_cs', 25, src='caso 2 (didáctico): LC 280, VA 110; la EV con His refractario adelanta la A 25 ms',
                  lab='A-A 255 (−25)')
# Caso 5: TRNAV atípica, LC 380, VA 265; EV-HR adelanta el V local > 60 ms y no cambia la A.
S['p5_ehr'] = ehr(460, 300, 'conc_cs', 0, early=25, src='caso 5 (LC 460 como el ECG real, VA 300); EV-HR con el V local adelantado > 60 ms, sin cambio de la A',
                  lab='A-A 460 (sin cambio)')
# Caso 6: PJRT, LC 521, VA 290; EV-HR retrasa la A 20 ms.
S['p6_ehr'] = ehr(300, 190, 'conc_cs', -20, src='caso 6 (LC 300 como el ECG real, VA 190); EV-HR que retrasa la A 20 ms', lab='A-A 320 (+20)')
# Caso 9: PJRT (Arias 2010), LC 480, VA 296; EV-HR adelanta la A (magnitud ilustrativa).
S['p9_ehr'] = ehr(310, 180, 'conc_cs', 20, src='caso 9 (LC 310 como el ECG real, VA 180); EV-HR que adelanta la A 20 ms', lab='A-A 290 (−20)')
S['p9_ehr']['pxms'] = 0.25
# Caso 4: TRAV lateral izquierda, LC 340, VA 115; desde el ápex no cambia la A, desde el VI basal la adelanta 20 ms.
S['p4_ehr_a'] = ehr(340, 115, 'left', 0, title='A. EV-HR desde el ápex del VD: la A no cambia', src='caso 4 (Veenhuyzen 2011: LC 340, VA 115); adelanto de 20 ms del caso',
                    lab='A-A 340')
S['p4_ehr_b'] = ehr(340, 115, 'left', 20, typ='lv', pace='CS 1-2', title='B. EV-HR desde el VI basal (rama del SC): adelanta la A 20 ms',
                    src='caso 4 (Veenhuyzen 2011: LC 340, VA 115); adelanto de 20 ms del caso', lab='A-A 320 (−20)', mark='EV-HR (VI)')

# Caso 4: estudio basal: estimulación ventricular con conducción VA excéntrica y no decremental (SA igual a 500 y 400).
sp = [0, 500, 1000, 1400, 1800]
S['p4_pre'] = dict(win=(-80, 2150), pxms=0.30, channels=CH, src='caso 4: conducción VA excéntrica, no decremental (SA 120 a 500 y a 400 ms, ilustrativo)',
    spikes=sp, beats=[(s, 'pa') for s in sp], atr=[(s + 120, 'left', -1) for s in sp],
    cal=[(sp[1], sp[1] + 122, 'CS 1-2', 'SA 120'), (sp[3], sp[3] + 122, 'CS 1-2', 'SA 120'), (sp[0], sp[1], 'RVA', '500'), (sp[2], sp[3], 'RVA', '400')],
    marks=[(sp[1] + 120, 'CS 9-10', 'A más precoz en el SC distal')])

# Caso 3: TA (LC 270, como el ECG real del caso); adenosina: bloqueo AV 2:1 y la TA sigue.
LC = 270
A = [i * LC for i in range(9)]
cond = [0, 1, 2, 4, 6, 7, 8]
hs = [A[i] + 100 for i in cond]
S['p3_ado'] = dict(win=(-80, A[-1] + 300), pxms=0.29, channels=CH, src='caso 3 (didáctico): valores ilustrativos',
    beats=[(h + HV, 'n') for h in hs], atr=[(a, 'cs_mid', 1) for a in A], h_ante=hs,
    cal=[(A[3], A[4], 'HRA', f'A-A {LC}')], marks=[(A[3] + 30, 'aVF', 'A sin V'), (A[5] + 30, 'aVF', 'A sin V')])

# Caso 6: sobreestimulación auricular en la PJRT (LC 300 como el ECG real; ΔAH 10 de Ho 2015). Estimulación a 280, 6 estímulos.
LC, VA, AH = 300, 190, 65
vs = [0, LC, 2 * LC]
A = [v + VA for v in vs]
sp = [A[-1] + 230 + 280 * k for k in range(6)]
pv = [s + 28 + AH + 10 + HV for s in sp]
last = pv[-1]
vs2 = [last + LC, last + 2 * LC]
S['p6_aop'] = dict(win=(-80, vs2[-1] + 300), pxms=0.25, channels=CH, title='Sobreestimulación auricular desde la AD alta a 280 ms',
    src='caso 6: valores ilustrativos (ΔAH 10 ms de Ho 2015)',
    beats=[(v, 'n') for v in vs + pv + vs2], aspikes=sp, apace_ch='HRA',
    atr=[(a, 'conc_cs', -1) for a in A] + [(s + 5, 'sinus', 1) for s in sp] + [(v + VA, 'conc_cs', -1) for v in [last] + vs2],
    h_ante=[v - HV for v in vs + pv + vs2],
    cal=[(A[1] + 8, vs[2] - HV, 'His d', f'AH {AH}'), (sp[-1] + 28, pv[-1] - HV, 'His d', f'AH {AH + 10}'), (sp[-2], sp[-1], 'HRA', 'S-S 280')],
    marks=[(pv[-1] + 40, 'I', 'ΔAH 10 → la aurícula está en el circuito')])

# Caso 9: encarrilamiento diferencial (Arias 2010): ΔVA −28 (base − ápex). SA y LC absolutos ilustrativos (SA ápex 438 publicado a otra LC).
def diff(sa, typ, pace, title):
    LC, VA = 310, 180
    svt = [0, LC]; sp = [600 + 295 * k for k in range(6)]
    A = [v + VA for v in svt] + [s + sa for s in sp]
    ret = A[-1] + (LC - VA)
    return dict(win=(-80, ret + 520), pxms=0.22, channels=CH, title=title, spikes=sp, pace_ch=pace,
        src='caso 9 (LC 310 como el ECG real): ΔVA −28 (base − ápex) de Arias 2010; SA ilustrativos, estimulación a 295',
        beats=[(v, 'n') for v in svt] + [(s, typ) for s in sp] + [(ret, 'n'), (ret + LC, 'n')],
        atr=[(a, 'conc_cs', -1) for a in A] + [(ret + VA, 'conc_cs', -1), (ret + LC + VA, 'conc_cs', -1)],
        h_ante=[v - HV for v in svt] + [ret - HV, ret + LC - HV],
        cal=[(svt[1], svt[1] + VA + 2, 'CS 9-10', f'VA {VA}'), (sp[-1], A[-1] + 2, 'CS 9-10', f'SA {sa}'),
             (A[-2] + 38, A[-1] + 38, 'HRA', 'A-A 295'), (svt[0], svt[1], 'RVA', f'LC {LC}')])
S['p9_diff_a'] = diff(280, 'pa', 'RVA', 'A. Desde el ápex del VD: SA − VA 100')
S['p9_diff_b'] = diff(252, 'lv', 'RVA', 'B. Desde la base: SA − VA 72 → ΔVA (base − ápex) −28: TRAV')

# Caso 10: vía nodoventricular. LC 390; EV-HR adelanta el His siguiente.
LC = 390
vs = [0, LC, 2 * LC]
h_exp = 3 * LC - HV
sp = h_exp - 10
hn = h_exp + LC - 25
after = [hn + HV, hn + HV + LC]
A = [vs[0] + 100, vs[1] + 130, after[0] + 100, after[1] + 130]
S['p10_ehr'] = dict(win=(-80, after[-1] + 250), pxms=0.28, channels=CH,
    src='Nagashima 2020 (vía nodoventricular, LC 390); EV-HR que adelanta el His siguiente 25 ms (ilustrativo); bloqueo VA tipo Wenckebach',
    beats=[(v, 'n') for v in vs] + [(sp, 'pa')] + [(v, 'n') for v in after], spikes=[sp],
    atr=[(a, 'conc_his', -1) for a in A], h_ante=[v - HV for v in vs] + [h_exp, hn, after[1] - HV],
    cal=[(vs[2] - HV, hn, 'His d', 'H-H 755 (en vez de 780)')],
    marks=[(sp, 'V1', 'EV-HR'), (hn, 'His p', 'H adelantado'), (vs[2] + 40, 'aVF', 'A bloqueada')])

# Caso 10: sobreestimulación del VD: fusión, His ortodrómico, V-V-A, PPI−LC 105 (Nagashima 2020).
LC = 390
vs = [0, LC]
sp = [700, 1060, 1420, 1780]
ret = sp[-1] + LC + 105
after = [ret, ret + LC]
A = [vs[0] + 100, 1060 + 110, 1780 + 400, after[1] + 100]
S['p10_vop'] = dict(win=(-80, after[-1] + 250), pxms=0.25, channels=CH,
    src='Nagashima 2020: PPI−LC 105, His ortodrómico, fusión constante y respuesta V-V-A; LC de estimulación 360 y VA ilustrativos',
    beats=[(v, 'n') for v in vs] + [(s, 'f') for s in sp] + [(v, 'n') for v in after], spikes=sp,
    atr=[(a, 'conc_his', -1) for a in A], h_ante=[v - HV for v in vs] + [s - 10 for s in sp] + [v - HV for v in after],
    cal=[(sp[-1], ret + 2, 'RVA', 'PPI−LC 105')],
    marks=[(sp[1] - 10, 'His p', 'H ortodr.'), (sp[2], 'V1', 'fusión'), (ret, 'aVF', 'V'), (after[1], 'aVF', 'V'), (after[1] + 100, 'His p', 'A')])

# Caso 11 (Mahaim): estimulación auricular decremental: el AV se alarga, el HV se acorta hasta hacerse negativo y aumenta el BRI.
sp = [0, 500, 900, 1250]
ahs = [90, 120, 160, 210]
ap = [150, 160, 170, 180]           # conducción decremental por la vía atriofascicular
typs = ['n', 'f', 'lb', 'lb']
hs = [s + 28 + a for s, a in zip(sp, ahs)]
qrs = [min(h + HV, s + d) for h, s, d in zip(hs, sp, ap)]
S['p11_adec'] = dict(win=(-80, 1620), pxms=0.40, channels=['HRA', 'His p', 'His d', 'CS 9-10', 'RVA'],
    src='caso 11 (Mahaim, didáctico): estimulación de la AD a 500, 400 y 350 ms; AV, AH y HV ilustrativos',
    beats=list(zip(qrs, typs)), aspikes=sp, apace_ch='HRA', atr=[(s + 5, 'sinus', 1) for s in sp], h_ante=hs,
    cal=[(hs[0], qrs[0], 'His d', 'HV 45'), (qrs[2], hs[2], 'His d', 'HV −18'), (sp[3], qrs[3], 'HRA', 'AV 180')],
    marks=[(qrs[1], 'V1', 'BRI incipiente'), (qrs[3], 'V1', 'BRI completo'), (hs[3], 'His p', 'H después del QRS')])

# Caso 11: EA desde la AD lateral con la unión refractaria adelanta el V sin cambiar el QRS y resetea (TRAV antidrómica por Mahaim).
# LC 260 como el ECG real del caso; AV por la vía 150, VA por el nodo 110. El EA cae 30 ms antes de la A esperada.
LC, VA = 260, 110
vs = [0, LC, 2 * LC, 3 * LC]
A = [v + VA for v in vs[:3]]
ea = vs[3] + VA - 30
v_new = 4 * LC - 25
after = [v_new + i * LC for i in range(3)]
A += [v + VA for v in after]
S['p11_eapre'] = dict(win=(-80, after[-1] + 220), pxms=0.30, channels=['HRA', 'AD lat', 'His p', 'His d', 'CS 9-10', 'RVA'],
    src='caso 11 (didáctico): LC 260; EA desde la AD lateral que adelanta el V 25 ms',
    beats=[(v, 'lb') for v in vs + after], aspikes=[ea], apace_ch='AD lat', atr=[(a, 'conc_his', -1) for a in A] + [(ea + 3, 'right', 1)],
    h_retro=[v + 25 for v in vs + after], extra={'AD lat': [(a + 30, 0.9, 1.0) for a in A]},
    cal=[(vs[2], vs[3], 'RVA', f'V-V {LC}'), (vs[3], v_new, 'RVA', f'V-V {LC - 25} (−25), mismo QRS')], marks=[(ea, 'V1', 'EA (AD lateral)')])

# Caso 11: potencial de la vía atriofascicular en el anillo tricuspídeo lateral (entre la A y el V), durante estimulación auricular.
sp = [0, 600, 1200]
S['p11_anillo'] = dict(win=(-80, 1600), pxms=0.42, channels=['HRA', 'Abl d', 'Abl p', 'His d', 'RVA'],
    src='caso 11 (didáctico): potencial de la vía (M) en el anillo tricuspídeo lateral, entre la A y el V',
    beats=[(s + 170, 'lb') for s in sp], aspikes=sp, apace_ch='HRA', atr=[(s + 5, 'right', 1) for s in sp], h_ante=[s + 210 for s in sp],
    extra={'Abl d': [(s + 25, 0.9, 1.0) for s in sp] + [(s + 75, 0.7, 0.5) for s in sp] + [(s + 220, 0.5, 1.6) for s in sp],
           'Abl p': [(s + 30, 0.8, 1.0) for s in sp] + [(s + 225, 0.4, 1.6) for s in sp]},
    marks=[(sp[1] + 75, 'Abl d', 'potencial M'), (sp[1] + 25, 'Abl p', 'A')])

# Caso 12: TRAV antidrómica por una vía derecha (LC 245, como el ECG real del caso). EA desde la AD lateral con la unión
# refractaria adelanta el V y la A 30 ms. QRS preexcitado con V1 negativo.
LC = 245
vs = [0, LC, 2 * LC, 3 * LC]
A = [v + 160 for v in vs[:3]]
ea = vs[3] + 130                         # 30 ms antes de la A esperada: el His ya se activó en forma retrógrada (unión refractaria)
v_new = 4 * LC - 30
after = [v_new + i * LC for i in range(3)]
A2 = [v + 160 for v in after]
S['p12_eapre'] = dict(win=(-80, after[-1] + 220), pxms=0.32, channels=['HRA', 'AD lat', 'His p', 'His d', 'CS 9-10', 'RVA'],
    src='caso 12 (didáctico): LC 245; EA desde la AD lateral que adelanta el V y la A 30 ms',
    beats=[(v, 'lb') for v in vs + after], aspikes=[ea], apace_ch='AD lat',
    atr=[(x, 'conc_his', -1) for x in A + A2] + [(ea + 3, 'right', 1)],
    h_retro=[v + 120 for v in vs + after], extra={'AD lat': [(x + 25, 0.8, 1.0) for x in A + A2]},
    cal=[(vs[2], vs[3], 'RVA', f'V-V {LC}'), (vs[3], v_new, 'RVA', f'V-V {LC - 30} (−30)'), (A[2], ea, 'HRA', f'A-A {LC - 30}')],
    marks=[(ea, 'V1', 'EA (AD lateral)'), (v_new, 'aVF', 'mismo QRS')])

# Caso 12: estimulación auricular en ritmo sinusal: preexcitación con AV corto que no se alarga (vía tipo Kent).
sp = [0, 500, 900, 1250]
hs = [s + 28 + a for s, a in zip(sp, [90, 120, 160, 210])]
S['p12_pre'] = dict(win=(-80, 1600), pxms=0.40, channels=['HRA', 'AD lat', 'His d', 'CS 9-10', 'RVA'],
    src='caso 12 (didáctico): estimulación de la AD a 500, 400 y 350 ms; el AV por la vía se mantiene en 95 ms mientras el AH se alarga',
    beats=[(s + 95, 'lb') for s in sp], aspikes=sp, apace_ch='HRA', atr=[(s + 5, 'sinus', 1) for s in sp], h_ante=hs,
    extra={'AD lat': [(s + 30, 0.8, 1.0) for s in sp] + [(s + 95 + 20, 0.9, 1.6) for s in sp]},
    cal=[(sp[1], sp[1] + 95, 'HRA', 'AV 95'), (sp[3], sp[3] + 95, 'HRA', 'AV 95')],
    marks=[(sp[3] + 95, 'V1', 'preexcitación máxima'), (hs[3], 'His d', 'H dentro del QRS')])

# Caso 13: ablación de la vía lenta en el doble disparo: desaparece el segundo His.
AA, AH1, H12 = 896, 90, 430
As = [i * AA for i in range(4)]
h1 = [a + AH1 for a in As]
h2 = [h1[0] + H12, h1[1] + H12]
vs = sorted([h + HV for h in h1 + h2])
S['p13_abll'] = dict(win=(-80, As[-1] + 450), pxms=0.22, channels=['HRA', 'His p', 'His d', 'Abl d'],
    src='Burri 2012: la radiofrecuencia en la vía lenta suprimió el doble disparo (AH y H1-H2 ilustrativos)',
    beats=[(v, 'n') for v in vs], atr=[(a, 'sinus', 1) for a in As], h_ante=h1 + h2,
    extra={'Abl d': [(a + 60, 0.5, 1.0) for a in As] + [(v + 30, 0.6, 1.6) for v in vs]},
    cal=[(As[2] - 200, As[-1] + 300, 'Abl d', 'RF en la vía lenta')],
    marks=[(h2[1], 'His d', 'H2'), (As[2] + 300, 'aVF', 'un solo QRS por P')])


# Caso 3: TA (LC 270). Sobreestimulación del VD a 240 (6 estímulos): las A se aceleran con secuencia retrógrada (distinta de la TA);
# al cortar, A-A-V: después del último A acelerado sale otra A del foco antes del V.
LC, SC = 270, 240
A0 = [0, LC, 2 * LC]
vs0 = [a + 100 + HV for a in A0]
sp = [vs0[-1] + 200 + SC * k for k in range(6)]
Aret = [s + 120 for s in sp]
focal = Aret[-1] + 330
v_after = focal + 100 + HV
S['p3_vop'] = dict(win=(-80, v_after + 380), pxms=0.25, channels=CH, title='Sobreestimulación ventricular desde el ápex del VD a 240 ms',
    src='caso 3 (didáctico): valores ilustrativos',
    beats=[(v, 'n') for v in vs0] + [(s, 'pa') for s in sp] + [(v_after, 'n'), (v_after + LC, 'n')], spikes=sp,
    atr=[(a, 'cs_mid', 1) for a in A0] + [(a, 'conc_his', -1) for a in Aret] + [(focal, 'cs_mid', 1), (focal + LC, 'cs_mid', 1)],
    h_ante=[v - HV for v in vs0] + [v_after - HV, v_after + LC - HV], h_retro=[s + 110 for s in sp],
    cal=[(A0[0], A0[1], 'HRA', f'A-A {LC}'), (Aret[-2], Aret[-1], 'HRA', f'A-A {SC}'), (Aret[-1], focal, 'CS 9-10', f'A-A {focal - Aret[-1]}')],
    marks=[(Aret[-1], 'His p', 'A'), (focal, 'His p', 'A'), (v_after, 'aVF', 'V')])


# Caso 8: TV fascicular posterior (LC 420, como el ECG real del caso). Con verapamilo se alarga la LC: P1-P2 y P2-P1 se alargan; P2-QRS no cambia.
def tvf(LC, p1p2, title):
    vs = [i * LC for i in range(6)]
    p2 = [v - 30 for v in vs]
    p1 = [x - p1p2 for x in p2]
    ext = {'LV 1-2': [(t, 0.32, 0.8) for t in p1] + [(t, 0.55, 0.7) for t in p2]}
    return dict(win=(-60, vs[-1] + 150), pxms=0.30, title=title, channels=['HRA', 'His d', 'LV 1-2', 'RVA'],
        src='caso 8: LC 420 como el ECG real; el alargamiento con verapamilo es ilustrativo, P2-QRS 30 ms en ambos',
        beats=[(v, 'rbs') for v in vs], atr=[(a, 'sinus', 1) for a in [130, 930, 1730] if a < vs[-1]], h_retro=[v + 15 for v in vs],
        extra=ext, cal=[(vs[1], vs[2], 'RVA', f'LC {LC}'), (p1[3], p2[3], 'LV 1-2', f'P1-P2 {p1p2}'), (p2[4], vs[4], 'LV 1-2', 'P2-V 30')])
S['p8_verap_a'] = tvf(420, 110, 'A. Antes del verapamilo')
S['p8_verap_b'] = tvf(480, 160, 'B. Con verapamilo: se alargan la LC y el P1-P2; el P2-QRS no cambia')

if __name__ == '__main__':
    only = sys.argv[3:] or list(S)
    for k in only:
        render(S[k], f'{OUT}/{k}.svg')
        print(k)
