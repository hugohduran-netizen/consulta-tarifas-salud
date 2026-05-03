import streamlit as st
import pandas as pd

# 1. Configuración de la página (DEBE ir de primero)
st.set_page_config(page_title="Consulta SOAT 2023", layout="wide")

# 2. Definición de la función (Antes de usarla)
@st.cache_data
def load_data():
    # Cargamos el archivo que subiste a GitHub
    df = pd.read_excel("Manual-Tarifario-SOAT-2023-.xlsx", sheet_name='SOAT 2023')
    return df

# 3. Interfaz de usuario
st.title("📊 Consulta de Manual Tarifario SOAT")

try:
    # Llamamos a la función
    df_soat = load_data()
    
    # Creamos las pestañas para organizar Artículos y Códigos
    tab1, tab2 = st.tabs(["🔍 Buscador de Códigos", "📜 Artículos y Parágrafos"])

    with tab1:
        busqueda = st.text_input("Ingrese código o descripción para buscar:")
        if busqueda:
            # Buscador global en todas las columnas
            mask = df_soat.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)
            resultados = df_soat[mask]
            st.write(f"Resultados encontrados: {len(resultados)}")
            st.dataframe(resultados, use_container_width=True)
        else:
            st.info("Escribe algo para empezar la búsqueda.")

    with tab2:
        st.subheader("Secciones de Normatividad")
        # Filtramos filas que contienen palabras clave de normatividad en la primera columna
        normativa = df_soat[df_soat.iloc[:, 0].astype(str).str.contains('ARTICULO|PARAGRAFO', case=False, na=False)]
        
        if not normativa.empty:
            seleccion = st.selectbox("Seleccione un Artículo o Parágrafo para visualizar:", normativa.iloc[:, 0].unique())
            if seleccion:
                texto_completo = normativa[normativa.iloc[:, 0] == seleccion]
                st.warning(f"**Contenido seleccionado:** {seleccion}")
                # Mostramos el resto de columnas de esa fila si tienen texto explicativo
                st.write(texto_completo.dropna(axis=1))
        else:
            st.write("No se detectaron filas con etiquetas de 'ARTICULO' o 'PARAGRAFO' en la columna principal.")

except Exception as e:
    st.error(f"Se produjo un error al cargar los datos: {e}")
    st.info("Verifica que el nombre del archivo en GitHub sea exactamente: Manual-Tarifario-SOAT-2023-.xlsx")

