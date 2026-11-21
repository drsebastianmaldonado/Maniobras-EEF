// Permite instalar la app y abrirla sin conexión. Primero la red (siempre lo último publicado); si no hay, la copia.
// Si cambiás un archivo, subí CACHE_VERSION.
const CACHE_VERSION = 'mef-v239';
const ARCHIVOS = ['./', './index.html', './anim.js', './anim-index.js', './manifest.json', './offline.json', './iconos/icon-192.png', './iconos/icon-512.png', './iconos/apple-touch-icon.png'];
// 'mef-imagenes' guarda las imágenes que el usuario descargó para usar sin conexión: no se borra al actualizar.
self.addEventListener('install', e => e.waitUntil(caches.open(CACHE_VERSION).then(c => c.addAll(ARCHIVOS)).then(() => self.skipWaiting())));
self.addEventListener('activate', e => e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE_VERSION && k !== 'mef-imagenes').map(k => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || !req.url.startsWith(self.location.origin)) return;
  e.respondWith(fetch(new Request(req.url, { cache: 'no-cache' }))
    .then(res => { if (res.ok) { const cp = res.clone(), img = /\/(figs|localizar)\//.test(new URL(req.url).pathname);
      caches.open(img ? 'mef-imagenes' : CACHE_VERSION).then(c => c.put(req, cp)); } return res; })   // las imágenes van a una sola caché, que no se borra al actualizar
    .catch(() => caches.match(req).then(r => r || caches.match('./index.html'))));
});
