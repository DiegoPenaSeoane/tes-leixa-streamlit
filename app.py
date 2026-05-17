import base64, gzip, io, re
import pandas as pd
from pathlib import Path

app = Path(__file__).resolve().parents[1] / "app.py"
text = app.read_text(encoding="utf-8")
m = re.search(r'BANK_B64 = """(.*?)"""', text, re.S)
raw = gzip.decompress(base64.b64decode(m.group(1)))
df = pd.read_csv(io.BytesIO(raw))
print("Preguntas:", len(df))
print(df["modulo"].value_counts())
assert len(df) == 10713
assert df["id"].is_unique
for col in ["enunciado","opcion_a","opcion_b","opcion_c","opcion_d","respuesta_correcta","explicacion"]:
    assert col in df.columns
for _, r in df[df["id"].astype(str).str.startswith("V819")].iterrows():
    opts=[r["opcion_a"],r["opcion_b"],r["opcion_c"],r["opcion_d"]]
    assert len(set(opts)) == 4, r["id"]
    ans = r["opcion_" + r["respuesta_correcta"].lower()]
    assert str(ans).lower() not in str(r["enunciado"]).lower(), (r["id"], ans)
print("OK v819")
