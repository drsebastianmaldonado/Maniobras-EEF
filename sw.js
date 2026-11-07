// Permite instalar la app y abrirla sin conexión. Primero la red (siempre lo último publicado); si no hay, la copia.
// Si cambiás un archivo, subí CACHE_VERSION.
const CACHE_VERSION = 'mef-v76';
const ARCHIVOS = ['./', './index.html', './manifest.json', './iconos/icon-192.png', './iconos/icon-512.png'];
self.addEventListener('install', e => e.waitUntil(caches.open(CACHE_VERSION).then(c => c.addAll(ARCHIVOS)).then(() => self.skipWaiting())));
self.addEventListener('activate', e => e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE_VERSION).map(k => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || !req.url.startsWith(self.location.origin)) return;
  e.respondWith(fetch(new Request(req.url, { cache: 'no-cache' }))
    .then(res => { if (res.ok) { const cp = res.clone(); caches.open(CACHE_VERSION).then(c => c.put(req, cp)); } return res; })
    .catch(() => caches.match(req).then(r => r || caches.match('./index.html'))));
});
