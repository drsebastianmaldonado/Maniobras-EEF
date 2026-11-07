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

if __name__ == '__main__':
    for k in (sys.argv[3:] or list(S)):
        render(S[k], f'{OUT}/{k}.svg')
        print(k)
