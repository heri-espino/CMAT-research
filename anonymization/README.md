# Anonymization / pseudonymization materials

Este directorio reúne material explicativo y reproducible sobre la protección de identificadores usada en `CMAT-research`.

Aunque el directorio se llama `anonymization` por conveniencia, el mecanismo descrito aquí es **pseudonimización determinística mediante HMAC-SHA256**, no anonimización absoluta. La implementación de referencia del repositorio se encuentra en `cmat_analysis/src/cmat_analysis/privacy.py`.

## Contenido

- `technical/pseudonimizacion_ids_cmat.tex`: explicación técnica.
- `non_technical/pseudonimizacion_ids_cmat.tex`: explicación orientada a lectura administrativa.
- `pseudonymization_demo.ipynb`: recorrido paso a paso con el ID de demostración `175199`, la misma clave ficticia usada en los documentos y el mismo pseudónimo esperado.
- `key_generator.py`: generador reproducible con semilla para demostraciones y generador criptográficamente seguro para claves reales.
- `velvetblue.sty`: copia del estilo académico usado por los papers del repositorio, tomada de `paper/paper1-ppa-persistence` / `paper/paper3-grading-heterogeneity` (mismo archivo en ambas ramas al momento de preparar este material).

## Ejemplo reproducible

La notebook utiliza únicamente una clave **ficticia**:

```text
ID:         175199
namespace:  stu
key:        7b41e7a1c76f6b50f58a0c628a3f0e8daed7ad4f6dd6c7e97ad31e8f8ad1e933
resultado:  stu_c504a778e1e4b331721d7c88f22c65e0
```

La clave real de los datos controlados no debe almacenarse en este directorio, en Git, en notebooks, en documentación ni en artefactos de ejecución.

## Sobre el generador con semilla

`generate_seeded_demo_key()` existe para que una demostración o clase produzca siempre el mismo resultado. Usa un generador determinístico y **no debe utilizarse para crear secretos de producción**. Para una clave real se incluye `generate_secure_key()`, que usa `secrets.token_hex(32)` y no acepta semilla deliberadamente.
