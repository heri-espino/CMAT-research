# Supuestos administrativos — confirmados

Estas definiciones quedaron confirmadas el 29 de agosto de 2026 y están implementadas en el pipeline.

1. **PPA:** el punto se obtiene al alcanzar **≥3 visitas**.
2. **Visitas elegibles para PPA:** cuentan **tres visitas cualesquiera al CMAT** durante el periodo del **primer intento de Matemáticas Universitarias**, no únicamente asesorías etiquetadas como esa materia.
3. **Unidad de visita:** cada fila del archivo de asesorías representa una visita independiente, incluso si un estudiante tiene varias el mismo día.
4. **Aprobación:** la calificación mínima aprobatoria es **7.5**.
5. **Estados académicos:** `BV`, `RT` y `BA` se consideran resultados adversos y, para el outcome continuo, se asume una calificación latente menor de 7.5. `EQV`, `REV` y `AC` indican que el estudiante acreditó la materia fuera del aula/profesor observado; se excluyen porque no se observa el contexto de evaluación comparable.
6. **Fecha de baja:** no está disponible. Se acepta contar las visitas del mismo periodo académico sin truncar el conteo en una fecha individual de baja.
7. **Cobertura de asesorías:** el archivo disponible llega de 2019-P a 2024-P; periodos académicos sin cobertura se excluyen de la inferencia primaria de exposición.
8. **Periodos:** la universidad utiliza periodos de cuatro meses: **Primavera, Verano y Otoño**. En los archivos actuales aparecen `P` y `O`; el código también soporta `V = Verano` para futuras bases.
9. **Covariables previas:** actualmente no se dispone de diagnóstico matemático, promedio de preparatoria, examen de admisión u otra medida individual pretratamiento. Por ello el ajuste de selección observado es limitado y no debe presentarse como identificación causal.
10. **Privacidad:** antes de compartir datos se deben pseudonimizar identificadores. El proyecto incluye `src/create_anonymized_release.py`, que usa HMAC-SHA256 con una llave secreta externa al ZIP. Para permitir el análisis temporal conserva el **día calendario** de cada asesoría, pero elimina la hora exacta, nombres y texto libre. Esto es pseudonimización, no garantía automática de anonimato; una liberación pública requiere revisión institucional por riesgo de reidentificación mediante cuasi-identificadores.
