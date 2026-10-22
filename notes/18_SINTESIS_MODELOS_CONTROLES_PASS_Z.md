# 18 — Síntesis científica: sensibilidad de PASS y Z a controles y especificación

**Actualización: 21 de octubre de 2026. Resultados efectivamente generados y guardados en la rama `paper/paper2.1-visit-frequency`.**

Esta nota integra las ocho regresiones de PASS (cuatro LPM y cuatro logísticas) y las cuatro regresiones OLS de `Z_GRADE_PRIMARY`. Los resultados fueron recuperados de los CSV generados, no reconstruidos a partir de porcentajes publicados. **No implica un nuevo experimento aleatorizado ni un cambio de la especificación principal del manuscrito.**

## Diseños y convenciones

| Modelo | Profesor-periodo | Carrera |
|---|---|---|
| A | Sin efectos fijos | Sin controles |
| B | Sin efectos fijos | Control |
| C | Efectos fijos | Sin controles |
| D | Efectos fijos | Control |

Los 12 modelos utilizan 6,627 primeros intentos elegibles distribuidos en 190 contextos profesor-periodo, el mismo esquema de ocho categorías `0/1/2/3/4/5/6/7+`, errores estándar robustos **agrupados por profesor-periodo en todas las especificaciones**, y **28 comparaciones por pares** con Holm por modelo, no entre todos los modelos a la vez. No es lícito escoger a posteriori la familia o el método que arroje más significancias como prueba confirmatoria.

PASS es binaria y se analiza mediante un LPM (diferencia de probabilidad) o un logit (diferencia de log-odds, transformada a odds ratio); `Z_GRADE_PRIMARY` es continua y se analiza con OLS (diferencia de Z). La variable Z incorpora el tratamiento numérico institucional previamente documentado para BV/RT/BA, a diferencia de PASS, y sus coeficientes no son puntos porcentuales.

## Cobertura de contrastes tras Holm

| Controles | Z-OLS (de 28) | PASS-LPM (de 28) | PASS-logit (de 28) |
|---|---:|---:|---:|
| A: ninguno | 6 | 3 | 2 |
| B: carrera | 6 | 4 | 2 |
| C: profesor-periodo | 6 | 8 | 6 |
| D: ambos | 7 | 8 | **ND** |

La logística D converge y produce estimaciones puntuales de OR, pero **su incertidumbre agrupada no es estimable**: faltan errores estándar, IC y valores p. La presencia de un `RuntimeWarning` por sí sola no identifica el mecanismo exacto del fallo. No reportar rechazos de Holm ni inferir precisión de las OR de D.

## Qué comparaciones explican esos conteos

- **Z-OLS:** los 6 contrastes significativos en A, B y C son exclusivamente las comparaciones entre **0 visitas y 1, 2, 3, 4, 5 o 7+**. En D se añade 0 contra 6. **Ninguna comparación entre dos frecuencias estrictamente positivas supera Holm** en los cuatro modelos.
- **PASS-LPM A:** significan 0–1, 0–4, 0–7+. **B:** se añade 0–2. **C y D:** significan los siete contrastes 0 contra cada grupo positivo y, además, **1–7+**, el único contraste positivo-positivo significativo en esas especificaciones exploratorias.
- **PASS-logit A y B:** significan 0–1 y 0–7+. **C:** significan 0–1, 0–2, 0–3, 0–4, 0–5 y 0–7+. No hay ninguna comparación significativa entre frecuencias positivas en A, B o C. **D:** no tiene inferencia utilizable.

Estos conjuntos evidencian que **la mayor parte del patrón significativo distingue cero visitas de frecuencias positivas**, sin identificar de forma robusta incrementos entre usuarios.

## Tres contrastes especialmente informativos

| Outcome/método | Contraste | A sin controles | D con ambos controles |
|---|---|---|---|
| PASS–LPM | 0→1 | +8.93 pp; Holm 0.0004 | +12.13 pp; Holm <0.0001 |
| PASS–LPM | 1→7+ | +8.06 pp; Holm 1.0000 | **+14.49 pp; Holm 0.0206** |
| PASS–LPM | 3→4 | +4.69 pp; Holm 1.0000 | +5.15 pp; Holm 1.0000 |
| Z–OLS | 0→1 | +0.280 Z; Holm <0.0001 | +0.305 Z; Holm <0.0001 |
| Z–OLS | 1→7+ | +0.238 Z; Holm 0.1571 | +0.244 Z; Holm 0.1623 |
| Z–OLS | 3→4 | −0.011 Z; Holm 1.0000 | −0.017 Z; Holm 1.0000 |

Para el **logit con solo efectos fijos (C)**, las odds de PASS de 7+ frente a una visita se estiman en **OR = 3.00**, IC95% **[1.32, 6.82]**, pero el **valor p ajustado por Holm es 0.1872**, de modo que no constituye evidencia multiplicidad-ajustada. El IC mostrado es bilateral *sin ajuste por multiplicidad*; por ello no se debe interpretar su exclusión de 1 como contradicción del resultado Holm. En el modelo logístico D se obtiene OR puntual 2.75 para ese par, **sin IC ni p válido**.

### Interpretación de la sensibilidad

1. **La separación entre ninguna visita y al menos algunas frecuencias positivas es relativamente estable**, especialmente para Z. En PASS la cantidad de pares detectados cambia al añadir efectos fijos profesor-periodo, mientras que controlar únicamente por carrera modifica menos la pauta.
2. **La señal de 1 frente a 7+ para PASS es frágil frente a especificaciones:** no sobrevive Holm en los LPM A y B, aparece en C y D, no sobrevive Holm en el logit C y no puede contrastarse en el logit D. No sostener que «7+ funciona mejor» ni presentar esa señal como umbral de eficacia.
3. **La frontera de PPA1, 3 frente a 4 visitas, no se distingue estadísticamente después de Holm** en las especificaciones válidas presentadas. La cuarta visita supera un requisito de actividad, pero no identifica una discontinuidad causal.
4. Los resultados no invalidan la **familia principal de comparaciones exclusivamente entre usuarios `1/2/3/4/5/6+`**, elegida antes de observar outcomes, cuyos contrastes positivos no sobrevivieron Holm. El corte exploratorio en 7+ y el modelo con cero incluido tienen otra población y otra familia inferencial.
5. **No colapsabilidad de OR:** es incorrecto comparar directamente números de OR entre modelos con diferentes covariables como si fueran la misma diferencia de probabilidad. El LPM, en cambio, expresa sus parámetros en puntos porcentuales bajo sus hipótesis.
6. Un mayor número de rechazos Holm en una especificación no demuestra menor sesgo, mejor predicción ni un efecto educativo causal; faltan preparación previa, motivación y datos individuales de PPA1.

## Ajuste en muestra de Z: no equivale a predicción futura

| Modelo | R² | R² ajustado | RMSE Z, en muestra |
|---|---:|---:|---:|
| A | 0.0175 | 0.0165 | 0.9769 |
| B | 0.0510 | 0.0389 | 0.9601 |
| C | 0.0202 | −0.0096 | 0.9755 |
| D | 0.0582 | 0.0179 | 0.9564 |

La mejora de R² en D sigue siendo limitada y proviene de un ajuste **en la misma muestra**; no se evaluó predicción en periodos futuros, por lo que no sería correcto presentar estos resultados como buen desempeño predictivo. Z se estandarizó dentro de profesor-periodo, circunstancia que también condiciona el significado de su ajuste.

## Recomendación para Paper 2.1

Conservar D-LPM para PASS y D-OLS para Z como modelos principales, junto con la especificación histórica entre usuarios, y situar A/B/C y los logit estimables en material suplementario de robustez. **No elevar 1→7+ al hallazgo principal**, pues su significancia depende del conjunto de controles y del método. Presentar la ausencia de pruebas de diferencias entre frecuencias positivas como un límite de resolución estadística, **no como demostración de equivalencia o de efecto nulo**.

Antes de utilizar D-logit inferencialmente, diagnosticar la covarianza agrupada y la variación intra-contexto de PASS; considerar una alternativa adecuada (por ejemplo, logística condicional, con atención a contextos excluidos y cambio de población) sin cambiar selectivamente el estimando. Tampoco presentar el resultado de modelos sin controles como causal.

## Procedencia de los resultados

- [PASS: ocho modelos y sus contrastes](../results/paper21/tables/adjustment_experiment/pass_pairwise_4x2.csv)
- [PASS: diagnósticos](../results/paper21/tables/adjustment_experiment/pass_model_diagnostics_4x2.csv)
- [Z: cuatro OLS y sus contrastes](../results/paper21/tables/adjustment_experiment/z_pairwise_4ols.csv)
- [Z: diagnósticos](../results/paper21/tables/adjustment_experiment/z_model_diagnostics_4ols.csv)
- [Informe PASS autogenerado](15_RESULTADOS_COMPARACION_LPM_LOGIT_CONTROLES.md)
- [Informe Z autogenerado](17_RESULTADOS_OLS_ZSCORE_CONTROLES.md)

Esta síntesis interpreta archivos agregados ya disponibles y **no modifica** los CSV canónicos ni los modelos o las figuras del manuscrito.
