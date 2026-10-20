# 14 — Experimento de controles: LPM frente a regresión logística

**Estado al 20 de octubre de 2026:** implementación disponible; **estimaciones sobre datos institucionales todavía pendientes de ejecutar y validar**. Sensibilidad adicional, no sustitución retrospectiva del modelo principal de Paper 2.1.

## Pregunta y diseño

¿Cambian los contrastes de PASS entre frecuencias (y sus valores p de Holm) al omitir efectos fijos profesor-periodo y controles por carrera?

| Modelo | Profesor-periodo | Carrera | Propósito |
|---|---|---|---|
| A | No | No | Contraste crudo entre frecuencias |
| B | No | Sí | Aislar el aporte del ajuste por carrera |
| C | Sí | No | Aislar el aporte de los efectos fijos docentes |
| D | Sí | Sí | Reproducir el modelo publicado como referencia |

Para **cada especificación** estimamos un modelo de probabilidad lineal (**LPM**) y un GLM binomial logístico (**logit**): **ocho regresiones** en total.

**Muestra:** mismos primeros intentos elegibles de Matemáticas Universitarias durante 2019–2024. Validamos **N=6,627** y **190** profesor-periodo; se usan los mismos casos completos de PASS, asistencia, profesor-periodo y carrera para los ocho modelos.

**Variable dependiente:** PASS=1 si la nota numérica es ≥7.5, incluido 7.5 exacto; PASS=0 para nota estrictamente inferior o estado BV, RT o BA, sin imputación numérica de PASS.

**Frecuencias:** 0, 1, 2, 3, 4, 5, 6 y 7+ visitas. El análisis original principal entre asistentes 1/2/3/4/5/6+ se mantiene como análisis principal del paper y no se reetiqueta retrospectivamente.

**Inferencia constante:** errores estándar robustos **agrupados por CLASSROOM_ID** para todos los modelos, incluso cuando no hay efectos fijos; **28 comparaciones por pares** para cada combinación método/especificación, todas «frecuencia más alta menos frecuencia más baja». Holm al 5% se aplica a las **28 pruebas de cada modelo**. No hay corrección conjunta entre las ocho familias, por lo cual no es válido elegir la especificación con el valor p más pequeño y presentarla como confirmatoria.

## Significado de los coeficientes

- **LPM:** las diferencias se expresan en puntos porcentuales de probabilidad de PASS. El modelo D debe recuperar los resultados canónicos existentes.
- **Logística:** las diferencias están en log-odds y sus exponenciales son **odds ratios condicionales**, no razones de probabilidades ni incrementos constantes en puntos porcentuales.
- Las OR pueden cambiar al modificar controles por **no colapsabilidad**, incluso sin confusión proporcional; los cambios entre A/B/C/D no se pueden atribuir automáticamente a una sola causa.

## Garantías antes de informar significancia

1. La rutina verifica que **los 28 contrastes LPM del modelo D coincidan** numéricamente con el CSV canónico **26k_zero_inclusive_7plus_pairwise_pass_lpm.csv**; ante discrepancias detiene la publicación de resultados.
2. La inferencia logística exige una matriz de covarianza robusta utilizable y **los 28 valores p finitos**. Si falla cualquiera, **no se calculan rechazos Holm**, se indica «ND» y se documenta el diagnóstico.
3. El CSV logístico anterior **26c_zero_inclusive_7plus_pass_logit_pairwise.csv** contiene errores estándar/valores p vacíos y 28 banderas inválidas de significancia. **No debe usarse como evidencia.** El código compartido ahora impide que una nueva corrida interprete NaN como rechazo Holm.
4. Se reportan advertencias de separación y problemas de convergencia. Las estimaciones puntuales no sustituyen la inferencia válida.
5. No se generan ni divulgan microdatos, identificadores de estudiantes o nombres; solamente estadísticos agregados.

## Ejecución reproducible

Archivo de ejecución: **code/run_paper21_model_controls_experiment.py**. Pruebas sintéticas: **cmat_analysis/tests/test_paper21_controls_experiment.py**.

Desde la raíz del repositorio, con los archivos institucionales autorizados disponibles:

    git switch paper/paper2.1-visit-frequency
    git pull --ff-only origin paper/paper2.1-visit-frequency
    conda activate cmat-research
    python -m pip install -e "./cmat_analysis[dev]"
    python -m pytest -q cmat_analysis/tests/test_paper21_controls_experiment.py
    python code/run_paper21_model_controls_experiment.py

Salidas cuando se ejecute:

- **results/paper21/tables/adjustment_experiment/pass_pairwise_4x2.csv**: efectos, IC, OR, p originales, p Holm y estado de cada contraste.
- **results/paper21/tables/adjustment_experiment/pass_model_diagnostics_4x2.csv**: fórmulas, muestra, convergencia, incidencias y rechazos.
- **notes/15_RESULTADOS_COMPARACION_LPM_LOGIT_CONTROLES.md**: reporte interpretativo generado a partir de las salidas reales.

También habrá un flujo de GitHub Actions **manual** que produce un artefacto temporal con esos CSV y la nota, sin ejecutarse en cada commit.

## Interpretación científica prevista

Analizar 0–1, 0–7+, 1–7+ y 3–4, primero a través de A/B/C/D dentro del LPM y después a través de A/B/C/D dentro de logística; distinguir cambios de magnitud, precisión y significancia ajustada. La comparación 3–4 **no** mide causalmente el incentivo PPA1. La ausencia de controles no equivale a ausencia de confusión, y contar visitas no establece un tratamiento causal. No reescribir el modelo principal en función de los p-values de esta sensibilidad.
