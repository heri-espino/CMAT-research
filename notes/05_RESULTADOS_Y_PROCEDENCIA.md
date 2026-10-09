# 05 — Resultados documentados: qué números podemos usar

**Tipo de documento:** extracción de reportes del repositorio, **no reestimación nueva**. Antes de escribir un número en inglés, localizar su CSV agregado en `results/paper21/tables/` y revisar que corresponde al outcome, población, agrupación y cluster declarados. Reproducir valores p y CIs con su misma especificación.

## 1. Benchmark, universo de 6,627 estudiantes

Con efectos fijos profesor–periodo, carrera y SE cluster-robust profesor–periodo:

| Comparación: cualquier visita menos 0 | Estimación | IC 95% | Evidencia |
|---|---:|---:|---|
| Calificación final Z (imputación canónica) | **+0.361 DE** | 0.302–0.421 | p<0.001 |
| PASS | **+15.3 puntos porcentuales** | 12.4–18.1 pp | p<0.001 |

Estas magnitudes se refieren a **asociación transversal de desempeño final**, no cambio individual ni impacto causal.

## 2. Frecuencias entre usuarios, agrupación histórica 6+

| Visitas | N | Z media descriptiva | Porcentaje PASS descriptivo |
|---|---:|---:|---:|
| 1 | 517 | 0.219 | 81.0% |
| 2 | 245 | 0.247 | 80.8% |
| 3 | 170 | 0.278 | 81.8% |
| 4 | 96 | 0.267 | 86.5% |
| 5 | 55 | 0.382 | 85.5% |
| 6+ | 151 | 0.401 | 86.8% |

Prueba omnibus entre asistentes: `p_Z=0.317`, `p_PASS=0.152`; **ningún par entre los seis grupos** sobrevive Holm (familia de 15 por outcome). Como ejemplo de por qué importa la multiplicidad, 1 vs 6+ en Z tiene p cruda 0.022 que pasa a 0.328 tras Holm; en PASS pasa de 0.011 a 0.171. Los puntos anteriores son **medias/tasas observadas**, no coeficientes ajustados ni una secuencia causal.

## 3. Sensibilidad granular y modelo completo de ocho categorías

La grilla actual del manuscrito es `0/1/2/3/4/5/6/7+`. Entre usuarios, en el análisis específico de siete frecuencias positivas, omnibus `p_Z=0.213` y `p_PASS=0.102`; allí no sobrevive ningún par Holm. Por separado, el **modelo completo con cero visitas incluido** registra que todos los contrastes `0` frente a cada nivel positivo del outcome Z sobreviven Holm, y que el contraste **`7+` vs `1` en PASS es +14.5 pp**, `p_Holm=0.0206`, con estimación logística de sensibilidad **OR=2.75**.

En términos descriptivos, `Z` pasa de 0.267 (4 visitas) a 0.382 (5), y de 0.288 (6 exactas) a 0.457 (7+); los saltos adyacentes **no** están resueltos inferencialmente. El grupo 7+ registra una tasa PASS descriptiva de **89.1%**; el de 6 exactas, 82.0%. El caso 7+ exige declarar soporte (N=101), que su partición no fue la originalmente congelada y qué familia de p se aplicó.

## 4. Sensibilidad al nivel de clustering

Al agrupar errores por **profesor** en lugar de profesor–periodo, el benchmark conserva +0.361 DE (IC 0.305–0.417; 53 clusters) y +15.3 pp PASS (IC 12.8–17.8; 53 clusters). Entre usuarios (51 clusters), omnibus `p_Z=0.0477` y `p_PASS=0.0551`. Ningún contraste continuo sobrevive Holm; en PASS `6+` vs `1` = **+12.0 pp** (IC 4.3–19.8; `p_Holm=0.0358`). Las diferencias entre resultados primarios y esta sensibilidad deben presentarse completas, no seleccionar la que convenga narrativamente.

## 5. Decomposición del resultado final

| Estado final (porcentaje de todos los estudiantes del grupo) | Sin visitas | Con 1+ |
|---|---:|---:|
| PASS | 72.1% | 82.4% |
| Nota numérica menor de 7.5 | 10.8% | 3.2% |
| BV/RT | 15.9% | 14.3% |
| BA | 1.2% | 0.2% |

**Entre no-PASS**, 923 de 1,504 no usuarios (61.4%) y 178 de 217 usuarios (82.0%) tuvieron resultado administrativo en lugar de fracaso numérico. Contraste ajustado = **+13.2 pp** (IC 6.8–19.6; p<0.001).

Separando códigos, entre no-PASS (BV contra fracaso numérico y excluyendo RT/BA), cualquier asistencia se asoció con **+16.8 pp** (IC 9.5–24.1; p<0.001). El análogo RT vs fracaso numérico fue **+0.5 pp** (IC -15.1–16.2; p=0.945). La composición no demuestra que estudiantes recibieran tutoría para escoger BV ni que BV protegiera su GPA. Entre usuarios, omnibus de composición no-PASS: p=0.495 administrativo/numérico; p=0.599 BV/RT/numérico; p=0.523 BV/numérico; no hubo pares positivos Holm-significativos.

## 6. Nota numérica observada y distribuciones

Sin imputar BA/BV/RT, la probabilidad ajustada de **fracaso numérico**, condicional a tener nota numérica, es bastante menor para quienes asistieron; entre usuarios, omnibus p=0.480 y ningún par de OR sobrevive Holm. La Z sólo numérica tiene prueba global entre usuarios **p=0.397**. No llamar a la diferencia entre imputado y observado un «efecto real de tutoría», pues cambian tanto la variable como la selección del subconjunto.

Se dispone además de extensiones GMM / skew-normal en `paper/docs/results/MIXTURE_ANALYSIS_RESULTS.md`. Son **exploratorias y secundarias respecto del plan actual basado en Holm**; los componentes gaussianos no son tipos de estudiantes y el resultado imputado depende de los códigos administrativos.

## 7. Proveniencia y reproducibilidad

- Resultado principal y sensibilidades: [PRELIMINARY_RESULTS.md](../paper/docs/results/PRELIMINARY_RESULTS.md).
- Resultados distribucionales: [MIXTURE_ANALYSIS_RESULTS.md](../paper/docs/results/MIXTURE_ANALYSIS_RESULTS.md).
- Salidas agregadas: `../results/paper21/tables/` y `../results/paper21/figures/`.
- Runner(s) y generación del paper: `../code/`, `../paper/paper_build.py`; biblioteca upstream `../cmat_analysis/`.
- El documento de estado registra, entre otros, Actions **35657154301** (GMM), **36678572075** (skew-normal), **36685329947** (integración completa 01–48), con hashes en [roadmap](../paper/docs/project/STATUS_AND_ROADMAP.md). No atribuir esas corridas a una nueva investigación Holm ni inferir que cada manuscrito generado haya sido verificado ahora.

**Control previo a publicación:** construir una matriz `número -> archivo CSV -> columna/filtro -> estimando -> método -> resultado impreso`; el archivo [10_MATRIZ_DE_AFIRMACIONES.md](10_MATRIZ_DE_AFIRMACIONES.md) es el punto de partida.