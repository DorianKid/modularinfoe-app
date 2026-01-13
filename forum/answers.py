import streamlit as st
from forum.db import get_conn

st.markdown("""
<style>

/* --- CONTENEDOR DE VOTOS --- */
div[data-testid="stHorizontalBlock"]:has(button[data-vote]) {
    justify-content: center;
}

/* --- BOTONES DE VOTO --- */
button[data-vote] {
    border-radius: 999px !important;
    padding: 0.2rem 0.6rem !important;
    font-size: 0.8rem !important;
    border: 1px solid #ddd !important;
    background: #f9fafb !important;
    transition: all 0.15s ease-in-out;
}

/* Hover */
button[data-vote]:hover {
    background: #eef2ff !important;
    border-color: #c7d2fe !important;
}

/* Disabled */
button[data-vote]:disabled {
    background: #f1f1f1 !important;
    color: #999 !important;
    border-color: #e5e7eb !important;
}

/* Separación mínima */
button[data-vote] + button[data-vote] {
    margin-left: 0.3rem;
}

</style>
""", unsafe_allow_html=True)


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
                        # --- Votos centrados y estilizados ---
                        st.markdown("<div class='vote-box'><div class='vote-inner'>", unsafe_allow_html=True)
                        
                        c1, c2 = st.columns(2)
                        
                        # 👍 Like
                        if aid in st.session_state.voted_answers:
                            c1.button(f"👍 {likes}", disabled=True, key=f"l_{aid}")
                        else:
                            if c1.button(f"👍 {likes}", key=f"l_{aid}"):
                                vote(aid, "likes")
                                st.session_state.voted_answers.add(aid)
                                st.rerun()
                        
                        # 👎 Dislike
                        if aid in st.session_state.voted_answers:
                            c2.button(f"👎 {dislikes}", disabled=True, key=f"d_{aid}")
                        else:
                            if c2.button(f"👎 {dislikes}", key=f"d_{aid}"):
                                vote(aid, "dislikes")
                                st.session_state.voted_answers.add(aid)
                                st.rerun()
                        
                        st.markdown("</div></div>", unsafe_allow_html=True)


    else:
        st.caption("Aún no hay respuestas para esta pregunta.")

    # --- Agregar respuesta ---
    with st.expander("✍️ Agregar solución"):
        key = f"ans_{question_id}"
        st.session_state.setdefault(key, "")

        col1, col2 = st.columns(2)
        with col1:
            new_answer = st.text_area(
                "Respuesta (LaTeX)",
                key=key,
                placeholder="Explica el procedimiento y usa $$ $$ para ecuaciones"
            )

        with col2:
            st.markdown(
                "<h4 style='text-align: center;'>👀 Vista previa</h4>",
                unsafe_allow_html=True
            )
            if new_answer.strip():
                st.markdown(new_answer, unsafe_allow_html=True)
    
        c1,c2,c3 = st.columns([3,2,2])
        with c2:
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
        
                # Reset seguro
                st.session_state.pop(key, None)
        
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

