# Maniobras en el EEF

App independiente con las maniobras del polígrafo de electrofisiología para el diagnóstico diferencial de las
taquicardias supraventriculares.

- **Algoritmo**: preguntas paso a paso (la pregunta actual arriba y el recorrido debajo), desde la relación AV hasta el
  diagnóstico, con acceso directo a la ficha de cada maniobra. La rama de RP largo sigue el algoritmo del autor
  (circuito inferior por encarrilamiento ventricular + circuito superior por ΔAH).
- **Arritmias**: buscador por mecanismo (TRNAV típica y atípica, TRAV septal y de pared libre, PJRT, vías
  nodofasciculares y nodoventriculares, TA, taquicardia de la unión, TRAV antidrómica, Mahaim) con los hallazgos que lo confirman, apoyan o
  descartan, y acceso a la ficha de cada maniobra.
- **Maniobras**: 13 fichas (cómo se hace, qué medir, tabla de interpretación con puntos de corte y fuente, trampas,
  esquemas de electrogramas).
- **Calculadora**: PPI−LC, cPPI−LC, SA−VA, ΔHA, encarrilamiento diferencial, ΔAH y AH TSV vs sinusal, con cortes de
  RP corto o largo.

Archivos: `index.html` (todo el contenido), `manifest.json` + `sw.js` (instalable y sin conexión), `iconos/`.
Está pensada para publicarse sola en GitHub Pages (por ejemplo, en un repositorio propio).

**Dr. Sebastián Maldonado** · Electrofisiólogo infantil
