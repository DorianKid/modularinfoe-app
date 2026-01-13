import streamlit as st
from forum.db import get_conn

def create_question():

    st.subheader("📝 Nueva pregunta")

    # Inicializar estado
    st.session_state.setdefault("q_title", "")
    st.session_state.setdefault("q_body", "")

    title = st.text_input(
        "Título *",
        key="q_title",
        placeholder="Ejercicio 15.2 de Mecánica (Resnick)"
    )

    col1, col2 = st.columns(2)

    with col1:
    
        body = st.text_area(
            "Pregunta (texto + LaTeX)",
            key="q_body",
            height=220,
            placeholder="Ejemplo: Si el $$2^{6x} = 24$$ ¿cuánto vale x?"
        )

    with col2:
        # --- Vista previa ---
        if body.strip():
            st.markdown("#### 👀 Vista previa")
            st.markdown(body, unsafe_allow_html=True)

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

        # 🔥 RESET TOTAL (inputs + preview)
        st.session_state.q_title = ""
        st.session_state.q_body = ""

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


