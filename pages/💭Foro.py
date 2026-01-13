import streamlit as st
from forum.db import get_conn

st.write("Probando conexión a Supabase...")

try:
    conn = get_conn()
    st.success("✅ Conexión exitosa a PostgreSQL (Supabase)")
    conn.close()
except Exception as e:
    st.error("❌ Error de conexión")
    st.code(str(e))
