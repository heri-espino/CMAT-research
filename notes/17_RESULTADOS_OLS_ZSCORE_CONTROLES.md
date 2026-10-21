# 17 — Resultados OLS sobre Z-score: sensibilidad a los controles

**Informe producido automáticamente al ejecutar las cuatro regresiones sobre la cohorte institucional autorizada.**

Verificación de reproducción: **PASS: all 28 model D effects match the canonical Z analysis**.

## Objetivo

Comparar las 28 diferencias de Z por pares entre ocho frecuencias (0/1/2/3/4/5/6/7+) mediante OLS con A: ningún ajuste; B: carrera; C: efectos fijos profesor-periodo; D: ambos. La muestra y la agrupación de errores estándar por profesor-periodo se mantienen constantes. Cada uno de los cuatro modelos tiene su propia familia Holm de 28 pruebas.

## Estadísticas descriptivas observadas de Z

| Frecuencia | N | Media Z | SD Z |
|---|---:|---:|---:|
| 0 | 5393 | -0.061 | 1.017 |
| 1 | 517 | 0.219 | 0.849 |
| 2 | 245 | 0.247 | 0.738 |
| 3 | 170 | 0.278 | 0.797 |
| 4 | 96 | 0.267 | 0.694 |
| 5 | 55 | 0.382 | 0.594 |
| 6 | 50 | 0.288 | 0.838 |
| 7+ | 101 | 0.457 | 0.624 |

## Resultados de los cuatro modelos

| Modelo | FE profesor-periodo | Carrera | R² (en muestra) | R² ajustado | RMSE (en muestra) | Estado | Holm significativos / 28 |
|---|---|---|---:|---:|---:|---|---:|
| A | No | No | 0.018 | 0.016 | 0.977 | valid | 6 |
| B | No | Sí | 0.051 | 0.039 | 0.960 | valid | 6 |
| C | Sí | No | 0.020 | -0.010 | 0.976 | valid | 6 |
| D | Sí | Sí | 0.058 | 0.018 | 0.956 | valid | 7 |

R² y RMSE aquí son **medidas de ajuste dentro de la muestra**, no predicciones evaluadas en estudiantes nuevos; los efectos fijos profesor-periodo pueden aumentar el ajuste sin mejorar la generalización a profesores o periodos no observados.

## Contrastes relevantes: diferencias de medias condicionales en Z

Cada coeficiente expresa **Z del grupo con más visitas menos Z del grupo con menos visitas**, en unidades de la desviación estándar usada por el estudio. Los IC del 95% y los valores p se basan en errores estándar agrupados por profesor-periodo.

| Modelo | Comparación | Diferencia de Z | IC 95% | p Holm | ¿Rechazo? |
|---|---|---:|---|---:|---|
| A | 0 → 1 | 0.280 | [0.201, 0.358] | 0.0000 | Sí |
| A | 0 → 7+ | 0.518 | [0.374, 0.662] | 0.0000 | Sí |
| A | 1 → 7+ | 0.238 | [0.065, 0.412] | 0.1571 | No |
| A | 2 → 3 | 0.031 | [-0.106, 0.169] | 1.0000 | No |
| A | 3 → 4 | -0.011 | [-0.186, 0.163] | 1.0000 | No |
| A | 6 → 7+ | 0.170 | [-0.128, 0.468] | 1.0000 | No |
| B | 0 → 1 | 0.271 | [0.193, 0.349] | 0.0000 | Sí |
| B | 0 → 7+ | 0.477 | [0.335, 0.620] | 0.0000 | Sí |
| B | 1 → 7+ | 0.207 | [0.032, 0.381] | 0.4273 | No |
| B | 2 → 3 | 0.007 | [-0.123, 0.138] | 1.0000 | No |
| B | 3 → 4 | 0.000 | [-0.168, 0.169] | 1.0000 | No |
| B | 6 → 7+ | 0.126 | [-0.176, 0.427] | 1.0000 | No |
| C | 0 → 1 | 0.317 | [0.234, 0.400] | 0.0000 | Sí |
| C | 0 → 7+ | 0.597 | [0.433, 0.761] | 0.0000 | Sí |
| C | 1 → 7+ | 0.280 | [0.092, 0.469] | 0.0746 | No |
| C | 2 → 3 | 0.038 | [-0.103, 0.179] | 1.0000 | No |
| C | 3 → 4 | -0.013 | [-0.192, 0.165] | 1.0000 | No |
| C | 6 → 7+ | 0.181 | [-0.126, 0.489] | 1.0000 | No |
| D | 0 → 1 | 0.305 | [0.222, 0.389] | 0.0000 | Sí |
| D | 0 → 7+ | 0.549 | [0.398, 0.701] | 0.0000 | Sí |
| D | 1 → 7+ | 0.244 | [0.064, 0.424] | 0.1623 | No |
| D | 2 → 3 | 0.013 | [-0.118, 0.145] | 1.0000 | No |
| D | 3 → 4 | -0.017 | [-0.191, 0.157] | 1.0000 | No |
| D | 6 → 7+ | 0.136 | [-0.158, 0.430] | 1.0000 | No |

Los **28 contrastes** de cada especificación, incluidos los no mostrados aquí, están en el CSV; esta tabla no constituye una nueva selección de pruebas basada en significancia.

## Comparación A frente a D

- **0 → 1:** A: ΔZ=0.280, Holm p=0.0000; D: ΔZ=0.305, Holm p=0.0000. Las diferencias entre ajustes no identifican efectos causales.
- **1 → 7+:** A: ΔZ=0.238, Holm p=0.1571; D: ΔZ=0.244, Holm p=0.1623. Las diferencias entre ajustes no identifican efectos causales.
- **3 → 4:** A: ΔZ=-0.011, Holm p=1.0000; D: ΔZ=-0.017, Holm p=1.0000. Las diferencias entre ajustes no identifican efectos causales.

## Diagnósticos y límites

- Las cuatro especificaciones devolvieron 28 contrastes con covarianza robusta estimable y corrección Holm definida.

**Z está estandarizada dentro del contexto profesor-periodo**; sus SD por frecuencia pueden diferir de 1. La variable Z usada en el paper incluye valores numéricos asignados a las bajas BV/RT/BA según el procedimiento previamente documentado, a diferencia de PASS. Por ello, una diferencia de Z puede depender en parte de cómo se imputaron esos estados; el contraste no equivale a una diferencia de calificaciones numéricas observadas únicamente.

Los controles por carrera y profesor-periodo no resuelven la autoselección, las diferencias en preparación matemática previa ni la motivación por PPA1. Los umbrales 2|3 y 3|4 son descriptivos; ninguno prueba que PPA1 o una visita adicional produzcan la diferencia.

Para valorar predicción futura habría que diseñar validación temporal o fuera de muestra con variables disponibles antes del desenlace, evitando fugas de información. Este experimento estima **asociaciones ajustadas**, no capacidad predictiva prospectiva.

Este informe es una sensibilidad adicional. Se conserva la especificación principal originalmente declarada para el artículo.
