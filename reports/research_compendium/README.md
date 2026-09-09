# Informe LaTeX CMAT - resultados v4

Este directorio contiene un borrador académico en LaTeX construido a partir de los resultados del pipeline `CMAT_publication_study_v4`.

Archivos principales:
- `informe_cmat.tex`: fuente LaTeX.
- `informe_cmat.pdf`: PDF compilado (26 páginas).
- `referencias.bib`: bibliografía inicial del proyecto en formato BibTeX para reutilización futura.
- `figures/`: figuras generadas por el pipeline v4 e incluidas en el informe.

El PDF actual usa una bibliografía manual dentro del `.tex` para poder compilar sin BibTeX. `referencias.bib` se conserva como archivo de trabajo para una versión futura del manuscrito.

Compilación:
```bash
pdflatex informe_cmat.tex
pdflatex informe_cmat.tex
```

El texto distingue explícitamente asociación de causalidad y presenta RQ1a, RQ1b, RQ2a, RQ2b y RQ3 con pregunta, respuesta empírica e interpretación.

## Sección aditiva de experimentos

El borrador principal se conserva sin recortar. Los experimentos añadidos en esta iteración están aislados en `new_section.tex` y se incorporan desde `informe_cmat.tex` mediante:

```tex
\input{new_section}
```

La sección documenta formalmente: (1) la justificación académica y estadística para agrupar exactamente 1 y 2 visitas, incluyendo TOST de equivalencia; (2) ANOVA de Welch de las cohortes `0`, `1--2`, `3`, `4+`, diagnóstico Brown--Forsythe, post hoc Games--Howell y una sensibilidad con errores agrupados por salón; y (3) la relación de licenciatura con uso del CMAT y con el desempeño Z relativo al salón, incluyendo una comprobación cluster-robust por profesor-periodo.

En todo el documento, un **salón** es profesor × misma materia × mismo periodo. En la cohorte de Matemáticas Universitarias la materia está fija, por lo que operacionalmente corresponde a profesor × periodo.

## Capítulo longitudinal PPA1 → Cálculo (v8)

El borrador sigue siendo acumulativo. No se eliminó `new_section.tex`. Se añadió un segundo archivo:

```tex
\input{ppa_progression_analysis}
```

`ppa_progression_analysis.tex` documenta el contexto administrativo PPA1/PPA2, la diferencia entre licenciatura oficial y licenciatura declarada en Google Forms, la auditoría de revalidaciones, la cohorte estricta MU-aprobado → Cálculo con calificación numérica, persistencia por grupos `0`, `1--2`, `3`, `4+`, el contraste `3` vs `4+`, modelos de persistencia, sensibilidad por materia específica, desempeño posterior `Z_Cálculo ~ Z_MU + patrón MU` y heterogeneidad por licenciatura.

El PDF compilado actual contiene 50 páginas. Para QA rutinario se valida compilación/log; no se requiere inspección visual página por página salvo problema de layout o petición explícita.
