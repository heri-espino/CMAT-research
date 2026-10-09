# 03 — Unidad de análisis, cohorte, variables y construcción de resultados

## Población y selección

Unidad: estudiante en su **primer intento elegible observado** de Matemáticas Universitarias (MU) durante un periodo con cobertura de CMAT. Se excluyen equivalencias, revalidaciones y otros registros administrativos que no representen una evaluación real dentro de un contexto profesor–periodo. No asumir que representa todos los estudiantes universitarios de UDLAP, a los que nunca cursaron MU o a cohortes fuera de la ventana observada.

- **N total:** 6,627 estudiantes.
- **Contextos de calificación:** 190 grupos de profesor × periodo académico.
- **Sin visitas:** 5,393.
- **Con al menos una visita:** 1,234.

| Visitas en el periodo | Estudiantes | Profesor-periodo con ese conteo |
|---|---:|---:|
| 0 | 5,393 | 190 |
| 1 | 517 | 152 |
| 2 | 245 | 114 |
| 3 | 170 | 84 |
| 4 | 96 | 69 |
| 5 | 55 | 40 |
| 6 exactas | 50 | 36 |
| 7+ | 101 | 57 |

El soporte es muy desigual: el grupo `7+` ya es una cola agrupada y exacto `6` es pequeño. Toda comparación ajustada requiere observar frecuencias comparables en contextos docentes comunes, no sólo suficientes estudiantes marginalmente.

## Especificaciones de frecuencia — cronología obligatoria

**Decisión previa a resultados:** `0 / 1 / 2 / 3 / 4 / 5 / 6+`, con `1 / 2 / 3 / 4 / 5 / 6+` para el modelo sólo entre usuarios. La auditoría de soporte identificó que distinguir `6` exactas de `7+` reduce el solapamiento mínimo entre pares adyacentes de **26 a 15** grupos profesor-periodo.

**Presentación posterior del manuscrito:** `0 / 1 / 2 / 3 / 4 / 5 / 6 / 7+`, conservando `6+` como análisis de sensibilidad. No renombrar la grilla más detallada como preregistrada ni cambiar retrospectivamente la agrupación por el contraste significativo de `7+`.

## Variables de exposición, ajuste y dependencia

- Exposición: número de visitas registradas durante todo el mismo periodo académico, incluso si el motivo/tópico de visita no fue MU.
- Ajuste: efectos fijos de `CLASSROOM_ID` (profesor × periodo), indicadores de `CLAVECARRERA` (programa/carrera).
- Incertidumbre primaria: errores estándar agrupados por profesor–periodo.
- Robustez: clustering por profesor para permitir correlación entre periodos impartidos por la misma persona.

Los modelos capturan asociaciones condicionadas por contexto observable, no eliminan autoselección ni diferencias de preparación matemática no medidas.

## Outcomes con significado distinto

**PASS**: 1 si la calificación numérica final es al menos **7.5**; 0 si es numérica menor a 7.5 o contiene **BA**, **BV** o **RT**. No se imputa una calificación numérica para calcular PASS.

**`Z_GRADE_PRIMARY`**: calificación final transformada a Z dentro de profesor–periodo, con una imputación numérica desfavorable, bajo el procedimiento canónico, para BA/BV/RT. Las notas numéricas originales se conservan. Este outcome es sensible a cómo se codifican los estados administrativos.

**Z numérico complete-case**: sólo estudiantes con calificación numérica observada, sin BA/BV/RT. No corresponde a la misma población condicionada que la variable continua imputada; su uso debe dejar claro el posible sesgo de selección.


## Ausencias relevantes

No se observan mejoras individuales pre/post ni se registra preparación inicial completa, motivación, duración de tutoría o cronología exacta de retiros. La variable PASS trata BA/BV/RT como no acreditación y la continua usa la imputación canónica; no se formulan inferencias independientes sobre tipos de retiro.
