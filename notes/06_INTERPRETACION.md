# 06 — Interpretación científica: lo que se desprende y lo que no

## Argumento principal (propuesto, pendiente de edición)

**El uso registrado de CMAT tiene una fuerte separación observacional entre ausencia de visitas y cualquier asistencia, pero la frecuencia posterior no puede leerse como una escalera monotónica de resultados mejores.** El estudio añade que el concepto de «no aprobar» encierra situaciones distintas: fracaso con calificación numérica, BV, RT y BA.

Este argumento permite describir a CMAT y su uso sin convertir resultados de asociaciones ajustadas en afirmaciones causales. Las comparaciones entre usuarios, el contexto PPA y la composición de resultados son necesarios para interpretar el benchmark `0 vs 1+`; no son tres papers independientes forzados a compartir una introducción.

## Lectura de cada conjunto de resultados

**Separación inicial:** +0.361 DE en Z y +15.3 pp en PASS sugieren una diferencia considerable de desempeño final observada entre asistentes y no asistentes, incluso dentro de profesor–periodo y carrera. No se observa el desempeño contrafactual de cada estudiante; preparación basal, dificultad, motivación, tiempo disponible y recomendación docente pueden afectar asistencia y outcomes simultáneamente.

**Frecuencia entre usuarios:** en la grilla fijada `1/2/3/4/5/6+` no hay contraste positivo Holm-significativo, lo que indica **insuficiente evidencia para distinguir claramente pares** con esta precisión, no «equivalencia» ni «ausencia de asociación». La cola es escasa y la sensibilidad por profesor sí admite un contraste amplio `1` vs `6+` en PASS. El resultado `7+` vs `1` de la grilla completa es interesante, pero debe explicitarse su familia, el soporte y que la resolución de cola fue posterior al soporte auditado.

**PPA a tres visitas:** es una frontera de incentivos potenciales, no un corte causal. En la comparación adyacente 2–3 no se observa una discontinuidad académica robusta. Si la idea de «visitas mayores a tres» se usa, explicar que exceden esa opción de actividad, sin asegurar ausencia de otros incentivos o motivos.

**Estados adversos:** la diferencia condicionada entre BV y fracaso numérico puede ser compatible con diferencias de navegación institucional, contacto con profesores o gestión académica; **no mide** ese mecanismo. RT no presenta el mismo patrón y BA es muy infrecuente entre usuarios. La tasa de retiros administrativos agregados es incluso **menor** entre usuarios que entre no usuarios: no escribir que «los usuarios se retiran más» por confundir tasas absolutas y proporciones condicionadas a no-PASS.

**Imputación:** una parte de la estructura de cola inferior del Z proviene de cómo se representan resultados no numéricos. Los modelos sólo con notas observadas son una comprobación distinta, que cambia la población analizada. Las mezclas gaussianas pueden explorar forma, pero no permiten inferir «dos clases de estudiantes».

## Hipótesis alternativas abiertas

- Preparación matemática previa y diagnóstico de entrada.
- Solicitud de apoyo por experimentar dificultad, no sólo por alto compromiso.
- Variación en profesor, carrera, horario y acceso material al centro.
- Incentivo PPA, recomendaciones docentes u otros requisitos institucionales.
- Menor tiempo para acumular visitas si un resultado administrativo se produce antes de cerrar el periodo.
- Composición por cohortes y normas de calificación; la estandarización no elimina toda heterogeneidad.

## Redacción recomendada / redacción que debe evitarse

| Preferible | Evitar |
|---|---|
| “Students with recorded CMAT attendance had higher adjusted final performance.” | “CMAT improved students’ performance.” |
| “Positive-frequency contrasts were not distinguishable after Holm adjustment.” | “More than one visit makes no difference.” |
| “The PPA threshold contextualises attendance counts.” | “Three visits causally change performance.” |
| “The BV-versus-numeric-failure composition was different conditional on non-PASS.” | “CMAT teaches students to withdraw strategically.” |
| “The imputed score distribution showed mixture-like features.” | “There are two types of students.” |

## Punto central de interpretación y tensión pendiente

La narrativa «ningún par positivo es diferente» es **demasiado fuerte** si se omite el hallazgo `7+` vs `1` con Holm en la familia completa y la sensibilidad `6+` vs `1` agrupada por profesor. Propuesta: enfatizar que **no existe evidencia robusta de una secuencia adyacente monotónica**, pero reconocer explícitamente señales de contraste entre asistencia baja y alta que dependen de especificación, ajuste y soporte.

**Fuentes:** [resultados](../paper/docs/results/PRELIMINARY_RESULTS.md), [hipótesis de gestión académica](../paper/docs/interpretation/ACADEMIC_MANAGEMENT_HYPOTHESIS.md), [nota sobre retiros](../paper/docs/interpretation/ADMINISTRATIVE_OUTCOME_NOTE.md), [cronología de grupos](../paper/docs/analysis/VISIT_GROUPING_DECISION.md).