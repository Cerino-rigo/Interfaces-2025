import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime
import os

from utils.load_data import load_sessions, load_lessons, load_interactions, load_users

# Cargar datos
sessions = load_sessions()

# Calcular KPIs
total_sesiones = len(sessions)
usuarios_unicos = sessions["Usuario"].nunique()
sesiones_por_usuario = sessions["Usuario"].value_counts()
promedio_sesiones_usuario = sesiones_por_usuario.mean()
promedio_sesiones_dia = sessions["fecha inicio"].dt.date.value_counts().mean()

# Crear resumen de texto
resumen = (
    f"Resumen de KPIs\n\n"
    f"- Total de sesiones registradas: {total_sesiones}\n"
    f"- Número de usuarios únicos: {usuarios_unicos}\n"
    f"- Promedio de sesiones por usuario: {promedio_sesiones_usuario:.2f}\n"
    f"- Promedio de sesiones por día: {promedio_sesiones_dia:.2f}\n"
)

# Crear gráfica de barras
plt.figure(figsize=(6, 4))
sesiones_por_usuario.head(10).plot(kind='bar', color='skyblue')
plt.title("Top 10 Usuarios con más sesiones")
plt.xlabel("Usuario")
plt.ylabel("Número de sesiones")
plt.tight_layout()
grafica_path = "grafica_sesiones.png"
plt.savefig(grafica_path)
plt.close()

# Crear PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
for linea in resumen.split("\n"):
    pdf.cell(0, 10, linea, ln=True)

pdf.image(grafica_path, x=10, y=pdf.get_y() + 5, w=180)
nombre_pdf = "reporte_kpis.pdf"
pdf.output(nombre_pdf)

# Interfaz Streamlit
st.title("📄 Generador de Reporte PDF con KPIs y Gráfica")

st.write("Resumen de KPIs:")
st.text(resumen)

st.image(grafica_path, caption="Top 10 Usuarios con más sesiones")

with open(nombre_pdf, "rb") as f:
    st.download_button("📥 Descargar PDF", f, file_name=nombre_pdf, mime="application/pdf")

