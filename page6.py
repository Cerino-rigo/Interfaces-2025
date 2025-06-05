import streamlit as st
import pandas as pd
from utils.load_data import load_sessions, load_lessons, load_interactions, load_users, load_cp_coords
from utils.styles import aplicar_estilos

import plotly.express as px
import plotly.graph_objects as go

aplicar_estilos()


# Selector en la barra lateral
data_type = st.sidebar.radio("Selecciona el tipo de datos:", ["Real", "Sintético"])

sessions = load_sessions(data_type)
lessons = load_lessons(data_type)
interactions = load_interactions(data_type)
users = load_users(data_type)
cp_coords = load_cp_coords()

st.title("Filtros generales de los datos")



sesiones_con_datos = sessions.merge(users, on='Usuario', how='left')
st.write(sesiones_con_datos)



merged_df_1 = lessons.merge(interactions, on=['sesion', 'leccion'], how='left')
st.write(merged_df_1)
merged_df_1 = sesiones_con_datos.merge(merged_df_1, on='sesion', how='left')
kpis_df_1 = merged_df_1.groupby('Usuario').agg(
    total_sesiones=('sesion', 'nunique'),
    duracion_promedio_sesion=('tiempo de sesion', 'mean'),
    total_lecciones=('leccion', 'nunique'),
    tasa_aciertos=('boton correcto', lambda x: x.sum() / x.count()),
    tiempo_promedio_interaccion=('tiempo de interaccion', 'mean'),
    distribucion_colores_presionados=('color presionado', lambda x: x.value_counts().to_dict())
).reset_index()
st.write(kpis_df_1)

st.write(len(kpis_df_1))


# KPIs
st.subheader('KPIs Clave')
col1,col2,col3 = st.columns(3)
tile = col1.container(height=120)
tile.metric('Total de Sesiones', kpis_df_1['total_sesiones'].sum())
tile = col2.container(height=120)
tile.metric('Duración Promedio de Sesión', round(kpis_df_1['duracion_promedio_sesion'].mean(),2))
tile = col3.container(height=120)
tile.metric('Total de Lecciones', kpis_df_1['total_lecciones'].sum())
col1,col2= st.columns(2)
tile = col1.container(height=120)
tile.metric('Tasa de Aciertos', round(kpis_df_1['tasa_aciertos'].mean(),2))
tile = col2.container(height=120)
tile.metric('Tiempo Promedio por Interacción', round(kpis_df_1['tiempo_promedio_interaccion'].mean(),2))


col1, col2, col3 = st.columns(3)

with col1:
    total_sesiones = kpis_df_1['total_sesiones'].sum()
    st.markdown(f'<div class="custom_tile"><h3>{total_sesiones}</h3><p>Total de Sesiones</p></div>', unsafe_allow_html=True)

with col2:
    duracion_promedio = round(kpis_df_1['duracion_promedio_sesion'].mean(), 2)
    st.markdown(f'<div class="custom_tile"><h3>{duracion_promedio}</h3><p>Duración Promedio de Sesión</p></div>', unsafe_allow_html=True)

with col3:
    total_lecciones = kpis_df_1['total_lecciones'].sum()
    st.markdown(f'<div class="custom_tile"><h3>{total_lecciones}</h3><p>Total de Lecciones</p></div>', unsafe_allow_html=True)
st.markdown('')
#st.markdown('#')
#st.markdown('##')
col1, col2 = st.columns(2)

with col1:
    tasa_aciertos = round(kpis_df_1['tasa_aciertos'].mean(), 2)
    st.markdown(f'<div class="custom_tile"><h3>{tasa_aciertos}</h3><p>Tasa de Aciertos</p></div>', unsafe_allow_html=True)

with col2:
    tiempo_interaccion = round(kpis_df_1['tiempo_promedio_interaccion'].mean(), 2)
    st.markdown(f'<div class="custom_tile"><h3>{tiempo_interaccion}</h3><p>Tiempo Promedio por Interacción</p></div>', unsafe_allow_html=True)


# Enriquecer con datos demográficos y geográficos
kpis_enriched = kpis_df_1.merge(users, on="Usuario", how="left")
st.write(kpis_enriched)
kpis_enriched = kpis_enriched.merge(cp_coords, on="CP", how="left")
st.write(kpis_enriched)

import pydeck as pdk
def mostrar():
    st.title("Mapas Geográficos de Pacientes")
    
    # Agrupación por zona
    agg_zones = kpis_enriched.groupby('TipoZona').agg({'Latitud':'mean', 'Longitud':'mean','CP':'count'}).reset_index()

    

# Mapa detallado con ScatterplotLayer

    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=kpis_enriched,
        get_position='[Longitud, Latitud]',
        get_color='[200, 30, 0, 160]',
        get_radius=50000,
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=kpis_enriched['Latitud'].mean(),
        longitude=kpis_enriched['Longitud'].mean(),
        zoom=4,
        pitch=50,
    )

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v10',
        initial_view_state=view_state,
        layers=[scatter_layer],
        tooltip={"text": "Usuario: {Usuario}\nTrastorno: {Trastorno}\nEdad: {Edad} años"}
    ))


    st.write("Distribución detallada por CP:")
    st.write(agg_zones)

mostrar()



