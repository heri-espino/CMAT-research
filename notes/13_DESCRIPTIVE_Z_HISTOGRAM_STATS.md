# Estadísticas descriptivas de Z en la figura 1 (2026-10-12)

El gráfico de resultados usa únicamente las tablas agregadas existentes. No se han reestimado los modelos ni reconstruido observaciones individuales.

**Media, desviación estándar e intervalo de confianza (95%):** se leen directamente de results/paper21/tables/10n_zero_inclusive_7plus_descriptives.csv, calculados para el grupo completo de frecuencia, incluidas las imputaciones documentadas para BV/RT/BA. Los IC son descriptivos de la media; no son intervalos ajustados por efectos fijos ni sustituyen Wald/Holm. La SD por frecuencia no tiene por qué ser uno, ya que la estandarización se hace dentro de profesor–periodo.

**Mediana:** no existe un estadístico exacto de mediana en la tabla de origen. El histograma results/paper21/tables/10s_zero_inclusive_7plus_imputed_z_histogram.csv contiene bins de 0.1 Z sólo en [-2,2]. Se construyen cotas conservadoras para la mediana de toda la frecuencia, dejando que los registros fuera del histograma se distribuyan en cualquier cola. La figura indica el punto medio de esas cotas como aproximación, y una barra púrpura delimita la ubicación compatible con los bins. **La barra púrpura no es un IC** ni la mediana exacta. Una mediana exacta exige recuperar un agregado de cuantiles generado de forma autorizada a partir de los microdatos.

## Estadísticas por frecuencia

| Visitas | N | Media Z | SD Z | IC 95% de media Z | Mediana Z: cotas por bins y colas | Fuera del gráfico |
|---|---:|---:|---:|---|---|---:|
| 0 | 5393 | -0.061 | 1.017 | [-0.088, -0.034] | [0.30, 0.50]; ≈0.40 | 357 (6.6%) |
| 1 | 517 | 0.219 | 0.849 | [0.146, 0.292] | [0.40, 0.50]; ≈0.45 | 12 (2.3%) |
| 2 | 245 | 0.247 | 0.738 | [0.154, 0.339] | [0.40, 0.50]; ≈0.45 | 5 (2.0%) |
| 3 | 170 | 0.278 | 0.797 | [0.158, 0.398] | [0.50, 0.60]; ≈0.55 | 3 (1.8%) |
| 4 | 96 | 0.267 | 0.694 | [0.128, 0.406] | [0.40, 0.60]; ≈0.50 | 1 (1.0%) |
| 5 | 55 | 0.382 | 0.594 | [0.225, 0.539] | [0.40, 0.50]; ≈0.45 | 0 (0.0%) |
| 6 | 50 | 0.288 | 0.838 | [0.055, 0.520] | [0.40, 0.70]; ≈0.55 | 2 (4.0%) |
| 7+ | 101 | 0.457 | 0.624 | [0.336, 0.579] | [0.50, 0.60]; ≈0.55 | 0 (0.0%) |

## Límites de interpretación

La asimetría de la distribución Z puede ser relevante, pero depende parcialmente del esquema de imputación de resultados sin calificación numérica. Los intervalos descriptivos no permiten inferir diferencias ajustadas entre frecuencias. Para ello se conservan las familias Holm del artículo. La figura se actualiza ejecutando python paper/paper_build.py --figures --paper.
