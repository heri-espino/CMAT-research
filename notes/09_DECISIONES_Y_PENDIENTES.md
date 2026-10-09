# 09 — Registro de decisiones y tareas para pasar de notas a paper

## Decisiones con fecha y origen

| Fecha / estado | Decisión o hecho | Qué significa al redactar |
|---|---|---|
| 2026-09-20 (documentado) | Agrupación originalmente elegida con auditoría ciega a outcomes: `1/2/3/4/5/6+` | Mantener como especificación con mayor soporte e indicar que `6/7+` se añadió como sensibilidad/reporting posterior |
| Investigación Paper 2.1 (documentada) | Efectos fijos profesor–periodo, carrera, SE agrupados; Wald + Holm por outcome/familia | Usarlos como estrategia inferencial principal |
| Investigación Paper 2.1 (documentada) | No se justificó un margen de equivalencia independiente | No afirmar grupos equivalentes ni usar no significación para fusionar categorías |
| 2026-10-09 (decisión del proyecto) | Priorizar redacción del paper basada en Holm; no prolongar tuning de fused lasso | Conservar `paper2.2.1` como investigación exploratoria separada |
| 2026-10-09 (esta carpeta) | Consolidar contexto, resultados, bibliografía, delimitación y target editorial **antes** de reescribir | Proteger decisiones, discrepancias y procedencia; no inventar una nueva corrida |

## Pendientes empíricos que requieren atención

- [ ] Revisar CSV de **modelo completo ocho grupos** contra el **modelo sólo usuarios**. Explicar, en Methods y Results, por qué `7+ vs 1` PASS es Holm-significativo en un modelo y no en otro; no mezclar sus valores p.
- [ ] Auditar resultado `6+ vs 1` PASS con clustering por profesor y su familia Holm.
- [ ] Verificar exactamente cómo `Z_GRADE_PRIMARY` imputa BA/BV/RT y cómo se estandariza cuando cambian las cohortes.
- [ ] Verificar formato de los intervalos, grados de libertad/corrección CR y si las tablas/figuras se derivan de la misma versión de datos.
- [ ] Confirmar contenido de la sensibilidad complete-case y, si hay examen diagnóstico/de ingreso comparable, evaluar su cobertura y naturaleza temporal **antes** de introducirlo.
- [ ] Revisar que las afirmaciones sobre composición no-PASS usen denominadores correctos.
- [ ] Decidir si GMM queda en suplemento, en una sección exploratoria breve o reservado a otro estudio; en ningún caso cambiar su estatus a «identificación de dos tipos de estudiantes».

## Verificación institucional y editorial pendiente

- [ ] Confirmar horarios, modalidad de registro, etiqueta de visitas y características históricas de CMAT.
- [ ] Confirmar vigencia y reglas de PPA / opción de tres visitas durante 2019–2024.
- [ ] Obtener definiciones y consecuencias oficiales históricas de BA, BV y RT; **no afirmar protección del promedio/GPA ni plazos de retiro sin fuente**.
- [ ] Incluir autorización ética, exención o acuerdo de uso de datos en su formulación exacta (actualmente falta).
- [ ] Revisar metadatos de autores, acceso a datos, financiación y divulgación de uso de IA.
- [ ] Verificar instrucciones actuales de TEAMAT y requerimientos de envío.
- [ ] Auditar claves bibliográficas, estado de acceso del texto Gokhool y Lawson, inclusión real de referencias en el manuscrito.

## Reglas de cierre

El apartado de métodos está listo para escribirse cuando estén claros el **universo de cada especificación y el conjunto de contrastes**. Results se considerará congelado sólo cuando cada cifra se relacione con su tabla/código y los resultados contradictorios por especificación estén presentados honestamente. Discussion sólo puede invocar mecanismos como hipótesis compatibles y mantener alternativas.

No abrir una nueva rama metodológica por una diferencia de p-values ni modificar agrupaciones para aumentar significación. Los experimentos adicionales requerirán decisión explícita, fecha y nuevo registro en este archivo.

## Siguiente tarea concreta

Construir la primera versión inglesa apoyada en estas notas: escoger título y pregunta nuclear, reordenar el manuscrito existente con Holm como eje, realizar matriz de trazabilidad para números relevantes y colocar GMM bajo el estatus que se acuerde. **Esta tarea aún no se ejecutó en la creación de `notes/`.**