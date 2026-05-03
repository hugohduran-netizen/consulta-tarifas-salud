import streamlit as st
import pandas as pd

st.set_page_config(page_title="Consulta SOAT 2023", layout="wide")

st.title("📊 Consulta de Manual Tarifario SOAT")

@st.cache_data
def load_data():
    # Leemos el archivo sin saltar filas inicialmente para no perder los títulos de los artículos
    df = pd.read_excel("Manual-Tarifario-SOAT-2023-.xlsx", sheet_name='SOAT 2023')
    return df

try:
    df_soat = load_data()

    busqueda = st.text_input("Busca por Código, Descripción, Artículo o Parágrafo:")

    if busqueda:
        # Esta línea busca el texto en CUALQUIER columna del archivo
        mask = df_soat.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)
        resultado = df_soat[mask]
        
        st.write(f"Se encontraron {len(resultado)} resultados:")
        st.dataframe(resultado, use_container_width=True)
    else:
        st.info("Escribe el número de un artículo o el nombre de un examen para comenzar.")
        st.dataframe(df_soat.head(20), use_container_width=True)

except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
