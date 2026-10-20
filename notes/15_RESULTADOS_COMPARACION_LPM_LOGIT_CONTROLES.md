# 15 — Resultados de la sensibilidad de controles: LPM y logit

**Estado: pendiente de ejecución sobre la cohorte institucional (20 de octubre de 2026).** Este archivo es una ficha de resultados por completar y **no contiene estimaciones nuevas**. La ejecución del script lo reemplaza por un informe automático, basado en los ocho modelos.

## Diseño de comparación

| Especificación | Profesor-periodo | Carrera | Métodos |
|---|---|---|---|
| A | Sin FE | Sin control | LPM, logística |
| B | Sin FE | Controlada | LPM, logística |
| C | Con FE | Sin control | LPM, logística |
| D | Con FE | Controlada | LPM, logística |

La muestra debe conservar 6,627 primeros intentos y 190 profesor-periodos. Cada uno de los ocho modelos examina **28 comparaciones entre 0, 1, 2, 3, 4, 5, 6 y 7+ visitas**, con errores estándar robustos agrupados por profesor-periodo y corrección Holm **dentro de cada modelo**. Los modelos no se han ejecutado en este entorno.

## Resultados confirmados del modelo D-LPM histórico (no son una nueva corrida)

- Frente a los no asistentes, cualquier asistencia se asoció con **+15.3 puntos porcentuales** de probabilidad de aprobación, IC95% de **+12.4 a +18.1 puntos**. Se trata del benchmark binario 0 frente a 1+, que no es igual a comparar grupos exactos 0/1/2/…
- En el modelo exploratorio de ocho grupos con controles, **7+ frente a una visita** tuvo **+14.5 puntos porcentuales**, Holm **p=0.0206**, en la familia de 28 pares; esa diferencia no resultó significativa después de Holm en la comparación sólo entre asistentes.
- Ningún contraste adyacente entre frecuencias positivas tuvo respaldo después de Holm. En particular **3 frente a 4** no demuestra un efecto del requisito PPA1.

**Fuente:** resultados canónicos de las tablas 10_benchmark_0_vs_1plus.csv y 26k_zero_inclusive_7plus_pairwise_pass_lpm.csv, previamente existentes en el repositorio.

**No se conocen aún los p-valores Holm de los modelos A, B y C**, ni la inferencia logística válida de A–D. No extrapolar los p-values actuales a modelos sin controles.

## Tabla a completar al ejecutar el experimento

| Método | Modelo | ¿Covarianza robusta válida? | Comparaciones Holm p<0.05 | 1 frente a 7+: estimación | 1 frente a 7+: Holm p |
|---|---|---|---|---|---|
| LPM | A | Pendiente | Pendiente | Pendiente | Pendiente |
| LPM | B | Pendiente | Pendiente | Pendiente | Pendiente |
| LPM | C | Pendiente | Pendiente | Pendiente | Pendiente |
| LPM | D | Pendiente de validación | Pendiente de validación | +14.5 pp, previamente calculado | 0.0206, previamente calculado |
| Logit | A | Pendiente | Pendiente | Pendiente | Pendiente |
| Logit | B | Pendiente | Pendiente | Pendiente | Pendiente |
| Logit | C | Pendiente | Pendiente | Pendiente | Pendiente |
| Logit | D | **No válida en el CSV logístico histórico** | No reportable | OR puntuales previas solamente | No reportable |

## Interpretación preliminar

Comparar las tasas observadas sin controles con el modelo D sugiere que la composición académica puede cambiar de manera apreciable las asociaciones estimadas, pero las tasas agregadas por frecuencia **no permiten reproducir los errores estándar agrupados ni los p-values Holm de un LPM sin controles**. Es indispensable ejecutar las cuatro especificaciones sobre la misma cohorte. El modelo logístico anterior presenta resultados puntuales de odds ratios, pero la inferencia es inválida debido a p-values y errores estándar ausentes, y por eso no aporta evidencia confirmatoria.

No confundir **odds ratios** con razones de probabilidades, ni atribuir diferencias en significancia a efectos de CMAT o de PPA1. La corrección Holm controla comparaciones múltiples **dentro de cada modelo**, no entre especificaciones elegidas después de revisar resultados.

## Cómo generar los resultados

El comando ejecuta y **reescribe esta misma nota** con tablas, diagnósticos e interpretaciones procedentes de los resultados reales:

    python code/run_paper21_model_controls_experiment.py

Alternativamente, GitHub → Actions → **Paper 2.1 - comparison of controls (LPM and logit)** → Run workflow, en la rama **paper/paper2.1-visit-frequency**. El archivo generado, los CSV agregados y los diagnósticos estarán en un artefacto temporal; GitHub Actions no los subirá automáticamente al repositorio.

Para los supuestos y las reglas de reporte véase [el protocolo del experimento](14_EXPERIMENTO_CONTROLES_LPM_LOGIT.md).
