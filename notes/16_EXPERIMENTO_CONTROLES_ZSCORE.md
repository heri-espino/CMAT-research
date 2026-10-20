# 16 — Sensibilidad de los Z-scores a los controles (cuatro modelos OLS)

**Fecha:** 20 de octubre de 2026. **Estado:** implementación disponible; falta ejecutar la corrida real y validar sus resultados. El presente experimento es una sensibilidad del Paper 2.1, no un nuevo modelo predictivo validado fuera de muestra.

## Pregunta

¿En qué medida cambia la asociación entre la **frecuencia de visitas a CMAT** y el **resultado continuo Z_GRADE_PRIMARY** al incorporar progresivamente controles por carrera y efectos fijos de profesor-periodo?

| Modelo | Efectos fijos profesor-periodo | Carrera | Estimador |
|---|---|---|---|
| **A** | No | No | OLS sobre Z |
| **B** | No | Sí | OLS sobre Z |
| **C** | Sí | No | OLS sobre Z |
| **D** | Sí | Sí | OLS sobre Z (referencia del manuscrito) |

En contraste con PASS, **Z es continuo y no corresponde una regresión logística**. Para comparar la sensibilidad de los dos outcomes, se mantiene la estructura A/B/C/D que ya se utiliza en los cuatro LPM y los cuatro modelos logísticos de PASS. En total, los experimentos comprenden **doce modelos: cuatro Z-OLS, cuatro LPM de PASS y cuatro logísticos de PASS**.

## Cohorte, controles y contrastes

- **Muestra:** primer intento elegible de Matemáticas Universitarias por estudiante entre primavera de 2019 y primavera de 2024; el script valida N=6,627 y 190 contextos profesor-periodo. Los casos completos de Z, frecuencia, profesor-periodo y carrera son comunes a las cuatro especificaciones Z.
- **Exposición categórica:** `0, 1, 2, 3, 4, 5, 6, 7+` visitas. Cero es la referencia para la parametrización, pero se calculan **los 28 pares** dentro de cada modelo.
- **Modelo:** `Z_GRADE_PRIMARY ~ C(VISIT_GROUP)` con `C(CLAVECARRERA)` y/o `C(CLASSROOM_ID)` según A/B/C/D. Las diferencias se reportan como **frecuencia mayor menos frecuencia menor**.
- **Inferencia:** errores estándar robustos **agrupados por CLASSROOM_ID incluso en A/B**, IC 95%, Wald bilateral y Holm al 5% por familia de **28 pruebas**. Ningún rechazo si la matriz robusta del conjunto de contrastes tiene rango insuficiente o algún valor p es indefinido.
- **Reproducción:** los 28 coeficientes D-OLS deben coincidir con `results/paper21/tables/26a_zero_inclusive_7plus_pairwise_continuous.csv`; si no coinciden, el ejecutable se detiene antes de guardar resultados. Es la misma muestra y modelo D que el análisis canónico.
- **Ajuste predictivo aparente:** se reportan R², R² ajustado y RMSE **en la muestra utilizada para estimar**. No se presentan como validación cruzada ni como predicción futura. Efectos fijos basados en profesor-periodo no permiten extrapolación directa a profesores o periodos inéditos.

El modelo canónico principal positivo 1/2/3/4/5/6+ no se reemplaza por esta sensibilidad exploratoria de ocho niveles. Tampoco se corrige conjuntamente por las **cuatro** familias Holm Z, de manera que escoger A, B, C o D según su valor p más favorable sería inapropiado.

## Precaución adicional para Z

`Z_GRADE_PRIMARY` procede de notas estandarizadas dentro de profesor-periodo y **contiene el esquema de imputación previamente documentado** para estudiantes con estados BV, RT y BA, mientras PASS se calcula sin imputación numérica. La media o SD de Z en cada grupo de frecuencia no tiene por qué ser 0 o 1. Las diferencias inferidas dependen, en parte, del esquema con el que se representan administrativamente esas observaciones; contrastes con notas numéricas observadas exclusivamente responderían a otra pregunta y requerirían declarar el cambio de población.

La diferencia A→D refleja cambios de ajuste y precisión, no la prueba de causalidad de la asistencia, de PPA1 ni la identificación de un umbral mínimo. Tampoco los parámetros permiten inferir habilidades matemáticas previas o motivación no observada.

## Ejecución

```bash
git switch paper/paper2.1-visit-frequency
git pull --ff-only origin paper/paper2.1-visit-frequency
conda activate cmat-research
python -m pip install -e "./cmat_analysis[dev]"
python -m pytest -q cmat_analysis/tests/test_paper21_zscore_controls_experiment.py
python code/run_paper21_zscore_controls_experiment.py
```

Archivos generados tras ejecutar:

- `results/paper21/tables/adjustment_experiment/z_pairwise_4ols.csv`: 112 comparaciones entre las cuatro especificaciones; cambios de Z, errores estándar agrupados, IC 95%, valores p originales y Holm, decisiones y validez.
- `results/paper21/tables/adjustment_experiment/z_model_diagnostics_4ols.csv`: fórmulas, N, 190 contextos, R², R² ajustado, RMSE en muestra y estado de inferencia.
- `notes/17_RESULTADOS_OLS_ZSCORE_CONTROLES.md`: reporte automático de medias y SD descriptivas, contrastes seleccionados, diferencias A frente a D e interpretación.

El workflow manual `paper21-controls-experiment.yml` ejecuta también los cuatro modelos Z y conserva los resultados en un **artefacto temporal de GitHub Actions**; no se ejecuta con cada commit ni incorpora automáticamente los resultados a la rama.

## Qué analizar una vez ejecutado

1. Cómo cambia `0→1`, `0→7+` y `1→7+` de A a D, tanto en valor de ΔZ como en el IC y Holm.
2. Si `2→3` o `3→4`, relevantes para la interpretación institucional de PPA1, se distinguen **sin afirmar efectos causales**.
3. Si los resultados de Z son consistentes con el patrón de PASS en sus propias unidades, sin confundir desviaciones estándar con puntos porcentuales.
4. Si el modelo D recupera las 28 estimaciones existentes y si todos los contrastes son estimables antes de comunicar diferencias significativas.

Para el diseño paralelo de PASS, véase [14_EXPERIMENTO_CONTROLES_LPM_LOGIT.md](14_EXPERIMENTO_CONTROLES_LPM_LOGIT.md).
