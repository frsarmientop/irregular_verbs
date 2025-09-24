import pandas as pd
import random
import streamlit as st

# Cargar el archivo CSV con los verbos irregulares subir
df = pd.read_csv("irregular_verbs.csv")

# Eliminar posibles columnas vacías o sin nombre
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Título de la aplicación
st.title("Práctica de Verbos Irregulares en Inglés")

# Selección aleatoria de un verbo y tipo de pregunta
verb = df.sample().iloc[0]
question_type = random.choice(["present", "past", "translation"])

# Mostrar la pregunta al usuario
if question_type == "present":
    st.subheader(f"¿Cuál es el presente del verbo '{verb['past']}'?")
elif question_type == "past":
    st.subheader(f"¿Cuál es el pasado del verbo '{verb['present']}'?")
elif question_type == "translation":
    st.subheader(f"¿Cuál es la traducción del verbo '{verb['present']}'?")

# Campo de respuesta del usuario
user_answer = st.text_input("Tu respuesta:")

# Verificar la respuesta
if user_answer:
    correct_answer = verb[question_type]
    if user_answer.strip().lower() == correct_answer.lower():
        st.success("¡Correcto! 🎉")
    else:
        st.error(f"Incorrecto. La respuesta correcta es: {correct_answer}")
