import pandas as pd
df = pd.read_csv("data/tes_leixa_banco_v653_streamlit_ready.csv.gz", dtype=str, encoding="utf-8-sig", compression="gzip").fillna("")
print("Preguntas:", len(df))
print("Respuestas inválidas:", int((~df["respuesta_correcta"].str.upper().isin(["A","B","C","D"])).sum()))
print("Duplicados ID:", int(df["id"].duplicated().sum()))
print("Módulos:", df["modulo"].nunique())
