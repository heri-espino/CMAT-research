# Nuevo estudio CMAT

El análisis orientado a publicación se ejecuta con:

```bash
python src/run_study.py
```

En Windows también puede usarse `run_study.bat`. Los resultados quedan en `outputs/study/`.

## Diseño confirmado

- Cohorte principal: **primer intento** de `MAT1012 — Matemáticas Universitarias`.
- Una observación primaria por estudiante; si repite después, se conserva solamente el primer intento.
- Exposición primaria: **todas las visitas al CMAT durante el mismo periodo académico** del primer intento, porque esa es la regla real del PPA.
- PPA alcanzado: `V ≥ 3`; uso más allá del umbral: `V > 3`.
- Grupos descriptivos: `0`, `1–2`, `3`, `4+`.
- Outcome primario: desempeño continuo estandarizado dentro de `profesor × periodo`.
- Outcome secundario: aprobación/no aprobación con umbral 7.5.
- `BV/RT/BA`: resultados adversos; `EQV/REV/AC`: acreditaciones externas sin aula/profesor observado y se excluyen.
- Cálculo I se utiliza como comparación descriptiva sin PPA y como seguimiento longitudinal de persistencia.
- El calendario soporta Primavera, Verano y Otoño (periodos de cuatro meses), aunque las bases actuales contienen P/O.
- No existen actualmente covariables individuales de desempeño previo; la autoselección sigue siendo la principal limitación inferencial.


## Módulo temporal

El pipeline conserva `VISIT_DATE` (día calendario), además de día de la semana, mes y día del mes. Produce análisis de:

- estudiantes que concentran 2 o 3+ visitas en un mismo día;
- estudiantes cuyas primeras tres visitas —el umbral PPA— ocurren el mismo día;
- fecha en la que cada estudiante alcanza su tercera visita;
- días con mayor número de visitas y de estudiantes únicos;
- picos recurrentes de demanda por periodo y distribución de días entre picos.

Los picos no se etiquetan como exámenes sin un calendario oficial de evaluaciones.

## RQ2b — regularidad temporal y desempeño

El proyecto separa **intensidad** (cuántas visitas) de **regularidad temporal** (qué tan distribuidas están). La métrica principal es:

```text
REGULARITY_MONTHLY_4 = min(meses calendario activos, 4) / min(visitas totales, 4)
```

El análisis primario de regularidad usa estudiantes con al menos 3 visitas y **calificación numérica final**. Ajusta por conteo de visitas (3, 4, 5, 6, 7, 8+), efectos fijos profesor×periodo y carrera. Los casos `BV/RT/BA` se incluyen solo como sensibilidad para este subanálisis porque no conocemos su fecha exacta de baja y por tanto no sabemos cuánto tiempo tuvieron disponible para distribuir visitas.

También se calculan semanas activas, días activos, span primera–última visita, máxima proporción de visitas en un día, entropía semanal y número efectivo de semanas. Para estudiantes con exactamente 3 visitas se reporta desempeño según 1, 2 o 3 meses activos.

## Periodicidad mensual

Como los exámenes dependen del profesor, no se asignan fechas de examen individuales. Institucionalmente la mayoría realiza aproximadamente 4 evaluaciones, cerca de una por mes. El pipeline complementa la detección de picos con autocorrelación diaria ajustada por día de semana y periodograma restringido a ciclos de 21–42 días. Los resultados se describen como **compatibles con el ciclo de evaluación**, no como identificación causal de exámenes.

## Crear una copia pseudonimizada para compartir

No publique el ZIP interno: contiene datos originales. Para generar una copia separada con identificadores HMAC y minimización de datos:

```bash
# Genere una llave de al menos 32 caracteres y guárdela FUERA del ZIP público.
python -c "import secrets; print(secrets.token_hex(32))" > ../cmat_pseudonym_key.txt
python src/create_anonymized_release.py --key-file ../cmat_pseudonym_key.txt --output ../CMAT_publication_study_anonymized.zip
```

La llave **no** se incluye en el ZIP. No debe compartirse junto con una liberación pública. El proceso elimina nombres de asesores, texto de temas y la **hora exacta**. Conserva únicamente el **día calendario** de la visita porque es necesario para los análisis temporales y mantiene visitas múltiples del mismo día como eventos distintos.

La pseudonimización no equivale por sí sola a anonimato completo: carrera, periodo, calificación y patrones raros de asistencia pueden ser cuasi-identificadores. Antes de una publicación de microdatos se requiere revisión institucional de privacidad/ética.

## Análisis adicionales conservados en el borrador

La ejecución principal también genera una familia de resultados `80_*.csv` a `97_*.csv` y las figuras 11--14. Estos análisis son **aditivos**: no reemplazan la especificación primaria y se conservaron para decidir posteriormente qué elementos pasan al manuscrito final.

Incluyen:

- equivalencia formal TOST de exactamente 1 vs. 2 visitas con margen ±0.20 Z, además de Welch, Mann--Whitney, Brunner--Munzel y tamaños de efecto;
- ANOVA de Welch de las cohortes `0`, `1-2`, `3`, `4+`, diagnóstico Brown--Forsythe y post-hoc Games--Howell;
- asociación entre licenciatura y patrón de uso (chi-cuadrada + permutación cuando hay celdas esperadas pequeñas, Cramér V);
- Welch ANOVA y modelo cluster-robust de diferencias de Z por licenciatura;
- interacción exploratoria licenciatura × cohorte con errores agrupados por profesor-periodo;
- índice de rendimiento por número exacto de visitas 1--12, primero en Z del salón y después estandarizado dentro de la licenciatura; los IC de medias son t de Student y la tendencia se reporta tanto en 1--12 como en una sensibilidad que conserva solo conteos exactos con n≥20;
- tabla 2×2 de uso MU→Cálculo con probabilidades condicionales e IC Wilson, diferencia de riesgos con IC Newcombe--Wilson, riesgo relativo, odds ratio, Fisher, Pearson, phi y McNemar.

En todo el proyecto, `Z_GRADE_PRIMARY` se interpreta respecto a un **salón = profesor × misma materia × mismo periodo**. En la cohorte primaria de MAT1012 la materia está fija, de modo que `CLASSROOM_ID` equivale a profesor × periodo.

## Capítulo PPA1 → Cálculo (v8)

El pipeline genera ahora una cohorte longitudinal estricta para estudiar adopción y persistencia del CMAT bajo la suposición de que MU corresponde al primer semestre/PPA1 y Cálculo I al siguiente periodo regular sin el mismo incentivo CMAT de PPA1.

Los análisis se implementan en:

- `src/cmat_analysis/study/ppa_progression.py`
- `src/cmat_analysis/study/ppa_plots.py`

Las tablas nuevas comienzan en `98_...` y llegan a `114_...`; las figuras nuevas son `15_...` y `16_...`.

El capítulo LaTeX asociado vive en `ppa_progression_analysis.tex` y se incorpora de forma aditiva mediante `\input{ppa_progression_analysis}`. No reemplaza `new_section.tex`.
