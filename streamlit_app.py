
import streamlit as st
import pandas as pd
import unicodedata

# Configuración de la página
st.set_page_config(page_title="Consulta SOAT 2023", layout="wide")

# Función para quitar tildes y normalizar texto
def normalizar_texto(texto):
    if not isinstance(texto, str):
        return str(texto)
    # Elimina tildes y convierte a minúsculas
    texto_norm = "".join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )
    return texto_norm.lower()

@st.cache_data
def load_data():
    # Cargamos el archivo
    df = pd.read_excel("Manual-Tarifario-SOAT-2023-.xlsx", sheet_name='SOAT 2023')
    return df

st.title("📊 Consulta de Manual Tarifario SOAT")

try:
    df_soat = load_data()
    
    tab1, tab2 = st.tabs(["🔍 Buscador Inteligente", "📜 Artículos y Parágrafos"])

    with tab1:
        busqueda = st.text_input("Ingrese su búsqueda (ej: articulo 40, acetaminofen, 19001):")
        
        if busqueda:
            # 1. Normalizamos la entrada del usuario
            busqueda_norm = normalizar_texto(busqueda)
            
            # 2. Creamos una versión del DataFrame temporalmente normalizada para buscar
            # Buscamos en todas las columnas
            mask = df_soat.apply(
                lambda row: row.astype(str).apply(normalizar_texto).str.contains(busqueda_norm).any(), 
                axis=1
            )
            
            resultados = df_soat[mask]
            st.success(f"Resultados encontrados: {len(resultados)}")
            st.dataframe(resultados, use_container_width=True)
        else:
            st.info("El buscador ahora ignora tildes y mayúsculas automáticamente.")

    with tab2:
        st.subheader("Secciones de Normatividad")
        # Filtro de normativa básico
        normativa = df_soat[df_soat.iloc[:, 0].astype(str).str.contains('ARTICULO|PARAGRAFO', case=False, na=False)]
        
        if not normativa.empty:
            seleccion = st.selectbox("Seleccione una sección:", normativa.iloc[:, 0].unique())
            if seleccion:
                st.warning(f"**Contenido:** {seleccion}")
                st.write(normativa[normativa.iloc[:, 0] == seleccion].dropna(axis=1))

except Exception as e:
    st.error(f"Error: {e}")
