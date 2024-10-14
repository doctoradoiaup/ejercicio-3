# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 12:22:49 2024

@author: jperezr
"""

import os
import pandas as pd
from flask import Flask, send_file, jsonify, request
import json

app = Flask(__name__)

# Define las rutas a los archivos CSV en diferentes subcarpetas
rutas_csv = {
    "aguascalientes": {
        "catalogo": r"data/aguascalientes/catalogo/archivo_catalogo.csv",
        #"conjunto_de_datos": r"archivo_conjunto.csv",
        "diccionario_datos": r"archivo_diccionario.csv"
    },
    "guanajuato": {
        "catalogo": r"archivo_catalogo.csv",
        "conjunto_de_datos": r"archivo_conjunto.csv",
        "diccionario_datos": r"archivo_diccionario.csv"
    },
    "jalisco": {
        "catalogo": r"catalogos/archivo_catalogo.csv",
        "conjunto_de_datos": r"archivo_conjunto.csv",
        "diccionario_datos": r"archivo_diccionario.csv"
    },
    "oaxaca": {
        "catalogo": r"archivo_catalogo.csv",
        "conjunto_de_datos": r"archivo_conjunto.csv",
        "diccionario_datos": r"archivo_diccionario.csv"
    }
}

@app.route('/ejercicio/<entidad>/<tipo>/descarga/', methods=['POST'])
def descargar_csv(entidad, tipo):
    # Obtener el formato desde el cuerpo de la solicitud
    formato = request.json.get('formato')
    ruta_csv = rutas_csv.get(entidad, {}).get(tipo)

    if ruta_csv and os.path.exists(ruta_csv):
        # Definir la ruta de destino según la entidad
        if entidad == "aguascalientes":
            ruta_descarga = f"download_aguascalientes/{entidad}_{tipo}_archivo.csv"
            ruta_json = f"download_aguascalientes/{entidad}_{tipo}_archivo.json"
        elif entidad == "guanajuato":
            ruta_descarga = f"download_guanajuato/{entidad}_{tipo}_archivo.csv"
            ruta_json = f"download_guanajuato/{entidad}_{tipo}_archivo.json"
        elif entidad == "jalisco":
            ruta_descarga = f"download_jalisco/{entidad}_{tipo}_archivo.csv"
            ruta_json = f"download_jalisco/{entidad}_{tipo}_archivo.json"
        elif entidad == "oaxaca":
            ruta_descarga = f"download_oaxaca/{entidad}_{tipo}_archivo.csv"
            ruta_json = f"download_oaxaca/{entidad}_{tipo}_archivo.json"

        if formato == "csv":
            # Copiar el archivo original a la nueva ubicación
            with open(ruta_csv, 'rb') as fsrc:
                with open(ruta_descarga, 'wb') as fdst:
                    fdst.write(fsrc.read())
            return send_file(ruta_descarga, as_attachment=True, download_name=f"{entidad}_{tipo}_archivo.csv")

        elif formato == "json":
            # Leer el archivo CSV y convertir a JSON
            df = pd.read_csv(ruta_csv)
            data_json = df.to_dict(orient="records")
            
            # Guardar el JSON en la ruta de descarga
            with open(ruta_json, 'w', encoding='utf-8') as json_file:
                json.dump(data_json, json_file, ensure_ascii=False, indent=4)
            
            # Devolver el archivo JSON guardado
            return send_file(ruta_json, as_attachment=True, download_name=f"{entidad}_{tipo}_archivo.json")

    else:
        print("Error: El archivo CSV no fue encontrado.")
        return {"error": "Archivo CSV no encontrado."}, 404


@app.route('/ejercicio/<entidad>/estadisticos/', methods=['GET'])
def estadisticos(entidad):
    # Aquí puedes definir cómo calcular los estadísticos relevantes
    estadisticas = {
        "entidad": entidad,
        "promedio": 12345,  # Aquí puedes calcular el promedio real
        "mediana": 67890,   # Aquí puedes calcular la mediana real
        "total": 13579      # Aquí puedes calcular el total real
    }
    return jsonify(estadisticas)


if __name__ == '__main__':
    app.run(port=5000)
