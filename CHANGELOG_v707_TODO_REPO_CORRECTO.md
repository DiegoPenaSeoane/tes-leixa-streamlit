# Configurar persistencia real

Para conservar progreso de cada usuario tras reinicios de Streamlit, añade Secrets:

```toml
GITHUB_TOKEN = "TU_TOKEN"
GITHUB_REPO = "diegopenaseoane/tes-leixa-streamlit"
GITHUB_BRANCH = "main"
GITHUB_STORE_PATH = "data/user_store.json"
```

El token debe tener permiso de lectura/escritura en Contents del repositorio.

Si la app muestra “GitHub persistente”, el progreso se guarda en el repositorio.
