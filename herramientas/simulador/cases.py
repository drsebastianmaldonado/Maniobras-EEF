import sys
sys.path.insert(0, sys.argv[1])
from simlib import render
OUT = sys.argv[2]
HV = 45
S = {}

# 1. Knight 1999: TRNAV típica, LC 430, estimulación VD 370 → A-V
#    VA 40, SA 190 (SA−VA 150) y PPI 600 (PPI−LC 170): ilustrativos, iguales a los del caso 1 de práctica.
svt = [0, 430]; sp = [700, 1070, 1440]
A = [v + 40 for v in svt] + [s + 190 for s in sp]
ret_v = sp[-1] + 600; ret_h = ret_v - HV; after = [ret_v, ret_v + 430]
S['knight99'] = dict(win=(-120, 2560), src='Knight 1999, fig. 1 (LC 430, estimulación 370); SA, PPI y VA ilustrativos',
    beats=[(v, 'n') for v in svt + after] + [(s, 'pa') for s in sp], spikes=sp,
    atr=[(a, 'conc_his', -1) for a in A + [v + 40 for v in after]],
    h_ante=[v - HV for v in svt + after], h_retro=[s + 120 for s in sp],
    cal=[(0, 430, 'RVA', 'LC TSV 430'), (sp[0], sp[1], 'RVA', 'S-S 370'), (sp[-1], ret_v + 2, 'RVA', 'PPI 600'),
         (sp[-1], A[-1] + 2, 'CS 9-10', 'SA 190'), (svt[1], svt[1] + 40, 'CS 9-10', 'VA 40')],
    marks=[(A[-1], 'HRA', 'último A'), (ret_v + 215, 'His p', 'PPI−LC 170 · SA−VA 150 → TRNAV')])

# 2. Veenhuyzen 2011 fig. 3: seudo A-A-V (TRNAV rápida-lenta). LC 380, VA 265, estimulación 360, SA 415, PPI 565.
#    Encarrilamiento con 6 estímulos, A-A a 360, LC y PPI.
LC, VA = 380, 265
svt = [0, LC]; sp = [700 + 360 * i for i in range(6)]
A = [v + VA for v in svt] + [s + 415 for s in sp]
ret = sp[-1] + 565; after = [ret, ret + LC]
S['veen11_pseudo'] = dict(win=(-100, after[-1] + 330), pxms=0.25, title='Encarrilamiento desde el ápex del VD a 360 ms',
    src='Veenhuyzen 2011, fig. 3: LC 380, estimulación 360, PPI 565',
    beats=[(v, 'n') for v in svt + after] + [(s, 'pa') for s in sp], spikes=sp,
    atr=[(a, 'conc_cs', -1) for a in A + [v + VA for v in after]],
    h_ante=[v - HV for v in svt + after], h_retro=[s + 120 for s in sp],
    cal=[(svt[0], svt[1], 'RVA', 'LC 380'), (sp[0], sp[1], 'RVA', 'S-S 360'), (sp[-1], ret + 2, 'RVA', 'PPI 565'),
         (A[4] + 38, A[5] + 38, 'HRA', 'A-A 360'), (A[5] + 38, A[6] + 38, 'HRA', 'A-A 360')],
    marks=[(A[-2] + 38, 'CS 9-10', 'A₁'), (A[-1] + 38, 'CS 9-10', 'A₂')])

# 3. González-Torrecilla 2006: PPI corregido (TRAV). Publicados: LC 300, PPI 440, AH 130 (1.er retorno) vs 80 (TSV).
#    Encarrilamiento desde el ápex con 6 estímulos; la LC de estimulación (270) es ilustrativa. VA 175 (TSV) y SA 265 resultan de lo anterior.
LC, VA, AHt, AHr, PPI, SC = 300, 175, 80, 130, 440, 270
svt = [i * LC for i in range(3)]
sp = [svt[-1] + SC + SC * i for i in range(6)]
A = [v + VA for v in svt] + [s + (PPI - HV - AHr) for s in sp]
ret = sp[-1] + PPI; after = [ret, ret + LC]
S['gt06'] = dict(win=(-80, after[-1] + 280), pxms=0.25,
    src='González-Torrecilla 2006, fig. 2: LC 300, PPI 440, AH 130 vs 80; LC de estimulación 270 ilustrativa',
    beats=[(v, 'n') for v in svt + after] + [(s, 'pa') for s in sp], spikes=sp,
    atr=[(a, 'conc_cs', -1) for a in A + [v + VA for v in after]],
    h_ante=[v - HV for v in svt + after], h_retro=[s + 60 for s in sp],
    cal=[(svt[0], svt[1], 'RVA', 'LC 300'), (sp[0], sp[1], 'RVA', 'S-S 270'), (sp[-1], ret + 2, 'RVA', 'PPI 440'),
         (A[4] + 38, A[5] + 38, 'HRA', 'A-A 270'), (A[5] + 38, A[6] + 38, 'HRA', 'A-A 270'),
         (A[1] + 8, svt[2] - HV, 'His d', 'AH 80'), (A[-1] + 8, ret - HV, 'His d', 'AH 130')])

# 4. Miller 1991: ΔHA en TRAV posteroseptal. LC 340; HA 199 en la TSV y 103 estimulando el VD a la LC de la TSV (en sinusal).
#    Panel A: TSV. Panel B: estimulación del ápex a 340 ms, 6 estímulos. El momento del His retrógrado (95 ms tras la espiga) es ilustrativo.
LC = 340
svt = [i * LC for i in range(5)]
S['miller91_a'] = dict(win=(-100, svt[-1] + 280), pxms=0.27, title='A. Taquicardia: HA 199 ms',
    src='Miller 1991, fig. 3: LC 340, HA 199 en la TSV',
    beats=[(v, 'n') for v in svt], atr=[(v - HV + 199, 'conc_cs', -1) for v in svt], h_ante=[v - HV for v in svt],
    cal=[(svt[0], svt[1], 'RVA', 'LC 340'), (svt[2] - HV, svt[2] - HV + 199 + 8, 'His d', 'HA 199')])
sp = [i * LC for i in range(6)]
hr = [x + 95 for x in sp]
S['miller91_b'] = dict(win=(-100, sp[-1] + 300), pxms=0.27,
    title='B. Estimulación del ápex del VD a 340 ms (la LC de la TSV), en ritmo sinusal: HA 103 ms',
    src='Miller 1991, fig. 3: HA 103 estimulando a la LC de la TSV; el momento del His retrógrado es ilustrativo',
    beats=[(x, 'pa') for x in sp], spikes=sp, atr=[(h + 103, 'conc_cs', -1) for h in hr],
    extra={'His p': [(h, 0.45, 0.6) for h in hr], 'His d': [(h, 0.7, 0.6) for h in hr]},
    cal=[(sp[0], sp[1], 'RVA', 'S-S 340'), (hr[2], hr[2] + 103 + 8, 'His d', 'HA 103')],
    marks=[(hr[3], 'His p', 'H retrógrado')])

# 5. Ho 2015 fig. 3: PJRT con captura ortodrómica del His. LC 521, VA 290, HA 335; estimulación 490: VA 309, HA 259; PPI 592.
#    Encarrilamiento con 6 estímulos.
LC, VA = 521, 290
svt = [i * LC for i in range(3)]
sp = [svt[-1] + 490 * (i + 1) for i in range(6)]
A = [v + VA for v in svt] + [s + 309 for s in sp]
ret = sp[-1] + 592; after = [ret, ret + LC]
S['ho15'] = dict(win=(-100, after[-1] + 380), pxms=0.2,
    src='Ho 2015, fig. 3: LC 521, estimulación 490, HA 335 (TSV) y 259 (estimulando), PPI 592',
    beats=[(v, 'n') for v in svt + after] + [(x, 'pa') for x in sp], spikes=sp,
    atr=[(a, 'conc_cs', -1) for a in A + [v + VA for v in after]],
    h_ante=[v - HV for v in svt + after] + [a - 259 for a in A[3:]],
    cal=[(svt[0], svt[1], 'RVA', 'LC 521'), (sp[0], sp[1], 'RVA', 'S-S 490'), (sp[-1], ret + 2, 'RVA', 'PPI 592'),
         (A[5] + 38, A[6] + 38, 'HRA', 'A-A 490'), (A[6] + 38, A[7] + 38, 'HRA', 'A-A 490'),
         (svt[2] - HV, A[2] + 8, 'His p', 'HA 335'), (A[-1] - 259, A[-1] + 8, 'His p', 'HA 259')],
    marks=[(A[-2] - 259, 'His d', 'H ortodr.')])

# 6. Veenhuyzen 2012 fig. 4: índice VA (ápex 142 ms, base 120 ms), estimulando en ritmo sinusal.
#    Dos paneles: A, ápex del VD; B, VD posterobasal. LC de estimulación 600 ilustrativa.
sp = [i * 600 for i in range(4)]
S['veen12_vai_a'] = dict(win=(-100, sp[-1] + 400), pxms=0.3, title='A. Estimulación del ápex del VD: VA 142 ms',
    src='Veenhuyzen 2012, fig. 4: VA 142 desde el ápex; LC de estimulación 600 ilustrativa',
    beats=[(x, 'pa') for x in sp], spikes=sp, atr=[(x + 142, 'cs_mid', -1) for x in sp], h_retro=[x + 110 for x in sp],
    cal=[(sp[1], sp[1] + 142, 'CS 5-6', 'VA 142'), (sp[0], sp[1], 'RVA', 'S-S 600')])
S['veen12_vai_b'] = dict(win=(-100, sp[-1] + 400), pxms=0.3, title='B. Estimulación del VD posterobasal: VA 120 ms',
    src='Veenhuyzen 2012, fig. 4: VA 120 desde la base; índice VA = 142 − 120 = +22 ms (> +10: vía septal)',
    channels=['HRA', 'His p', 'His d', 'CS 9-10', 'CS 7-8', 'CS 5-6', 'CS 3-4', 'CS 1-2', 'VD basal'], pace_ch='VD basal',
    beats=[(x, 'pb') for x in sp], spikes=sp, atr=[(x + 120, 'cs_mid', -1) for x in sp], h_retro=[x + 140 for x in sp],
    cal=[(sp[1], sp[1] + 120, 'CS 5-6', 'VA 120'), (sp[0], sp[1], 'VD basal', 'S-S 600')])

# 7. Veenhuyzen 2012 fig. 1: EV His refractaria que adelanta la A 19 ms (LC 444, vía derecha). VA 150 ilustrativo.
LC, VA = 444, 150
svt = [i * LC for i in range(4)]
A = [v + VA for v in svt[:3]]
s_hr = svt[3] - HV                     # cae en el momento del His esperado
A3 = svt[3] + VA - 19                  # A adelantada
v4 = A3 + (LC - VA); v5 = v4 + LC
S['veen12_ehr'] = dict(win=(-100, v5 + 330), pxms=0.3,
    src='Veenhuyzen 2012, fig. 1: LC 444; la EV con His refractario adelanta la A 19 ms (VA 150 ilustrativo)',
    beats=[(v, 'n') for v in svt[:3]] + [(s_hr, 'f'), (v4, 'n'), (v5, 'n')], spikes=[s_hr],
    atr=[(a, 'right', -1) for a in A + [A3, v4 + VA, v5 + VA]],
    h_ante=[v - HV for v in svt[:3] + [v4, v5]] + [s_hr],
    cal=[(A[1], A[2], 'HRA', 'A-A 444'), (A[2], A3, 'HRA', 'A-A 425 (−19)')],
    marks=[(s_hr, 'V1', 'EV-HR'), (s_hr, 'His p', 'H')])

if __name__ == '__main__':
    for k, sc in S.items():
        render(sc, f'{OUT}/{k}.svg')
        print(k)
