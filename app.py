import streamlit as st
import pandas as pd

st.set_page_config(page_title="Irregular Verbos 2 - MAPI", page_icon="📚")

@st.cache_data
def load_data():
    return pd.read_csv("irregular_verbs.csv")

verbs = load_data()

# Estado
if "score" not in st.session_state:
    st.session_state.score = 0
if "total" not in st.session_state:
    st.session_state.total = 0
if "finished" not in st.session_state:
    st.session_state.finished = False
if "current" not in st.session_state:
    st.session_state.current = None
if "input_key" not in st.session_state:
    st.session_state.input_key = 0  # para refrescar el input

def new_question():
    row = verbs.sample(1).iloc[0]
    st.session_state.current = {
        "present": row["present"],
        "past": row["past"],
        "translation": row.get("translation", "")
    }
    # cada vez que hay nueva pregunta cambiamos la clave
    st.session_state.input_key += 1

if st.session_state.current is None and not st.session_state.finished:
    new_question()

st.title("📚 Irregular Verbs Quiz con Traducción")

if not st.session_state.finished:
    verb = st.session_state.current
    st.subheader(f"Escribe el pasado de: **{verb['present']}**")

    # key dinámico: al cambiar, el input se “resetea”
    answer = st.text_input(
        "Tu respuesta:",
        key=f"answer_{st.session_state.input_key}"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Comprobar"):
            st.session_state.total += 1
            if answer.strip().lower() == verb["past"].lower():
                st.session_state.score += 1
                st.success("✅ Correcto!")
            else:
                st.error(f"❌ Incorrecto. Respuesta correcta: {verb['past']}")

            if verb["translation"]:
                st.info(f"Traducción: **{verb['translation']}**")

            new_question()  # esto cambia input_key -> limpia el campo

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