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


# Caso 1 (didáctico, TRNAV típica): AH 90, HV 45; inducción con S1-S2 600-300, AH 280 (salto), LC 430, VA 40.
S['c1_basal'] = basal('caso 1 (didáctico): AH 90, HV 45, ilustrativo')

sp = [0, 600, 900]
hs = [s + 28 + a for s, a in zip(sp, [90, 90, 280])]
VA, LC = 40, 430
for _ in range(4):
    hs.append(hs[-1] + LC)
vs = [h + HV for h in hs]
A_echo = [v + VA for v in vs[2:]]
S['c1_ind'] = dict(win=(-80, vs[-1] + 200), pxms=0.30, title='Inducción: extraestímulo auricular (S1-S2 600-300)', channels=CH6,
    src='caso 1 (didáctico): valores ilustrativos',
    beats=[(v, 'n') for v in vs], aspikes=sp, apace_ch='HRA',
    atr=[(s + 5, 'sinus', 1) for s in sp] + [(a, 'conc_his', -1) for a in A_echo], h_ante=hs,
    cal=[(sp[1] + 28, hs[1], 'His d', 'AH 90'), (sp[2] + 28, hs[2], 'His d', 'AH 280'),
         (sp[1], sp[2], 'HRA', 'S2 300'), (vs[3], vs[4], 'RVA', f'LC {LC}')])

if __name__ == '__main__':
    for k in (sys.argv[3:] or list(S)):
        render(S[k], f'{OUT}/{k}.svg')
        print(k)
