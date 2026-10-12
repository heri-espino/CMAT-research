# 05 — Resultados de frecuencia y ajuste Holm

Fuente: tablas CSV agregadas de `results/paper21/tables/`. Esta nota resume resultados ya estimados; no constituye una corrida nueva.

## Cuatro rangos propuestos a partir de PPA1 (sólo descriptivos)

Los N por rango son `0=5,393`, `1–3=932`, `4–6=201` y `7+=101`, calculados directamente de los conteos existentes. En el modelo de ocho frecuencias, ninguno de los seis pares internos a `1–3` y `4–6` sobrevivió Holm en Z o PASS; **esto no demuestra equivalencia**. La única diferencia Holm-significativa entre frecuencias positivas del modelo completo es `1` frente a `7+` para PASS, además de siete comparaciones de `0` contra frecuencias positivas por outcome. Los cuatro rangos siguen siendo una hipótesis descriptiva y no un modelo de cuatro niveles contrastado.

## Benchmark

Con N=6,627 y 190 grupos profesor–periodo, cualquier asistencia frente a cero se asocia con **+0.36118 DE** en calificación Z (IC 95% 0.30172–0.42065) y **+15.2917 pp** en PASS (IC 12.4376–18.1457 pp). Fuente `10_benchmark_0_vs_1plus.csv`.

## Entre usuarios: agrupación originalmente congelada

N=1,234, 176 profesor–periodo, frecuencias `1/2/3/4/5/6+`. Omnibus **p=0.31655** para Z y **p=0.15222** para PASS; **ningún par entre los 15** supera Holm en cada outcome. Comparar 1 con 6+: Z p cruda 0.022 vs Holm 0.328; PASS p cruda 0.011 vs Holm 0.171. Fuentes `12_primary_omnibus.csv`, `13_primary_pairwise_continuous.csv`, `14_primary_pairwise_pass.csv`.

## Sensibilidad entre usuarios: cola 7+

`1/2/3/4/5/6/7+`, 21 contrastes por outcome. Omnibus Z **p=0.21257**, PASS **p=0.10198**; ningún par sobreviviendo Holm. Fuente `21_sensitivity_7plus_omnibus.csv` y tablas `22`–`23`.

## Modelo completo, cero incluido

`0/1/2/3/4/5/6/7+`, N=6,627, 28 contrastes por outcome. Todos los `0` frente a cada frecuencia positiva sobreviven Holm en Z y PASS. En PASS, `7+` menos una visita = **+14.4865 pp**, IC 95% [5.9074, 23.0656] pp, p-Holm **0.02056**; este resultado pertenece al modelo completo, no a la muestra exclusiva de usuarios. Fuente `26k_zero_inclusive_7plus_pairwise_pass_lpm.csv`; Z: `26a_zero_inclusive_7plus_pairwise_continuous.csv`; matrices `26b`, `26e`–`26h`.

## Sensibilidad: varianza agrupada por profesor

En usuarios (51 profesores), omnibus Z **p=0.0477**, PASS **p=0.0551**. El contraste no adyacente PASS `6+` contra `1` = **+12.0 pp** (IC 4.3–19.8, p-Holm 0.0358); ningún contraste de Z supera Holm. El benchmark se mantiene cerca de +0.361 Z y +15.3 pp PASS. Fuentes `26_instructor_cluster_pairwise_continuous.csv`, `27_instructor_cluster_pairwise_pass.csv`, `28_instructor_cluster_omnibus.csv` y `29_instructor_cluster_benchmark_0_vs_1plus.csv`.

## Validez e interpretación

Estos resultados son asociaciones ajustadas, no efectos causales. Ausencia de rechazo entre categorías positivas no implica equivalencia. No fundir las familias de 15, 21 y 28 pares ni escoger retrospectivamente un contraste al conocer su p-value. La agrupación 6+ se decidió antes de revisar outcomes; la presentación 7+ fue posterior.

**Pendiente:** reconciliar todos los números y leyendas con la compilación actual, la definición de Z y las decisiones de clustering; documentar el commit de una eventual reestimación controlada.
## Figura de contexto y procedencia (2026-10-12)

La figura de tres paneles al inicio de Results se construye exclusivamente con dos tablas agregadas ya existentes, `10n_zero_inclusive_7plus_descriptives.csv` para `n` y `pass_rate`, y `10s_zero_inclusive_7plus_imputed_z_histogram.csv` para los bins del resultado estandarizado. Presenta PASS/no PASS a la izquierda; en el centro, histogramas transparentes por frecuencia con los componentes PASS y no-PASS, **normalizados por todos los estudiantes de cada frecuencia**, sin inventar una distribución por estudiante; a la derecha, número total de estudiantes por frecuencia en escala logarítmica. Los bins de Z exportados sólo cubren aproximadamente `-2..2`; el caption indica que las colas fuera de esta ventana no aparecen en el histograma. **No** dibujar un punto fijo 7.5 en el eje Z, pues ese punto pertenece a la nota numérica original y cambia tras estandarizar por profesor–periodo. Los cuatro rangos PPA1 son ayudas descriptivas, no cuatro grupos identificados inferencialmente. Se eliminó la tabla extensa de ocho medias/IC de la sección principal en favor de esta figura; sus números siguen en las tablas CSV.

## Umbral numérico y desglose actualizado de Figura 1 (2026-10-12)

El código `cmat_analysis/src/cmat_analysis/measures/_grades.py` fija `PASS = (GRADE_NUMERIC >= passing_grade)`, con `passing_grade = 7.5`; las notas numéricas estrictamente `<7.5` se codifican como fracaso. `>=7.5` incluye exactamente 7.5, no utiliza `<=7.5` para definir fracaso. El archivo `10o_zero_inclusive_7plus_exact_administrative_composition.csv` proporciona los cinco estados `pass`, `numeric_grade_below_7.5`, `BV`, `RT`, `BA`, mientras `10s_zero_inclusive_7plus_imputed_z_histogram.csv` conserva las mismas categorías para el histograma Z (estados administrativos imputados únicamente en el continuo). Figura 1 los presenta como **PASS azul**, **fracaso numérico naranja** y **BV/RT/BA dorado**, usando la totalidad de cada grupo como denominador.

Condicional a no-PASS: `10f_nonpass_management_descriptives_0_vs_1plus.csv`: 0 visitas 581 numéricos y 923 administrativos de 1,504; 1+ visitas 39 numéricos y 178 administrativos de 217. `10e_nonpass_management_benchmark_0_vs_1plus.csv`: diferencia ajustada administrativa vs numérica = +0.132261, IC 95% [.068029,.196494], p=0.00005443, N=1,721. Esta **comparación auxiliar** no es parte de las familias Holm del artículo y no responde por qué alguien obtuvo BA, BV o RT.
