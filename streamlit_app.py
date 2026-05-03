import streamlit as st
import pandas as pd

# ... (mantener la carga de datos igual) ...

try:
    df_soat = load_data()
    
    # Dividimos la pantalla en dos: Buscador y Normativa
    tab1, tab2 = st.tabs(["🔍 Buscador de Códigos", "📜 Artículos y Parágrafos"])

    with tab1:
        busqueda = st.text_input("Ingrese código o descripción:")
        if busqueda:
            mask = df_soat.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)
            st.dataframe(df_soat[mask], use_container_width=True)

    with tab2:
        # Filtramos solo las filas que parecen ser artículos o parágrafos
        normativa = df_soat[df_soat.iloc[:, 0].astype(str).str.contains('ARTICULO|PARAGRAFO', case=False, na=False)]
        
        seleccion = st.selectbox("Seleccione un Artículo para leerlo:", normativa.iloc[:, 0].unique())
        
        if seleccion:
            # Mostramos la fila completa de ese artículo
            detalle = normativa[normativa.iloc[:, 0] == seleccion]
            st.warning(f"**Detalle legal:** {seleccion}")
            st.write("Consulte los códigos asociados en la pestaña de buscador.")

except Exception as e:
    st.error(f"Error: {e}")
