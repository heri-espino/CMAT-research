# 2026-10-11 — PPA1 y representación triangular de Holm

## Corrección institucional

Los puntos PPA1 de la modalidad descrita se obtienen **al completar la tercera visita a CMAT**. La comparación 2|3 incluye el momento de cumplimiento, pero **3|4** separa las asistencias necesarias para cumplir el requisito de las visitas posteriores. La vigencia histórica exacta por periodo o estudiante todavía debe verificarse.

## Hipótesis visual de cuatro segmentos

| Segmento de asistencia | N |
|---|---:|
| 0 | 5,393 |
| 1–3 | 932 |
| 4–6 | 201 |
| 7+ | 101 |
| **Total** | **6,627** |

Los conteos proceden de `results/paper21/tables/10n_zero_inclusive_7plus_descriptives.csv`: 1–3 = 517+245+170; 4–6 = 96+55+50. **No se han ajustado modelos nuevos con cuatro factores fusionados.**

## Heatmaps con triángulo superior

El código `code/figures_paper21.py` muestra solamente las 28 celdas por encima de la diagonal para cada outcome. En el panel de efectos, el valor es **grupo de mayor frecuencia menos grupo de menor frecuencia**; Z tiene unidades DE y PASS puntos porcentuales. En los paneles de valores p crudos y ajustados por Holm sólo se imprimen las celdas del triángulo superior, con separación después de visitas **0, 3 y 6**. Los separadores son institucionales y exploratorios, **no pruebas de hipótesis sobre changepoints**.

## Evidencia que los datos existentes sí permiten

- Dentro de los rangos 1–3 y 4–6 hay seis pares en total. En los contrastes completos de ocho niveles, **ninguno de esos seis pares sobrevive Holm**, tanto para Z como para PASS, pero ello **no demuestra equivalencia**.
- Los siete contrastes entre cero y cada frecuencia positiva sobreviven Holm en Z y PASS.
- En PASS, también sobrevive el contraste entre una visita y 7+ (diferencia de 14.5 puntos porcentuales, p-Holm 0.0206) en la **familia de 28 pares del modelo completo**, no en el análisis sólo entre usuarios.
- No hay evidencia Holm-significativa de un salto **adyacente** entre 3 y 4, ni entre 6 y 7+.
- Estos resultados **no demuestran que existan exactamente cuatro regímenes**. Su presentación es un marco interpretativo del incentivo PPA1 y la cola de asistencia, no una conclusión inferencial.

## Fuentes verificables

`paper/docs/analysis/VISIT_GROUPING_DECISION.md`, `results/paper21/tables/26a_zero_inclusive_7plus_pairwise_continuous.csv`, `results/paper21/tables/26k_zero_inclusive_7plus_pairwise_pass_lpm.csv`, las matrices `26b` y `26e`–`26h`, y los tres PDF de `results/paper21/figures/`.