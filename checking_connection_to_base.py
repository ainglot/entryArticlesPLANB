import streamlit as st
import psycopg2

# Function to establish a connection to Supabase PostgreSQL
def get_connection():
    return psycopg2.connect(
        host=st.secrets["database"]["host"],
        database=st.secrets["database"]["database"],
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"],
        port=st.secrets["database"]["port"]
    )

# Test połączenia
try:
    conn = get_connection()
    st.write("Połączono z bazą danych!")
    conn.close()
except Exception as e:
    st.write("Błąd połączenia:", e)
