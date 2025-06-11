import streamlit as st
from fpdf import FPDF
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import os

from utils.load_data import load_sessions, load_lessons, load_interactions, load_users

# Cargar datos
sessions = load_sessions()
lessons = load_lessons()
interactions = load_interactions()
users = load_users()

# Clase personalizada para el PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, self.title, ln=1, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, ln=1, fill=True, align='C')

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_chapter_with_plot(self, title, body, plot_path):
        self.add_page()
        self.chapter_title(title)
        self.chapter_body(body)
        if os.path.exists(plot_path):
            self.image(plot_path, x=10, y=self.get_y(), w=180)
            self.ln()

# Función para generar contenido automático del reporte
def generar_insights(sessions, lessons, interactions, users):
    total_sesiones = len(sessions)
    total_lecciones = len(lessons)
    total_interacciones = len(interactions)
    usuarios_unicos = users["Usuario"].nunique()

    texto = (
        f"- Total de sesiones registradas: {total_sesiones}\n"
        f"- Total de lecciones disponibles: {total_lecciones}\n"
        f"- Total de interacciones en la plataforma: {total_interacciones}\n"
        f"- Número de usuarios únicos: {usuarios_unicos}\n\n"
    )

    sesiones_por_usuario = sessions["Usuario"].value_counts().mean()
    texto += f"- Promedio de sesiones por usuario: {sesiones_por_usuario:.2f}\n"

    sesiones_diarias = sessions["fecha inicio"].dt.date.value_counts().mean()
    texto += f"- Promedio de sesiones por día: {sesiones_diarias:.2f}\n"

    return texto

# Función para generar una gráfica y guardarla como imagen
def generar_grafica_sesiones(sessions, output_path="grafica_sesiones.png"):
    conteo = sessions["Usuario"].value_counts().head(10)
    plt.figure(figsize=(8, 4))
    conteo.plot(kind='bar', color='skyblue')
    plt.title("Top 10 Usuarios con más sesiones")
    plt.xlabel("Usuario")
    plt.ylabel("Número de sesiones")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return output_path

# Generador del PDF
def crear_pdf(titulo, autor, cuerpo, plot_path, nombre_archivo="reporte.pdf"):
    pdf = PDF()
    pdf.set_title(titulo)
    pdf.set_author(autor)
    pdf.add_chapter_with_plot("Resumen de Métricas", cuerpo, plot_path)
    pdf.output(nombre_archivo)
    return nombre_archivo

# Interfaz Streamlit
def mostrar_generador_pdf(sessions, lessons, interactions, users):
    st.subheader("📄 Generador de Reporte Automático")

    titulo = st.text_input("Título del Reporte", value="Reporte de Actividad")
    autor = st.text_input("Autor del Reporte", value="Sistema Automatizado")
    
    if st.button("Generar PDF"):
        cuerpo = generar_insights(sessions, lessons, interactions, users)
        grafica_path = generar_grafica_sesiones(sessions)
        archivo_pdf = crear_pdf(titulo, autor, cuerpo, grafica_path)
        with open(archivo_pdf, "rb") as f:
            st.download_button("📥 Descargar PDF", f, file_name=archivo_pdf, mime="application/pdf")

mostrar_generador_pdf(sessions, lessons, interactions, users)

