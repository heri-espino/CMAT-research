# Paper 2.1 — cuaderno de investigación previo a la reescritura

**Rama:** `paper/paper2.1-visit-frequency` · **Fecha de apertura:** 2026-10-09 · **Idioma de trabajo:** español; manuscrito previsto en inglés.

Este directorio es la **memoria editorial y científica de Paper 2.1**, cuya estrategia principal vuelve a ser el análisis de frecuencias con efectos fijos, contrastes Wald y corrección múltiple de Holm. No es un conjunto de resultados recién calculados, no sustituye los archivos de procedencia y **no autoriza a convertir las asociaciones observadas en efectos causales**.

**Aclaración de portafolio:** Paper 1 (`paper/paper1-ppa-persistence`) estudia persistencia del uso después del incentivo PPA y es otra rama. La decisión de «quedarnos con Holm» pertenece a Paper 2.1, que es el manuscrito de frecuencia de asistencia que queremos priorizar ahora. Si se decide unificarlo con Paper 2 o renumerar las publicaciones, se documentará antes de mover archivos.

## Ruta de lectura para cualquier agente nuevo

1. [Propósito, preguntas, límites y decisión de alcance](01_OBJETIVO_Y_DELIMITACION.md).
2. [Qué es CMAT y su contexto institucional](02_CMAT_Y_CONTEXTO.md).
3. [Cohorte, exposición, resultados y comparabilidad](03_DATOS_Y_VARIABLES.md).
4. [Diseño estadístico, Holm y familias de contrastes](04_METODOLOGIA_HOLM.md).
5. [Resultados comprobables y divergencias entre especificaciones](05_RESULTADOS_Y_PROCEDENCIA.md).
6. [Interpretación, argumentos y explicaciones alternativas](06_INTERPRETACION.md).
7. [Literatura, estado del arte y vacío que aborda el artículo](07_LITERATURA_Y_GAP.md).
8. [Revista objetivo y estrategia de redacción](08_JOURNAL_Y_PLAN_DE_MANUSCRITO.md).
9. [Pendientes, decisiones científicas y criterios de cierre](09_DECISIONES_Y_PENDIENTES.md).
10. [Matriz de afirmaciones y fuentes verificables](10_MATRIZ_DE_AFIRMACIONES.md).

## Documentos originales — fuente de verdad

- `../paper/docs/analysis/ANALYSIS_PLAN.md`, `OUTCOME_FRAMEWORK.md`, `VISIT_GROUPING_DECISION.md`.
- `../paper/docs/results/PRELIMINARY_RESULTS.md` y `MIXTURE_ANALYSIS_RESULTS.md`.
- `../paper/docs/interpretation/ACADEMIC_MANAGEMENT_HYPOTHESIS.md`.
- `../paper/docs/project/PROJECT_CONTEXT.md` y `STATUS_AND_ROADMAP.md`.
- `../literature_selected/READING_GUIDE.md`, `ACCESS_NOTES.md`, `../paper/references.bib`.
- `../submission/METADATA.md`, `../paper/sections/01.tex` a `04.tex`.
- Datos agregados canónicos en `../results/paper21/`; código de ejecución en `../code/`; funciones reutilizables en `../cmat_analysis/`.

Las cifras de estas notas son **transcripciones resumidas** de esos registros y se deben verificar nuevamente contra tablas exportadas antes de actualizar el manuscrito. Si hay una discrepancia, mantenerla visible y documentar cuál especificación la produce; no «corregir» números por intuición.

## Reglas de edición

Registrar siempre: **observado / interpretación / hipótesis / decisión / por verificar**. No cambiar decisiones históricas como si hubieran sido tomadas antes de mirar resultados. Separar explícitamente las familias de contrastes de Holm y distinguir el análisis entre usuarios del modelo con cero visitas incluido. No llamar equivalentes a dos grupos sólo porque su contraste no fue significativo. No inventar definiciones administrativas, políticas universitarias históricas, aprobación ética, especificaciones de la revista ni cifras no disponibles.

Las notas no deben contener datos individuales, pseudónimos de estudiantes, tablas de baja frecuencia que permitan identificación ni claves. El `main` de este repositorio aloja recursos reutilizables; esta carpeta es **exclusiva de la rama del paper**.

**Estado:** documentación inicial recopilada de fuentes existentes; no se ha reejecutado la investigación ni se ha modificado el texto del artículo en esta fase.