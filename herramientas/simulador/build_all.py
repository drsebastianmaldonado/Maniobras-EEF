"""Regenera todos los registros simulados de figs/sim/ (fichas), figs/sim/prac/ (modo práctica) y figs/sim/casos/ (presentación).
Uso: python3 build_all.py <carpeta temporal>
Los ECG de 12 derivaciones y los registros reales no se tocan."""
import contextlib, copy, io, os, subprocess, sys
from PIL import Image

D = os.path.dirname(os.path.abspath(__file__))
TMP = sys.argv[1]
FIGS = os.path.join(D, '..', '..', 'figs', 'sim')
sys.path.insert(0, D)
sys.argv = ['x', D, TMP]
from simlib import render
import ecg12

S = {}
for m in ['cases', 'cases2', 'cases3', 'cases4', 'cases5']:
    g = {'__name__': 'x'}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open(os.path.join(D, m + '.py')).read().split("if __name__")[0], g)
    S.update(g['S'])
g = {'__name__': 'x'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(os.path.join(D, 'practica.py')).read().split("if __name__")[0], g)
USADAS, limpiar = g['USADAS'], g['limpiar']


def neutro(sc, titulo):
    sc = copy.deepcopy(sc)
    sc['title'] = titulo
    sc['src'] = 'modo práctica (sin interpretación)'
    sc['marks'] = [(m[0], m[1], 'EV') for m in sc.get('marks', []) if m[2] in ('EV-HR', 'EV')]
    sc['cal'] = [(a, b, c, d.split(' (')[0]) for a, b, c, d in sc['cal']]
    return sc


jobs = []   # (destino, [(nombre svg, escenario | ('ecg', clave))])


def panels(base):
    if base in S:
        return [base]
    return sorted(k for k in S if k.startswith(base + '_') and k[len(base) + 1:] in ('a', 'b', 'c'))


def add(dest, items):
    jobs.append((dest, items))


for f in sorted(os.listdir(FIGS)):
    if not f.endswith('.png'):
        continue
    n = f[:-4]
    if n == 'trnav_bys':
        add(f, [(k, S[k]) for k in ('bys_a', 'bys_b', 'bys_c')])
    elif n == 'p17_vop':
        add(f, [(k, S[k]) for k in ('c17s_vop_a', 'c17s_vop_b')])
    elif n == 'p17_ehr':
        add(f, [('c17s_ehr', S['c17s_ehr'])])
    elif n in ('pm_doppa', 'tada05'):
        add(f, [(n, S[n]), (n + '_ecg', ('ecg', 'pm_ecg' if n == 'pm_doppa' else 'ma_ecg'))])
    elif panels(n):
        add(f, [(k, S[k]) for k in panels(n)])
    else:
        print('sin escenario:', f)

NEUTRO = {'p16_vop': [('bys_b', 'Sobreestimulación del VD a 320 ms')], 'p16_ehr': [('bys_c', 'EV con His refractario')],
          'p17_vop': [('c17s_vop_a', 'A. TSV 1: sobreestimulación del VD a 360 ms'), ('c17s_vop_b', 'B. TSV 2: sobreestimulación del VD a 210 ms')],
          'p17_ehr': [('c17s_ehr', 'TSV 1: EV con His refractario')]}
for f in sorted(os.listdir(os.path.join(FIGS, 'prac'))):
    if not f.endswith('.png'):
        continue
    n = f[:-4]
    if n in NEUTRO:
        add('prac/' + f, [('pr_' + k, neutro(S[k], t)) for k, t in NEUTRO[n]])
        continue
    ks = panels(n)
    if not ks:
        print('sin escenario:', 'prac/' + f)
    elif all(k in USADAS for k in ks):
        add('prac/' + f, [('pr_' + k, limpiar(k, S[k])) for k in ks])
    else:
        add('prac/' + f, [('pr_' + k, S[k]) for k in ks])

for f in sorted(os.listdir(os.path.join(FIGS, 'casos'))):
    if not f.endswith('.png'):
        continue
    n = f[:-4]
    if n == 'c16_ind':
        add('casos/' + f, [('ca_bys_a', neutro(S['bys_a'], 'Taquicardia'))])
    elif n in S:
        add('casos/' + f, [('ca_' + n, S[n])])

os.makedirs(TMP, exist_ok=True)
hechos = set()
for dest, items in jobs:
    for name, sc in items:
        if name in hechos:
            continue
        hechos.add(name)
        if isinstance(sc, tuple):
            ecg12.render(sc[1], ecg12.ECGS[sc[1]], os.path.join(TMP, name + '.svg'))
        else:
            render(sc, os.path.join(TMP, name + '.svg'))
subprocess.run(['node', os.path.join(D, 'png.js'), TMP], check=True, stdout=subprocess.DEVNULL)

for dest, items in jobs:
    ims = [Image.open(os.path.join(TMP, name + '.png')) for name, _ in items]
    w = max(i.width for i in ims)
    c = Image.new('RGB', (w, sum(i.height for i in ims)), 'white')
    y = 0
    for i in ims:
        c.paste(i, (0, y))
        y += i.height
    c.convert('L').save(os.path.join(FIGS, dest), optimize=True)
print(len(jobs), 'imágenes regeneradas')
