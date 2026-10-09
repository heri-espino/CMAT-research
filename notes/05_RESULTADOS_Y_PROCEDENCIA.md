# 05 — Resultados de frecuencia y ajuste Holm

Fuente: tablas CSV agregadas de `results/paper21/tables/`. Esta nota resume resultados ya estimados; no constituye una corrida nueva.

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