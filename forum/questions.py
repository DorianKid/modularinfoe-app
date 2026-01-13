import streamlit as st
from forum.db import get_conn

def on_title_change():
    st.session_state.title_ready = bool(
        st.session_state.q_title.strip()
    )

def create_question():
    st.subheader("📝 Nueva pregunta")

    # Inicializar estado
    st.session_state.setdefault("q_title", "")
    st.session_state.setdefault("q_body", "")
    st.session_state.setdefault("title_ready", False)

    st.text_input(
        "Título",
        key="q_title",
        placeholder="Ejemplo: Ejercicio 15.2 de Mecánica (Resnick)",
        on_change=on_title_change
    )

    col1, col2 = st.columns(2)

    with col1:
        body = st.text_area(
            "Pregunta (LaTeX)",
            key="q_body",
            height=180,
            placeholder="Ejemplo: $$\\int 2^{6x}$$\n\n¿Por qué $$\\sqrt{2}$$ es irracional?"
        )

    with col2:
        st.markdown(
            "<h4 style='text-align: center;'>👀 Vista previa</h4>",
            unsafe_allow_html=True
        )
        if body.strip():
            st.markdown(body, unsafe_allow_html=True)

    c1,c2,c3 = st.columns([1,1,1])
    with c3:
        if st.button("📤 Publicar pregunta",
                     disabled=not st.session_state.title_ready):
                         
            conn = get_conn()
            c = conn.cursor()
            c.execute(
                "INSERT INTO questions (title, body) VALUES (%s, %s)",
                (
                    st.session_state.q_title.strip(),
                    body.strip()
                )
            )
            conn.commit()
            conn.close()
    
            # 🔥 RESET TOTAL
            st.session_state.q_title = ""
            st.session_state.q_body = ""
            st.session_state.title_ready = False
    
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



























