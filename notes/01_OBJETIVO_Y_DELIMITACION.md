# 01 — Objetivo y delimitación científica

## Qué artículo estamos preparando

**Estudio:** frecuencia de asistencia al Centro de Aprendizaje de Matemáticas (CMAT) y composición de los resultados académicos en Matemáticas Universitarias (MU). El contraste inicial `0 vs 1+` es el punto de partida, pero el interés del estudio es determinar **qué diferencias ajustadas pueden distinguirse entre frecuencias positivas** y si la asistencia se relaciona con distintas formas de no acreditar la asignatura.

**Título de trabajo registrado en `submission/METADATA.md`:** *Beyond First Attendance: Frequency of Mathematics Support Use and the Composition of Academic Outcomes*. El manuscrito de `paper/sections/01.tex` usa una variante más amplia que menciona incentivos y heterogeneidad; **hay que unificar el título**, no presuponer que ambos son definitivos.

**Pregunta central propuesta:** ¿cómo se relaciona la frecuencia registrada de uso de CMAT durante el periodo de MU con la calificación final ajustada al contexto docente, la probabilidad de aprobar y la composición de los resultados adversos, cuando se controla explícitamente la multiplicidad de comparaciones?

## Preguntas específicas

1. ¿Se reproduce la asociación entre cualquier visita y resultados más favorables frente a cero visitas?
2. Condicional a asistir alguna vez, ¿hay evidencia global de diferencias entre niveles de frecuencia?
3. ¿Qué pares difieren estadísticamente después de corrección Holm, y cómo cambian las conclusiones entre los modelos que incluyen cero visitas y los restringidos a usuarios?
4. ¿Qué ocurre alrededor de tres visitas, cifra vinculada al incentivo PPA durante parte del periodo observado, **sin** suponer una discontinuidad causal?
5. ¿Es distinta la composición entre fracaso numérico, baja voluntaria (BV), retiro temporal (RT) y baja académica (BA) según el uso registrado?
6. ¿Persisten las afirmaciones al reagrupar la cola en `6+`, cambiar el nivel de cluster, o restringir los resultados continuos a notas numéricas observadas?

## Contribución que sí podemos defender

- Analizar **participación inicial** y **frecuencia entre usuarios** como márgenes distintos.
- Evitar una lectura de «dosis-beneficio» visita por visita, reportando coeficientes, intervalos, pruebas globales y Holm.
- Poner en el mismo marco la calificación continua y PASS, que no contestan la misma pregunta.
- Separar los tipos de resultado adverso, en particular BV frente a fracaso numérico, sin atribuir motivaciones observadas a los estudiantes.
- Explicitar cómo un incentivo institucional de tres visitas **complica la interpretación de la exposición**.

## Qué NO investiga este paper

No estima una mejora individual antes y después de una tutoría; no dispone de asignación aleatoria a visitas, recomendación o profesor; no demuestra que cuatro visitas «causen» un cambio; no clasifica personalidades o motivaciones; no afirma que falta de significación implique equivalencia.

## Alcance editorial decidido hoy

**Holm es el método de inferencia múltiple del artículo. Los únicos outcomes principales son Z y PASS; el estudio se detiene en las comparaciones de frecuencia, sus ajustes y las sensibilidades relacionadas.**

**Fuente:** [contexto del proyecto](../paper/docs/project/PROJECT_CONTEXT.md), [plan analítico](../paper/docs/analysis/ANALYSIS_PLAN.md), [estado](../paper/docs/project/STATUS_AND_ROADMAP.md) y [metadatos de envío](../submission/METADATA.md).