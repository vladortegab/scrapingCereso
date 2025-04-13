import pandas as pd
import re
import json
import os

# Obtiene la ruta del directorio del script actual
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construye la ruta correcta al archivo JSON
file_path = os.path.join(script_dir, "primera_vista.json")
output_path = os.path.join(script_dir, "archivo_limpio_primera_vista.json")

# Verifica si el archivo existe
if not os.path.exists(file_path):
    print(f"El archivo {file_path} no existe.")
    exit()

# Intenta leer el JSON como un DataFrame
try:
    df = pd.read_json(file_path, dtype=str, encoding="utf-8")
except ValueError as e:
    print(f"Error al cargar el JSON: {e}")
    exit()

# Asegurar que la columna "Detalles" no contenga valores nulos
if "Detalles" in df.columns:
    df["Detalles"] = df["Detalles"].fillna("")
    df = df[~df["Detalles"].str.contains("No se encontraron detalles", na=False, case=False)]
else:
    print("La columna 'Detalles' no se encuentra en el JSON.")
    exit()

# Función para extraer diálogos desde la columna "Detalles"
def extraer_dialogos(id_caso, detalle):
    """
    Extrae los diálogos de la columna 'Detalles' y los estructura en una lista.
    """                                                                                          
    patrones = re.findall(
        r'\s*(Tabla\s*\d+):?\s*\|\s*Usuario:\s*([^|]+)\s*\|\s*Mensaje:\s*([^|]+)\s*(?:\|\s*Fecha:\s*([\d/-]+|N/A))?\s*(?:\|\s*Hora:\s*([^|]+|N/A))?', 
        detalle
    )

    dialogos = []
    if patrones:
        for tabla, usuario, mensaje, fecha, hora in patrones:
            dialogos.append({
                "Tabla": tabla.strip(),
                "Usuario": usuario.strip(),
                "Mensaje": mensaje.strip(),
                "Fecha": fecha.strip() if fecha else "N/A",
                "Hora": hora.strip() if hora else "N/A"
            })
    
    return dialogos

# Diccionario para agrupar datos por referencia
datos_json = {}

if "Referencia" not in df.columns:
    print("La columna 'Referencia' no se encuentra en el JSON.")
    exit()

for _, row in df.iterrows():
    id_caso = row["Referencia"]  
    dialogos = extraer_dialogos(id_caso, row["Detalles"])  

    if dialogos:  
        if id_caso not in datos_json:
            datos_json[id_caso] = {"Referencia": id_caso, "Detalles": []}
        datos_json[id_caso]["Detalles"].extend(dialogos)


# Convertir a lista para guardar en un archivo JSON
resultado_json = list(datos_json.values())

# Guardar en archivo
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(resultado_json, f, indent=4, ensure_ascii=False)

print(f"Archivo limpio guardado en: {output_path}")