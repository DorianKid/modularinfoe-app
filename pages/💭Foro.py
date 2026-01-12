import streamlit as st
from forum.db import init_db
from forum.questions import create_question
from forum.questions import list_questions

st.set_page_config(page_title="Foro", layout="wide")

init_db()

st.title("💬 Foro Académico")

create_question()
st.divider()
list_questions()
