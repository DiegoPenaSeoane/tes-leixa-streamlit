# Comprobación rápida v8.21

1. Abre `app.py` en GitHub.
2. Las primeras líneas deben empezar así:

```python
import base64, gzip, hashlib, io, json, random
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(...)
```

3. No debe aparecer al inicio una línea como:

```python
text = app.read_text(...)
```

4. La app debe cargar el banco desde `BANK_B64`, no desde un CSV externo.
