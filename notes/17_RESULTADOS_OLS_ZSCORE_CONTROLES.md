# 17 — Resultados de la sensibilidad de Z-score (OLS A/B/C/D)

**Estado: pendiente de ejecución (20 de octubre de 2026).** Este archivo contiene únicamente la **referencia canónica ya estimada** de Paper 2.1. Cuando se ejecute `code/run_paper21_zscore_controls_experiment.py`, se reemplazará por el informe de las **cuatro regresiones reales**, incluyendo R², RMSE, cambios A→D, IC y p de Holm.

## Diseño previsto

| Especificación | Profesor-periodo | Carrera | Estado |
|---|---|---|---|
| A | No | No | Pendiente |
| B | No | Sí | Pendiente |
| C | Sí | No | Pendiente |
| D | Sí | Sí | Resultados canónicos conocidos; requiere reproducción |

Todas usarán 0/1/2/3/4/5/6/7+ visitas, **N=6,627**, 190 profesor-periodos, errores estándar agrupados por profesor-periodo y las mismas **28 comparaciones con Holm en cada especificación**.

## Modelo D-OLS: cifras ya existentes, no nuevas

| Comparación | Diferencia estimada Z, grupo alto menos bajo | p Holm de los 28 pares |
|---|---:|---:|
| 0 → 1 | +0.305 | <0.001 |
| 0 → 7+ | +0.549 | <0.001 |
| 1 → 7+ | +0.244 | 0.1623 |
| 2 → 3 | +0.013 | 1.000 |
| 3 → 4 | −0.017 | 1.000 |
| 6 → 7+ | +0.136 | 1.000 |

Fuente: `results/paper21/tables/26a_zero_inclusive_7plus_pairwise_continuous.csv`. Estas son diferencias **ajustadas** por profesor-periodo y carrera en el modelo exploratorio de ocho frecuencias; no son estimaciones causales ni efectos marginales de cada visita adicional.

El contraste 1→7+ tiene p **sin ajustar** aproximadamente 0.0077, pero **no supera Holm** dentro de los 28 pares de Z en ese modelo. Ninguna comparación adyacente entre usuarios aporta un umbral confirmado.

## ¿Qué falta para responder la nueva pregunta?

Todavía **no están calculadas** las estimaciones ni los valores p Holm de A/B/C para Z; tampoco los R² y RMSE. No se pueden obtener mediante una manipulación de las medias descriptivas de los grupos, pues deben respetarse la dependencia intraclúster, los controles específicos y la muestra común.

## Interpretación pendiente después de la ejecución

La corrida producirá `results/paper21/tables/adjustment_experiment/z_pairwise_4ols.csv` y `z_model_diagnostics_4ols.csv`, además de reescribir esta nota con la tabla detallada de los cuatro modelos y los contrastes 0→1, 0→7+, 1→7+, 2→3, 3→4 y 6→7+.

Recordatorio: las diferencias de Z se interpretan en unidades de resultado estandarizado, no en puntos porcentuales; además, `Z_GRADE_PRIMARY` incorpora las imputaciones ya documentadas para BV/RT/BA. R² y RMSE dentro de muestra no demuestran precisión predictiva en cohortes futuras, sobre todo cuando se incorporan efectos fijos de profesor-periodo.

El estudio es **observacional**, y la disponibilidad continua de la alternativa PPA1 de tres visitas no hace de 3→4 un contraste causal.

## Ejecución

```bash
python -m pytest -q cmat_analysis/tests/test_paper21_zscore_controls_experiment.py
python code/run_paper21_zscore_controls_experiment.py
```

También está previsto en el workflow manual de GitHub Actions `paper21-controls-experiment.yml`. El PDF principal del paper no se altera por este experimento.
