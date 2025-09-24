import streamlit as st
import pandas as pd
import random

# ------------------------
# Estado de la sesión
# ------------------------
if "score" not in st.session_state:
    st.session_state.score = 0
if "total" not in st.session_state:
    st.session_state.total = 0
if "finished" not in st.session_state:
    st.session_state.finished = False


# ------------------------
# Cargar datos
# ------------------------
verbs = pd.read_csv("irregular_verbs.csv")  # Ajusta la ruta si es distinta

# Eliminar posibles columnas vacías o sin nombre
verbs = verbs.loc[:, ~verbs.columns.str.contains('^Unnamed')]

# Título de la aplicación
st.title("Práctica de Verbos Irregulares en Inglés MAPI 2")

# ------------------------
# Lógica de preguntas
# ------------------------
if not st.session_state.finished:
    # Escoger verbo aleatorio
    verb = verbs.sample(1).iloc[0]
    present = verb["present"]
    past = verb["past"]

    st.write(f"Escribe el pasado de: **{present}**")

    user_answer = st.text_input("Tu respuesta:")

    # Botón para responder
    if st.button("Comprobar"):
        st.session_state.total += 1
        if user_answer.strip().lower() == past.lower():
            st.success("✅ Correcto!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Incorrecto. Respuesta correcta: {past}")

    # Botón para terminar
    if st.button("Terminar cuestionario"):
        st.session_state.finished = True

else:
    # ------------------------
    # Resultado final
    # ------------------------
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
