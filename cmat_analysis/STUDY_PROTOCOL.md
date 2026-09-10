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

El outcome principal es la calificación final continua, estandarizada dentro de `profesor × periodo`:

`Z_i = (Y_i - media_del_contexto) / sd_del_contexto`.

### BV / RT / BA

Administrativamente se asume que estos estados corresponden a un resultado adverso con desempeño inferior al umbral aprobatorio de 7.5. Como no se observa una nota numérica exacta, el análisis continuo principal imputa valores por debajo de 7.5 dentro del contexto profesor-periodo y estandariza después.

Sensibilidades preespecificadas:

1. imputación uniforme bajo 7.5;
2. análisis únicamente de calificaciones numéricas.

La estabilidad de signo/magnitud entre estas especificaciones es más importante que una única imputación puntual.

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

- descriptivos e IC95% por `0`, `1–2`, `3`, `4+`;
- contraste `V>3` vs `V≤3` con Welch, Mann–Whitney, Brunner–Munzel, probabilidad de superioridad, correlación biserial por rangos y Cliff's delta;
- OLS con efectos fijos `profesor × periodo` y errores estándar agrupados por ese mismo contexto;
- especificación adicional con carrera;
- sensibilidades de imputación.

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

## RQ3 — persistencia longitudinal

Entre estudiantes que progresan posteriormente a `MAT1022 — Cálculo I`, ¿el patrón de uso del CMAT durante Matemáticas Universitarias predice la utilización del CMAT en el primer intento posterior de Cálculo, cuando ya no existe el PPA?

Se reporta explícitamente como análisis condicionado a quienes progresan a Cálculo; no se generaliza esa subcohorte a todos los alumnos que iniciaron Matemáticas Universitarias.

## Autoselección y alcance causal

La asistencia al CMAT es voluntaria. Actualmente no existen diagnóstico matemático, promedio de preparatoria, examen de admisión u otras medidas individuales pretratamiento. Solo se observan carrera y contexto académico/profesor-periodo.

Por tanto:

- los modelos con efectos fijos reducen heterogeneidad del contexto de evaluación;
- cualquier propensity weighting disponible solo ajusta desequilibrios **observados** y debe permanecer como sensibilidad;
- no se afirma que `V` cause `Z` sin un diseño adicional que identifique causalidad.

La autoselección por motivación, dificultad percibida, hábitos de estudio u otras variables no observadas sigue siendo una limitación central.

## Privacidad

El proyecto interno contiene identificadores originales. Para compartir una versión de trabajo se implementa pseudonimización determinística mediante **HMAC-SHA256 con una llave secreta externa**, además de minimización de campos y eliminación/coarsening de información no necesaria. Para reproducir el análisis temporal, la versión pseudonimizada conserva la **fecha calendario (día)** de la asesoría, pero elimina la hora exacta.

La llave nunca debe formar parte del ZIP compartido. Hashing/pseudonimización no garantiza anonimato completo: carrera, periodo, calificación y combinaciones raras pueden actuar como cuasi-identificadores. Una liberación pública de microdatos debe pasar por revisión institucional de privacidad/ética.

## Abstract provisional

University mathematics support centers provide voluntary academic assistance, yet students' decisions to initiate and continue using these services may reflect both academic need and institutional incentives. This study examines the association between use of a Mathematics Learning Center and continuous academic performance among students taking their first attempt at an introductory university mathematics course at a private university in Mexico. In this setting, first-course students obtain a non-grade participation credit after reaching three visits to the center; any center visit during that academic term counts toward the threshold, while the incentive does not apply in the subsequent calculus course. Using linked administrative academic and support-center records, tutoring exposure is assigned only within the same academic term as the student's first course attempt. The primary outcome is continuous academic performance standardized within instructor-by-term evaluation contexts, while course passing is secondary. Students are additionally classified as non-users, limited users, students attending exactly to the three-visit threshold, and students continuing beyond the threshold. Calendar-day attendance is used to characterize same-day concentration, recurrent approximately monthly service-demand cycles, and whether visits are temporally distributed across the term. Students who progress to Calculus I are followed to characterize persistence of support use after the incentive no longer applies. Fixed-effects models, robust distributional comparisons, and sensitivity analyses for adverse non-numeric course outcomes are used to assess the stability of associations. Because no individual-level pre-course achievement covariates are currently available, the study explicitly retains an observational interpretation and treats self-selection into support use as a principal limitation.

*El abstract permanece sin resultados hasta congelar la especificación final.*

## Análisis exploratorios adicionales del borrador (no sustituyen el protocolo primario)

Mientras el documento permanezca en fase de recopilación, se conservan análisis adicionales para decidir la especificación final. Se justifica el grupo 1--2 tanto por el significado institucional (ambos niveles están por debajo de PPA) como por equivalencia TOST de su outcome continuo usando un margen de ±0.20 Z. Las cuatro cohortes se comparan mediante ANOVA de Welch y Games--Howell debido a heterogeneidad de varianzas.

La licenciatura se estudia en dos dimensiones: asociación con utilización del CMAT y diferencias en la media de Z respecto al salón. Para inferencia omnibus se requieren al menos 30 estudiantes por programa; las interacciones carrera×cohorte se restringen adicionalmente a programas con al menos 100 estudiantes y al menos 5 observaciones en cada cohorte. Los modelos complementarios usan covarianza cluster-robust por profesor-periodo.

Para visitas exactas 1--12 se construye un índice relativo a licenciatura. Dado que Z ya es el número de desviaciones estándar respecto al salón, se realiza una segunda estandarización dentro de carrera, `R=(Z-media_carrera)/sd_carrera`, y se resume `E[R|V=v]`. Los conteos altos con n<20 se marcan explícitamente como inestables.

La persistencia individual MU→Cálculo se analiza como una tabla 2×2 de cualquier visita/no visita y se reportan probabilidades condicionales, diferencia de riesgos, RR, OR, Fisher/Pearson y phi. McNemar se reporta por separado porque responde a una pregunta distinta: cambio marginal de prevalencia entre cursos en los mismos estudiantes.

---

## Actualización v8 — arquitectura longitudinal PPA1 → Cálculo

Esta actualización es **aditiva** y no elimina los análisis anteriores. Para las preguntas específicas sobre incentivo y persistencia se define una cohorte más estrecha.

### Contexto administrativo fijado

- CMAT atiende libremente a estudiantes vigentes de licenciatura en matemáticas y estadística, desde cursos básicos hasta avanzados.
- Cada fila de asesoría corresponde a un registro de Google Forms capturado por estudiantes de servicio social/becario. Se asume que el registro representa una visita real, aunque existe posible error humano/duplicación.
- Varias visitas el mismo día son administrativamente plausibles porque los profesores se relevan por bloques de horario; no se interpretan automáticamente como manipulación.
- Todos los asesores son profesores.
- PPA1 se trata como requisito de participación de primer semestre; PPA2 corresponde al segundo semestre y no se considera el mismo incentivo CMAT de PPA1.
- Suposición del estudio: el estudiante típico cumple PPA1 en su primer semestre, por lo que MU representa el contexto PPA1 y Cálculo I el periodo posterior sin ese mismo incentivo CMAT.
- El umbral operacional conservado para el análisis es **3 registros CMAT durante MU**. El estudio no intenta inferir cuántos puntos PPA1 exactos recibió cada estudiante ni su motivación psicológica individual.

### Dos fuentes de licenciatura

1. `CLAVECARRERA`: registro académico oficial asociado al intento de materia.
2. `carrera`: licenciatura declarada en el Google Form de cada asesoría.

El segundo campo solo existe para usuarios del CMAT, por lo que no debe usarse como covariable basal para comparar usuarios y no usuarios. El campo oficial se usa en modelos; el campo del formulario se conserva como descripción contemporánea y para un crosswalk observado.

### Revalidaciones

El extracto oficial puede replicar una materia ya aprobada cuando se acredita para otra licenciatura. El pipeline conserva un audit previo a excluir filas sin profesor y marca:

- `real_attempt_candidate`;
- `likely_post_pass_revalidation`;
- `likely_same_period_career_replication`;
- `administrative_non_attempt`.

Una fila posterior a una aprobación previa del mismo curso no se interpreta como nuevo intento. Estas banderas son reglas administrativas conservadoras, no variables oficiales proporcionadas por la universidad.

### Cohorte primaria PPA1–Cálculo

Se requiere:

1. primer intento real de MU;
2. aprobación numérica de ese primer intento (`>=7.5`);
3. primer Cálculo I real posterior;
4. calificación numérica de Cálculo;
5. cobertura de asesorías en ambos periodos;
6. Z válido en ambos salones;
7. Cálculo en el siguiente periodo regular Primavera/Otoño.

La sensibilidad permite cualquier primer Cálculo posterior.

### Z-score del capítulo v8

Para cada materia:

`salón = profesor × misma materia × mismo periodo`.

El Z de MU y Cálculo se calcula usando como referencia **todas las calificaciones numéricas de intentos reales candidatos del salón**, no solamente la subcohorte longitudinal:

`Z = (calificación - media_salon) / sd_salon`.

### Preguntas v8

- ¿Cómo cambia `P(uso CMAT en Cálculo | grupo de visitas MU)` entre `0`, `1–2`, `3`, `4+`?
- ¿Exactamente 3 difiere de 4+ en persistencia posterior?
- ¿La relación con persistencia se aplana después del umbral de 3?
- ¿Se conserva la asociación usando visitas etiquetadas específicamente como MU y Cálculo?
- ¿El patrón de uso en MU predice `Z_Cálculo` después de condicionar por `Z_MU`, licenciatura y periodo?
- ¿La licenciatura explica heterogeneidad adicional en persistencia y en `ΔZ = Z_Cálculo - Z_MU`?

Ninguna de estas preguntas convierte el umbral de tres visitas en un diseño de regresión discontinua; el estudiante controla el número de visitas.
