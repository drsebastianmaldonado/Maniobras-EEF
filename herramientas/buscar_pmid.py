import re, json, time, urllib.request, urllib.parse, html
src = open('/home/user/maniobras-eef/index.html').read()
i = src.index('const REFS = {'); j = src.index('\n};', i)
block = src[i:j]
refs = re.findall(r"^  ([a-z0-9]+): \['((?:[^'\\]|\\.)*)', '((?:[^'\\]|\\.)*)'\]", block, re.M)
E = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
def get(u):
    for k in range(4):
        try:
            with urllib.request.urlopen(u, timeout=30) as r: return json.load(r)
        except Exception as e: time.sleep(1.5 * (k + 1))
    return None
out = {}
for key, short, full in refs:
    t = html.unescape(re.sub('<[^>]+>', '', full)).replace("\\'", "'")
    doi = re.search(r'doi:\s*(10\.[^\s)]+)', t)
    yr = re.search(r'\b(19|20)\d\d\b', short)
    au = t.split(' ')[0].strip(',')
    parts = t.split('. ')
    title = parts[1] if len(parts) > 2 else ''
    rec = {'short': short, 'doi': doi.group(1).rstrip('.') if doi else None, 'title': title, 'au': au}
    if key in ('autor', 'josephson', 'ehra09'):
        out[key] = rec; continue
    q = None
    if title and len(title) > 15:
        words = [w for w in re.findall(r"[A-Za-z0-9]+", title) if len(w) > 3][:9]
        q = ' AND '.join(f'{w}[ti]' for w in words) + f' AND {au}[au]'
        if yr: q += f' AND {yr.group(0)}[dp]'
    if q:
        r = get(E + 'esearch.fcgi?db=pubmed&retmode=json&retmax=3&term=' + urllib.parse.quote(q))
        ids = r['esearchresult']['idlist'] if r else []
        if not ids and yr:  # sin el año
            r = get(E + 'esearch.fcgi?db=pubmed&retmode=json&retmax=3&term=' + urllib.parse.quote(q.rsplit(' AND ', 1)[0]))
            ids = r['esearchresult']['idlist'] if r else []
        rec['ids'] = ids
        if ids:
            s = get(E + 'esummary.fcgi?db=pubmed&retmode=json&id=' + ids[0])
            if s:
                d = s['result'][ids[0]]
                rec['pm_title'] = d.get('title', '')
                rec['pm_year'] = d.get('pubdate', '')[:4]
                rec['pm_au'] = d['authors'][0]['name'] if d.get('authors') else ''
                rec['pm_doi'] = next((a['value'] for a in d.get('articleids', []) if a['idtype'] == 'doi'), None)
        time.sleep(0.4)
    out[key] = rec
json.dump(out, open('/tmp/claude-0/-home-user/8932440b-277c-5165-9e50-ac25912bb324/scratchpad/pm.json', 'w'), ensure_ascii=False, indent=1)
ok = sum(1 for r in out.values() if r.get('ids')); print(len(out), 'refs;', ok, 'con PMID;', sum(1 for r in out.values() if r['doi']), 'con DOI en el texto')
for k, r in out.items():
    if not r.get('ids'): print('SIN', k, r['short'], '|', r['title'][:80])
