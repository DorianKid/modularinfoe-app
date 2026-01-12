# forum/questions.py
import streamlit as st
from forum.db import get_conn

def create_question():
    st.subheader("📝 Nueva pregunta")

    title = st.text_input("Título")
    body = st.text_area(
        "Pregunta (puedes usar LaTeX)",
        placeholder=r"\int_0^\infty e^{-x^2} dx"
    )

    if st.button("Publicar pregunta"):
        if not title or not body:
            st.warning("Completa todos los campos")
            return

        conn = get_conn()
        c = conn.cursor()
        c.execute(
            "INSERT INTO questions (title, body) VALUES (?, ?)",
            (title, body)
        )
        conn.commit()
        conn.close()

        st.success("Pregunta publicada")

def list_questions():
    st.subheader("📚 Preguntas")

    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, title, body FROM questions ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()

    if not rows:
        st.info("Aún no hay preguntas")
        return

    for qid, title, body in rows:
        with st.expander(title):
            st.markdown(f"$$\n{body}\n$$", unsafe_allow_html=True)
