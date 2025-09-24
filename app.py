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