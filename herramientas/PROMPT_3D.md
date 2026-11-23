# Prompt para trabajar con las animaciones 3D (copiar y pegar en otro chat)

Trabajamos en el repositorio `drsebastianmaldonado/Maniobras-EEF` (rama `main`, se publica sola en GitHub Pages: https://drsebastianmaldonado.github.io/Maniobras-EEF/). Agregalo a la sesión, clonalo y leé `CLAUDE.md` antes de empezar. Escribime en español rioplatense, con respuestas cortas.

Quiero seguir con las **animaciones 3D anatómicas** de la app. Así están hechas:

**Archivos**
- `3d/ver.html?a=<id>`: visor 3D general. Toma el escenario de cada animación de `anim.js` (expuesto en `window.ANIM_DATA = { ANIMS, G, LANES0, FOR }`) y lo dibuja en el corazón 3D. Los `<id>` son las claves de `ANIMS` (por ejemplo `vop_0`, `ppi_1`, `ado_trav`, `tvfabl_rf`).
- `3d/vop.html`: animación especial de la sobreestimulación ventricular en la TRNAV típica, con el circuito en el triángulo de Koch.
- `3d/modelos/corazon.glb`: corazón de BodyParts3D (CC BY-SA 2.1 Japan; atribución en `3d/modelos/LEEME.txt` y al pie de cada página). Pared, válvulas, aorta, cavas y seno coronario, recortados y simplificados.
- `3d/lib/`: three.js r160 (`three.module.min.js`) y sus addons en `3d/lib/jsm/` (GLTFLoader, EffectComposer, UnrealBloomPass, OutputPass). Se cargan con un import map; no hay que instalar nada.
- `anim.js`: escenarios de todas las animaciones (2D y 3D usan los mismos). Cada escenario devuelve `{ ev, wv, flA, flV, cols, stims, ints, ... }`: eventos del trazado, frentes que viajan (`wv: [{ c: 'ante'|'retro'|'focus', pts: [[[x, y], t], ...] }]` en coordenadas del esquema 2D, puntos `G`), activaciones auriculares y ventriculares, choques (✕), estímulos y corchetes de medición.

**Cómo funciona el visor (`3d/ver.html`)**
- **Estilo rayos X:** shader fresnel aditivo violeta, fondo negro y bloom.
- **Sistema de conducción:** His, ramas y Purkinje generados sobre el modelo, con tiempos propios. La pared se ilumina por vértice: un frente brillante y una estela.
- **Del esquema al 3D:**
  - Los puntos del esquema 2D pasan al 3D con un ajuste afín (`fit`/`map2`) sobre hitos del modelo (nodo AV, His, ápex, ostium del SC, AD, AI, VI lateral).
  - Los puntos del sistema de conducción van anclados exactamente al His y las ramas del modelo (`ANC`).
  - Dentro del miocardio ventricular no se dibuja el punto: ahí el frente se ve en la pared.
- **Parte crítica (`WIN`):** se marca con cámara lenta, cámara cerca mirando desde el lado donde ocurre, rótulo arriba y respuesta escrita en el 1.er latido de retorno (`sc.resp` o la conclusión `sc.verdict`).
  - Encarrilamiento: último latido estimulado y 1.er latido de retorno.
  - Extraestímulo: el extraestímulo y el latido siguiente.
  - Estimulación en sinusal: cada estímulo y su respuesta.
  - Adenosina: su efecto y cómo termina o sigue.
- **Casos especiales que ya están resueltos:**
  - Vía accesoria gruesa y rotulada (`sc.ap`).
  - BRI funcional y rama-rama (`sc.bbbL`, `sc.bbr`): el VI se activa a través del septum.
  - Doble fisiología nodal (`sc.nodal`): vías lenta y rápida en la cara septal de la AD, con la cámara en el Koch.
  - Nodos AV gemelos (`sc.twin`): nodo anterior anterosuperior, posterior junto al ostium del SC y His posterior unido a la rama derecha.
  - TV fascicular (`sc.fasc`): P1 = miocardio septal lento, P2 = fascículo posterior, cámara desde el VI; la ablación hace una línea de lesiones contiguas desde P2 hacia la hemirrama anterior.
  - Foco de la TA en la VPSI (`G.focus`).
- **Debajo de la escena:** trazado (canales de `lanes`, con S1/S2 y corchetes) y diagrama de escalera (altura del frente en el esquema en función del tiempo, con la parte crítica resaltada).
- **En la app:** cada animación de las fichas tiene el botón "◆ Ver en 3D" (lo agrega `anim.js`, en `mount`).

**Reglas**
- Cambios de mecanismo o de tiempos: en el escenario de `anim.js` (así cambian juntas la 2D y la 3D). Cambios de dibujo 3D: en `3d/ver.html`.
- Después de cada cambio: subir la versión en `index.html` (`const APPV`) y en `sw.js` (`CACHE_VERSION`), correr `node herramientas/anim_index.js` si cambió `anim.js`, probar y hacer push a `main`. Pruebas en `CLAUDE.md`. Para el 3D, Playwright con `--use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader`; esperar `window.__ready()` y mover el tiempo con `window.__setT(ms)`.
- Darme links directos del tipo `https://drsebastianmaldonado.github.io/Maniobras-EEF/3d/ver.html?a=<id>&v=<versión>` y recordarme recargar.
- La revisión de las 47 animaciones 3D está en el issue #3: marcá las que apruebe y anotá los cambios en el resumen del issue.

Lo que quiero hacer ahora: <escribí acá el pedido>
