# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 12:27:28 2024

@author: jperezr
"""

import streamlit as st
import requests

# Título de la aplicación
st.title("Evaluación del Ejercicio 3")

# Sidebar para los criterios de evaluación
st.sidebar.title("Criterios a evaluar")

st.sidebar.subheader("Procesamiento y análisis de datos)")
st.sidebar.write("""
En **`app_flask.py`**:
- Se cargaron y procesaron los archivos CSV desde las rutas especificadas para cada entidad federativa.
- Se añadió la conversión de CSV a formato JSON usando Pandas y se implementó su almacenamiento en las rutas específicas.

En **`app_streamlit.py`**:
- Se permitieron seleccionar la entidad, la subcarpeta y el formato (CSV o JSON) para hacer las solicitudes a la API Flask.
- Los datos se descargan y procesan dinámicamente según la selección del usuario.
""")

st.sidebar.subheader("Diseño, implementación y ejecución del algoritmo)")
st.sidebar.write("""
En **`app_flask.py`**:
- Se implementó una API RESTful con endpoints POST para la descarga de archivos CSV y JSON.
- Se diseñó un sistema flexible para gestionar rutas de múltiples entidades y carpetas de destino para los archivos procesados.
- El algoritmo incluye la conversión de CSV a JSON y se permite al usuario descargar cualquiera de los dos formatos.

En **`app_streamlit.py`**:
- Se construyó una interfaz de usuario amigable para interactuar con la API Flask.
- Los usuarios pueden seleccionar la entidad federativa, el tipo de datos, y el formato de descarga (CSV o JSON).
""")

st.sidebar.subheader("Análisis de resultados")
st.sidebar.write("""
- Se validó que los archivos CSV y JSON fueran descargados correctamente en las rutas específicas de cada entidad federativa.
- Se verificó que los datos convertidos de CSV a JSON mantuvieran la estructura correcta y que la descarga se realizara sin errores.
""")

st.sidebar.subheader("Documentación de la solución")
st.sidebar.write("""
En **`app_flask.py`**:
- Se documentaron claramente las rutas para cada entidad y se describió el proceso de conversión y almacenamiento de datos en ambos formatos (CSV y JSON).

En **`app_streamlit.py`**:
- Se explicó cómo los usuarios pueden interactuar con la API seleccionando los criterios deseados (entidad, subcarpeta y formato).
""")

# Interacción con la API Flask desde Streamlit
st.subheader("Descargar datos de las entidades federativas")

# Seleccionar la entidad federativa
entidad = st.selectbox("Seleccionar la entidad federativa", ["aguascalientes", "guanajuato", "jalisco", "oaxaca"])

# Seleccionar la subcarpeta de datos
tipo_datos = st.selectbox("Seleccionar el tipo de datos", ["catalogo", "conjunto_de_datos", "diccionario_datos"])

# Seleccionar el formato de descarga
formato = st.selectbox("Seleccionar el formato de descarga", ["csv", "json"])

# Botón para descargar el archivo
if st.button("Descargar archivo"):
    url = f"http://localhost:5000/ejercicio/{entidad}/{tipo_datos}/descarga/"
    response = requests.post(url, json={"formato": formato})

    if response.status_code == 200:
        st.success(f"El archivo {formato.upper()} ha sido descargado con éxito.")
        st.download_button(label="Descargar archivo", data=response.content, file_name=f"{entidad}_{tipo_datos}_archivo.{formato}")
    else:
        st.error("Error al descargar el archivo.")
