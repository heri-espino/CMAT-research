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
