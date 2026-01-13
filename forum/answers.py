import streamlit as st
from forum.db import get_conn

def answers_section(question_id: int):

    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT id, body, likes, dislikes
        FROM answers
        WHERE question_id = %s
        ORDER BY likes DESC
    """, (question_id,))
    answers = c.fetchall()
    conn.close()

    # --- Si hay respuestas, mostrarlas en expander ---
    if answers:
        with st.expander(f"💡 Ver respuestas ({len(answers)})"):
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
        st.caption("Aún no hay respuestas para esta pregunta.")

    # --- Siempre permitir agregar respuesta ---
    with st.expander("✍️ Agregar solución"):
        new_answer = st.text_area(
            "Respuesta (texto + LaTeX)",
            key=f"ans_{question_id}",
            placeholder="Usa $$ ... $$ para ecuaciones"
        )
        
        if new_answer.strip():
            st.markdown("#### 👀 Vista previa de la respuesta")
            st.markdown(new_answer, unsafe_allow_html=True)

        if st.button("Responder", key=f"btn_ans_{question_id}"):
            if not new_answer.strip():
                st.warning("La respuesta no puede estar vacía")
                return

            conn = get_conn()
            c = conn.cursor()
            c.execute(
                "INSERT INTO answers (question_id, body) VALUES (%s, %s)",
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
        f"UPDATE answers SET {field} = {field} + 1 WHERE id = %s",
        (answer_id,)
    )
    conn.commit()
    conn.close()

