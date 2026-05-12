# v7.10 — Fix app.py correcto

## Problema

El error:

`File "/mount/src/tes-leixa-streamlit/app.py", line 2`

demuestra que el `app.py` subido al repo no es la app completa, sino un script corto de validación.

## Solución

Sobrescribe en GitHub:

- app.py
- requirements.txt

con los de este ZIP.

## Comprobación

Al abrir `app.py` en GitHub, NO debe empezar así:

```python
df = pd.read_csv(...)
```

Debe ser un archivo largo y debe contener:

`Banco v7.10 · app.py correcto.`
