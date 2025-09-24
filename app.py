import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Irregular Verbs Quiz", page_icon="📚")

# ==========================
# Cargar datos solo una vez
# ==========================
@st.cache_data
def load_data():
    # El CSV debe tener: present,past,translation
    return pd.read_csv("irregular_verbs.csv")

verbs = load_data()

# ==========================
# Estado de sesión
# ==========================
if "score" not in st.session_state:
    st.session_state.score = 0
if "total" not in st.session_state:
    st.session_state.total = 0
if "finished" not in st.session_state:
    st.session_state.finished = False
if "current" not in st.session_state:
    st.session_state.current = None

def new_question():
    row = verbs.sample(1).iloc[0]
    st.session_state.current = {
        "present": row["present"],
        "past": row["past"],
        "translation": row.get("translation", "")
    }

if st.session_state.current is None and not st.session_state.finished:
    new_question()

st.title("📚 Irregular Verbs Quiz con Traducción")

# ==========================
# Lógica principal
# ==========================
if not st.session_state.finished:
    verb = st.session_state.current
    st.subheader(f"Escribe el pasado de: **{verb['present']}**")

    answer = st.text_input("Tu respuesta:", key="answer_input")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Comprobar"):
            st.session_state.total += 1
            if answer.strip().lower() == verb["past"].lower():
                st.session_state.score += 1
                st.success("✅ Correcto!")
            else:
                st.error(f"❌ Incorrecto. Respuesta correcta: {verb['past']}")
            
            # Mostrar traducción (si existe)
            if verb["translation"]:
                st.info(f"Traducción: **{verb['translation']}**")

            new_question()
            st.session_state.answer_input = ""

    with col2:
        if st.button("Terminar cuestionario"):
            st.session_state.finished = True

# ==========================
# Resultado final
# ==========================
if st.session_state.finished:
    st.subheader("🎯 Resultado final")
    st.write(f"Aciertos: **{st.session_state.score}**")
    st.write(f"Total preguntas: **{st.session_state.total}**")
    if st.session_state.total > 0:
        porcentaje = 100 * st.session_state.score / st.session_state.total
        st.write(f"Porcentaje: **{porcentaje:.1f}%**")

    if st.button("Volver a empezar"):
        st.session_state.score = 0
        st.session_state.total = 0
        st.session_state.finished = False
        st.session_state.current = None