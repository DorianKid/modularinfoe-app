import streamlit as st
from forum.db import get_conn


def answers_section(question_id: int):

    st.session_state.setdefault("voted_answers", set())

    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT id, body, likes, dislikes, is_accepted
        FROM answers
        WHERE question_id = %s
        ORDER BY
            is_accepted DESC,
            (likes - dislikes) DESC,
            created_at ASC
    """, (question_id,))
    answers = c.fetchall()
    conn.close()

    # --- Mostrar respuestas ---
    if answers:
        with st.expander(f"💡 Ver respuestas ({len(answers)})"):
            max_score = max((l - d) for _, _, l, d, _ in answers)

            for aid, body, likes, dislikes, is_accepted in answers:
                score = likes - dislikes

                with st.container(border=True):
                    # Etiquetas visuales
                    if is_accepted:
                        st.success("🟢 Solución aceptada")
                    elif score == max_score and score > 0:
                        st.markdown("⭐ **Respuesta más valorada**")

                    st.markdown(body, unsafe_allow_html=True)

                    # --- Votos centrados ---
                    left, center, right = st.columns([3, 4, 3])
                    with center:
                        c1, c2 = st.columns(2)

                        # Like
                        if aid in st.session_state.voted_answers:
                            c1.button(f"👍 {likes}", disabled=True, key=f"l_{aid}")
                        else:
                            if c1.button(f"👍 {likes}", key=f"l_{aid}"):
                                vote(aid, "likes")
                                st.session_state.voted_answers.add(aid)
                                st.rerun()

                        # Dislike
                        if aid in st.session_state.voted_answers:
                            c2.button(f"👎 {dislikes}", disabled=True, key=f"d_{aid}")
                        else:
                            if c2.button(f"👎 {dislikes}", key=f"d_{aid}"):
                                vote(aid, "dislikes")
                                st.session_state.voted_answers.add(aid)
                                st.rerun()

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
                """
                INSERT INTO answers (question_id, body)
                VALUES (%s, %s)
                """,
                (question_id, new_answer.strip())
            )
            conn.commit()
            conn.close()

            # Reset
            del st.session_state[key]
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

