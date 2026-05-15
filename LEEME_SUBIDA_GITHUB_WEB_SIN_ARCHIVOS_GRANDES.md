# TES Leixa v811 ligera para GitHub Web

Esta versión está preparada para evitar el error de GitHub: **file is too large**.

## Qué cambia

- Mantiene el banco v811 de **9813 preguntas** embebido en `app.py`.
- No incluye el CSV grande sin comprimir.
- No incluye archivos de datos pesados.
- Preserva Planes: el banco incluye Anatomofisiología, Logística y Planes.

## Qué subir a GitHub

Arrastra a la raíz del repositorio solo estos elementos:

```text
app.py
requirements.txt
README_v811_PLANES_PLUS_DISTRACTORES.md
CHANGELOG_v811_PLANES_PLUS_DISTRACTORES.md
docs/
scripts/
```

## Qué NO subir

No subas estos archivos del paquete anterior porque causan el fallo de tamaño:

```text
data/TES_v811_BANCO_FUSIONADO_9813_PLANES_PLUS_DISTRACTORES.csv
data/TES_v811_ADDON_ANATOMIA_LOGISTICA_DISTRACTORES_REFORZADOS.csv
data/TES_v811_ADDON_PLANES_1200_ALTA_DIFICULTAD.csv
```

Tampoco reemplaces:

```text
user_store.json
user_store (2).json
```

## Después de subir

En Streamlit:

```text
Manage app → Clear cache → Reboot app
```

Resultado esperado:

```text
Banco 9813
```
