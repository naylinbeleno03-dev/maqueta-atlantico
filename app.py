import streamlit as st
import pandas as pd
import random
import base64

# Configuración de la página
st.set_page_config(
    page_title="Estadística - Zona Metropolitana del Atlántico",
    page_icon="🎡",
    layout="centered"
)

# Cargar imagen de fondo si existe
def cargar_fondo(ruta_imagen):
    try:
        with open(ruta_imagen, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(3, 4, 94, 0.55);
            z-index: -1;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except FileNotFoundError:
        pass

cargar_fondo("fondo.png")

# Título Principal
st.markdown("<h1 style='text-align: center; color: #fcbf49;'>🎡 Juego de Estadística</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #ffffff;'>Área Metropolitana del Atlántico</h3>", unsafe_allow_html=True)
st.write("---")

# Base de Datos de Preguntas de Estadística
preguntas = [
    {
        "num": 1,
        "pregunta": "1. ¿Cuál es el segundo municipio con más población en tu maqueta?",
        "opciones": ["Galapa", "Malambo", "Puerto Colombia", "Barranquilla"],
        "correcta": "Malambo",
        "pista": "Es la segunda frecuencia absoluta (fi) más alta con 153.223 habitantes."
    },
    {
        "num": 2,
        "pregunta": "2. ¿Qué municipio concentra la mayor población (Moda de la muestra)?",
        "opciones": ["Malambo", "Galapa", "Barranquilla", "Puerto Colombia"],
        "correcta": "Barranquilla",
        "pista": "Es el valor con mayor frecuencia (fi = 1.275.854 habitantes)."
    },
    {
        "num": 3,
        "pregunta": "3. ¿Qué puente conecta la zona metropolitana con el departamento del Magdalena?",
        "opciones": ["Muelle de Puerto Colombia", "Puente Alberto Pumarejo", "Gran Malecón", "Ventanal al Mundo"],
        "correcta": "Puente Alberto Pumarejo",
        "pista": "Es el puente atirantado representativo sobre el Río Magdalena."
    },
    {
        "num": 4,
        "pregunta": "4. ¿Cuál es la población total (N) entre los 4 municipios representados?",
        "opciones": ["2.100.000 hab", "1.275.854 hab", "1.564.805 hab", "980.500 hab"],
        "correcta": "1.564.805 hab",
        "pista": "Suma exacta de las 4 frecuencias: 1.275.854 + 153.223 + 70.042 + 65.686."
    },
    {
        "num": 5,
        "pregunta": "5. ¿Qué ecosistema clave de agua dulce y salada se encuentra en la zona?",
        "opciones": ["Parque Tayrona", "Ciénaga de Mallorquín y Bocas de Ceniza", "Laguna de Guatavita", "Caño Cristales"],
        "correcta": "Ciénaga de Mallorquín y Bocas de Ceniza",
        "pista": "Desembocadura directa del Río Magdalena en el Mar Caribe."
    },
    {
        "num": 6,
        "pregunta": "6. ¿Qué municipio destaca por su muelle histórico sobre el Mar Caribe?",
        "opciones": ["Galapa", "Malambo", "Puerto Colombia", "Barranquilla"],
        "correcta": "Puerto Colombia",
        "pista": "Municipio costero representado con 65.686 habitantes (4,2%)."
    },
    {
        "num": 7,
        "pregunta": "7. ¿Qué significa la escala 1 cm = 50.000 habitantes?",
        "opciones": [
            "1 cm equivale a 50.000 metros",
            "Cada cm de la barra representa 50.000 personas",
            "La maqueta mide 50 cm",
            "Hay 50.000 municipios"
        ],
        "correcta": "Cada cm de la barra representa 50.000 personas",
        "pista": "Proporción escalar para representar cuantitativamente la población."
    }
]

# Inicializar Estado de Sesión
if "pregunta_actual" not in st.session_state:
    st.session_state.pregunta_actual = None
if "mostrar_pista" not in st.session_state:
    st.session_state.mostrar_pista = False

col1, col2 = st.columns(2)

with col1:
    if st.button("🎡 ¡GIRAR RULETA!", use_container_width=True, type="primary"):
        st.session_state.pregunta_actual = random.choice(preguntas)
        st.session_state.mostrar_pista = False

with col2:
    ver_tabla = st.checkbox("📊 Ver Tabla de Frecuencias")

# Mostrar Tabla de Frecuencias
if ver_tabla:
    st.subheader("📊 Distribución Frecuencial de Población")
    data = {
        "Municipio": ["Barranquilla", "Malambo", "Galapa", "Puerto Colombia"],
        "Población (fi)": [1275854, 153223, 70042, 65686],
        "Porcentaje (%)": ["81.5%", "9.8%", "4.5%", "4.2%"]
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
    
    st.info("""
    * **Total (N):** 1.564.805 habitantes
    * **Moda:** Barranquilla (81.5%)
    * **Rango Poblacional:** 1.210.168 habitantes
    * **Escala Maqueta:** 1 cm = 50.000 habitantes
    """)

# Mostrar Pregunta Seleccionada
if st.session_state.pregunta_actual:
    q = st.session_state.pregunta_actual
    st.subheader(q["pregunta"])

    if st.button("💡 Pedir Ayuda / Fórmula"):
        st.session_state.mostrar_pista = True

    if st.session_state.mostrar_pista:
        st.warning(f"**Pista:** {q['pista']}")

    respuesta = st.radio("Selecciona tu respuesta:", q["opciones"], key=f"q_{q['num']}")

    if st.button("Verificar Respuesta"):
        if respuesta == q["correcta"]:
            st.success("😊 ¡Correcto! Excelente análisis estadístico.")
            st.balloons()
        else:
            st.error(f"😢 ¡Incorrecto! Revisa la tabla de frecuencias e inténtalo de nuevo.")
