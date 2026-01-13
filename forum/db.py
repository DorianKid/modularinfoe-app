# forum/db.py
import psycopg2
import streamlit as st
import socket

def get_conn():
    # 🔴 Fuerza IPv4 (clave)
    socket.setdefaulttimeout(10)
    return psycopg2.connect(
        host=st.secrets["DB_HOST"],
        dbname=st.secrets["DB_NAME"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        port=int(st.secrets.get("DB_PORT", 5432)),
        sslmode="require",
        options="-c client_encoding=UTF8",
        connect_timeout=10
    )
