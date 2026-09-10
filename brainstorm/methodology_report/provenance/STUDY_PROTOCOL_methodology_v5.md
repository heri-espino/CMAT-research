# CMAT — protocolo del estudio orientado a publicación

## Título provisional

**From Incentivized Attendance to Persistent Help-Seeking: Longitudinal Use of a University Mathematics Support Center and Academic Performance**

**Español:** *Del uso incentivado a la búsqueda persistente de apoyo: utilización longitudinal de un centro universitario de apoyo matemático y desempeño académico*.

## Prioridad científica

El **outcome primario es desempeño académico continuo**. La aprobación/no aprobación es secundaria. El PPA no forma parte de la calificación: funciona como una característica institucional que permite distinguir el umbral de participación (`V ≥ 3`) del uso que continúa después de haberlo alcanzado (`V > 3`).

Secuencia conceptual:

`PPA → adopción/uso del CMAT → uso más allá del umbral → desempeño continuo → persistencia posterior en Cálculo`.

El estudio es observacional. Ninguna de estas flechas se interpreta automáticamente como efecto causal.

## Cohorte primaria

- Una observación por estudiante.
- Primer intento estándar de `MAT1012 — Matemáticas Universitarias`.
- Si el estudiante repite posteriormente, su primer intento se conserva; los intentos posteriores no entran en la cohorte primaria.
- `EQV`, `REV` y `AC` se excluyen: representan acreditaciones externas/equivalentes cuyo profesor y aula de evaluación no están observados.
- `BV`, `RT` y `BA` se conservan como resultados académicos adversos.
- La inferencia primaria de exposición se restringe a periodos con cobertura real del archivo de asesorías.

## Calendario

La universidad trabaja con periodos de aproximadamente cuatro meses:

1. Primavera (`P`),
2. Verano (`V`),
3. Otoño (`O`).

Las bases actuales contienen Primavera y Otoño; el pipeline soporta también Verano para futuras ampliaciones y ordena cronológicamente los periodos con tres posiciones por año.

## Exposición primaria

Para el estudiante `i` en su primer intento de Matemáticas Universitarias:

`V_i = número de visitas cualesquiera al CMAT durante el mismo año y periodo académico del intento`.

Esta es la definición primaria porque coincide con la regla institucional del PPA. Las visitas etiquetadas específicamente como Matemáticas Universitarias se conservan como sensibilidad descriptiva, no como exposición principal.

### Grupos alrededor del umbral

- `0`: ninguna visita;
- `1–2`: uso limitado sin alcanzar PPA;
- `3`: alcanza exactamente el umbral;
- `4+`: uso más allá del umbral.

Además se definen:

- `PPA_REACHED = 1(V ≥ 3)`;
- `BEYOND_PPA = 1(V > 3)`.

El contraste binario principal de continuidad con el estudio exploratorio es `V > 3` versus `V ≤ 3`. Este contraste no se denomina “motivación intrínseca”; solo significa uso observado después del umbral necesario para el PPA.

## Outcome primario — desempeño continuo

El outcome principal es la calificación final continua, estandarizada dentro de `profesor × periodo` para un curso dado:

`Z_i = (Y_i^* - media_del_contexto) / sd_del_contexto`.

### BV / RT / BA e imputación KDE

Administrativamente se asume que `BV`, `RT` y `BA` corresponden a resultados académicos adversos por debajo del umbral aprobatorio de 7.5. No se les asigna arbitrariamente una calificación fija. Para cada salón `c = profesor × curso × periodo`, se forma el conjunto observado de calificaciones numéricas `X_j < 7.5`.

Si ese conjunto contiene al menos dos valores y varianza positiva, se ajusta `scipy.stats.gaussian_kde(X, bw_method=None)`. `bw_method=None` es el valor por defecto de SciPy y utiliza la regla de Scott; en una dimensión el factor de ancho de banda es `n^(-1/5)` multiplicando la escala de covarianza muestral. La densidad estimada puede escribirse como

`f_hat_h(x) = (1 / (n h)) Σ_j K((x-X_j)/h)`,

con kernel gaussiano. Los valores imputados se obtienen por remuestreo del KDE con semilla 42 y rechazo de draws fuera de `[0,7.5)`, para impedir que un outcome administrativamente adverso se convierta en una nota aprobatoria.

Casos límite:

1. si el salón tiene valores sub-7.5 pero el pool es degenerado (un solo valor o varianza cero), se remuestrea empíricamente ese pool;
2. si el salón no tiene ninguna calificación numérica observada debajo de 7.5, se utiliza `U(0,7.5)` como fallback;
3. la sensibilidad uniforme imputa todos los outcomes adversos mediante cuantiles interiores deterministas de `U(0,7.5)`;
4. la sensibilidad complete-case utiliza únicamente calificaciones numéricas.

Después de completar `Y_i^*`, se calcula el Z-score con media y desviación estándar muestral (`ddof=1`) del salón completo. La estabilidad de signo/magnitud entre estas especificaciones es más importante que una única imputación puntual. El outcome binario `PASS` no requiere imputación numérica: `BV/RT/BA` se codifican directamente como `PASS=0`.

## Outcome secundario — aprobación

`PASS = 1` si la calificación numérica es `≥ 7.5`.

`PASS = 0` si la calificación numérica es `< 7.5` o el estado es `BV`, `RT` o `BA`.

Este outcome no requiere asignar una calificación numérica a una baja.

## RQ1 — patrón de uso alrededor del PPA

¿La distribución de **todas las visitas al CMAT durante Matemáticas Universitarias** muestra una concentración o cambio de continuación alrededor de `V = 3`, y cómo se compara descriptivamente con Cálculo I, donde el PPA no aplica?

Métricas:

- distribución exacta de `V`;
- `P(V = 3)`;
- proporción que alcanza PPA `P(V ≥ 3)`;
- proporción que continúa más allá `P(V > 3)`;
- índice local `P(V=3) / mean[P(V=2), P(V=4)]`;
- curva `P(V ≥ k+1 | V ≥ k)`.

Cálculo I no se trata como control causal del PPA, porque también cambian curso, periodo, dificultad y composición de estudiantes.


## RQ1b — concentración temporal de visitas y calendario académico

La fecha calendario de cada asesoría se conserva a resolución de **día**. Esto permite estudiar dos mecanismos descriptivos adicionales sin cambiar el outcome primario de desempeño:

1. **Concentración intra-día alrededor del PPA.** Para cada estudiante se calcula el máximo de visitas en un mismo día, la fecha de la tercera visita, cuántas visitas ocurrieron en esa fecha y si las primeras tres visitas ocurrieron el mismo día. Tres visitas en un día se reportan como *asistencia concentrada*; no se atribuye automáticamente una motivación estratégica.
2. **Picos de demanda del CMAT.** Se construye una serie diaria de visitas y estudiantes únicos para cada periodo. Como exploración reproducible se detectan picos sobre una suma móvil centrada de 7 días de estudiantes-día, con separación mínima de 21 días y prominencia mínima `max(5, 12% del máximo del periodo)`. La periodicidad se resume mediante los días entre picos.

Las fechas exactas de examen dependen del profesor y no están observadas. Institucionalmente, sin embargo, la mayoría de los profesores aplica aproximadamente **cuatro evaluaciones, cerca de una por mes**, mientras todos los cursos comparten las mismas fechas generales de inicio y cierre. Por ello, los picos agregados se interpretan únicamente como **concentración temporal compatible con un ciclo de evaluación aproximadamente mensual**; no se asigna un pico específico a un examen concreto.

Como diagnóstico formal complementario, el pipeline elimina el promedio por día de la semana, detrenda linealmente cada serie diaria y calcula (a) autocorrelación para rezagos de 14–45 días y (b) el componente dominante de un periodograma restringido a periodos de 21–42 días. Estas medidas describen periodicidad; no identifican causalmente los exámenes como origen de la demanda.

## RQ2 — pregunta principal de desempeño

Entre estudiantes en su primer intento de Matemáticas Universitarias, ¿el uso del CMAT —en particular el uso más allá del umbral PPA— se asocia con mayor desempeño continuo?

Análisis principal:

- descriptivos e IC95% para cinco grupos `0`, `1`, `2`, `3`, `4+`;
- Welch ANOVA global para medias con varianzas heterogéneas;
- las 10 comparaciones por pares mediante Games–Howell, que admite varianzas y tamaños muestrales distintos;
- un único modelo OLS `Z ~ grupo_visitas + FE_salon + FE_carrera_oficial`, con errores estándar cluster-robust por salón; de este modelo se extraen las mismas 10 diferencias ajustadas y se controlan los 10 p-values mediante Holm;
- los contrastes históricos `V>3` vs `V≤3` y `V≥3` vs `V<3` se conservan como sensibilidad/continuidad histórica, no como especificación principal;
- Mann–Whitney, Brunner–Munzel y medidas de superioridad se conservan para los contrastes binarios históricos;
- sensibilidades de imputación.

La especificación exacta `0/1/2/3/4+` es prioritaria para responder si el patrón es una dosis monotónica o, alternativamente, una diferencia entre no uso y cualquier uso positivo.

## RQ2b — regularidad temporal y desempeño

Pregunta secundaria preespecificada:

> **Conditional on overall CMAT utilization, is more temporally distributed support use associated with higher continuous academic performance?**

La motivación es separar dos dimensiones observables del uso:

- **intensidad:** número total de visitas `V_i`;
- **distribución temporal:** qué tan extendidas están esas visitas a lo largo del periodo.

Como las fechas exactas de los cuatro exámenes dependen del profesor, la métrica primaria no etiqueta visitas como “pre-examen”. Se usa una aproximación mensual reproducible:

`REGULARITY_MONTHLY_4 = min(meses calendario activos, 4) / min(V_i, 4)`.

La medida pertenece a `(0,1]` entre usuarios. Un valor de 1 indica que las visitas están distribuidas entre tantos meses como el número de visitas permite, hasta cuatro ciclos mensuales; valores menores indican mayor concentración temporal.

Sensibilidades descriptivas:

- número de días activos;
- número de semanas activas;
- días entre primera y última visita;
- proporción máxima de visitas concentrada en un solo día;
- entropía semanal y **número efectivo de semanas**, `exp(H)`, donde `H = -Σ p_w log(p_w)`;
- `EFFECTIVE_WEEKS_PER_VISIT`, que vale 1 cuando cada visita ocurre en una semana distinta y disminuye al concentrarse.

### Población primaria de RQ2b

La especificación primaria se restringe a estudiantes con `V ≥ 3` **y calificación numérica final**. La razón es que `BV/RT/BA` pueden abandonar antes de terminar el semestre y, como no se observa la fecha exacta de baja, tendrían mecánicamente menos oportunidad de distribuir visitas a lo largo de cuatro meses. Los outcomes imputados se conservan como sensibilidad, no como análisis principal de regularidad.

Modelo principal:

`Z_complete_i = β_R R_i + fixed effects de intensidad + α_(profesor×periodo) + carrera + ε_i`.

La intensidad se controla de manera flexible mediante categorías de conteo `3, 4, 5, 6, 7, 8+`, y los errores estándar se agrupan por `profesor × periodo`. El parámetro de interés es `β_R`.

Además se reporta una comparación descriptiva especialmente limpia entre estudiantes con **exactamente tres visitas**: desempeño continuo según si esas tres visitas ocurrieron en uno, dos o tres meses calendario. Al fijar `V=3`, esa comparación elimina mecánicamente el número total de visitas como explicación, aunque sigue siendo observacional y puede reflejar organización/motivación no observada.

Hipótesis preespecificada:

`H2b: β_R > 0`.

La hipótesis rival es que una característica no observada —por ejemplo organización, motivación o percepción de dificultad— determine simultáneamente regularidad y desempeño; por ello, incluso un `β_R > 0` no se interpretará causalmente.

## Análisis longitudinal MU → Cálculo

Un análisis es **longitudinal** cuando la misma unidad —aquí, el mismo estudiante identificado por su ID— se observa en al menos dos momentos ordenados. Para cada estudiante `i`, se enlaza su primer intento real de MU en `t` con su primer intento posterior real de Cálculo en `t'>t`. Por ello, las visitas y el desempeño de MU son temporalmente anteriores a los outcomes de Cálculo.

Entre estudiantes que progresan posteriormente a `MAT1022 — Cálculo I`, se evalúa si el patrón de uso del CMAT durante MU predice la utilización posterior del CMAT en Cálculo. Una fila de la tabla longitudinal representa una transición del mismo estudiante, no dos muestras transversales independientes.

Esta temporalidad es útil pero **no identifica causalidad**: estudiantes con una propensión estable a pedir ayuda, mayor necesidad académica u otras características no observadas pueden asistir en ambos periodos.

La cohorte con cobertura CMAT en el primer Cálculo posterior contiene `N=4,211` estudiantes y es un subconjunto seleccionado de la cohorte completa de primer MU (`N=6,627`). Para el análisis de desempeño contemporáneo en MU, los 6,627 siguen siendo la población principal. Restringir retrospectivamente el análisis de MU a quienes en el futuro llegan a Cálculo condiciona en una variable posterior al periodo de MU, cambia el estimando y puede introducir sesgo de selección. Por eso se reportan ambos análisis explícitamente: cohorte completa y cohorte de progresores.

## Autoselección y alcance causal

La asistencia al CMAT es voluntaria. Actualmente no existen diagnóstico matemático, promedio de preparatoria, examen de admisión u otras medidas individuales pretratamiento. Solo se observan carrera y contexto académico/profesor-periodo.

Por tanto:

- los modelos con efectos fijos reducen heterogeneidad del contexto de evaluación;
- cualquier propensity weighting disponible solo ajusta desequilibrios **observados** y debe permanecer como sensibilidad;
- no se afirma que `V` cause `Z` sin un diseño adicional que identifique causalidad.

La autoselección por motivación, dificultad percibida, hábitos de estudio u otras variables no observadas sigue siendo una limitación central.

## Privacidad

El proyecto interno contiene identificadores originales. La carrera oficial utilizada en los modelos procede del registro académico del intento real de la materia. Las visitas del CMAT se enlazan a ese registro mediante el ID del estudiante; no es necesario tratar la carrera declarada en el formulario de visita como covariable basal.

Para compartir una versión de trabajo se implementa pseudonimización determinística mediante **HMAC-SHA256 con una llave secreta externa**, además de minimización de campos y eliminación/coarsening de información no necesaria. La llave nunca debe formar parte del ZIP compartido.

HMAC-SHA256 es pseudonimización y control de enlace, no anonimización absoluta. Carrera, periodo, secuencia curricular, calificaciones, fechas y combinaciones raras siguen siendo cuasi-identificadores. Para un release público, la opción de menor riesgo es **no publicar microdatos por estudiante**: liberar código, protocolo, tablas agregadas, figuras, hashes de integridad y, si se desea, datos sintéticos. Si alguna liberación de microdatos fuese institucionalmente autorizada, se requeriría evaluación formal de disclosure risk, eliminación de pseudónimos persistentes, generalización/supresión de celdas raras, coarsening temporal y control de acceso. No se debe prometer ``anonimato absoluto'' para un panel longitudinal rico.

## Abstract provisional

University mathematics support centers provide voluntary academic assistance, yet students' decisions to initiate and continue using these services may reflect both academic need and institutional incentives. This study examines the association between use of a Mathematics Learning Center and continuous academic performance among students taking their first attempt at an introductory university mathematics course at a private university in Mexico. In this setting, first-course students obtain a non-grade participation credit after reaching three visits to the center; any center visit during that academic term counts toward the threshold, while the incentive does not apply in the subsequent calculus course. Using linked administrative academic and support-center records, tutoring exposure is assigned only within the same academic term as the student's first course attempt. The primary outcome is continuous academic performance standardized within instructor-by-term evaluation contexts, while course passing is secondary. Students are additionally classified as non-users, limited users, students attending exactly to the three-visit threshold, and students continuing beyond the threshold. Calendar-day attendance is used to characterize same-day concentration, recurrent approximately monthly service-demand cycles, and whether visits are temporally distributed across the term. Students who progress to Calculus I are followed to characterize persistence of support use after the incentive no longer applies. Fixed-effects models, robust distributional comparisons, and sensitivity analyses for adverse non-numeric course outcomes are used to assess the stability of associations. Because no individual-level pre-course achievement covariates are currently available, the study explicitly retains an observational interpretation and treats self-selection into support use as a principal limitation.

*El abstract permanece sin resultados hasta congelar la especificación final.*
