# forum/admin.py
import streamlit as st
from forum.db import get_conn

# -------------------------
# Estado admin (temporal)
# -------------------------
def is_admin() -> bool:
    return st.session_state.get("admin", False)

def set_admin(value: bool):
    st.session_state["admin"] = value


# -------------------------
# Moderación
# -------------------------
def delete_question(question_id: int):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "DELETE FROM questions WHERE id = %s",
        (question_id,)
    )
    conn.commit()
    conn.close()

def delete_answer(answer_id: int):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "DELETE FROM answers WHERE id = %s",
        (answer_id,)
    )
    conn.commit()
    conn.close()


# -------------------------
# Solución aceptada
# -------------------------
def accept_answer(answer_id: int, question_id: int):
    conn = get_conn()
    c = conn.cursor()

    # desmarcar todas
    c.execute(
        "UPDATE answers SET is_accepted = false WHERE question_id = %s",
        (question_id,)
    )

    # marcar la correcta
    c.execute(
        "UPDATE answers SET is_accepted = true WHERE id = %s",
        (answer_id,)
    )

    conn.commit()
    conn.close()


# -------------------------
# Área / tags (admin)
# -------------------------
def update_question_area(question_id: int, area: str):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "UPDATE questions SET area = %s WHERE id = %s",
        (area, question_id)
    )
    conn.commit()
    conn.close()
