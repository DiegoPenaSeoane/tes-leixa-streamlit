# TES v810 SAFE ADDON — preservar 3413 + Planes

Este paquete está adaptado al repositorio que has mostrado. Está diseñado para subirse sin pisar `app.py`, `README.md` ni los CSV originales.

## Qué añade

- `TES_V810_SAFE_ADDON/addons/tes_addon_anatomia_logistica_5200.csv`
- Cargador seguro que fusiona el banco original con el addon.
- Motor de repaso espaciado para falladas/acertadas.
- Scripts de diagnóstico y creación de CSV fusionado.

## Qué NO hace

- No reemplaza las 3413 preguntas originales.
- No borra Planes.
- No sobrescribe `app.py`.
- No sobrescribe `README.md`.
- No cambia `user_store.json`.

## Resultado esperado

La app debería pasar de 3413 a aproximadamente:

`3413 + 5200 - duplicados conservadores`

Es normal que el total final no sea exactamente 8613 si hay duplicados exactos.

## Parche mínimo en `app.py`

Como no has subido el contenido de `app.py`, no puedo sustituirlo con seguridad. Haz este cambio mínimo donde ahora se carga el CSV del banco:

```python
from TES_V810_SAFE_ADDON.app_modules.bank_loader_v810_safe import load_bank_v810_safe

# Sustituye SOLO la línea o función que carga el banco por:
banco = load_bank_v810_safe()
```

Si tu app usa otro nombre, por ejemplo `df`, `preguntas`, `bank` o `data`, usa el mismo nombre:

```python
df = load_bank_v810_safe()
```

## Diagnóstico opcional

Desde la raíz del repo:

```bash
python TES_V810_SAFE_ADDON/scripts/diagnosticar_v810_seguro.py
```

## Crear CSV fusionado opcional

```bash
python TES_V810_SAFE_ADDON/scripts/crear_csv_fusionado_v810.py
```

Esto crea en raíz:

`TES_LEIXA_BANCO_V810_FUSIONADO_SEGURO.csv`

No borra nada.
