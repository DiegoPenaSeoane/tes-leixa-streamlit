# Instrucciones para subir a GitHub/Streamlit

## Opción segura

1. Descomprime este ZIP en una carpeta aparte.
2. Abre tu repositorio de la app v809.
3. Copia solo estas carpetas al repo:
   - `data/`
   - `app_modules/`
   - `docs/`
   - `tests/`
4. No borres el banco anterior hasta comprobar que la app arranca.
5. Lanza la app localmente.
6. Comprueba que puede leer `data/tes_banco_master_2400_plus.csv`.
7. Cuando funcione, sube cambios a GitHub.

## Validación antes de subir

Ejecuta:

```bash
python tests/test_bank_integrity.py
```

## Cambio recomendado de UX

En la pantalla de resultado de cada pregunta, mostrar:

- Correcta/incorrecta.
- Explicación corta.
- Si falla: explicación extendida + error típico + mnemotecnia.
- Botones: `La sabía`, `Dudé`, `Fallé por concepto`, `Fallé por despiste`.

Eso permite que el motor de repaso ajuste intervalos mejor que solo acertada/fallada.
