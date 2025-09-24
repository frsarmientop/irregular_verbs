import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Irregular Verbs Quiz", page_icon="📚")

@st.cache_data
def load_data():
    return pd.read_csv("irregular_verbs.csv")

verbs = load_data()

# ----- Estado de sesión -----
if "score" not in st.session_state:
    st.session_state.score = 0
if "total" not in st.session_state:
    st.session_state.total = 0  # preguntas realizadas
if "finished" not in st.session_state:
    st.session_state.finished = False
if "current" not in st.session_state:
    st.session_state.current = None
if "input_key" not in st.session_state:
    st.session_state.input_key = 0
if "awaiting_answer" not in st.session_state:
    st.session_state.awaiting_answer = True
if "hint_type" not in st.session_state:
    st.session_state.hint_type = "present"
if "asked_indices" not in st.session_state:
    st.session_state.asked_indices = set()

MAX_QUESTIONS = 10

def new_question():
    """Selecciona un verbo aleatorio que no haya sido usado y una pista aleatoria."""
    # si ya se hicieron 10 preguntas, marcar finalizado
    if st.session_state.total >= MAX_QUESTIONS:
        st.session_state.finished = True
        return
    # seleccionar un verbo que no se haya preguntado
    remaining = set(range(len(verbs))) - st.session_state.asked_indices
    if not remaining:
        st.session_state.finished = True
        return
    idx = random.choice(list(remaining))
    st.session_state.asked_indices.add(idx)
    row = verbs.iloc[idx]
    st.session_state.current = {
        "present": row["Present"],
        "past": row["Past"],
        "past_participle": row["Past Participle"]
    }
    st.session_state.hint_type = random.choice(["present", "past", "past_participle"])
    st.session_state.awaiting_answer = True
    st.session_state.input_key += 1
    st.session_state.total += 1

# ----- UI -----
st.title("Irregular Verbs Quiz")

if st.session_state.finished:
    st.success(f"Juego terminado. Puntaje final: {st.session_state.score}/{st.session_state.total}")
    if st.button("Reiniciar"):
        for k in ["score", "total", "finished", "current", "asked_indices"]:
            st.session_state[k] = 0 if k in ["score", "total"] else (False if k=="finished" else None if k=="current" else set())
        st.session_state.input_key = 0
        new_question()
else:
    if st.session_state.current is None:
        new_question()

    if st.session_state.current:
        hint_type = st.session_state.hint_type
        answer_type = "present" if hint_type != "present" else "past"

        st.write(f"Completa la forma **{answer_type}** del verbo dado en {hint_type}:")
        st.write(f"Pista: **{st.session_state.current[hint_type]}**")

        user_answer = st.text_input("Tu respuesta:", key=st.session_state.input_key)

        if st.button("Comprobar") and st.session_state.awaiting_answer:
            correct = st.session_state.current[answer_type]
            if user_answer.strip().lower() == correct.lower():
                st.session_state.score += 1
                st.success("Correcto!")
            else:
                st.error(f"Incorrecto. La respuesta correcta es {correct}.")
            st.session_state.awaiting_answer = False

        # Botones de control
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Siguiente pregunta") and not st.session_state.awaiting_answer:
                new_question()
        with col2:
            if st.button("Terminar"):
                st.session_state.finished = True

        st.write(f"Puntaje: {st.session_state.score}/{st.session_state.total}")
