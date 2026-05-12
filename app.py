import json
from pathlib import Path
import pandas as pd

bank = Path("data/tes_leixa_banco_v653_streamlit_ready.csv.gz")
users = Path("data/user_store.json")

df = pd.read_csv(bank, dtype=str, encoding="utf-8-sig", compression="gzip").fillna("")
print("Preguntas:", len(df))
print("Respuestas inválidas:", int((~df["respuesta_correcta"].str.upper().isin(["A","B","C","D"])).sum()))
print("IDs duplicados:", int(df["id"].duplicated().sum()))

store = json.loads(users.read_text(encoding="utf-8"))
print("Usuarios:", ", ".join(store["users"].keys()))
