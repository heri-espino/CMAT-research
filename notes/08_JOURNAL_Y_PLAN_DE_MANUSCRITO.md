# 08 — Revista, contribución y ruta de redacción

## Revista objetivo registrada

Los metadatos, plantilla y manuscrito actuales están orientados a **Teaching Mathematics and its Applications: An International Journal of the IMA (TEAMAT)**, revista del ámbito de enseñanza/aprendizaje de matemáticas en educación superior. Véanse `../submission/METADATA.md`, `../submission/README.md`, la clase `ima-authoring-template` en `../paper/sections/01.tex` y `../paper/README.md`.

**No confundir** con el objetivo de Paper 1 (`paper/paper1-ppa-persistence`), cuyo borrador apunta a *Studies in Higher Education*. Son artículos con distintas preguntas, revista y evidencia.

**Pendiente de verificar en fuente editorial vigente**: alcance de TEAMAT para una contribución metodológica observacional, límites de palabras, tipos de manuscrito, exigencia de anonimización, formato actual, declaraciones obligatorias, política sobre datos protegidos, IA y figuras. La presencia de la plantilla no demuestra que todas las políticas actuales estén cumplidas.

## Opciones editoriales si no se envía a TEAMAT (revisión 2026-10-12)

La orientación metodológica del manuscrito sigue siendo **Wald/Holm** para Z y PASS, pero el aporte educativo debe presentarse como un problema de interpretación de los registros de apoyo matemático, particularmente cuando conviven asistencia voluntaria e incentivos de **integración social y cultural de primer semestre**. La opción CMAT de **tres visitas PPA1 permaneció vigente en toda la ventana** del análisis; no se ha identificado su efecto ni se conoce la elegibilidad individual.

| Revista | Ajuste al manuscrito | Adaptación antes de enviar | Alcance/editorial |
|---|---|---|---|
| **PRIMUS (Problems, Resources, and Issues in Mathematics Undergraduate Studies)** | **Primera alternativa** por educación matemática universitaria y evaluación de programas docentes de varios cursos | Hacer explícita la implicación transferible para coordinadores de centros, moderar el énfasis en p-values y explicar la combinación de apoyo e incentivos | [Aims & Scope](https://www.tandfonline.com/action/journalInformation?journalCode=upri20&show=aimsScope): exige idea/evidencia novedosa y transferibilidad, evaluación de iniciativas/programas |
| **International Journal of Mathematical Education in Science and Technology (IJMEST)** | Alternativa disciplinar con audiencia amplia de educación matemática y transferencia a docencia universitaria | Fortalecer la aportación a pedagogía de matemáticas, la comparación con programas previos y límites de inferencia; no presentarlo como estadística sin aplicación didáctica | [Aims & Scope](https://www.tandfonline.com/action/journalInformation?journalCode=tmes20&show=aimsScope): vínculo explícito con educación y pedagogía |
| **Journal of Learning Development in Higher Education (JLDHE)** | Opción interdisciplinaria si se reescribe en torno a acceso y desarrollo del aprendizaje en servicios institucionales | Requiere conexión teórica sustantiva con *learning development* y generalización entre disciplinas, no sólo una evaluación descriptiva de una iniciativa local | [About](https://jldhe.aldinhe.ac.uk/about/): rechaza evaluaciones locales sin fundamentación teórica y desalienta tecnicismo estadístico excesivo |
| **Journal of University Teaching and Learning Practice (JUTLP)** | Alternativa generalista si la pregunta pasa a políticas universitarias de apoyo/participación | Necesita consecuencias concretas para la práctica de enseñanza/aprendizaje, más allá de correlaciones entre visitas y notas | [About](https://open-publishing.org/journals/index.php/jutlp/about): investigación bien diseñada y resultados que cambian prácticas universitarias |

**Costos (según páginas editoriales consultadas):** PRIMUS e IJMEST admiten publicación convencional sin APC y acceso abierto opcional con APC; JLDHE indica acceso abierto sin tasa de envío ni APC. Los costos, instrucciones de envío y criterios editoriales deben reconfirmarse cuando se decida enviar.

**Selección propuesta:** mantener TEAMAT como primera opción actual; si no fuera viable, **PRIMUS** como alternativa más directa al enfoque matemáticas universitarias, seguido de **IJMEST**. JLDHE sería adecuado únicamente tras una reorientación considerable hacia *learning development*. Ninguna revista garantiza aceptación.

**Diferenciación frente al trabajo previo:** Jacob y Ní Fhloinn (2019) y Rickard y Mills (2018) ya analizan frecuencia de visitas y desempeño; por tanto el artículo **no** es el primero en estudiar una relación dosis-respuesta ni presenta Holm como método nuevo. La aportación defendible es evaluar **cuánta resolución entre frecuencias** permite una cohorte académica determinada, preservando familias de comparaciones y el contexto de un incentivo institucional **no académico**, sin convertir los cortes visuales en cuatro grupos contrastados.

## Posicionamiento del paper para TEAMAT

Problema del campo: los centros de apoyo matemático utilizan registros de asistencia para evaluar alcance y rendimiento, pero «cualquier uso» oculta heterogeneidad de frecuencia y el registro final de «no-PASS» mezcla sucesos académicos diversos. Aporte: análisis de exposición categórica ordenada con variación entre contextos docentes, **familias explícitas de contrastes Holm** y una evaluación de cómo los resultados administrativos influyen en la interpretación.


## Estructura de reescritura propuesta (manuscrito en inglés)

1. **Introduction / related work.** Qué son los centros de apoyo; participación y selección; evidencia de resultados; diferencia entre iniciar asistencia y frecuentar; vacío de investigación y preguntas concretas.
2. **Institutional setting.** CMAT, registro por visita, MU y PPA1 como programa de integración social/cultural de primer semestre, opción de tres visitas a CMAT vigente durante toda la ventana, y cautela sobre elegibilidad individual no observada.
3. **Data, variables and sample.** N, grupos profesor–periodo, primer intento, exposición de periodo completo, PASS y Z/imputación, BA/BV/RT y selección.
4. **Statistical methods.** Efectos fijos, covarianza agrupada, benchmark, omnibus sólo usuarios, contrastes Wald y Holm con familias definidas; cronología de `6+` versus `7+`.
5. **Results — performance.** Perfil 0–7+, benchmark, omnibus/contrastes entre usuarios, sensibilidad de la cola, agrupación de varianza por profesor; presentar 7+ con su estatus exploratorio correcto.
6. **Results — sensitivity.** Agrupación por profesor, cola de asistencia y outcome numérico observado.
7. **Discussion.** Autoselección e incentivo, significado de una no-diferencia, otras explicaciones y valor para evaluación de centros de apoyo.
8. **Limitations / conclusion.** No causalidad, ausencia de línea basal homogénea, datos administrativos y aplicabilidad.

No es una orden de descartar las secciones existentes: [`paper/sections/01.tex`–`04.tex`](../paper/README.md) **ya contienen un draft extenso**. Primero hay que comparar el texto existente con la narrativa central de Holm y entonces reorganizarlo, preservando referencias y salidas verificadas.

## Figuras y tablas prioritarias (reutilizar outputs existentes)

- Tabla de tamaño y soporte de las frecuencias.
- Figura del perfil por visitas, sin sugerir continuidad causal.
- Matriz de efectos pareados en Z, con magnitud y marcas de Holm.
- Matriz equivalente de diferencias en PASS, en puntos porcentuales.
- Tabla legible de omnibus entre usuarios, familias de Holm y principales sensibilidades.

Evitar que heatmaps codifiquen sólo p-values; color debe representar la **magnitud/dirección de los efectos** y señales adicionales indican incertidumbre, como fija el protocolo original.

## Etapas antes de redactar la versión final

**A.** Congelar qué análisis será principal y cómo se describirá el resultado 7+ sin reescribir cronología. **B.** Verificar cada número y leyenda contra CSV. **C.** Resolver políticas históricas y declaraciones institucionales. **D.** Redactar versión inglesa clara, con cada afirmación de Results trazable a estimandos/tablas. **E.** Compilar clean y commented, revisar como referee y alinear envío TEAMAT.

**Fuentes:** [metadatos](../submission/METADATA.md), [paper actual](../paper/README.md), [roadmap](../paper/docs/project/STATUS_AND_ROADMAP.md), [análisis pre-outcome](../paper/docs/analysis/ANALYSIS_PLAN.md).