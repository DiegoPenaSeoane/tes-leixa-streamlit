from pathlib import Path

app = Path("app.py").read_text(encoding="utf-8")
assert "Banco v8.20" in app
assert "ACRONYM_GLOSSARY" in app
assert "Entrenar trampas/siglas" in app
assert "render_confusion_dashboard" in app
assert "familia_confusion" in app
print("OK v820: siglas + confusiones + modo de entrenamiento instalados")
