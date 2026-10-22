# Paper 2.1 — comparación de controles en LPM y logística

**Resultados generados únicamente al ejecutar el script sobre datos institucionales autorizados.**
Todos los modelos usan la misma muestra completa, PASS binario, ocho grupos 0/1/2/3/4/5/6/7+ y errores estándar agrupados por profesor-periodo.
En cada modelo y método Holm se aplica a las 28 comparaciones, únicamente si las 28 pruebas son estimables.
La omisión de controles no implica ausencia de dependencia intraclúster ni identifica causalidad.

## Tamaños y tasas observadas
| Visitas | N | PASS observado |
|---|---:|---:|
| 0 | 5393 | 72.1% |
| 1 | 517 | 81.0% |
| 2 | 245 | 80.8% |
| 3 | 170 | 81.8% |
| 4 | 96 | 86.5% |
| 5 | 55 | 85.5% |
| 6 | 50 | 82.0% |
| 7+ | 101 | 89.1% |

## Estado de las ocho regresiones
| Método | Modelo | FE profesor-periodo | Carrera | N | Estado inferencial | Holm significativos / 28 |
|---|---|---|---|---:|---|---:|
| LPM | A | No | No | 6627 | valid | 3 |
| LPM | B | No | Sí | 6627 | valid | 4 |
| LPM | C | Sí | No | 6627 | valid | 8 |
| LPM | D | Sí | Sí | 6627 | valid | 8 |
| logit | A | No | No | 6627 | valid | 2 |
| logit | B | No | Sí | 6627 | valid | 2 |
| logit | C | Sí | No | 6627 | valid | 6 |
| logit | D | Sí | Sí | 6627 | not_estimable | ND |

## Comparaciones seleccionadas (grupo alto menos grupo bajo)
Se preservan los 28 pares en el CSV. Los contrastes mostrados son 0–1, 0–7+, 1–7+ y 3–4. El 3–4 **no** es una prueba causal de PPA1.

| Método | Modelo | Comparación | Diferencia PASS (pp) / OR | IC 95% | p Holm |
|---|---|---|---|---|---|
| LPM | A | 0 → 1 | 8.93 pp | [4.91, 12.95] | 0.0004 |
| LPM | A | 0 → 7+ | 17.00 pp | [10.31, 23.68] | 0.0000 |
| LPM | A | 1 → 7+ | 8.06 pp | [-0.22, 16.34] | 1.0000 |
| LPM | A | 3 → 4 | 4.69 pp | [-5.56, 14.95] | 1.0000 |
| LPM | B | 0 → 1 | 8.51 pp | [4.56, 12.47] | 0.0007 |
| LPM | B | 0 → 7+ | 15.19 pp | [8.52, 21.86] | 0.0002 |
| LPM | B | 1 → 7+ | 6.68 pp | [-1.60, 14.96] | 1.0000 |
| LPM | B | 3 → 4 | 5.66 pp | [-4.10, 15.42] | 1.0000 |
| LPM | C | 0 → 1 | 12.36 pp | [8.66, 16.06] | 0.0000 |
| LPM | C | 0 → 7+ | 28.19 pp | [20.14, 36.23] | 0.0000 |
| LPM | C | 1 → 7+ | 15.83 pp | [6.85, 24.81] | 0.0121 |
| LPM | C | 3 → 4 | 5.01 pp | [-4.88, 14.89] | 1.0000 |
| LPM | D | 0 → 1 | 12.13 pp | [8.41, 15.85] | 0.0000 |
| LPM | D | 0 → 7+ | 26.62 pp | [19.11, 34.12] | 0.0000 |
| LPM | D | 1 → 7+ | 14.49 pp | [5.91, 23.07] | 0.0206 |
| LPM | D | 3 → 4 | 5.15 pp | [-4.46, 14.77] | 1.0000 |
| logit | A | 0 → 1 | OR 1.65 | [1.28, 2.13] | 0.0027 |
| logit | A | 0 → 7+ | OR 3.16 | [1.64, 6.10] | 0.0159 |
| logit | A | 1 → 7+ | OR 1.91 | [0.90, 4.09] | 1.0000 |
| logit | A | 3 → 4 | OR 1.42 | [0.64, 3.17] | 1.0000 |
| logit | B | 0 → 1 | OR 1.64 | [1.27, 2.12] | 0.0039 |
| logit | B | 0 → 7+ | OR 2.93 | [1.50, 5.70] | 0.0422 |
| logit | B | 1 → 7+ | OR 1.78 | [0.82, 3.86] | 1.0000 |
| logit | B | 3 → 4 | OR 1.53 | [0.70, 3.33] | 1.0000 |
| logit | C | 0 → 1 | OR 2.16 | [1.67, 2.78] | 0.0000 |
| logit | C | 0 → 7+ | OR 6.48 | [3.08, 13.62] | 0.0000 |
| logit | C | 1 → 7+ | OR 3.00 | [1.32, 6.82] | 0.1872 |
| logit | C | 3 → 4 | OR 1.52 | [0.66, 3.48] | 1.0000 |
| logit | D | 0 → 1 | OR 2.20 | [ND, ND] | ND |
| logit | D | 0 → 7+ | OR 6.05 | [ND, ND] | ND |
| logit | D | 1 → 7+ | OR 2.75 | [ND, ND] | ND |
| logit | D | 3 → 4 | OR 1.50 | [ND, ND] | ND |

## Cambios entre el modelo sin controles (A) y el modelo completo (D)
- **LPM, 0 → 1:** A: 8.93 pp, Holm p=0.0004; D: 12.13 pp, Holm p=0.0000. Cambiar ajustes puede modificar magnitud e incertidumbre, pero no identifica causalidad.
- **LPM, 1 → 7+:** A: 8.06 pp, Holm p=1.0000; D: 14.49 pp, Holm p=0.0206. Cambiar ajustes puede modificar magnitud e incertidumbre, pero no identifica causalidad.
- **LPM, 3 → 4:** A: 4.69 pp, Holm p=1.0000; D: 5.15 pp, Holm p=1.0000. Cambiar ajustes puede modificar magnitud e incertidumbre, pero no identifica causalidad.
- **logit, 0 → 1:** A: OR 1.65, Holm p=0.0027; D: ND (inferencia no validada). Cambiar ajustes puede modificar magnitud e incertidumbre, pero no identifica causalidad.
- **logit, 1 → 7+:** A: OR 1.91, Holm p=1.0000; D: ND (inferencia no validada). Cambiar ajustes puede modificar magnitud e incertidumbre, pero no identifica causalidad.
- **logit, 3 → 4:** A: OR 1.42, Holm p=1.0000; D: ND (inferencia no validada). Cambiar ajustes puede modificar magnitud e incertidumbre, pero no identifica causalidad.

## Cómo interpretar la comparación
A = sin controles; B = solo carrera; C = solo efectos fijos profesor-periodo; D = ambos.
El LPM expresa diferencias ajustadas de probabilidad en puntos porcentuales. La logística expresa **odds ratios condicionales**, no razones de probabilidades ni incrementos constantes en puntos porcentuales. Un OR más grande no implica automáticamente un efecto educativo más grande.
Los cambios entre especificaciones pueden reflejar composición, falta de soporte, no colapsabilidad de las odds ratios o dificultades inferenciales. No atribuir el cambio de un valor p a un mecanismo causal sin mayor evidencia.
Las familias Holm se mantienen separadas por especificación y método. Si un modelo tiene covarianza singular, fallos de separación o valores p indefinidos, los resultados afectados deben declararse ND, nunca significativos.

## Diagnóstico y límites
- logit D: not_estimable. ; warnings=RuntimeWarning.

Los modelos no incorporan habilidad matemática previa ni motivación por PPA1; ninguna asociación constituye un efecto causal. No se ha modificado el modelo principal ni la inferencia del manuscrito.
