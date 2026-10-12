# 2026-10-12 — Resultado no-PASS, hipótesis sobre becas y próxima evaluación de PPA1

## Verificación operativa del umbral de aprobación

**PASS** se calcula en `cmat_analysis/src/cmat_analysis/measures/_grades.py` mediante `GRADE_NUMERIC >= config.passing_grade` con `passing_grade=7.5`. Una nota exactamente 7.5 **aprueba**, por lo que la categoría fracaso numérico debe usar **`GRADE_NUMERIC < 7.5`** y nunca `<= 7.5`. BV/RT/BA reciben `PASS=0` como estados administrativos, pero **no reciben una nota numérica artificial para PASS**; la imputación de nota adversa es una operación separada para el outcome Z continuo.

## Qué queda sustentado con resultados institucionales ya producidos

Fuente `results/paper21/tables/10f_nonpass_management_descriptives_0_vs_1plus.csv`:

| Condicionado a no aprobar | 0 visitas | 1+ visitas |
|---|---:|---:|
| No-PASS total | 1,504 | 217 |
| Calificación numérica <7.5 | 581 (38.6%) | 39 (18.0%) |
| Resultado administrativo BV/RT/BA | 923 (61.4%) | 178 (82.0%) |

El estimador auxiliar ajustado en `results/paper21/tables/10e_nonpass_management_benchmark_0_vs_1plus.csv` para el outcome *administrative rather than numeric outcome among non-PASS* es **+0.132261** (IC 95% **0.068029–0.196494**, p nominal **0.00005443**) usando 1,721 estudiantes con no-PASS de 187 contextos profesor–periodo. Los contrastes de composición **no pertenecen a las familias Holm** de 15, 21 y 28 pares para Z y PASS. No comparan tasas poblacionales de retiro en todos los asistentes ni implican que asistir *cause* una baja.

Los cinco estados se mantienen distinguibles en `results/paper21/tables/10o_zero_inclusive_7plus_exact_administrative_composition.csv`. Las categorías BV, RT y BA se agrupan visualmente como **sin calificación numérica** sólo para la figura, porque no representan un promedio numérico final; no equivalen a una elección voluntaria homogénea.

## Hipótesis sobre preservación de beca: compatible, pero no demostrada

Podría ocurrir que una persona que acudió a CMAT buscando aprobar y anticipó un fracaso numérico considerase un retiro para evitar deteriorar su promedio acumulado, especialmente si cuenta con beca y debe mantener un mínimo. **No tenemos** variable de beca, tipo/porcentaje, promedio antes de la materia, detalle de movimiento permitido, fechas de visita/solicitud de baja ni motivos individuales. Por tanto la evidencia no puede confirmar quién tomó una decisión, cuándo, ni por qué. Tampoco sabemos si los registros BA o RT son comparables con BV.

**Documentos públicos UDLAP consultados (referencias contextuales, no equivalencia automática al reglamento 2019–2024):**
- Lineamientos de apoyos educativos, [UDLAP](https://online.udlap.mx/apoyoeducativo/lineamientos-generales.aspx): mantener promedio acumulado mínimo y no exceder el número de movimientos permitidos según tipo de beca.
- [Servicios escolares: bajas y retiros](https://serviciosescolaresudlap.azurewebsites.net/bajasyretiros): BV es retiro de una materia; RT afecta las materias del periodo y el sitio indica que no afecta promedio. Para BV y becas, hay límites específicos.
- [Lineamientos de beca GAC](https://online.udlap.mx/becas/files/lineamientosLicEsp/LINLIC-GAC.pdf): ejemplo de beca con promedio acumulado mínimo y restricciones sobre BV/reprobación/RT. **Su versión de 2026 no demuestra que esa regulación ni ese beneficio rigieran durante el periodo 2019–2024**.

**Posible refutación:** algunas becas limitan la suma de retiros y reprobaciones; si un estudiante ya agotó dichos movimientos, retirarse podría perjudicar su situación tanto como reprobar. No dar por sentado que una BV preserva una beca.

## Estudios nuevos propuestos, no realizados

1. **Becas / decisiones de retiro**: comparar, con autorización institucional y minimización de datos, estudiantes con y sin beca, nivel de beca, promedio anterior, exposición a límites de retiros, fechas de visitas y resultados finales. Explorar el riesgo de entrar en cada tipo de registro después de controlar preparación previa y momento del periodo, y complementar con documentación o entrevistas sobre motivos reales. Identificar el sesgo de selección por condicionar a no-PASS.
2. **Incentivo PPA1**: las actividades sociales y culturales de primer semestre (eventos deportivos, teatro, danza y organizaciones estudiantiles) incluyen la opción de acreditar una actividad mediante tres visitas a CMAT, vigente durante toda la ventana de estudio según la aclaración institucional. Obtener elegibilidad, acreditación, fechas y opciones alternativas por estudiante, y diseñar una comparación apropiada. No hay cambio de política conocido ni la frontera `3|4` prueba un efecto.

La página pública del [CMAT](https://info.udlap.mx/centrodematematicas/conocenos.aspx) confirma una opción de obtener puntos PPA1 por cumplir el programa de actividades, pero **no documenta allí por sí sola el requisito histórico exacto de tres visitas**. Su disponibilidad, propósito y continuidad fueron confirmados con información institucional suministrada en el proyecto (2026-10-12); archivar un reglamento histórico es un pendiente documental, no una duda sobre su existencia durante el periodo.

## Límite del Paper 2.1

Este manuscrito mantiene como **eje inferencial principal Wald + Holm para Z y PASS**. La composición no-PASS se menciona sólo como diagnóstico descriptivo y comparación auxiliar previamente disponible; no se introdujo una batería adicional de pruebas, no se infieren motivos, y ambos mecanismos propuestos se ubican en futuras investigaciones.
