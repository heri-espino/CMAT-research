# 08 — Revista, contribución y ruta de redacción

## Revista objetivo registrada

Los metadatos, plantilla y manuscrito actuales están orientados a **Teaching Mathematics and its Applications: An International Journal of the IMA (TEAMAT)**, revista del ámbito de enseñanza/aprendizaje de matemáticas en educación superior. Véanse `../submission/METADATA.md`, `../submission/README.md`, la clase `ima-authoring-template` en `../paper/sections/01.tex` y `../paper/README.md`.

**No confundir** con el objetivo de Paper 1 (`paper/paper1-ppa-persistence`), cuyo borrador apunta a *Studies in Higher Education*. Son artículos con distintas preguntas, revista y evidencia.

**Pendiente de verificar en fuente editorial vigente**: alcance de TEAMAT para una contribución metodológica observacional, límites de palabras, tipos de manuscrito, exigencia de anonimización, formato actual, declaraciones obligatorias, política sobre datos protegidos, IA y figuras. La presencia de la plantilla no demuestra que todas las políticas actuales estén cumplidas.

## Posicionamiento del paper para TEAMAT

Problema del campo: los centros de apoyo matemático utilizan registros de asistencia para evaluar alcance y rendimiento, pero «cualquier uso» oculta heterogeneidad de frecuencia y el registro final de «no-PASS» mezcla sucesos académicos diversos. Aporte: análisis de exposición categórica ordenada con variación entre contextos docentes, **familias explícitas de contrastes Holm** y una evaluación de cómo los resultados administrativos influyen en la interpretación.

Procurar que los resultados matemático-educativos predominen sobre la enumeración de todas las extensiones estadísticas disponibles. La mezcla gaussiana puede quedar como sensibilidad breve o suplemento **si** se considera que interrumpe el argumento de Holm; su eventual exclusión no debe borrar la evidencia ni presentarse como fallo del método.

## Estructura de reescritura propuesta (manuscrito en inglés)

1. **Introduction / related work.** Qué son los centros de apoyo; participación y selección; evidencia de resultados; diferencia entre iniciar asistencia y frecuentar; vacío de investigación y preguntas concretas.
2. **Institutional setting.** CMAT, registro por visita, MU y la opción PPA de tres visitas con cautelas temporales.
3. **Data, variables and sample.** N, grupos profesor–periodo, primer intento, exposición de periodo completo, PASS y Z/imputación, BA/BV/RT y selección.
4. **Statistical methods.** Efectos fijos, covarianza agrupada, benchmark, omnibus sólo usuarios, contrastes Wald y Holm con familias definidas; cronología de `6+` versus `7+`.
5. **Results — performance.** Perfil 0–7+, benchmark, omnibus/contrastes entre usuarios, sensibilidad de la cola, agrupación de varianza por profesor; presentar 7+ con su estatus exploratorio correcto.
6. **Results — outcome composition.** PASS/numérico/BV/RT/BA; modelos condicionados a no-PASS; distinción BV vs RT.
7. **Discussion.** Autoselección e incentivo, significado de una no-diferencia, otras explicaciones y valor para evaluación de centros de apoyo.
8. **Limitations / conclusion.** No causalidad, ausencia de línea basal homogénea, datos administrativos y aplicabilidad.
9. **Supplement (si conviene).** GMM, análisis detallados de cola y pruebas adicionales con cautela metodológica.

No es una orden de descartar las secciones existentes: [`paper/sections/01.tex`–`04.tex`](../paper/README.md) **ya contienen un draft extenso**. Primero hay que comparar el texto existente con la narrativa central de Holm y entonces reorganizarlo, preservando referencias y salidas verificadas.

## Figuras y tablas prioritarias (reutilizar outputs existentes)

- Tabla de tamaño y soporte de las frecuencias.
- Figura del perfil por visitas, sin sugerir continuidad causal.
- Matriz de efectos pareados en Z, con magnitud y marcas de Holm.
- Matriz equivalente de diferencias en PASS, en puntos porcentuales.
- Tabla legible de omnibus entre usuarios, familias de Holm y principales sensibilidades.
- Composición de los cinco tipos de outcome, destacando diferencia entre porcentajes globales y condicionales a no-PASS.

Evitar que heatmaps codifiquen sólo p-values; color debe representar la **magnitud/dirección de los efectos** y señales adicionales indican incertidumbre, como fija el protocolo original.

## Etapas antes de redactar la versión final

**A.** Congelar qué análisis será principal y cómo se describirá el resultado 7+ sin reescribir cronología. **B.** Verificar cada número y leyenda contra CSV. **C.** Resolver políticas históricas y declaraciones institucionales. **D.** Redactar versión inglesa clara, con cada afirmación de Results trazable a estimandos/tablas. **E.** Compilar clean y commented, revisar como referee y alinear envío TEAMAT.

**Fuentes:** [metadatos](../submission/METADATA.md), [paper actual](../paper/README.md), [roadmap](../paper/docs/project/STATUS_AND_ROADMAP.md), [análisis pre-outcome](../paper/docs/analysis/ANALYSIS_PLAN.md).