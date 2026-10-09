# 10 — Matriz de afirmaciones que necesitan una fuente antes de publicarse

**Objetivo:** que ningún agente escriba una oración cuantitativa «porque estaba en una conversación». Identificar documento canónico, especificación y limitación; conectar luego con CSV concreto de `results/paper21/tables/` y su commit de generación.

| Afirmación candidata | Documento fuente | Modelo/población | Límite de lo que autoriza |
|---|---|---|---|
| CMAT funciona como centro de apoyo universitario fuera de clases | `paper/sections/02.tex` | Contexto histórico | Verificar operación/hora con institución |
| Tres visitas podían completar una opción PPA | `paper/sections/02.tex`, `VISIT_GROUPING_DECISION.md` | Parte del periodo | No asume vigencia uniforme ni incentivo exógeno |
| N=6,627, 190 profesor-periodos, 5,393 no asistentes | `PRELIMINARY_RESULTS.md`, `sections/02.tex` | Primer MU elegible | No generalizar a todos los estudiantes |
| Asistir 1+ vs 0 se asocia con +0.361 Z y +15.3 pp PASS | `PRELIMINARY_RESULTS.md` §1 | Benchmark ajustado | No causal, no mejora pre/post |
| Entre usuarios con 6+ agrupado los omnibus no rechazan | `PRELIMINARY_RESULTS.md` §2 | 1/2/3/4/5/6+, FE/CR | No demuestra equivalencia |
| Entre usuarios de 7 categorías positivas la prueba global PASS p=.102 | `PRELIMINARY_RESULTS.md` §3 | Especificación detallada | No reemplazar con full-grid p |
| `7+` vs `1` PASS +14.5 pp, Holm p=.0206 | `PRELIMINARY_RESULTS.md` introducción | Modelo completo `0..7+` | Cronología exploratoria del 7+ y familia de 28 |
| Profesor-cluster PASS `6+` vs 1 +12.0 pp, Holm p=.0358 | `PRELIMINARY_RESULTS.md` §7 | Sensibilidad por profesor; usuarios | No es frontera adyacente |
| El journal objetivo es TEAMAT | `submission/METADATA.md`, `paper/README.md` | Estrategia editorial vigente en repo | Revalidar requisitos actuales directamente |
| Gokhool y Lawson (2026) separa uso y frecuencia | `literature_selected/ACCESS_NOTES.md` | Sólo abstract disponible | No citar significancia, coeficientes o limitaciones no leídas |

## Regla de uso

**Documento fuente** no equivale automáticamente a tabla reproducible. Antes de publicación, agregar el nombre exacto de CSV agregado, versión/commit, filtro, unidad, escalamiento y familia de p para cada fila inferencial. Si un número de manuscrito no coincide con el registro canónico, crear incidencia en `notes/09_DECISIONES_Y_PENDIENTES.md` y resolverla, nunca elegir a ojo.

**Rutas:** `../paper/docs/results/PRELIMINARY_RESULTS.md`, `../paper/docs/results/MIXTURE_ANALYSIS_RESULTS.md`, `../paper/docs/analysis/VISIT_GROUPING_DECISION.md`, `../paper/docs/interpretation/ACADEMIC_MANAGEMENT_HYPOTHESIS.md`, `../literature_selected/ACCESS_NOTES.md`, `../submission/METADATA.md`.
