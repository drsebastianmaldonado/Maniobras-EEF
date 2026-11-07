# Simulador de registros de polígrafo

Genera los registros simulados de `figs/sim/` a partir de los intervalos publicados en cada artículo.
Todo el trazado es sintético; solo se rotulan los intervalos publicados y cada imagen lleva la leyenda
"REGISTRO SIMULADO".

- `simlib.py`: motor (canales, morfologías, secuencias auriculares, calibres).
- `cases.py` y `cases2.py`: un escenario por caso (latidos, espigas, activaciones, His, calibres).
- `png.js`: convierte los SVG en PNG con Playwright.

Uso:

    python3 cases.py <carpeta de simlib.py> <carpeta de salida>
    node png.js <carpeta de salida>

Después se convierten a escala de grises y se copian a `figs/sim/`.

Orden de los canales: `simlib.distal_primero` los muestra de distal a proximal (His d antes que His p, Abl d antes que Abl p,
SC 1-2 primero), como en el polígrafo del autor.

Para regenerar todo de una vez (fichas, modo práctica y presentación de los casos):

    python3 build_all.py <carpeta temporal>
