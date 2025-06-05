import pandas as pd
import streamlit as st

@st.cache_data
def load_sessions(data_type="Real"):
    if data_type == "Real":
        return pd.read_csv("Tableros/data/sessions.csv", parse_dates=["fecha inicio", "fecha fin"])
    else:
        return pd.read_csv("Tableros/data/syntetic_sessions.csv", parse_dates=["fecha inicio", "fecha fin"])

@st.cache_data
def load_lessons(data_type="Real"):
    if data_type == "Real":
        return pd.read_csv("Tableros/data/lessons.csv", parse_dates=["fecha inicio", "fecha fin"])
    else:
        return pd.read_csv("Tableros/data/syntetic_lessons.csv", parse_dates=["fecha inicio", "fecha fin"])

@st.cache_data
def load_interactions(data_type="Real"):
    if data_type == "Real":
        return pd.read_csv("Tableros/data/interactions.csv", parse_dates=["fecha"])
    else:
        return pd.read_csv("Tableros/data/syntetic_interactions.csv", parse_dates=["fecha"])

@st.cache_data
def load_users(data_type="Real"):
    if data_type == "Real":
        return pd.read_csv("Tableros/data/users.csv")
    else:
        return pd.read_csv("Tableros/data/syntetic_users.csv")
    

@st.cache_data
def load_administrators():
    return pd.read_csv("Tableros/data/dataadministrators.csv")

@st.cache_data
def load_cp_coords():
    return pd.read_csv('Tableros/data/MX_CP_CoordZone.csv')

