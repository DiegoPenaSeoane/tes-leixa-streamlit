
import base64
import hashlib
import json
import random
import urllib.error
import urllib.request
from datetime import datetime, timezone, date
from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(page_title="TES Leixa — Test táctil", page_icon="🚑", layout="wide")

BANK_PATHS = [
    Path("data/tes_leixa_banco_v653_streamlit_ready.csv.gz"),
    Path("tes_leixa_banco_v653_streamlit_ready.csv.gz"),
]
STORE_PATHS = [
    Path("data/user_store.json"),
    Path("user_store.json"),
]
OPTION_COLS = {"A": "opcion_a", "B": "opcion_b", "C": "opcion_c", "D": "opcion_d"}
VERSION_LABEL = "Banco v7.12 · rescate final: fallos explicados y guardado verificado."


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def n(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def hp(password, salt):
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


def default_store():
    def make_user(username, display_name, password, role, must_change):
        salt = hashlib.sha256((username + password + "tes-leixa-v712").encode("utf-8")).hexdigest()[:16]
        return {
            "display_name": display_name,
            "salt": salt,
            "password_hash": hp(password, salt),
            "role": role,
            "active": True,
            "must_change_password": must_change,
            "created_at": now_iso(),
            "updated_at": now_iso(),
        }

    users = {
        "diego": make_user("diego", "Diego", "tes2026", "administrador", False),
        "anton": make_user("anton", "Anton", "1234", "usuario", True),
        "melisa": make_user("melisa", "Melisa", "1111", "usuario", True),
        "elvira": make_user("elvira", "Elvira", "2222", "usuario", True),
        "lucia": make_user("lucia", "Lucia", "3333", "usuario", True),
    }
    return {
        "schema_version": "2.0",
        "updated_at": now_iso(),
        "users": users,
        "progress": {
            uid: {
                "answered": [],
                "wrong_ids": [],
                "correct_ids": [],
                "settings": {
                    "daily_goal": 142,
                    "target_pct": 90,
                    "study_days_first_round": 12,
                    "study_days_second_round": 12,
                },
                "last_save_status": "",
            }
            for uid in users
        },
    }


def ensure_store(store):
    base = default_store()
    store.setdefault("schema_version", "2.0")
    store.setdefault("updated_at", now_iso())
    store.setdefault("users", {})
    store.setdefault("progress", {})
    for uid, u in base["users"].items():
        store["users"].setdefault(uid, u)
    for uid in store["users"]:
        store["progress"].setdefault(uid, {})
        p = store["progress"][uid]
        p.setdefault("answered", [])
        p.setdefault("wrong_ids", [])
        p.setdefault("correct_ids", [])
        p.setdefault("settings", {"daily_goal": 142, "target_pct": 90, "study_days_first_round": 12, "study_days_second_round": 12})
        p.setdefault("last_save_status", "")
    return store


def local_store():
    for path in STORE_PATHS:
        try:
            if path.exists():
                return ensure_store(json.loads(path.read_text(encoding="utf-8")))
        except Exception:
            pass
    return default_store()


def gh_configured():
    return all(k in st.secrets for k in ["GITHUB_TOKEN", "GITHUB_REPO"])


def gh_headers():
    return {
        "Authorization": f"Bearer {st.secrets['GITHUB_TOKEN']}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def gh_path():
    return st.secrets.get("GITHUB_STORE_PATH", "data/user_store.json")


def gh_branch():
    return st.secrets.get("GITHUB_BRANCH", "main")


def gh_repo():
    return st.secrets["GITHUB_REPO"]


def gh_read():
    url = f"https://api.github.com/repos/{gh_repo()}/contents/{gh_path()}?ref={gh_branch()}"
    req = urllib.request.Request(url, headers=gh_headers(), method="GET")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        content = base64.b64decode(payload["content"]).decode("utf-8")
        return ensure_store(json.loads(content)), payload.get("sha")
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None, None
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"GitHub READ HTTP {exc.code}: {detail[:500]}")
    except Exception as exc:
        raise RuntimeError(f"GitHub READ error: {exc}")


def gh_write(store, sha=None, message="TES Leixa guarda progreso"):
    raw = json.dumps(store, ensure_ascii=False, indent=2)
    body = {
        "message": message,
        "content": base64.b64encode(raw.encode("utf-8")).decode("ascii"),
        "branch": gh_branch(),
    }
    if sha:
        body["sha"] = sha
    url = f"https://api.github.com/repos/{gh_repo()}/contents/{gh_path()}"
    req = urllib.request.Request(url, headers=gh_headers(), data=json.dumps(body).encode("utf-8"), method="PUT")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        return payload.get("content", {}).get("sha")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"GitHub WRITE HTTP {exc.code}: {detail[:700]}")
    except Exception as exc:
        raise RuntimeError(f"GitHub WRITE error: {exc}")


def load_store():
    st.session_state.persistence_mode = "Temporal"
    st.session_state.persistence_error = ""
    st.session_state.store_sha = None

    if gh_configured():
        try:
            store, sha = gh_read()
            if store is None:
                # Si no existe en GitHub, lo crea.
                store = local_store()
                sha = gh_write(store, None, "Inicializa user_store TES Leixa")
            st.session_state.store_sha = sha
            st.session_state.persistence_mode = "GitHub persistente"
            return store
        except Exception as exc:
            st.session_state.persistence_error = str(exc)
            st.session_state.persistence_mode = "ERROR GitHub: usando temporal"
            return local_store()

    st.session_state.persistence_error = "Faltan Secrets GITHUB_TOKEN o GITHUB_REPO."
    return local_store()


def save_store(store, message):
    store["updated_at"] = now_iso()
    st.session_state.store = store
    if gh_configured():
        try:
            new_sha = gh_write(store, st.session_state.get("store_sha"), message)
            st.session_state.store_sha = new_sha
            st.session_state.persistence_mode = "GitHub persistente"
            st.session_state.last_save = "OK GitHub " + now_iso()
            return True, st.session_state.last_save
        except Exception as exc:
            st.session_state.persistence_error = str(exc)
            st.session_state.last_save = "ERROR GitHub: " + str(exc)
            return False, st.session_state.last_save
    st.session_state.last_save = "TEMPORAL: faltan Secrets"
    return False, st.session_state.last_save


def bank_path():
    for path in BANK_PATHS:
        if path.exists():
            return path
    return BANK_PATHS[0]


@st.cache_data(show_spinner=False)
def load_bank(path_str):
    path = Path(path_str)
    if not path.exists():
        raise FileNotFoundError(f"No encuentro el banco en {path_str}")
    comp = "gzip" if path.suffix == ".gz" else None
    df = pd.read_csv(path, dtype=str, encoding="utf-8-sig", compression=comp).fillna("")
    df.columns = [str(c).strip() for c in df.columns]
    needed = [
        "id", "modulo", "tema", "subtema", "nivel_dificultad", "tipo_pregunta",
        "enunciado", "opcion_a", "opcion_b", "opcion_c", "opcion_d", "respuesta_correcta",
        "explicacion", "porque_no_a", "porque_no_b", "porque_no_c", "porque_no_d",
        "regla_oro", "error_tipico", "tip_examen", "minileccion", "mnemotecnia",
        "tabla_esquema", "conceptos_clave", "estado_app",
    ]
    for col in needed:
        if col not in df.columns:
            df[col] = ""
    if "cuadro_aprendizaje" not in df.columns:
        df["cuadro_aprendizaje"] = df["tabla_esquema"]
    df["respuesta_correcta"] = df["respuesta_correcta"].str.upper().str.strip()
    df = df[df["respuesta_correcta"].isin(["A", "B", "C", "D"])].copy()
    return df.reset_index(drop=True)


def init():
    defaults = {
        "store": None,
        "store_sha": None,
        "persistence_mode": "Temporal",
        "persistence_error": "",
        "last_save": "",
        "logged": False,
        "uid": "",
        "role": "",
        "display_name": "",
        "order": [],
        "idx": 0,
        "answered": False,
        "selected": None,
        "last_filter": "",
    }
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)


def progress(store, uid):
    store = ensure_store(store)
    return store["progress"][uid]


def authenticate(store, username, password):
    uid = username.strip().lower()
    user = store.get("users", {}).get(uid)
    if not user or not user.get("active", False):
        return None
    if hp(password, user["salt"]) == user["password_hash"]:
        return user
    return None


def option(q, letter):
    return n(q.get(OPTION_COLS[letter], ""))


def why(q, letter):
    return n(q.get(f"porque_no_{letter.lower()}", ""))


def detect_table(q):
    blob = " ".join(n(q.get(k, "")) for k in ["enunciado", "tema", "subtema", "conceptos_clave", "tabla_esquema"]).lower()
    if "glasgow" in blob or "retira al dolor" in blob:
        return """### Glasgow

| Puntos | Ocular | Verbal | Motora |
|---:|---|---|---|
| 6 | — | — | Obedece órdenes |
| 5 | — | Orientado | Localiza dolor |
| 4 | Espontánea | Confuso | Retira al dolor |
| 3 | Al habla | Palabras inapropiadas | Flexión anormal |
| 2 | Al dolor | Sonidos incomprensibles | Extensión anormal |
| 1 | Ninguna | Ninguna | Ninguna |

**Regla:** O + V + M. Retira dolor = M4; localiza dolor = M5."""
    if "start" in blob or "triaje" in blob:
        return """### START

| Criterio | Prioridad |
|---|---|
| Camina | Verde inicial |
| No respira tras abrir vía aérea | Negro |
| Respira tras abrir vía aérea | Rojo |
| FR > 30 | Rojo |
| Perfusión alterada | Rojo |
| No obedece órdenes | Rojo |
| Resto no ambulante estable | Amarillo |"""
    if "fefo" in blob or "fifo" in blob or "stock" in blob or "caduc" in blob:
        return """### Stock

| Caso | Regla |
|---|---|
| Caducidad manda | FEFO |
| Entrada manda | FIFO |
| Caducado/no apto | retirar y registrar |
| Termolábil | cadena de frío |
| Ruptura | reposición/alternativa segura |"""
    return ""


def render_failure_explanation(q, selected, correct):
    """Explicación completa obligatoria en TODOS los fallos."""
    selected_text = option(q, selected)
    correct_text = option(q, correct)

    st.markdown("## Aprendizaje del fallo")
    st.markdown(f"### Respuesta correcta: **{correct}. {correct_text}**")
    st.markdown(f"**Tu respuesta:** {selected}. {selected_text}")

    table = n(q.get("cuadro_aprendizaje", "")) or n(q.get("tabla_esquema", "")) or detect_table(q)
    if table:
        st.markdown("### Tabla / esquema para aprenderlo")
        st.markdown(table)

    exp = n(q.get("explicacion", ""))
    if exp:
        st.markdown("### Explicación")
        st.markdown(exp)
    else:
        st.markdown("### Explicación")
        st.markdown(
            f"La opción correcta es **{correct_text}**. La clave es identificar el dato técnico del enunciado "
            f"y relacionarlo con el concepto concreto de **{n(q.get('tema',''))} / {n(q.get('subtema',''))}**."
        )

    why_selected = why(q, selected)
    st.markdown("### Por qué fallaste")
    if why_selected:
        st.markdown(why_selected)
    else:
        st.markdown(
            f"**{selected_text}** puede sonar plausible porque pertenece al mismo entorno de estudio, "
            f"pero no responde al criterio concreto que pide el enunciado. En esta pregunta manda **{correct_text}**."
        )

    st.markdown("### Descarte de distractores")
    any_why = False
    for L in ["A", "B", "C", "D"]:
        if L == correct:
            continue
        txt = why(q, L)
        if txt:
            any_why = True
            st.write(f"- **{L}. {option(q, L)}:** {txt}")
    if not any_why:
        for L in ["A", "B", "C", "D"]:
            if L != correct:
                st.write(f"- **{L}. {option(q, L)}:** distractor cercano, pero no cumple el criterio exacto del caso.")

    st.markdown("### Regla de oro")
    regla = n(q.get("regla_oro", ""))
    st.markdown(regla if regla else "Ubica primero el contexto del caso y después aplica el criterio técnico exacto.")

    st.markdown("### Error típico")
    err = n(q.get("error_tipico", ""))
    st.markdown(err if err else "Elegir una opción que pertenece al mismo tema, pero no al dato diferencial de la pregunta.")

    st.markdown("### Tip de examen")
    tip = n(q.get("tip_examen", ""))
    st.markdown(tip if tip else "Subraya palabras clave del enunciado: fase, prioridad, estructura, signo clínico, zona o criterio numérico.")

    st.markdown("### Mini-lección")
    mini = n(q.get("minileccion", ""))
    st.markdown(mini if mini else "Convierte este fallo en una regla: concepto → criterio que lo define → caso donde se aplica → trampa habitual.")

    mn = n(q.get("mnemotecnia", ""))
    if mn:
        st.markdown("### Mnemotecnia")
        st.markdown(mn)

    conceptos = n(q.get("conceptos_clave", ""))
    if conceptos:
        st.markdown("### Conceptos clave")
        st.markdown(conceptos)


def reset_order(df):
    st.session_state.order = list(range(len(df)))
    random.shuffle(st.session_state.order)
    st.session_state.idx = 0
    st.session_state.answered = False
    st.session_state.selected = None


def seen_ids(p):
    return {str(x.get("id", "")) for x in p.get("answered", [])}


def plan_stats(df, p):
    total = len(df)
    seen = len(seen_ids(p))
    daily = (total + 11) // 12
    return {
        "total": total,
        "seen": seen,
        "unseen": max(total - seen, 0),
        "wrong": len(p.get("wrong_ids", [])),
        "daily": daily,
        "vuelta1": min(round(seen / total * 100, 1), 100) if total else 0,
    }


def login_screen(store):
    st.title("🚑 TES Leixa — Acceso")
    st.caption(VERSION_LABEL)
    st.info(f"Persistencia: {st.session_state.persistence_mode}")
    if st.session_state.persistence_error:
        st.error("Error de persistencia: " + st.session_state.persistence_error)

    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Entrar", use_container_width=True):
        user = authenticate(store, username, password)
        if user:
            uid = username.strip().lower()
            st.session_state.logged = True
            st.session_state.uid = uid
            st.session_state.role = user.get("role", "usuario")
            st.session_state.display_name = user.get("display_name", uid)
            user["last_login"] = now_iso()
            ok, msg = save_store(store, f"Login {uid}")
            st.session_state.last_save = msg
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")


def app_screen(store, df):
    uid = st.session_state.uid
    p = progress(store, uid)

    st.title("🚑 TES Leixa — Test táctil")
    st.caption(VERSION_LABEL)

    if st.session_state.persistence_mode != "GitHub persistente":
        st.error("ATENCIÓN: la persistencia NO está en GitHub. El progreso puede perderse.")
        if st.session_state.persistence_error:
            st.code(st.session_state.persistence_error)
    else:
        st.success("Persistencia: GitHub persistente")

    tabs = st.tabs(["📝 Test", "📊 Estadísticas", "👤 Cuenta", "🛠️ Diagnóstico"])

    with tabs[0]:
        stats = plan_stats(df, p)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Banco", stats["total"])
        c2.metric("Vistas", stats["seen"])
        c3.metric("No vistas", stats["unseen"])
        c4.metric("Fallos pendientes", stats["wrong"])

        with st.sidebar:
            st.write(f"Usuario: **{st.session_state.display_name}**")
            st.write(f"Persistencia: **{st.session_state.persistence_mode}**")
            mode = st.radio("Modo", ["Plan de hoy", "Solo no respondidas", "Solo mis fallos", "Alta/filtro_10", "Libre"])
            modules = ["Todos"] + sorted([x for x in df["modulo"].unique() if str(x).strip()])
            module = st.selectbox("Módulo", modules)
            if st.button("Reiniciar bloque"):
                st.session_state.order = []
                st.rerun()
            if st.button("Cerrar sesión"):
                st.session_state.logged = False
                st.rerun()

        work = df.copy()
        if module != "Todos":
            work = work[work["modulo"] == module]

        seen = seen_ids(p)
        wrong = set(p.get("wrong_ids", []))

        if mode == "Solo no respondidas":
            work = work[~work["id"].isin(seen)]
        elif mode == "Solo mis fallos":
            work = work[work["id"].isin(wrong)]
        elif mode == "Alta/filtro_10":
            work = work[work["nivel_dificultad"].str.lower().str.contains("alta|filtro_10", na=False)]
        elif mode == "Plan de hoy":
            w1 = work[work["id"].isin(wrong)]
            w2 = work[~work["id"].isin(seen)]
            w3 = work[work["nivel_dificultad"].str.lower().str.contains("alta|filtro_10", na=False)]
            work = pd.concat([w1, w2, w3]).drop_duplicates("id")

        work = work.reset_index(drop=True)
        key = f"{mode}|{module}|{len(work)}|{len(p.get('answered', []))}"
        if st.session_state.last_filter != key:
            st.session_state.last_filter = key
            reset_order(work)

        if work.empty:
            st.warning("No hay preguntas con esos filtros.")
            return

        if not st.session_state.order:
            reset_order(work)

        if st.session_state.idx >= len(st.session_state.order):
            st.success("Bloque terminado.")
            if st.button("Nuevo bloque"):
                reset_order(work)
                st.rerun()
            return

        q = work.iloc[st.session_state.order[st.session_state.idx]]
        corr = n(q.get("respuesta_correcta")).upper()

        st.divider()
        st.write(f"**Pregunta {st.session_state.idx + 1} de {len(st.session_state.order)}**")
        st.caption(f"{n(q.get('id'))} · {n(q.get('modulo'))} · {n(q.get('tema'))} · {n(q.get('nivel_dificultad'))}")
        st.markdown(f"### {n(q.get('enunciado'))}")

        for L in ["A", "B", "C", "D"]:
            if st.button(f"{L}. {option(q, L)}", key=f"{L}_{st.session_state.idx}_{n(q.get('id'))}", use_container_width=True, disabled=st.session_state.answered):
                st.session_state.selected = L
                st.session_state.answered = True
                qid = n(q.get("id"))
                ok = L == corr
                entry = {
                    "timestamp": now_iso(),
                    "id": qid,
                    "modulo": n(q.get("modulo")),
                    "tema": n(q.get("tema")),
                    "subtema": n(q.get("subtema")),
                    "dificultad": n(q.get("nivel_dificultad")),
                    "respuesta_usuario": L,
                    "respuesta_correcta": corr,
                    "correcta": int(ok),
                }
                p["answered"].append(entry)
                if ok:
                    if qid not in p["correct_ids"]:
                        p["correct_ids"].append(qid)
                    if qid in p["wrong_ids"]:
                        p["wrong_ids"].remove(qid)
                else:
                    if qid not in p["wrong_ids"]:
                        p["wrong_ids"].append(qid)
                ok_save, msg = save_store(store, f"Progreso {uid} {qid}")
                p["last_save_status"] = msg
                st.rerun()

        if st.session_state.answered:
            selected = st.session_state.selected
            if selected == corr:
                st.success("Correcto. Esta pregunta queda dominada y no entra en repaso de fallos.")
            else:
                st.error(f"Incorrecto. Correcta: {corr}. {option(q, corr)}")
                st.warning("Esta pregunta entra en 'Solo mis fallos'.")
                render_failure_explanation(q, selected, corr)

            if st.button("Siguiente pregunta", use_container_width=True):
                st.session_state.idx += 1
                st.session_state.answered = False
                st.session_state.selected = None
                st.rerun()

    with tabs[1]:
        log = pd.DataFrame(p.get("answered", []))
        st.subheader("Progreso")
        st.write(f"Respondidas: **{len(log)}**")
        if not log.empty:
            ok = int(log["correcta"].sum())
            st.write(f"Aciertos: **{ok}**")
            st.write(f"Fallos: **{len(log)-ok}**")
            st.write(f"% acierto: **{round(ok/len(log)*100,1)}%**")
            st.dataframe(log.tail(100), use_container_width=True, hide_index=True)

    with tabs[2]:
        st.subheader("Mi cuenta")
        st.write(f"Usuario: **{uid}**")
        st.write(f"Rol: **{st.session_state.role}**")
        st.write(f"Último guardado: {st.session_state.get('last_save','')}")
        st.write(f"Persistencia: **{st.session_state.persistence_mode}**")

    with tabs[3]:
        st.subheader("Diagnóstico")
        st.write("Versión:", VERSION_LABEL)
        st.write("Banco usado:", str(bank_path()))
        st.write("Preguntas cargadas:", len(df))
        st.write("Persistencia:", st.session_state.persistence_mode)
        st.write("Último guardado:", st.session_state.get("last_save", ""))
        if st.session_state.persistence_error:
            st.error(st.session_state.persistence_error)
        st.write("Secrets detectados:", "GITHUB_TOKEN" in st.secrets and "GITHUB_REPO" in st.secrets)
        st.write("Repo configurado:", st.secrets.get("GITHUB_REPO", "(sin repo)") if "GITHUB_REPO" in st.secrets else "(sin repo)")


init()
if st.session_state.store is None:
    st.session_state.store = load_store()

store = st.session_state.store

if not st.session_state.logged:
    login_screen(store)
    st.stop()

try:
    df_all = load_bank(str(bank_path()))
except Exception as exc:
    st.error("No se pudo cargar el banco.")
    st.code(str(exc))
    st.stop()

app_screen(store, df_all)
