import json, subprocess, textwrap, html
# Uso: node herramientas/pruebas/exportar_arbol.js /tmp/arbol.json  (con el servidor local en :8765)
#      python3 herramientas/flujograma.py /tmp/arbol.json   → prototipos/flujo/*.png y *.svg
import sys, tempfile
D = tempfile.gettempdir() + '/'
T = json.load(open(sys.argv[1] if len(sys.argv) > 1 else D + 'tree.json'))
T['L_long']['dx'] = 'Combinación de los dos circuitos: V en el circuito + ΔAH < 20 → PJRT · V en el circuito + ΔAH > 40 → NFRT · VD lejos + ΔAH > 40 → TRNAV atípica · ΔAH 20–40 → zona gris · VD lejos + ΔAH < 20 → discordante (probable PJRT)'
import os.path
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'prototipos', 'flujo') + '/'
import os; os.makedirs(OUT, exist_ok=True)

def wrap(s, w):
    return '\n'.join(textwrap.wrap(s, w)) or s
def esc(s):
    return html.escape(s).replace('\n', '<BR/>')

FIGS = [
 ('0_general', 'Punto de partida: QRS, relación AV y secuencia auricular', 'start', ['start', 'av', 'seq', 'vasep', 'rp']),
 ('1_va_corto', 'Concéntrica con VA septal ≤ 70 ms', 'vop_t', ['vop_t', 'P_avnrt_t', 'jt', 'jt2', 'P_at_P_avnrt_t', 'atc_P_avnrt_t', 'noacc_t', 'ucp_t', 'term_t', 'rsc_t']),
 ('2_rp_corto', 'RP corto con VA > 70 ms', 'vop_s', ['vop_s', 'P_at_fus_s', 'atc_fus_s', 'fus_s', 'meas_s', 'bord', 'noacc_s', 'term_s', 'rsc_s', 'rsc_s2']),
 ('3_rp_largo', 'RP largo', 'vop_l', ['vop_l', 'ehr_l', 'P_pjrt', 'low_l', 'up_l', 'noacc', 'term_l', 'rsc_l', 'rsc_l2']),
 ('4_excentrica', 'Activación excéntrica y nodos AV gemelos', 'vop_e', ['vop_e', 'P_avrt_free', 'ecc2', 'P_at_P_avrt_free', 'atc_P_avrt_free', 'noacc_e', 'twin1', 'twin2', 'term_e', 'rsc_e']),
 ('5_no_1a1', 'Relación AV distinta de 1:1', 'atb', ['atb', 'atb2', 'vgta', 'nv', 'jt2v', 'df1']),
 ('6_qrs_ancho', 'QRS ancho', 'wh', ['wh', 'bbr1', 'P_bbr', 'bbr2', 'pw1', 'pw2', 'pw3', 'pw4', 'vtq']),
]
HOME = {}
for f, title, root, ids in FIGS:
    for i in ids: HOME.setdefault(i, f)
FIGN = {f: n for n, (f, *_ ) in enumerate(FIGS)}

for f, title, root, ids in FIGS:
    L = ['digraph G {', 'graph [rankdir=TB, fontname="Inter", bgcolor="white", nodesep=0.35, ranksep=0.45, pad=0.3, label=<<B>%s</B>>, labelloc=t, fontsize=26];' % esc(f'Figura {FIGN[f]}. {title}'),
         'node [fontname="Inter", fontsize=13, shape=box, style="rounded,filled", fillcolor="#ffffff", color="#9aa0b4", penwidth=1.3, margin="0.18,0.10"];',
         'edge [fontname="Inter", fontsize=11, color="#6c6c74", fontcolor="#3c3c44", arrowsize=0.7];']
    drawn = set()
    def node(k):
        if k in drawn: return
        drawn.add(k); n = T[k]
        if k in ids and not n.get('leaf') and not n.get('pre'):
            L.append(f'"{k}" [label=<{esc(wrap(n["q"], 34))}>];')
        elif n.get('pre'):
            L.append(f'"{k}" [label=<<FONT POINT-SIZE="10" COLOR="#1a8a3f"><B>DIAGNÓSTICO MÁS PROBABLE</B></FONT><BR/><B>{esc(wrap(n["dx"], 28))}</B>>, fillcolor="#e3f6e9", color="#1faa4a", penwidth=2];')
        elif n.get('leaf'):
            fc, cc = {'warn': ('#fff1dc', '#d97a00'), 'gray': ('#eceff3', '#8a93a6')}.get(n['tone'], ('#e4f0ff', '#0a74f0'))
            L.append(f'"{k}" [label=<<FONT POINT-SIZE="10" COLOR="{cc}"><B>RESULTADO</B></FONT><BR/><B>{esc(wrap(n["dx"], 30))}</B>>, fillcolor="{fc}", color="{cc}", penwidth=2];')
        else:   # pregunta que se desarrolla en otra figura
            L.append(f'"{k}" [label=<{esc(wrap(n["q"], 30))}<BR/><FONT POINT-SIZE="10" COLOR="#7a3fd0">→ sigue en la figura {FIGN[HOME[k]]}</FONT>>, style="rounded,dashed", fillcolor="#faf7ff", color="#7a3fd0"];')
    for k in ids:
        if k not in T: continue
        node(k); n = T[k]
        if n.get('leaf'): continue
        for o in n['opts']:
            g = o['go']; node(g)
            if n.get('pre'):
                acc = o['t'].startswith('Lo tomo')
                L.append(f'"{k}" -> "{g}" [label=<{esc("Lo tomo" if acc else "Sigo sospechando")}>, color="{"#1faa4a" if acc else "#7a3fd0"}", fontcolor="{"#1a8a3f" if acc else "#7a3fd0"}", penwidth={2 if acc else 1.4}, style={"solid" if acc else "dashed"}];')
            else:
                L.append(f'"{k}" -> "{g}" [label=<{esc(wrap(o["t"], 26))}>];')
    L.append('}')
    open(D + f + '.dot', 'w').write('\n'.join(L))
    subprocess.run(['dot', '-Tpng', '-Gdpi=130', D + f + '.dot', '-o', OUT + f + '.png'], check=True)
    subprocess.run(['dot', '-Tsvg', D + f + '.dot', '-o', OUT + f + '.svg'], check=True)
    print(f, 'ok')
# nodos no incluidos en ninguna figura
allq = {k for k, v in T.items() if not v.get('leaf')}
print('sin figura:', sorted(allq - set(HOME)))
