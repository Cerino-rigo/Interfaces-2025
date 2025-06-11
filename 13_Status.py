import streamlit as st 
import time
from random import choice, randint

st.title(":mag: Real-Time Status Monitoring Dashboard")

col1, col2, col3 = st.columns(3)

#Panel de notificaciones generalesw
with col1:
    st.header("General Notification")
    st.success(":white_check_mark: All systems operational!")
    st.info(":information_source: System update scheduled for tonight.")

with col2:
    st.header("Alerts & Warnings")
    st.warning(":warning: CPU Usage reaching high levels.")
    st.error(":x: Server 3 is not responding.")

with col3:
    st.header("System Exception")
    st.exception(RuntimeError("RuntimeError: Failed to load configuration file."))

#Simulación de actualización de datos cada 2 segundos
st.subheader(":bar_chart: Live Status Updates")
status_area = st.empty()

for _ in range(10):
    update_type = choice(["success", "warning", "error", "info"])
    message = {
        "success": f":white_check_mark: All systems stable at {time.strftime('%H:%M:%S')}",
        "warning": f":warning: Memory usage at {randint(80, 95)}%!",
        "error": f":x: Critical error in Service {randint(1, 5)}!",
        "info": f":information_source: Routine maintence scheduled."
    }

    with status_area.container():
        getattr(st, update_type)(message[update_type])
    time.sleep(0.2)


######Elementos de status con markdown

st.title(":mag: Real-Time Status Monitoring Dashboard")

col1, col2, col3 = st.columns(3)

# Panel de notificaciones generales usando HTML para personalizar colores
with col1:
    st.header("General Notification")
    ##Opción 1
    st.markdown(
        "<div style='background-color: #d4edda; color: #155724; padding: 10px; border-radius: 5px;'>"
        "<strong>✔️ All systems operational!</strong></div>", unsafe_allow_html=True)
    st.markdown("")

    ##Opción 2
    st.markdown("""
    <div style='background-color:#d4edda; padding:10px; border-radius:5px; color:#155724; font-weight:bold'>
        ✅ All systems operational!
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    st.markdown(
        "<div style='background-color: #cce5ff; color: #004085; padding: 10px; border-radius: 5px;'>"
        "<strong>ℹ️ System update scheduled for tonight.</strong></div>", unsafe_allow_html=True)

with col2:
    st.header("Alerts & Warnings")
    st.markdown(
        "<div style='background-color: #fff3cd; color: #856404; padding: 10px; border-radius: 5px;'>"
        "<strong>⚠️ CPU Usage reaching high levels.</strong></div>", unsafe_allow_html=True)
    st.markdown("")
    st.markdown(
        "<div style='background-color: #f8d7da; color: #721c24; padding: 10px; border-radius: 5px;'>"
        "<strong>❌ Server 3 is not responding.</strong></div>", unsafe_allow_html=True)

with col3:
    st.header("System Exception")
    # Para errores, puedes usar el texto en rojo o estilo personalizado
    st.markdown(
        "<div style='background-color: #f8d7da; color: #721c24; padding: 10px; border-radius: 5px;'>"
        "<strong>RuntimeError: Failed to load configuration file.</strong></div>", unsafe_allow_html=True)

# Simulación de actualización de datos cada 2 segundos
st.subheader(":bar_chart: Live Status Updates")
status_area = st.empty()

for _ in range(10):
    update_type = choice(["success", "warning", "error", "info"])
    message = {
        "success": "<strong style='color: #155724;'>✔️ All systems stable at {}</strong>".format(time.strftime('%H:%M:%S')),
        "warning": "<strong style='color: #856404;'>⚠️ Memory usage at {}%!</strong>".format(randint(80, 95)),
        "error": "<strong style='color: #721c24;'>❌ Critical error in Service {}!</strong>".format(randint(1, 5)),
        "info": "<strong style='color: #004085;'>ℹ️ Routine maintenance scheduled.</strong>"
    }

    with status_area.container():
        st.markdown(message[update_type], unsafe_allow_html=True)
    time.sleep(0.2)