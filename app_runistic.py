import streamlit as st
import pandas as pd
import os  
import urllib.parse

# 1. CONFIGURACIÓN VISUAL
st.set_page_config(
    page_title="Runistic", 
    page_icon="🧬", 
    layout="centered",
    initial_sidebar_state="expanded" # <--- CAMBIO: Ahora siempre estará abierta
)

# --- ESTILOS LIMPIOS PERO CON BARRA VISIBLE ---
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    .stApp { background-color: #0E1117; color: white; }
    
    [data-testid="stMetric"] {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 15px;
        border: 1px solid #333;
    }
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 2. LÓGICA DE DATOS (Movida arriba para que el selector aparezca primero)
archivo_excel = "atletas_runistic.xlsm"

if os.path.exists(archivo_excel):
    try:
        df_atletas = pd.read_excel(archivo_excel)
        # El selector ahora es lo primero que verás en la barra lateral
        seleccion = st.sidebar.selectbox(
            "👤 Seleccionar Atleta", 
            df_atletas["Nombre"], 
            key="selector_principal"
        )
        
        datos = df_atletas[df_atletas["Nombre"] == seleccion].iloc[0]
        
        # Variables del Excel
        nombre_atleta = datos["Nombre"]
        carrera = datos["Meta"]
        fase = datos["Fase"]
        semana = datos["Semana"]
        total_semanas = datos["Total_semanas"]
        umbral_ritmo = datos["Umbral"]
        mensaje_semanal = datos["Mensaje"] 
        
    except Exception as e:
        st.error(f"Error de base de datos: {e}")
        nombre_atleta, carrera, fase, semana, total_semanas, umbral_ritmo, mensaje_semanal = "Error", "N/A", "N/A", 0, 0, 4.0, "Revisa tu Excel"
else:
    st.sidebar.warning(f"No se encontró {archivo_excel}.")
    nombre_atleta, carrera, fase, semana, total_semanas, umbral_ritmo, mensaje_semanal = "Demo", "Maratón", "Base", 1, 16, 4.30, "Bienvenido."

# 3. NAVEGACIÓN LATERAL (Debajo del selector)
st.sidebar.markdown("---")
menu = st.sidebar.radio("🧭 Navegación", 
    ["Dashboard", "Mi Macrociclo", "Mi Fase Actual", "Mis Zonas", "Calculadora de Carrera", "Biblioteca de Sesiones", "Academia"])

# 4. MÓDULOS DE LA APP
if menu == "Dashboard":
    st.title(f"Hola, {nombre_atleta}")
    st.markdown(f"**🎯 Objetivo:** {carrera}")
    
    progreso = semana / total_semanas
    st.progress(progreso)
    st.caption(f"Progreso del plan: {int(progreso*100)}%")

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    col1.metric("Fase", fase)
    col2.metric("Semana", f"{semana}/{total_semanas}")
    col3.metric("Ritmo Umbral", f"{umbral_ritmo} m/k")

    st.markdown("### 🚀 Enfoque Semanal")
    st.info(mensaje_semanal)
    
    st.markdown("---")
    # BOTÓN DE WHATSAPP (Asegúrate de poner tu número real abajo)
    numero_coach = "52449XXXXXXX" 
    mensaje_wa = urllib.parse.quote(f"Hola Coach Arturo, soy {nombre_atleta}. Tengo una duda sobre mi fase de {fase}.")
    link_wa = f"https://wa.me/{numero_coach}?text={mensaje_wa}"
    
    st.markdown(f'''
        <a href="{link_wa}" target="_blank">
            <button style="width:100%; border-radius:25px; background-color:#25D366; color:white; font-weight:bold; border:none; height:3em; cursor:pointer;">
                💬 Hablar con mi Coach
            </button>
        </a>
        ''', unsafe_allow_html=True)

elif menu == "Mi Macrociclo":
    st.header("📍 Mi Macrociclo")
    fases_macro = [
        {"fase": "Base", "obj": "Capacidad aeróbica", "estado": "Actual" if fase == "Base" else "Completado"},
        {"fase": "Específica", "obj": "Ritmos de carrera", "estado": "Actual" if fase == "Específica" else "Pendiente"},
        {"fase": "Taper", "obj": "Supercompensación", "estado": "Actual" if fase == "Taper" else "Pendiente"}
    ]
    st.table(pd.DataFrame(fases_macro))

elif menu == "Mis Zonas":
    st.header("📊 Zonas de Entrenamiento")
    st.write(f"Cálculos para {nombre_atleta} (Umbral: {umbral_ritmo})")
    zonas_data = {
        "Zona": ["Z1", "Z2", "Z3", "Z4", "Z5"],
        "Ritmo sugerido": [
            f"> {umbral_ritmo + 1.20:.2f}",
            f"{umbral_ritmo + 0.50:.2f} - {umbral_ritmo + 1.15:.2f}",
            f"{umbral_ritmo + 0.15:.2f} - {umbral_ritmo + 0.45:.2f}",
            f"{umbral_ritmo - 0.05:.2f} - {umbral_ritmo + 0.10:.2f}",
            f"< {umbral_ritmo - 0.10:.2f}"
        ],
        "RPE": ["1-3", "4-5", "6", "7-8", "9-10"]
    }
    st.table(pd.DataFrame(zonas_data))

elif menu == "Calculadora de Carrera":
    st.header("🏁 Proyector de Tiempos")
    ritmo_10k, ritmo_21k, ritmo_42k = umbral_ritmo * 0.96, umbral_ritmo * 1.05, umbral_ritmo * 1.15
    col1, col2, col3 = st.columns(3)
    with col1:
        t = ritmo_10k * 10
        st.metric("Meta 10K", f"{int(t//60)}h {int(t%60)}m")
    with col2:
        t = ritmo_21k * 21.097
        st.metric("Meta 21K", f"{int(t//60)}h {int(t%60)}m")
    with col3:
        t = ritmo_42k * 42.195
        st.metric("Meta 42K", f"{int(t//60)}h {int(t%60)}m")

elif menu == "Biblioteca de Sesiones":
    st.header("📚 Guía Técnica")
    tipo = st.selectbox("Tipo de sesión:", ["Tempo", "Fondo", "Series VO2Max"])
    if tipo == "Tempo": st.info("Esfuerzo 'cómodamente duro'. Tolerancia al lactato.")

elif menu == "Academia":
    st.header("🎓 Academia Runistic")
    if "Base" in fase:
        with st.expander("📝 Mitocondrias y Resistencia"): st.write("Explicación sobre la biogénesis mitocondrial...")