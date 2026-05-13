# TES Leixa v8.03 — Login reparado

## Qué corrige

Si `user_store.json` venía de versiones anteriores, podía tener hashes antiguos o corruptos.

Ahora:

- diego / tes2026 entra aunque el hash viejo esté mal
- anton / 1234 entra
- melisa / 1111 entra
- elvira / 2222 entra
- lucia / 3333 entra
- si entra con una contraseña inicial válida, repara el hash automáticamente
- añade botón “Restablecer usuarios iniciales”

## Subir

Sube solo:

- app.py
- requirements.txt
- README_v803_LOGIN_REPARADO.md

Después:

- Commit changes
- Streamlit → Reboot app
- Ctrl + F5

Debe aparecer:

`Banco v8.03 · login reparado`
