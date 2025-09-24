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
    st.session_state.total = 0
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

def new_question():
    """Selecciona un verbo aleatorio y una pista aleatoria."""
    idx = random.randint(0, len(verbs) - 1)
    row = verbs.iloc[idx]
    st.session_state.current = {
        "present": row["present"],
        "past": row["past"],
        "translation": row.get("translation", "")
    }
    st.session_state.hint_type = random.choice(["present", "translation", "past"])
    st.session_state.input_key += 1
    st.session_state.awaiting_answer = True
    st.session_state.feedback = ""
    st.session_state.translation = ""

def check_answer():
    verb = st.session_state.current
    answer = st.session_state[f"answer_{st.session_state.input_key}"]
    st.session_state.total += 1
    st.session_state.awaiting_answer = False
    if answer.strip().lower() == verb["past"].lower():
        st.session_state.score += 1
        st.session_state.feedback = "✅ ¡Correcto!"
    elif answer.strip().lower() == verb["present"].lower():
        st.session_state.score += 1
        st.session_state.feedback = "✅ ¡Correcto!"
    else:
        st.session_state.feedback = f"❌ Incorrecto. Respuesta correcta: {verb['past']}"
    if verb["translation"]:
        st.session_state.translation = verb["translation"]

# Si no hay pregunta actual, crear la primera
if st.session_state.current is None and not st.session_state.finished:
    new_question()

st.title("📚 Irregular Verbs Quiz-2 ** Welcome Maria Paz Sarmiento Tamayo * MAPIs CHAMPIONS")

for i in range(10):
    if not st.session_state.finished:
        verb = st.session_state.current
        hint_type = st.session_state.hint_type

        if hint_type == "present":
            st.subheader(f"Escribe el pasado de: **{verb['present']}**")
        elif hint_type == "translation":
            st.subheader(f"Escribe el pasado del verbo traducido como: **{verb['translation']}**")
        elif hint_type == "past":
            st.subheader(f"¿Cuál es el presente del verbo que también se escribe como: **{verb['past']}**?")

        st.text_input(
            "Tu respuesta:",
            key=f"answer_{st.session_state.input_key}",
            on_change=check_answer
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.session_state.awaiting_answer and st.button("Comprobar"):
                check_answer()

        if not st.session_state.awaiting_answer:
            st.markdown(st.session_state.feedback)
            if st.session_state.translation:
                st.info(f"Traducción: **{st.session_state.translation}**")

        if st.button("Siguiente pregunta"):
            new_question()
            st.rerun()

        with col2:
            if st.button("Terminar cuestionario"):
                st.session_state.finished = True


st.subheader("🎯 Resultado final")
st.write(f"Aciertos: **{st.session_state.score}**")
st.write(f"Total preguntas: **{st.session_state.total}**")
if st.session_state.total > 0:
    pct = 100 * st.session_state.score / st.session_state.total
    st.write(f"Porcentaje: **{pct:.1f}%**")
if st.button("Volver a empezar"):
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.finished = False
    st.session_state.current = None
    st.session_state.input_key = 0
    st.session_state.awaiting_answer = True
    st.rerun()