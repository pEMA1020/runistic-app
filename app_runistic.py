import streamlit as st
import pandas as pd
import os  

# 1. CONFIGURACIÓN VISUAL
st.set_page_config(
    page_title="Runistic", 
    page_icon="🧬", 
    layout="centered",
    initial_sidebar_state="collapsed" # Inicia con el menú cerrado para parecer más App
)

# --- ESTILOS PARA APARIENCIA DE APP NATIVA ---
hide_st_style = """
    <style>
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Fondo y texto general */
    .stApp { background-color: #0E1117; color: white; }
    
    /* Tarjetas de métricas (Metrics) */
    [data-testid="stMetric"] {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 15px;
        border: 1px solid #333;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }
    
    /* Ajuste de botones para que parezcan de App */
    .stButton > button {
        width: 100%;
        border-radius: 25px;
        height: 3em;
        background-color: #e74c3c;
        color: white;
        border: none;
    }
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 2. NAVEGACIÓN LATERAL
st.sidebar.title("🧬 Runistic App")
menu = st.sidebar.radio("Menú de Entrenamiento", 
    ["Dashboard", "Mi Macrociclo", "Mi Fase Actual", "Mis Zonas", "Calculadora de Carrera", "Biblioteca de Sesiones", "Academia"])

# 3. LÓGICA DE DATOS (Excel)
archivo_excel = "atletas_runistic.xlsm"

if os.path.exists(archivo_excel):
    try:
        df_atletas = pd.read_excel(archivo_excel)
        seleccion = st.sidebar.selectbox("Seleccionar Atleta", df_atletas["Nombre"], key="selector_principal")
        
        datos = df_atletas[df_atletas["Nombre"] == seleccion].iloc[0]
        
        # Extracción de variables
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
    nombre_atleta, carrera, fase, semana, total_semanas, umbral_ritmo, mensaje_semanal = "Demo", "Maratón", "Base", 1, 16, 4.30, "Bienvenido a la demo."

# 4. MÓDULOS DE LA APP
if menu == "Dashboard":
    st.title(f"Hola, {nombre_atleta}")
    st.markdown(f"**🎯 Próximo objetivo:** {carrera}")
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    col1.metric("Fase", fase)
    col2.metric("Semana", f"{semana}/{total_semanas}")
    col3.metric("Ritmo Umbral", f"{umbral_ritmo} m/k")

    st.markdown("### 🚀 Enfoque Semanal")
    st.info(mensaje_semanal)
    
    st.markdown("### 🔑 Sesiones Clave")
    st.write("📖 Consulta la **Biblioteca** para detalles técnicos.")

elif menu == "Mi Macrociclo":
    st.header("📍 Mi Macrociclo")
    st.write(f"Planificación estratégica para {nombre_atleta}.")
    fases_macro = [
        {"fase": "Base", "obj": "Capacidad aeróbica", "estado": "Actual" if fase == "Base" else "Completado"},
        {"fase": "Específica", "obj": "Ritmos de carrera", "estado": "Actual" if fase == "Específica" else "Pendiente"},
        {"fase": "Taper", "obj": "Supercompensación", "estado": "Actual" if fase == "Taper" else "Pendiente"}
    ]
    st.table(pd.DataFrame(fases_macro))

elif menu == "Mi Fase Actual":
    st.header(f"Fase: {fase}")
    st.markdown(f"**Análisis Fisiológico para {nombre_atleta}:**")
    if "Base" in fase:
        st.write("Estamos construyendo mitocondrias. El enfoque es volumen a baja intensidad.")
    elif "Específica" in fase:
        st.write("Enfoque en tolerancia al lactato y ritmos específicos de competencia.")
    else:
        st.write("Fase de ajuste. Escucha a tu cuerpo y prioriza la recuperación.")

elif menu == "Mis Zonas":
    st.header("📊 Zonas de Entrenamiento")
    st.write(f"Cálculos personalizados (Umbral: {umbral_ritmo})")
    zonas_data = {
        "Zona": ["Z1", "Z2", "Z3", "Z4", "Z5"],
        "Ritmo sugerido": [
            f"> {umbral_ritmo + 1.20:.2f}",
            f"{umbral_ritmo + 0.50:.2f} - {umbral_ritmo + 1.15:.2f}",
            f"{umbral_ritmo + 0.15:.2f} - {umbral_ritmo + 0.45:.2f}",
            f"{umbral_ritmo - 0.05:.2f} - {umbral_ritmo + 0.10:.2f}",
            f"< {umbral_ritmo - 0.10:.2f}"
        ],
        "Esfuerzo (RPE)": ["1-3", "4-5", "6", "7-8", "9-10"]
    }
    st.table(pd.DataFrame(zonas_data))

elif menu == "Calculadora de Carrera":
    st.header("🏁 Proyector de Tiempos")
    st.write(f"Proyecciones para un umbral de **{umbral_ritmo} min/km**.")

    ritmo_10k = umbral_ritmo * 0.96
    ritmo_21k = umbral_ritmo * 1.05
    ritmo_42k = umbral_ritmo * 1.15

    col1, col2, col3 = st.columns(3)
    with col1:
        t_10k = ritmo_10k * 10
        st.metric("Meta 10K", f"{int(t_10k // 60)}h {int(t_10k % 60)}m")
        st.caption(f"Paso: {ritmo_10k:.2f}")
    with col2:
        t_21k = ritmo_21k * 21.097
        st.metric("Meta 21K", f"{int(t_21k // 60)}h {int(t_21k % 60)}m")
        st.caption(f"Paso: {ritmo_21k:.2f}")
    with col3:
        t_42k = ritmo_42k * 42.195
        st.metric("Meta 42K", f"{int(t_42k // 60)}h {int(t_42k % 60)}m")
        st.caption(f"Paso: {ritmo_42k:.2f}")

elif menu == "Biblioteca de Sesiones":
    st.header("📚 Guía de Ejecución")
    tipo = st.selectbox("Selecciona tipo de sesión:", ["Tempo", "Fondo", "Series VO2Max"])
    if tipo == "Tempo":
        st.info("Objetivo: Tolerancia al lactato. Esfuerzo 'cómodamente duro'.")

elif menu == "Academia":
    st.header("🎓 Academia Runistic")
    st.write(f"Contenido para fase: **{fase}**")
    if "Base" in fase:
        with st.expander("📝 Mitocondrias y Resistencia"):
            st.write("La base aeróbica es el cimiento de tu rendimiento...")
    if "Específica" in fase:
        with st.expander("📝 Optimización de Glucógeno"):
            st.write("Estrategias de carga para sesiones de alta intensidad...")