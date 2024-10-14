# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 12:27:28 2024

@author: jperezr
"""

import os
import pandas as pd
import streamlit as st
import json

# Define las rutas a los archivos CSV en diferentes subcarpetas
rutas_csv = {
    "aguascalientes": {
        "catalogo": r"data/aguascalientes/catalogo/archivo_catalogo.csv",
        "diccionario_datos": r"data/aguascalientes/diccionario_datos/archivo_diccionario.csv"
    },
    "guanajuato": {
        "catalogo": r"data/guanajuato/catalogo/archivo_catalogo.csv",
        "diccionario_datos": r"data/guanajuato/diccionario_datos/archivo_diccionario.csv"
    },
    "jalisco": {
        "catalogo": r"data/jalisco/catalogo/catalogos/archivo_catalogo.csv",
        "diccionario_datos": r"data/jalisco/diccionario_datos/archivo_diccionario.csv"
    },
    "oaxaca": {
        "catalogo": r"data/oaxaca/catalogo/catalogos/archivo_catalogo.csv",
        "diccionario_datos": r"data/oaxaca/diccionario_datos/archivo_diccionario.csv"
    }
}

# Función para obtener estadísticos de un archivo CSV
def obtener_estadisticas(entidad):
    # Obtener ruta del catalogo
    ruta_csv = rutas_csv.get(entidad, {}).get("catalogo")
    
    if ruta_csv and os.path.exists(ruta_csv):
        df = pd.read_csv(ruta_csv)
        estadisticas = {
            "entidad": entidad,
            "promedio": df.mean(numeric_only=True).to_dict(),  # Promedio de todas las columnas numéricas
            "mediana": df.median(numeric_only=True).to_dict(),  # Mediana de todas las columnas numéricas
            "total": df.sum(numeric_only=True).to_dict()       # Total de todas las columnas numéricas
        }
        return estadisticas
    else:
        return None

# Configuración de Streamlit
st.title("API de Datos de Entidades Federativas")

# Seleccionar la entidad federativa
entidad = st.selectbox("Seleccionar la entidad federativa", ["aguascalientes", "guanajuato", "jalisco", "oaxaca"])

# Subir archivo si se quiere descargar
tipo_datos = st.selectbox("Seleccionar el tipo de datos", ["catalogo", "diccionario_datos"])

# Seleccionar el formato de descarga
formato = st.selectbox("Seleccionar el formato de descarga", ["csv", "json"])

# Botón para descargar el archivo
if st.button("Descargar archivo"):
    ruta_csv = rutas_csv.get(entidad, {}).get(tipo_datos)
    
    if ruta_csv and os.path.exists(ruta_csv):
        if formato == "csv":
            with open(ruta_csv, 'rb') as f:
                st.download_button(label="Descargar archivo CSV", data=f, file_name=os.path.basename(ruta_csv))
        elif formato == "json":
            df = pd.read_csv(ruta_csv)
            data_json = df.to_dict(orient="records")
            json_data = json.dumps(data_json, ensure_ascii=False, indent=4)
            st.download_button(label="Descargar archivo JSON", data=json_data, file_name=f"{entidad}_{tipo_datos}.json")
    else:
        st.error("Error: Archivo CSV no encontrado.")

# Endpoint de estadísticos
if st.button("Obtener Estadísticos"):
    estadisticas = obtener_estadisticas(entidad)
    
    if estadisticas:
        st.json(estadisticas)
    else:
        st.error("Error: No se pudieron obtener estadísticos para esta entidad.")
