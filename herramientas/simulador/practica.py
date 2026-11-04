"""Versiones para el modo práctica: los mismos registros, sin diagnóstico ni cuentas.
- La leyenda solo dice "modo práctica" (sin artículo ni mecanismo).
- Se sacan los rótulos con cuentas o conclusiones (SA−VA, PPI−LC, Δ, →) y las diferencias entre paréntesis.
- Se agregan las mediciones crudas que hacen falta para que el alumno calcule (LC, SA, PPI).
Uso: python3 practica.py <carpeta de simlib.py> <carpeta de salida>"""
import copy, re, sys
D, OUT = sys.argv[1], sys.argv[2]
sys.path.insert(0, D)
import cases, cases2, cases3, cases4
from simlib import render

S = {**cases.S, **cases2.S, **cases3.S, **cases4.S}

USADAS = ['arias10', 'burri12', 'ho15', 'knight99', 'michaud01', 'p10_ehr', 'p10_vop', 'p11_adec', 'p11_anillo', 'p11_eapre',
          'p12_eapre', 'p12_pre', 'p13_abll', 'p2_ehr', 'p3_ado', 'p3_vop', 'p4_ehr_a', 'p4_ehr_b', 'p4_pre', 'p5_ehr', 'p6_aop',
          'p6_ehr', 'p8_verap_a', 'p8_verap_b', 'p9_diff_a', 'p9_diff_b', 'p9_ehr', 'tvf_post', 'veen11_fusion', 'veen11_pseudo', 'veen12_jt']

TITULOS = {'p4_ehr_a': 'A. EV-HR desde el ápex del VD', 'p4_ehr_b': 'B. EV-HR desde el VI basal (rama del SC)',
           'p8_verap_a': 'A. Antes del verapamilo', 'p8_verap_b': 'B. Con verapamilo',
           'p9_diff_a': 'A. Desde el ápex del VD', 'p9_diff_b': 'B. Desde la base del VD'}

RENOMBRAR = {'LC TSV 430': 'LC 430', 'VA': 'VA 120', 'SA': 'SA 160', 'PPI': 'PPI 550', 'PPI−LC 105': 'PPI 495',
             'A adelantada': 'A-A 460', 'potencial M': 'potencial'}

# Calibres agregados: la LC (o el A-A) de la TSV, para que se pueda calcular
EXTRA = {'michaud01': [(0, 470, 'RVA', 'LC 470')], 'p10_vop': [(0, 390, 'RVA', 'LC 390')], 'p10_ehr': [(0, 390, 'RVA', 'LC 390')],
         'p11_eapre': [(0, 300, 'His d', 'LC 300')], 'p12_eapre': [(0, 280, 'His d', 'LC 280')]}
EHR = ['p2_ehr', 'p4_ehr_a', 'p4_ehr_b', 'p5_ehr', 'p6_ehr', 'p9_ehr']   # se agrega el A-A de la TSV


def limpiar(k, sc):
    sc = copy.deepcopy(sc)
    sc['src'] = 'modo práctica (sin interpretación)'
    sc['title'] = TITULOS.get(k, None if not sc.get('title') else sc['title'])
    cal = []
    for t1, t2, ch, lab in sc.get('cal', []):
        lab = RENOMBRAR.get(lab, lab)
        lab = re.sub(r'\s*\((?:[−+]\d+|sin cambio|en vez de [^)]*)\)', '', lab).replace(', mismo QRS', '')
        if any(x in lab for x in ('−LC', 'SA−VA', 'SA − VA', 'Δ', '→')):
            continue
        cal.append((t1, t2, ch, lab))
    cal += EXTRA.get(k, [])
    if k in EHR:
        a0, a1 = sc['atr'][0][0], sc['atr'][1][0]
        cal.append((a0 + 2, a1 + 2, 'CS 9-10', f'A-A {a1 - a0}'))
    if any(l.startswith('PPI') for *_, l in cal) and not any(l.startswith('LC') for *_, l in cal):
        n = sorted(t for t, typ in sc['beats'] if typ == 'n')
        cal.append((n[0], n[1], 'RVA', f'LC {n[1] - n[0]}'))
    sc['cal'] = cal
    sc['marks'] = [(t, ch, RENOMBRAR.get(l, l)) for t, ch, l in sc.get('marks', []) if not any(x in l for x in ('→', 'Δ', 'TRAV', 'TRNAV'))]
    return sc


if __name__ == '__main__':
    for k in USADAS:
        render(limpiar(k, S[k]), f'{OUT}/{k}.svg')
        print(k)
