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
    st.session_state.awaiting_answer = True  # <-- NUEVO: controla si hay que responder

def new_question():
    """Selecciona un verbo aleatorio y resetea el input."""
    idx = random.randint(0, len(verbs) - 1)
    row = verbs.iloc[idx]
    st.session_state.current = {
        "present": row["present"],
        "past": row["past"],
        "translation": row.get("translation", "")
    }
    st.session_state.input_key += 1
    st.session_state.awaiting_answer = True

# Si no hay pregunta actual, crear la primera
if st.session_state.current is None and not st.session_state.finished:
    new_question()

st.title("📚 Irregular Verbs Quiz con Traducción")

if not st.session_state.finished:
    verb = st.session_state.current
    st.subheader(f"Escribe el pasado de: **{verb['present']}**")

    # Input se “resetea” con cada nueva pregunta
    answer = st.text_input(
        "Tu respuesta:",
        key=f"answer_{st.session_state.input_key}"
    )

    col1, col2 = st.columns(2)

    # ---- Botón Comprobar ----
    with col1:
        if st.session_state.awaiting_answer and st.button("Comprobar"):
            st.session_state.total += 1
            st.session_state.awaiting_answer = False  # Evita dobles clics
            if answer.strip().lower() == verb["past"].lower():
                st.session_state.score += 1
                st.success("✅ ¡Correcto!")
            else:
                st.error(f"❌ Incorrecto. Respuesta correcta: {verb['past']}")
            if verb["translation"]:
                st.info(f"Traducción: **{verb['translation']}**")

            # Botón Siguiente pregunta
            if st.button("Siguiente pregunta"):
                new_question()

    # ---- Botón Terminar ----
    with col2:
        if st.button("Terminar cuestionario"):
            st.session_state.finished = True

else:
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