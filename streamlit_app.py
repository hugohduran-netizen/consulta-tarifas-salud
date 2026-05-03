import streamlit as st
import pandas as pd

st.set_page_config(page_title="Consulta SOAT 2023", layout="wide")

st.title("📊 Consulta de Manual Tarifario SOAT")

# Función para cargar los datos
@st.cache_data
def load_data():
    # Leemos la hoja 'SOAT 2023' saltando las filas de encabezado decorativo
    df = pd.read_excel("Manual-Tarifario-SOAT-2023-.xlsx", sheet_name='SOAT 2023', skiprows=3)
    # Renombrar columnas para facilitar la búsqueda
    df.columns = ['Código', 'Descripción', 'Factor SMLDV', 'Factor UVT', 'Valor 2022', 'Valor 2023', 'Valor 2024', 'Valor 2025']
    return df

try:
    df_soat = load_data()

    # Buscador interactivo
    busqueda = st.text_input("Busca por código o descripción del procedimiento:")

    if busqueda:
        # Filtramos los datos
        resultado = df_soat[
            df_soat['Código'].astype(str).str.contains(busqueda, case=False) | 
            df_soat['Descripción'].astype(str).str.contains(busqueda, case=False)
        ]
        st.write(f"Se encontraron {len(resultado)} resultados:")
        st.dataframe(resultado, use_container_width=True)
    else:
        st.info("Escribe algo arriba para empezar a buscar.")
        st.dataframe(df_soat.head(10), use_container_width=True)

except Exception as e:
    st.error(f"Asegúrate de subir el archivo Excel a GitHub. Error: {e}")
