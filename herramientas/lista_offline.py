#!/usr/bin/env python3
"""Genera offline.json: la lista de archivos que el botón "Descargar para usar sin conexión" guarda en el teléfono.

Correlo antes de publicar si agregaste, sacaste o renombraste imágenes:
    python3 herramientas/lista_offline.py
Incluye figs/ (salvo figs/reserva, que no se usa en la app) y localizar/.
"""
import json, os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXT = ('.png', '.jpg', '.jpeg', '.svg', '.webp', '.html')
archivos, total = [], 0
for base in ('figs', 'localizar'):
    for d, subdirs, fs in os.walk(os.path.join(RAIZ, base)):
        subdirs[:] = sorted(s for s in subdirs if os.path.relpath(os.path.join(d, s), RAIZ) != os.path.join('figs', 'reserva'))
        for f in sorted(fs):
            if f.lower().endswith(EXT):
                ruta = os.path.join(d, f)
                archivos.append(os.path.relpath(ruta, RAIZ).replace(os.sep, '/'))
                total += os.path.getsize(ruta)
with open(os.path.join(RAIZ, 'offline.json'), 'w') as fh:
    json.dump({'bytes': total, 'archivos': archivos}, fh, ensure_ascii=False, separators=(',', ':'))
print(f'{len(archivos)} archivos, {total / 1e6:.1f} MB')
