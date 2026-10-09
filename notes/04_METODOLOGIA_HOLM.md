# 04 — Contrastes Wald, efectos fijos y ajuste Holm

## Estrategia estadística principal: Wald y Holm

La comparación inicial `0 vs 1+` es un benchmark; la pregunta de frecuencia se evalúa **entre usuarios (`K>=1`)**. Para cada uno de los outcomes principales:

- **Z continuo:** OLS con indicadores de frecuencia, efectos fijos de profesor–periodo y controles de carrera. Los coeficientes/contrastes se expresan en desviaciones estándar del resultado canónico.
- **PASS:** modelo lineal de probabilidad con los mismos controles; sus contrastes se expresan en **puntos porcentuales**, no como riesgos relativos ni odds ratios. Logit se puede reportar como sensibilidad claramente diferenciada.
- **Varianza:** estimación robusta agrupada a nivel profesor–periodo, con una sensibilidad de clustering por profesor.
- **Prueba global (omnibus):** contrastar la hipótesis conjunta de igualdad de los niveles ajustados entre las frecuencias positivas. Su valor p no sustituye ni resume por sí solo la incertidumbre de contrastes individuales.
- **Contrastes Wald:** comparar cada pareja de grupos a partir de las diferencias de coeficientes y la matriz de covarianza cluster-robust; reportar diferencia, SE, IC del 95%, valor p sin ajuste y valor p con Holm.

## Qué controla Holm

Para una familia de `m` contrastes previamente definida, ordenar los valores p `p_(1) <= ... <= p_(m)` y compararlos secuencialmente con niveles `alpha/(m-j+1)` (equivalente a comunicar valores p ajustados por el procedimiento escalonado de Holm). El control del **family-wise error rate** responde a la multiplicidad de comparaciones dentro de esa familia cuando sus pruebas individuales están bien calibradas; no corrige autoselección, especificación errónea, múltiples decisiones exploratorias fuera de familia ni incertidumbre causal.

Familias que deben **permanecer distintas**, según pregunta y diseño:

| Diseño | Categorías | Pares posibles | Estatus interpretativo |
|---|---|---:|---|
| Entre usuarios, agrupación pre-outcome | 1/2/3/4/5/6+ | 15 por outcome | Especificación originalmente soportada |
| Entre usuarios, 6 separado de 7+ | 1/2/3/4/5/6/7+ | 21 por outcome | Sensibilidad/exploración posterior |
| Modelo que incluye no usuarios | 0/1/2/3/4/5/6/7+ | 28 por outcome | Perfil completo de manuscrito; no equiparar con prueba entre usuarios |
| Benchmark simple | 0 frente a 1+ | 1 por outcome | Puente con Paper 2; contraste conceptualmente separado |

No unir retrospectivamente los `m=15`, `m=21` y `m=28` valores p en una sola familia sin una justificación explícita. Los contrastes con números idénticos de visitas pero con **muestras y controles diferentes** tampoco se pueden tratar como el mismo resultado.

## Particular atención al caso 7+ y a los resultados entre usuarios

Los registros existentes muestran **7+ frente a 1 visita en PASS = +14.5 pp, p-Holm 0.0206** bajo el **modelo completo de ocho grupos**. En cambio, el análisis restringido a usuarios con la grilla detallada tiene prueba global PASS `p=0.102`, y el documento de resultados indica que **ningún contraste de esa sensibilidad sobrevive Holm**. Los dos hallazgos no se deben amalgamar; sus muestras, matrices de covarianza y familias son distintas. Antes de decidir cuál destacar en el abstract, verificar directamente sus tablas y especificaciones.

Con la especificación histórica `1/2/3/4/5/6+`, los omnibus entre usuarios fueron **p=0.317 (Z)** y **p=0.152 (PASS)**; ninguno de sus 15 pares alcanzó significación después de Holm. La ausencia de rechazo **no es** prueba de que todos los coeficientes sean iguales, de que exista un plateau o de rendimientos decrecientes.

En la sensibilidad con clustering por **profesor**, el omnibus entre usuarios produjo `p=0.0477` para Z y `p=0.0551` para PASS; además `6+` menos 1 visita en PASS fue +12.0 pp (p-Holm 0.0358). No es lícito decir que «ningún contraste positivo de PASS es significativo en ninguna especificación»; tampoco describe un incremento monotónico o un efecto causal de alcanzar 6 visitas.

## Equivalencia: decisión explícita

**No hay márgenes clínico/educativamente justificados de equivalencia fijados antes de ver estos resultados.** Por tanto, **NO** interpretar p>0.05 como igualdad, no ejecutar pruebas de equivalencia post hoc y no fusionar categorías basándose únicamente en contrastes no significativos.

## Orden propuesto de exposición de métodos/resultados

1. Cohorte, conteos, soporte e incentivo PPA como factor de selección.
2. Contraste benchmark `0 vs 1+` en Z y PASS.
3. **Análisis sólo entre usuarios con las categorías pre-outcome `1/2/3/4/5/6+`**, pruebas omnibus y familia Holm de 15.
4. Análisis de resolución `6/7+` y modelo completo de ocho categorías, identificando por separado el contraste destacado 7+ vs 1 y su familia.
5. Variación de incertidumbre al agrupar por profesor y otras sensibilidades.
6. Composición de resultados académicos: PASS/numérico/BV/RT/BA y contrastes condicionados no-PASS, con sus propias familias inferenciales.

## Prohibiciones interpretativas

No «a cada visita mejora la nota»; no «tres visitas causan...»; no «dos categorías son equivalentes»; no describir los OR logit como diferencias en probabilidad. Holm resuelve multiplicidad definida, **no causalidad**.

**Fuentes:** [plan de análisis](../paper/docs/analysis/ANALYSIS_PLAN.md), [agrupación y cronología](../paper/docs/analysis/VISIT_GROUPING_DECISION.md), [outcomes](../paper/docs/analysis/OUTCOME_FRAMEWORK.md), [resultados controlados](../paper/docs/results/PRELIMINARY_RESULTS.md).