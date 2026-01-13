# forum/admin_page.py
import streamlit as st
from forum.db import get_conn
from forum.admin import (
    delete_question,
    delete_answer,
    accept_answer,
    update_question_area
)

def admin_page():

    st.set_page_config(page_title="Admin Foro", layout="wide")
    st.title("🛡️ Administración del Foro")

    st.warning(
        "Página de administración oculta. "
        "No compartas esta URL."
    )

    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT id, title, body, area
        FROM questions
        ORDER BY id DESC
    """)
    questions = c.fetchall()
    conn.close()

    for qid, title, body, area in questions:
        with st.container(border=True):
            st.markdown(f"### {title}")
            st.markdown(body, unsafe_allow_html=True)

            st.caption(f"Área: {area or 'Sin asignar'}")

            new_area = st.text_input(
                "Editar área",
                value=area or "",
                key=f"area_{qid}"
            )

            col1, col2 = st.columns(2)

            if col1.button("🗑️ Eliminar pregunta", key=f"del_q_{qid}"):
                delete_question(qid)
                st.rerun()

            if col2.button("💾 Guardar área", key=f"save_area_{qid}"):
                update_question_area(qid, new_area)
                st.rerun()

            # Respuestas
            conn = get_conn()
            c = conn.cursor()
            c.execute("""
                SELECT id, body, is_accepted
                FROM answers
                WHERE question_id = %s
            """, (qid,))
            answers = c.fetchall()
            conn.close()

            for aid, body_a, is_accepted in answers:
                with st.container(border=True):
                    st.markdown(body_a, unsafe_allow_html=True)

                    if is_accepted:
                        st.success("🟢 Solución aceptada")

                    colA, colB = st.columns(2)

                    if colA.button("🗑️ Eliminar respuesta", key=f"del_a_{aid}"):
                        delete_answer(aid)
                        st.rerun()

                    if not is_accepted:
                        if colB.button("✔ Marcar solución", key=f"acc_{aid}"):
                            accept_answer(aid, qid)
                            st.rerun()
