# forum/answers.py
import streamlit as st
from forum.db import get_conn

def add_answer(question_id: int):
    body = st.text_area(
        "Respuesta (LaTeX permitido)",
        key=f"answer_{question_id}"
    )

    if st.button("Responder", key=f"btn_{question_id}"):
        if not body:
            st.warning("La respuesta está vacía")
            return

        conn = get_conn()
        c = conn.cursor()
        c.execute(
            "INSERT INTO answers (question_id, body) VALUES (?, ?)",
            (question_id, body)
        )
        conn.commit()
        conn.close()
        st.success("Respuesta enviada")

def list_answers(question_id: int):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "SELECT body FROM answers WHERE question_id = ?",
        (question_id,)
    )
    rows = c.fetchall()
    conn.close()

    if rows:
        st.markdown("**Respuestas:**")
        for (body,) in rows:
            st.markdown(f"$$\n{body}\n$$", unsafe_allow_html=True)
