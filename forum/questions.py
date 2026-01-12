import streamlit as st
from forum.db import get_conn

def create_question():
    st.subheader("📝 Nueva pregunta")

    title = st.text_input(
        "Título *",
        placeholder="Ejercicio 15.2 de Mecánica (Resnick)"
    )

    body = st.text_area(
        "Pregunta (texto + LaTeX)",
        height=220,
        placeholder=(
            "Escribe tu pregunta usando texto normal.\n\n"
            "Para ecuaciones usa $$ ... $$\n\n"
            "Ejemplo:\n"
            "¿Cuál es la solución del sistema\n"
            "$$ m\\ddot{x} + kx = 0 $$\n"
            "y su aceleración?"
        )
    )

    # Validación fuerte
    can_publish = bool(title.strip())

    if not can_publish:
        st.info("El título es obligatorio")

    if st.button("📤 Publicar pregunta", disabled=not can_publish):
        conn = get_conn()
        c = conn.cursor()
        c.execute(
            "INSERT INTO questions (title, body) VALUES (%s, %s)",
            (title.strip(), body.strip())
        )
        conn.commit()
        conn.close()
        st.success("Pregunta publicada correctamente")
        st.rerun()

def list_questions():
    st.subheader("📚 Preguntas del foro")

    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT id, title, body
        FROM questions
        ORDER BY id DESC
    """)
    questions = c.fetchall()
    conn.close()

    if not questions:
        st.info("Aún no hay preguntas en el foro")
        return

    for qid, title, body in questions:
        with st.container(border=True):
            st.markdown(f"### {title}")
            st.markdown(body, unsafe_allow_html=True)

            from forum.answers import answers_section
            answers_section(qid)

