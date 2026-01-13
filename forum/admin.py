# forum/admin.py
from forum.db import get_conn

def delete_question(question_id: int):
    """
    Elimina una pregunta y TODAS sus respuestas asociadas
    """
    conn = get_conn()
    c = conn.cursor()

    # Primero eliminar respuestas (por FK o seguridad)
    c.execute(
        "DELETE FROM answers WHERE question_id = %s",
        (question_id,)
    )

    # Luego eliminar la pregunta
    c.execute(
        "DELETE FROM questions WHERE id = %s",
        (question_id,)
    )

    conn.commit()
    conn.close()


def delete_answer(answer_id: int):
    """
    Elimina una respuesta específica
    """
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "DELETE FROM answers WHERE id = %s",
        (answer_id,)
    )
    conn.commit()
    conn.close()

def accept_answer(answer_id: int, question_id: int):
    """
    Marca una respuesta como solución aceptada
    (solo puede haber una por pregunta)
    """
    conn = get_conn()
    c = conn.cursor()

    # Desmarcar todas las respuestas de la pregunta
    c.execute(
        "UPDATE answers SET is_accepted = false WHERE question_id = %s",
        (question_id,)
    )

    # Marcar la seleccionada
    c.execute(
        "UPDATE answers SET is_accepted = true WHERE id = %s",
        (answer_id,)
    )

    conn.commit()
    conn.close()

def update_question_area(question_id: int, area: str):
    """
    Asigna o actualiza el área académica de una pregunta
    """
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "UPDATE questions SET area = %s WHERE id = %s",
        (area, question_id)
    )
    conn.commit()
    conn.close()
