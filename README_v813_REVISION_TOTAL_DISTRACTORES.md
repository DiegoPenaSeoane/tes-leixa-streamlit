# TES Leixa v813 — revisión total de distractores

Versión preparada para subir por GitHub Web sin CSV gigante.

## Resultado

- Banco total: **9813 preguntas**.
- Mantiene Planes, Anatomofisiología y Logística.
- Banco embebido en `app.py`, igual que en las versiones ligeras.
- Revisión aplicada a **9694 filas** con microfamilias de distractores.
- Enunciados reescritos por riesgo de llevar la respuesta dentro: **682**.

## Qué se corrige

1. Se eliminan enunciados que nombraban literalmente la respuesta correcta.
2. Se sustituyen distractores lejanos por distractores de la misma microfamilia.
3. Se refuerzan explicaciones: la explicación indica por qué la correcta lo es y por qué las trampas no lo son.
4. Se evita que una pregunta pueda acertarse solo por descarte lógico.

## Microfamilias usadas

- Vejiga / uretra / uréter / riñón / próstata / vesícula seminal / testículo.
- Hipoxia / hipoxemia / hipercapnia / isquemia / anoxia / cianosis.
- Fémur / tibia / peroné / húmero / radio / cúbito / rótula.
- FIFO / FEFO / rotura de stock / stock mínimo / punto de pedido / pedido mínimo.
- Alerta / alarma / activación / desactivación / normalización / rehabilitación.
- CECOP / CECOPI / PMA / dirección del plan / comité asesor / gabinete de información.
- Grupo sanitario / intervención / seguridad / logístico / apoyo técnico.
- Plan territorial / plan especial / autoprotección / DRP / interfase / catálogo / mapa de riesgos.

## Subida

Arrastra estos elementos a la raíz del repo:

```text
app.py
requirements.txt
README_v813_REVISION_TOTAL_DISTRACTORES.md
CHANGELOG_v813_REVISION_TOTAL_DISTRACTORES.md
docs/
scripts/
```

No reemplaces `user_store.json` ni `user_store (2).json`.

Después: Streamlit → Manage app → Clear cache → Reboot.
