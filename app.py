
import base64
import hashlib
import json
import random
import urllib.request
from datetime import datetime, timezone, date
from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(page_title="TES Leixa — Test táctil", page_icon="🚑", layout="wide")

DATA_PATHS = [
    Path("data/tes_leixa_banco_v653_streamlit_ready.csv.gz"),
    Path("tes_leixa_banco_v653_streamlit_ready.csv.gz"),
    Path("data/tes_leixa_banco_v653_streamlit_ready.csv"),
    Path("tes_leixa_banco_v653_streamlit_ready.csv"),
]
USER_STORE_PATHS = [
    Path("data/user_store.json"),
    Path("user_store.json"),
]
USER_STORE_PATH = USER_STORE_PATHS[0]
OPTION_COLUMNS = {"A": "opcion_a", "B": "opcion_b", "C": "opcion_c", "D": "opcion_d"}

REQUIRED_COLUMNS = [
    "id", "modulo", "tema", "subtema", "nivel_dificultad", "tipo_pregunta",
    "enunciado", "opcion_a", "opcion_b", "opcion_c", "opcion_d", "respuesta_correcta",
    "explicacion", "porque_no_a", "porque_no_b", "porque_no_c", "porque_no_d",
    "regla_oro", "error_tipico", "tip_examen", "minileccion", "mnemotecnia",
    "tabla_esquema", "conceptos_clave", "estado_app"
]


def normalize_text(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def today_str():
    return date.today().isoformat()


def hash_password(password, salt):
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


def make_user(username, display_name, password, role):
    salt = hashlib.sha256((username + password + "tes-leixa").encode("utf-8")).hexdigest()[:16]
    return {
        "display_name": display_name,
        "salt": salt,
        "password_hash": hash_password(password, salt),
        "role": role,
        "active": True,
        "must_change_password": username != "diego",
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }


def default_store():
    users = {
        "diego": make_user("diego", "Diego", "tes2026", "administrador"),
        "anton": make_user("anton", "Anton", "1234", "usuario"),
        "melisa": make_user("melisa", "Melisa", "1111", "usuario"),
        "elvira": make_user("elvira", "Elvira", "2222", "usuario"),
        "lucia": make_user("lucia", "Lucia", "3333", "usuario"),
    }
    progress = {
        uid: {
            "answered": [],
            "wrong_ids": [],
            "correct_ids": [],
            "settings": {
                "daily_goal": 142,
                "target_pct": 90,
                "study_days_first_round": 12,
                "study_days_second_round": 12,
                "exam_plan_start": today_str(),
            },
        }
        for uid in users
    }
    return {
        "schema_version": "1.1",
        "updated_at": now_iso(),
        "users": users,
        "progress": progress,
    }


def ensure_store_shape(store):
    base = default_store()
    store.setdefault("schema_version", "1.1")
    store.setdefault("users", {})
    store.setdefault("progress", {})
    for uid, user in base["users"].items():
        store["users"].setdefault(uid, user)
    for uid in store["users"].keys():
        store["progress"].setdefault(uid, {
            "answered": [],
            "wrong_ids": [],
            "correct_ids": [],
            "settings": {
                "daily_goal": 142,
                "target_pct": 90,
                "study_days_first_round": 12,
                "study_days_second_round": 12,
                "exam_plan_start": today_str(),
            },
        })
        p = store["progress"][uid]
        p.setdefault("answered", [])
        p.setdefault("wrong_ids", [])
        p.setdefault("correct_ids", [])
        p.setdefault("settings", {})
        s = p["settings"]
        s.setdefault("daily_goal", 142)
        s.setdefault("target_pct", 90)
        s.setdefault("study_days_first_round", 12)
        s.setdefault("study_days_second_round", 12)
        s.setdefault("exam_plan_start", today_str())
    return store


def load_local_store():
    for path in USER_STORE_PATHS:
        try:
            if path.exists():
                return ensure_store_shape(json.loads(path.read_text(encoding="utf-8")))
        except Exception:
            pass
    return default_store()


def github_configured():
    return all(k in st.secrets for k in ["GITHUB_TOKEN", "GITHUB_REPO"])


def github_headers():
    return {
        "Authorization": f"Bearer {st.secrets['GITHUB_TOKEN']}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
    }


def github_store_path():
    return st.secrets.get("GITHUB_STORE_PATH", "data/user_store.json")


def read_github_store():
    repo = st.secrets["GITHUB_REPO"]
    branch = st.secrets.get("GITHUB_BRANCH", "main")
    path = github_store_path()
    url = f"https://api.github.com/repos/{repo}/contents/{path}?ref={branch}"
    req = urllib.request.Request(url, headers=github_headers())
    with urllib.request.urlopen(req, timeout=20) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    content = base64.b64decode(payload["content"]).decode("utf-8")
    return ensure_store_shape(json.loads(content)), payload.get("sha")


def write_github_store(store, sha, message):
    repo = st.secrets["GITHUB_REPO"]
    branch = st.secrets.get("GITHUB_BRANCH", "main")
    path = github_store_path()
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    store["updated_at"] = now_iso()
    raw = json.dumps(store, ensure_ascii=False, indent=2)
    body = {
        "message": message,
        "content": base64.b64encode(raw.encode("utf-8")).decode("ascii"),
        "branch": branch,
    }
    if sha:
        body["sha"] = sha
    req = urllib.request.Request(url, headers=github_headers(), data=json.dumps(body).encode("utf-8"), method="PUT")
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def load_store():
    if github_configured():
        try:
            store, sha = read_github_store()
            st.session_state.store_sha = sha
            st.session_state.persistence_mode = "GitHub persistente"
            return store
        except Exception as exc:
            st.warning(f"No pude leer persistencia GitHub. Uso sesión temporal. Detalle: {exc}")
    st.session_state.store_sha = None
    st.session_state.persistence_mode = "Sesión temporal"
    return load_local_store()


def save_store(store, message):
    st.session_state.store = store
    if github_configured():
        try:
            result = write_github_store(store, st.session_state.get("store_sha"), message)
            st.session_state.store_sha = result.get("content", {}).get("sha", st.session_state.get("store_sha"))
            st.session_state.persistence_mode = "GitHub persistente"
            return True, "Guardado permanente."
        except Exception as exc:
            return False, f"No guardado permanente: {exc}"
    return False, "Sin GitHub Secrets: guardado solo durante la sesión."


def get_data_path():
    for path in DATA_PATHS:
        if path.exists():
            return path
    return DATA_PATHS[0]


@st.cache_data(show_spinner=False)
def load_questions(path_str):
    path = Path(path_str)
    if not path.exists():
        raise FileNotFoundError("No encuentro el banco: data/tes_leixa_banco_v653_streamlit_ready.csv.gz")
    compression = "gzip" if path.suffix == ".gz" else None
    df = pd.read_csv(path, dtype=str, encoding="utf-8-sig", compression=compression).fillna("")
    df.columns = [str(c).strip() for c in df.columns]
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    df["respuesta_correcta"] = df["respuesta_correcta"].str.strip().str.upper()
    df = df[df["respuesta_correcta"].isin(["A", "B", "C", "D"])].copy()
    return df.reset_index(drop=True)


def init_state():
    defaults = {
        "store": None,
        "store_sha": None,
        "persistence_mode": "Sesión temporal",
        "logged": False,
        "uid": "",
        "display_name": "",
        "role": "usuario",
        "order": [],
        "idx": 0,
        "answered": False,
        "selected": None,
        "last_filter": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def get_progress(store, uid):
    ensure_store_shape(store)
    return store["progress"][uid]


def auth_user(store, username, password):
    username = username.strip().lower()
    user = store.get("users", {}).get(username)
    if not user or not user.get("active", False):
        return None
    if hash_password(password, user["salt"]) == user["password_hash"]:
        return user
    return None


def option_text(q, letter):
    return normalize_text(q.get(OPTION_COLUMNS[letter], ""))


def why_not(q, letter):
    return normalize_text(q.get(f"porque_no_{letter.lower()}", ""))


def detect_tags(q):
    blob = " ".join(
        normalize_text(q.get(k, ""))
        for k in ["id", "modulo", "tema", "subtema", "enunciado", "conceptos_clave", "explicacion", "tabla_esquema"]
    ).lower()
    out = []
    if any(x in blob for x in ["glasgow", "abre ojos", "palabras inapropiadas", "retira al dolor", "localiza el dolor"]): out.append("glasgow")
    if any(x in blob for x in ["start", "triaje start", "rpm"]): out.append("start")
    if any(x in blob for x in ["fefo", "fifo", "stock", "caducidad", "cadena de frío", "cadena de frio"]): out.append("stock")
    if any(x in blob for x in ["drp", "dispositivo de riesgo", "pma", "psa", "desactivación", "desmontaje", "operatividad"]): out.append("drp")
    if any(x in blob for x in ["ictus", "código ictus", "codigo ictus"]): out.append("ictus")
    if any(x in blob for x in ["rcp", "desfibrilación", "desfibrilacion", "dea", "cadena de supervivencia"]): out.append("rcp")
    if any(x in blob for x in ["sepsis", "qsofa"]): out.append("sepsis")
    if any(x in blob for x in ["húmero", "humero", "radio", "cúbito", "cubito", "fémur", "femur", "tibia", "peroné", "hueso", "brazo", "antebrazo"]): out.append("huesos")
    if any(x in blob for x in ["hipocondrio", "epigastrio", "flanco", "fosa ilíaca", "fosa iliaca", "abdomen", "apéndice", "bazo"]): out.append("abdomen")
    if any(x in blob for x in ["plan territorial", "plan especial", "autoprotección", "autoproteccion", "mapa de riesgo"]): out.append("planes")
    if any(x in blob for x in ["vulnerabilidad", "daño potencial", "probabilidad", "reevaluación", "riesgo"]): out.append("riesgo")
    if any(x in blob for x in ["imv", "múltiples víctimas", "multiples victimas", "sectorización", "evacuación regulada", "noria"]): out.append("imv")
    if any(x in blob for x in ["radio", "emisora", "comunicaciones", "ccu", "canal"]): out.append("comunicaciones")
    return out[:2]


TABLES = {
    "glasgow": """### Baremo de Glasgow

| Puntos | Apertura ocular | Respuesta verbal | Respuesta motora |
|---:|---|---|---|
| 6 | — | — | Obedece órdenes / movimiento espontáneo |
| 5 | — | Orientado / balbuceo | Localiza el dolor / retira al tocar |
| 4 | Espontánea | Confuso / llanto irritable | Retira ante estímulo doloroso |
| 3 | Al habla / estímulo verbal | Palabras inapropiadas / llanto al dolor | Flexión anormal |
| 2 | Al dolor | Sonidos incomprensibles / quejido al dolor | Extensión anormal |
| 1 | Ninguna | Ninguna | Ninguna |

**Regla:** Glasgow total = Ocular + Verbal + Motora. **Trampa:** retira al dolor = M4; localiza dolor = M5.""",
    "start": """### START / triaje

| Criterio | Resultado |
|---|---|
| Camina | Verde inicial, reevaluable |
| No respira tras abrir vía aérea | Negro |
| Respira tras abrir vía aérea | Rojo |
| FR > 30/min | Rojo |
| Perfusión alterada | Rojo |
| No obedece órdenes sencillas | Rojo |
| Respira ≤30, perfusión conservada y obedece | Amarillo |""",
    "stock": """### Stock, FEFO/FIFO y cadena de frío

| Situación | Criterio |
|---|---|
| Caducidad relevante | FEFO: sale antes lo que antes caduca |
| Orden de entrada relevante | FIFO: sale antes lo que entró antes |
| Material caducado/no apto | Segregar, retirar y registrar |
| Termolábil | Mantener cadena de frío y control térmico |
| Ruptura de stock | Reposición y alternativa segura |""",
    "drp": """### DRP / PMA / PSA

| Fase o estructura | Clave |
|---|---|
| Análisis de riesgos | Dimensiona medios |
| Activación | Inicio formal |
| Ejecución | Operatividad del dispositivo |
| Desactivación | Cierre parcial o total |
| Memoria | Evaluación y mejora |
| PMA/PSA | Circuito de entrada, asistencia y salida |""",
    "ictus": """### Código Ictus

| Paso | Clave |
|---|---|
| Reconocimiento precoz | Déficit neurológico focal súbito |
| Activación | Aviso/priorización inmediata |
| Traslado | Centro útil |
| Tiempo | Cada minuto cuenta |
| Registro | Hora de inicio o última vez visto bien |""",
    "rcp": """### Cadena de supervivencia

| Eslabón | Acción |
|---|---|
| Reconocer parada | Valorar respuesta y respiración |
| Activar 112 | Pedir ayuda y DEA |
| RCP precoz | Compresiones de calidad |
| Desfibrilación precoz | DEA si indicado |
| SVA y cuidados posteriores | Continuidad asistencial |""",
    "sepsis": """### Sepsis / qSOFA

| Criterio qSOFA | Alarma |
|---|---|
| FR ≥ 22/min | Riesgo |
| PAS ≤ 100 mmHg | Riesgo |
| Alteración mental | Riesgo |
| Sospecha infección + deterioro | Priorizar valoración sanitaria |""",
    "huesos": """### Huesos por región

| Región | Huesos |
|---|---|
| Brazo | Húmero |
| Antebrazo | Radio y cúbito |
| Muslo | Fémur |
| Pierna | Tibia y peroné |
| Mano | Carpo, metacarpianos, falanges |
| Pie | Tarsos, metatarsianos, falanges |""",
    "abdomen": """### Regiones abdominales

| Región | Contenido orientativo |
|---|---|
| Hipocondrio derecho | Hígado y vesícula |
| Epigastrio | Estómago, duodeno, páncreas |
| Hipocondrio izquierdo | Bazo |
| Fosa ilíaca derecha | Apéndice |
| Hipogastrio | Vejiga / pelvis |
| Fosa ilíaca izquierda | Sigma |""",
    "planes": """### Tipos de planes

| Tipo | Ámbito |
|---|---|
| Territorial | Emergencias generales de un territorio |
| Especial | Riesgo concreto |
| Autoprotección | Centro, actividad o instalación |
| DRP | Evento previsible |""",
    "riesgo": """### Riesgo

| Concepto | Significado |
|---|---|
| Riesgo | Probabilidad + daño potencial + vulnerabilidad |
| Peligro | Fuente capaz de causar daño |
| Vulnerabilidad | Debilidad ante el daño |
| Reevaluación | Cambio de escenario = cambio de riesgo |""",
    "imv": """### IMV

| Paso | Acción |
|---|---|
| Seguridad | No aumentar víctimas |
| Sectorización | Caliente, templada, fría |
| Triaje | Priorizar |
| Estabilización mínima | Actuar lo imprescindible |
| Evacuación regulada | Centro útil |""",
    "comunicaciones": """### Comunicaciones

| Regla | Clave |
|---|---|
| Brevedad | ID, ubicación, prioridad y recurso |
| Confirmación | Asegurar recepción |
| Canal común | Evitar caos |
| CCU | Coordina recursos y evacuación |""",
}


def render_forced_tables(q):
    tags = detect_tags(q)
    if tags:
        st.markdown("### Tabla clave para aprender este concepto")
        for tag in tags:
            if tag in TABLES:
                st.markdown(TABLES[tag])
                st.divider()
    table = normalize_text(q.get("cuadro_aprendizaje", "")) or normalize_text(q.get("tabla_esquema", ""))
    if table:
        st.markdown("### Tabla / resumen específico de esta pregunta")
        st.markdown(table)
        st.divider()



def fallback_learning_for_failure(q, selected, correct):
    """Aprendizaje garantizado si el CSV viene pobre o faltan campos."""
    selected_text = option_text(q, selected)
    correct_text = option_text(q, correct)
    tema = normalize_text(q.get("tema", ""))
    subtema = normalize_text(q.get("subtema", ""))
    conceptos = normalize_text(q.get("conceptos_clave", ""))

    st.markdown("### Aprendizaje mínimo garantizado del fallo")
    st.markdown(f"**Respuesta correcta:** {correct}. {correct_text}")

    if selected_text:
        st.markdown(
            f"**Por qué no era {selected}:** marcaste **{selected_text}**, "
            f"pero en este caso el dato que decide la respuesta apunta a **{correct_text}**."
        )

    if tema or subtema:
        st.markdown(f"**Qué debes estudiar aquí:** {tema} · {subtema}")

    if conceptos:
        st.markdown(f"**Conceptos clave:** {conceptos}")

    st.markdown(
        "**Regla de estudio:** no memorices solo la letra correcta; aprende qué dato del enunciado "
        "activa esa respuesta y en qué situación las otras opciones sí podrían ser válidas."
    )

    st.markdown(
        "**Error típico:** elegir una opción que pertenece al mismo tema, pero no al contexto exacto "
        "del caso planteado."
    )

    st.markdown(
        "**Mini-lección:** vuelve a leer el enunciado buscando tres cosas: situación, prioridad y criterio técnico. "
        "La opción correcta debe encajar con las tres."
    )


def render_failure_learning(q, selected, correct):
    """Siempre muestra aprendizaje completo en fallos."""
    show_learning(q, selected, correct)

    # Refuerzo adicional siempre visible para evitar fallos sin explicación útil.
    st.divider()
    fallback_learning_for_failure(q, selected, correct)


def show_learning(q, selected, correct):
    render_forced_tables(q)
    regla = normalize_text(q.get("regla_oro", ""))
    exp = normalize_text(q.get("explicacion", ""))
    if regla:
        st.markdown(f"**Regla de oro:** {regla}")
    if exp:
        st.markdown(f"**Explicación:** {exp}")
    if selected != correct:
        why = why_not(q, selected)
        if why:
            st.markdown(f"**Por qué no {selected}:** {why}")
    st.markdown("**Descarte de distractores:**")
    for L in ["A", "B", "C", "D"]:
        if L != correct:
            text = why_not(q, L)
            if text:
                st.write(f"- **{L}:** {text}")
    for label, key in [
        ("Error típico", "error_tipico"),
        ("Tip de examen", "tip_examen"),
        ("Mini-lección", "minileccion"),
        ("Mnemotecnia", "mnemotecnia"),
    ]:
        value = normalize_text(q.get(key, ""))
        if value:
            st.markdown(f"**{label}:** {value}")


def reset_order(df):
    st.session_state.order = list(range(len(df)))
    random.shuffle(st.session_state.order)
    st.session_state.idx = 0
    st.session_state.answered = False
    st.session_state.selected = None


def current_question(df):
    if not st.session_state.order:
        reset_order(df)
    if st.session_state.idx >= len(st.session_state.order):
        return None
    return df.iloc[st.session_state.order[st.session_state.idx]]


def get_round_targets(total_questions):
    first_daily = (total_questions + 11) // 12
    second_daily = (total_questions + 11) // 12
    return first_daily, second_daily


def user_seen_ids(progress):
    return {str(x.get("id", "")) for x in progress.get("answered", [])}


def user_today_log(progress):
    today = today_str()
    return [x for x in progress.get("answered", []) if str(x.get("timestamp", "")).startswith(today)]


def build_plan(df_all, progress):
    total = len(df_all)
    seen = user_seen_ids(progress)
    wrong = set(progress.get("wrong_ids", []))
    correct = set(progress.get("correct_ids", []))
    unseen_count = max(total - len(seen), 0)
    first_daily, second_daily = get_round_targets(total)

    log = pd.DataFrame(progress.get("answered", []))
    answered_today = len(user_today_log(progress))

    first_round_pct = min(round(len(seen) / total * 100, 1), 100) if total else 0
    second_round_attempts = max(len(progress.get("answered", [])) - total, 0)
    second_round_pct = min(round(second_round_attempts / total * 100, 1), 100) if total else 0

    if len(seen) < total:
        phase = "Vuelta 1"
        daily_goal = first_daily
        new_target = max(daily_goal - answered_today, 0)
    else:
        phase = "Vuelta 2"
        daily_goal = second_daily
        new_target = max(daily_goal - answered_today, 0)

    return {
        "total": total,
        "seen": len(seen),
        "unseen": unseen_count,
        "wrong_pending": len(wrong),
        "correct_seen": len(correct),
        "answered_today": answered_today,
        "phase": phase,
        "daily_goal": daily_goal,
        "remaining_today": new_target,
        "first_round_pct": first_round_pct,
        "second_round_pct": second_round_pct,
    }


def render_login(store):
    st.title("🚑 TES Leixa — Acceso")
    st.caption("Banco v7.11 · fallos con explicación garantizada.")
    username = st.text_input("Usuario").strip().lower()
    password = st.text_input("Contraseña", type="password")
    if st.button("Entrar", use_container_width=True):
        user = auth_user(store, username, password)
        if user:
            st.session_state.logged = True
            st.session_state.uid = username
            st.session_state.display_name = user.get("display_name", username)
            st.session_state.role = user.get("role", "usuario")
            user["last_login"] = now_iso()
            ok, msg = save_store(store, f"Login {username}")
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")
    st.info(f"Persistencia: {st.session_state.persistence_mode}")
    if st.session_state.persistence_mode != "GitHub persistente":
        st.warning("Persistencia temporal: si no configuras GitHub Secrets, al reiniciar Streamlit se pueden perder sesiones/progreso.")


def render_plan_dashboard(df_all, progress):
    plan = build_plan(df_all, progress)
    st.subheader("🎯 Plan 12 + 12 días")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Fase actual", plan["phase"])
    c2.metric("Objetivo diario", plan["daily_goal"])
    c3.metric("Hechas hoy", plan["answered_today"])
    c4.metric("Pendientes hoy", plan["remaining_today"])

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("Vuelta 1", f"{plan['first_round_pct']}%")
    c6.metric("Vuelta 2", f"{plan['second_round_pct']}%")
    c7.metric("No vistas", plan["unseen"])
    c8.metric("Fallos pendientes", plan["wrong_pending"])

    st.progress(plan["first_round_pct"] / 100 if plan["phase"] == "Vuelta 1" else plan["second_round_pct"] / 100)
    st.info("Modo recomendado: primero completa 'Solo no respondidas'. Después trabaja 'Solo mis fallos' y dificultad alta/filtro_10.")


def render_test(store, df_all):
    uid = st.session_state.uid
    progress = get_progress(store, uid)

    with st.sidebar:
        st.caption(f"Usuario: {st.session_state.display_name}")
        st.caption(f"Rol: {st.session_state.role}")
        st.caption(f"Persistencia: {st.session_state.persistence_mode}")
        st.caption(f"Preguntas: {len(df_all)}")

        mode = st.radio(
            "Modo estudio",
            ["Plan de hoy", "Solo no respondidas", "Solo mis fallos", "Dificultad alta/filtro_10", "Libre"],
            index=0,
        )

        modules = ["Todos"] + sorted([x for x in df_all["modulo"].unique() if str(x).strip()])
        module = st.selectbox("Módulo", modules)
        difficulties = ["Todas"] + sorted([x for x in df_all["nivel_dificultad"].unique() if str(x).strip()])
        difficulty = st.selectbox("Dificultad", difficulties)

        if st.button("Reiniciar bloque", use_container_width=True):
            st.session_state.order = []
            st.rerun()

        if st.button("Cerrar sesión", use_container_width=True):
            st.session_state.logged = False
            st.rerun()

    render_plan_dashboard(df_all, progress)

    df = df_all.copy()
    if module != "Todos":
        df = df[df["modulo"] == module]
    if difficulty != "Todas":
        df = df[df["nivel_dificultad"] == difficulty]

    seen = user_seen_ids(progress)
    wrong = set(progress.get("wrong_ids", []))

    if mode == "Solo no respondidas":
        df = df[~df["id"].isin(seen)]
    elif mode == "Solo mis fallos":
        df = df[df["id"].isin(wrong)]
    elif mode == "Dificultad alta/filtro_10":
        df = df[df["nivel_dificultad"].str.lower().str.contains("alta|filtro_10", na=False)]
    elif mode == "Plan de hoy":
        plan = build_plan(df_all, progress)
        if plan["phase"] == "Vuelta 1":
            df_unseen = df[~df["id"].isin(seen)]
            df_wrong = df[df["id"].isin(wrong)]
            df_high = df[df["nivel_dificultad"].str.lower().str.contains("alta|filtro_10", na=False)]
            df = pd.concat([df_wrong, df_unseen, df_high]).drop_duplicates(subset=["id"])
        else:
            df_wrong = df[df["id"].isin(wrong)]
            df_high = df[df["nivel_dificultad"].str.lower().str.contains("alta|filtro_10", na=False)]
            df_seen = df[df["id"].isin(seen)]
            df = pd.concat([df_wrong, df_high, df_seen]).drop_duplicates(subset=["id"])

    df = df.reset_index(drop=True)
    filter_key = f"{mode}|{module}|{difficulty}|{len(df)}|{len(progress.get('answered', []))}"
    if st.session_state.last_filter != filter_key:
        st.session_state.last_filter = filter_key
        reset_order(df)

    if df.empty:
        st.warning("No hay preguntas con esos filtros.")
        return

    q = current_question(df)
    if q is None:
        st.success("Bloque terminado.")
        if st.button("Empezar otro bloque", use_container_width=True):
            reset_order(df)
            st.rerun()
        return

    st.divider()
    st.write(f"**Pregunta {st.session_state.idx + 1} de {len(st.session_state.order)}**")
    st.caption(f"{normalize_text(q.get('id'))} · {normalize_text(q.get('modulo'))} · {normalize_text(q.get('tema'))} · {normalize_text(q.get('nivel_dificultad'))}")
    st.markdown(f"### {normalize_text(q.get('enunciado'))}")

    correct = normalize_text(q.get("respuesta_correcta")).upper()

    for L in ["A", "B", "C", "D"]:
        if st.button(f"{L}. {option_text(q, L)}", key=f"{L}_{st.session_state.idx}_{normalize_text(q.get('id'))}", use_container_width=True, disabled=st.session_state.answered):
            st.session_state.selected = L
            st.session_state.answered = True
            ok = L == correct
            qid = normalize_text(q.get("id"))
            entry = {
                "timestamp": now_iso(),
                "id": qid,
                "modulo": normalize_text(q.get("modulo")),
                "tema": normalize_text(q.get("tema")),
                "subtema": normalize_text(q.get("subtema")),
                "dificultad": normalize_text(q.get("nivel_dificultad")),
                "tipo": normalize_text(q.get("tipo_pregunta")),
                "respuesta_usuario": L,
                "respuesta_correcta": correct,
                "correcta": int(ok),
            }
            progress["answered"].append(entry)
            if ok:
                if qid not in progress["correct_ids"]:
                    progress["correct_ids"].append(qid)
                if qid in progress["wrong_ids"]:
                    progress["wrong_ids"].remove(qid)
            else:
                if qid not in progress["wrong_ids"]:
                    progress["wrong_ids"].append(qid)
            save_store(store, f"Progreso {uid} {qid}")
            st.rerun()

    log = pd.DataFrame(progress.get("answered", []))
    total_answered = len(log)
    ok_count = int(log["correcta"].sum()) if not log.empty else 0
    bad_count = total_answered - ok_count
    c1, c2, c3 = st.columns(3)
    c1.metric("Mis aciertos", ok_count)
    c2.metric("Mis fallos", bad_count)
    c3.metric("Fallos pendientes", len(progress.get("wrong_ids", [])))

    if st.session_state.answered:
        selected = st.session_state.selected
        if selected == correct:
            st.success("Correcto.")
            st.info("Correcta: queda dominada y no entra en repaso de fallos.")
        else:
            st.error(f"Incorrecto. Respuesta correcta: {correct}. {option_text(q, correct)}")
            st.warning("Esta pregunta entra en 'Solo mis fallos' y aquí tienes el aprendizaje completo.")
            with st.expander("Aprendizaje profundo del fallo", expanded=True):
                render_failure_learning(q, selected, correct)

        if st.button("Siguiente pregunta", use_container_width=True):
            st.session_state.idx += 1
            st.session_state.answered = False
            st.session_state.selected = None
            st.rerun()


def render_stats(store, df_all):
    uid = st.session_state.uid
    progress = get_progress(store, uid)
    log = pd.DataFrame(progress.get("answered", []))

    st.header("📊 Estadísticas y planning")
    render_plan_dashboard(df_all, progress)

    total_answered = len(log)
    ok = int(log["correcta"].sum()) if not log.empty else 0
    bad = total_answered - ok
    pct = round(ok / total_answered * 100, 1) if total_answered else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Respondidas", total_answered)
    c2.metric("Aciertos", ok)
    c3.metric("Fallos", bad)
    c4.metric("% acierto", pct)

    if log.empty:
        st.info("Todavía no hay respuestas registradas.")
        return

    st.subheader("Rendimiento por módulo")
    mod = log.groupby("modulo").agg(preguntas=("id", "count"), aciertos=("correcta", "sum")).reset_index()
    mod["fallos"] = mod["preguntas"] - mod["aciertos"]
    mod["% acierto"] = (mod["aciertos"] / mod["preguntas"] * 100).round(1)
    st.dataframe(mod.sort_values("% acierto"), use_container_width=True, hide_index=True)

    st.subheader("Subtemas débiles")
    weak = log.groupby(["modulo", "tema", "subtema"]).agg(preguntas=("id", "count"), aciertos=("correcta", "sum")).reset_index()
    weak["fallos"] = weak["preguntas"] - weak["aciertos"]
    weak["% acierto"] = (weak["aciertos"] / weak["preguntas"] * 100).round(1)
    weak = weak[(weak["preguntas"] >= 2) & (weak["% acierto"] < 90)].sort_values("% acierto")
    st.dataframe(weak.head(30), use_container_width=True, hide_index=True)

    st.download_button("Descargar mi progreso CSV", log.to_csv(index=False).encode("utf-8-sig"), f"progreso_{uid}.csv", "text/csv", use_container_width=True)


def render_account(store):
    uid = st.session_state.uid
    user = store["users"][uid]

    st.header("👤 Mi cuenta")
    st.write(f"Usuario: **{uid}**")
    st.write(f"Rol: **{user.get('role', 'usuario')}**")
    st.write(f"Persistencia: **{st.session_state.persistence_mode}**")

    name = st.text_input("Nombre visible", value=user.get("display_name", uid))
    if st.button("Guardar nombre", use_container_width=True):
        user["display_name"] = name.strip() or uid
        st.session_state.display_name = user["display_name"]
        user["updated_at"] = now_iso()
        ok, msg = save_store(store, f"Cambia nombre {uid}")
        st.success(msg)

    st.subheader("Cambiar contraseña")
    old = st.text_input("Contraseña actual", type="password")
    new = st.text_input("Nueva contraseña", type="password")
    new2 = st.text_input("Repetir nueva contraseña", type="password")
    if st.button("Actualizar contraseña", use_container_width=True):
        if new != new2:
            st.error("Las contraseñas nuevas no coinciden.")
        elif len(new) < 4:
            st.error("La nueva contraseña debe tener al menos 4 caracteres.")
        elif hash_password(old, user["salt"]) != user["password_hash"]:
            st.error("Contraseña actual incorrecta.")
        else:
            salt = hashlib.sha256((uid + now_iso()).encode("utf-8")).hexdigest()[:16]
            user["salt"] = salt
            user["password_hash"] = hash_password(new, salt)
            user["must_change_password"] = False
            user["updated_at"] = now_iso()
            ok, msg = save_store(store, f"Cambia contraseña {uid}")
            st.success(msg)


def render_admin(store):
    if st.session_state.role != "administrador":
        st.warning("Solo administrador.")
        return

    st.header("🛠️ Administración")
    rows = []
    for uid, user in store.get("users", {}).items():
        progress = get_progress(store, uid)
        rows.append({
            "usuario": uid,
            "nombre": user.get("display_name", ""),
            "rol": user.get("role", ""),
            "activo": user.get("active", False),
            "respondidas": len(progress.get("answered", [])),
            "fallos_pendientes": len(progress.get("wrong_ids", [])),
            "ultimo_login": user.get("last_login", ""),
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    st.download_button("Descargar user_store.json", json.dumps(store, ensure_ascii=False, indent=2).encode("utf-8"), "user_store.json", "application/json", use_container_width=True)


init_state()

# v7.03: arranque ultrarrápido.
# No lee GitHub ni carga el banco antes de pintar la pantalla.
if st.session_state.store is None:
    st.session_state.store = load_local_store()
    st.session_state.persistence_mode = "Arranque local rápido"

store = st.session_state.store

if not st.session_state.logged:
    st.title("🚑 TES Leixa — Acceso")
    st.caption("Banco v7.11 · fallos con explicación garantizada.")
    st.info("La app ya está arrancada. Entra con tu usuario para cargar banco y progreso.")
    render_login(store)
    st.stop()

# Después de entrar, intenta sincronizar persistencia real si está configurada.
if st.session_state.persistence_mode != "GitHub persistente" and github_configured():
    try:
        st.session_state.store = load_store()
        store = st.session_state.store
    except Exception:
        pass

try:
    df_all = load_questions(str(get_data_path()))
except Exception as exc:
    st.error("No se pudo cargar el banco de preguntas.")
    st.code(str(exc))
    st.stop()

st.title("🚑 TES Leixa — Test táctil")
st.caption("Banco v7.11 · fallos con explicación garantizada.")

tabs = ["📝 Test táctil", "📊 Estadísticas y planning", "👤 Mi cuenta"]
if st.session_state.role == "administrador":
    tabs.append("🛠️ Administración")

tab_objs = st.tabs(tabs)

with tab_objs[0]:
    render_test(store, df_all)
with tab_objs[1]:
    render_stats(store, df_all)
with tab_objs[2]:
    render_account(store)
if st.session_state.role == "administrador":
    with tab_objs[3]:
        render_admin(store)
