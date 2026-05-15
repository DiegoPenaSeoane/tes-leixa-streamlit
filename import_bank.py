from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
BANK = ROOT / "data" / "tes_banco_master_2400_plus.csv"
REQUIRED = ["id","materia","pregunta","opcion_A","opcion_B","opcion_C","opcion_D","respuesta_correcta","explicacion_corta","explicacion_extendida"]

def main():
    rows = list(csv.DictReader(BANK.open("r", encoding="utf-8-sig")))
    assert len(rows) >= 2400, f"Se esperaban al menos 2400 preguntas, hay {len(rows)}"
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids)), "Hay IDs duplicados"
    for col in REQUIRED:
        assert col in rows[0], f"Falta columna {col}"
    for r in rows:
        assert r["respuesta_correcta"] in "ABCD", f"Respuesta inválida: {r['id']}"
        opts = [r["opcion_A"], r["opcion_B"], r["opcion_C"], r["opcion_D"]]
        assert all(opts), f"Opción vacía: {r['id']}"
        assert len(set(opts)) == 4, f"Opciones repetidas: {r['id']}"
    print(f"OK: {len(rows)} preguntas validadas")

if __name__ == "__main__":
    main()
