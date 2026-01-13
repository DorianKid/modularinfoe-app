import streamlit as st
from forum.db import get_conn

def answers_section(question_id: int):

    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT id, body, likes, dislikes
        FROM answers
        WHERE question_id = %s
        ORDER BY likes DESC, created_at ASC
    """, (question_id,))
    answers = c.fetchall()
    conn.close()

    # --- Mostrar respuestas ---
    if answers:
        with st.expander(f"💡 Ver respuestas ({len(answers)})"):
            for aid, body, likes, dislikes in answers:
                with st.container(border=True):

                    st.markdown('<div class="vote-center">', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    
                    if col1.button(f"👍 {likes}", key=f"like_{aid}"):
                        vote(aid, "likes")
                        st.rerun()
                    
                    if col2.button(f"👎 {dislikes}", key=f"dislike_{aid}"):
                        vote(aid, "dislikes")
                        st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)


    else:
        st.caption("Aún no hay respuestas para esta pregunta.")

    # --- Agregar respuesta ---
    with st.expander("✍️ Agregar solución"):
        key = f"ans_{question_id}"
        st.session_state.setdefault(key, "")

        new_answer = st.text_area(
            "Respuesta (texto + LaTeX)",
            key=key,
            placeholder="Explica el procedimiento y usa $$ $$ para ecuaciones"
        )

        # Vista previa
        if new_answer.strip():
            st.markdown("#### 👀 Vista previa")
            st.markdown(new_answer, unsafe_allow_html=True)

        if st.button("Responder", key=f"btn_{question_id}"):
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

            # 🔥 Reset del textbox de respuesta
            st.session_state[key] = ""
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

