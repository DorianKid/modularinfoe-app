import streamlit as st
from forum.db import get_conn

def answers_section(question_id: int):

    with st.expander("💡 Ver respuestas / agregar solución"):

        # --- listar respuestas ---
        conn = get_conn()
        c = conn.cursor()
        c.execute("""
            SELECT id, body, likes, dislikes
            FROM answers
            WHERE question_id = ?
            ORDER BY likes DESC
        """, (question_id,))
        answers = c.fetchall()
        conn.close()

        if answers:
            for aid, body, likes, dislikes in answers:
                with st.container(border=True):
                    st.markdown(body, unsafe_allow_html=True)

                    col1, col2, col3 = st.columns([1, 1, 8])

                    if col1.button("👍", key=f"like_{aid}"):
                        vote(aid, "likes")
                        st.rerun()

                    if col2.button("👎", key=f"dislike_{aid}"):
                        vote(aid, "dislikes")
                        st.rerun()

                    col3.markdown(f"👍 {likes} | 👎 {dislikes}")

        else:
            st.info("Aún no hay respuestas")

        # --- agregar respuesta ---
        st.markdown("#### ✍️ Agregar respuesta")

        new_answer = st.text_area(
            "Respuesta (texto + LaTeX)",
            key=f"ans_{question_id}",
            placeholder="Explica el procedimiento y usa $$ $$ para ecuaciones"
        )

        if st.button("Responder", key=f"btn_ans_{question_id}"):
            if not new_answer.strip():
                st.warning("La respuesta no puede estar vacía")
                return

            conn = get_conn()
            c = conn.cursor()
            c.execute(
                "INSERT INTO answers (question_id, body) VALUES (?, ?)",
                (question_id, new_answer.strip())
            )
            conn.commit()
            conn.close()
            st.success("Respuesta agregada")
            st.rerun()

def vote(answer_id: int, field: str):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        f"UPDATE answers SET {field} = {field} + 1 WHERE id = ?",
        (answer_id,)
    )
    conn.commit()
    conn.close()
