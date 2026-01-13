import streamlit as st
from forum.questions import create_question, list_questions

st.markdown("""
<style>
.vote-center {
    display: flex;
    justify-content: center;
    gap: 1rem;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Foro Académico",
    layout="wide"
)

st.title("💭 Foro Académico")

st.markdown(
    """
    Este foro funciona como un **repositorio académico de preguntas y soluciones**.

    - Puedes escribir **texto normal y ecuaciones en LaTeX**
    - Usa `$$ ... $$` para los entornos matemáticos
    - Las respuestas pueden votarse según su utilidad
    """
)

st.divider()

# Crear nueva pregunta
create_question()

st.divider()

# Listar preguntas existentes
list_questions()
