# TES Leixa v8.10 — Fusión segura 8613 + repaso optimizado

Este paquete está hecho a partir de tu ZIP conservado `TES_LEIXA_APP_v809_TABLAS_PERSONALIZADAS.zip`.

## Qué cambia

- `app.py` deja de contener solo el banco embebido de 3413 preguntas.
- Ahora contiene el banco fusionado completo: **8613 preguntas**.
- Se conservan las **3413 preguntas originales**, incluidas las de **Planes** y el resto del banco v809.
- Se añaden **5200 preguntas nuevas validadas de Anatomía y Logística**.
- Se mejora `Plan de hoy` para priorizar:
  1. fallos pendientes,
  2. preguntas con más fallos históricos,
  3. temas débiles,
  4. preguntas no vistas,
  5. dificultad alta/filtro_10,
  6. repasos antiguos.

## Cómo subirlo a GitHub sin estropear nada

1. Descomprime este ZIP.
2. En GitHub, arrastra a la raíz del repo **solo estos elementos principales**:
   - `app.py`
   - `requirements.txt` si quieres mantener el mismo
   - carpeta `data/` solo como copia de auditoría, no es imprescindible para que funcione
   - carpeta `scripts/` si quieres verificar
3. Acepta reemplazar `app.py`.
4. No subas ni reemplaces `user_store.json`.
5. En Streamlit: `Manage app` → `Clear cache` → `Reboot app`.

## Resultado esperado

En la pantalla principal debe aparecer:

`Banco 8613`

No debe aparecer ya `3413`.

## Verificación local opcional

```bash
python scripts/verificar_v810.py
```

Debe devolver:

```text
TOTAL 8613
OK v810: app.py contiene 8613 preguntas y conserva el banco embebido.
```

## Importante

La app sigue siendo de archivo único. Los CSV de `data/` son para auditoría y revisión, pero el `app.py` ya lleva el banco fusionado embebido. Esto evita que vuelva a leer el banco antiguo.
