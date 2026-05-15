# TES Leixa v8.11 — Planes ampliado + distractores reforzados

Actualización lista para arrastrar a GitHub.

## Resultado

- Banco total: **9813 preguntas**.
- MP0061 Anatomofisiología: **4570**.
- MP0053 Logística sanitaria: **3124**.
- MP0059 Planes de emergencias: **2119**.

## Qué cambia

1. Se preserva el banco v809/v810 anterior.
2. Se añaden **1200 preguntas nuevas de Planes de Emergencias** con dificultad alta/filtro_10.
3. Se refuerzan distractores de Anatomía y Logística del bloque v810: las opciones incorrectas son conceptos reales y cercanos, no respuestas obvias.
4. Se mantienen explicaciones, porqués de descarte, regla de oro, error típico, tip de examen, minilección, mnemotecnia y tabla de repaso.
5. `app.py` queda con el banco embebido, por eso Streamlit debe pasar a mostrar **Banco 9813** tras limpiar caché/reboot.

## Cómo subir

Arrastra a la raíz del repositorio:

```text
app.py
requirements.txt
data/
scripts/
docs/
README_v811_PLANES_PLUS_DISTRACTORES.md
CHANGELOG_v811_PLANES_PLUS_DISTRACTORES.md
```

No sustituyas ni subas `user_store.json` si quieres conservar usuarios/progreso.

## Después en Streamlit

- Manage app → Clear cache
- Reboot app

Señal correcta: debe aparecer **Banco 9813**.
