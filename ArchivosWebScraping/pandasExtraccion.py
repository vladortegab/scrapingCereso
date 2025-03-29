""" import pandas as pd
import re

# Cargar el archivo CSV original con encoding utf-8
df = pd.read_csv("segunda_vista.csv", dtype=str, encoding="utf-8")

# Asegurar que la columna "Detalles" no contenga valores nulos
df["Detalles"] = df["Detalles"].fillna("")

# Filtrar filas donde "Detalles" no sea "No se encontraron detalles"
df = df[~df["Detalles"].str.contains("No se encontraron detalles", na=False, case=False)]

# Función para extraer diálogos desde la columna "Detalles"
def extraer_dialogos(id_caso, detalle):
"""
    #Extrae los diálogos de la columna 'Detalles' y los estructura en filas separadas.
"""                                                                                          
    # Expresión regular mejorada para capturar fechas y horas opcionales
    patrones = re.findall(
        r'📌\s*(Tabla\s*\d+):?\s*\|\s*Usuario:\s*([^|]+)\s*\|\s*Mensaje:\s*([^|]+)\s*(?:\|\s*Fecha:\s*([\d/-]+|N/A))?\s*(?:\|\s*Hora:\s*([^|]+|N/A))?', 
        detalle
    )

    dialogos = []

    # Si hay diálogos, procesarlos
    if patrones:
        for tabla, usuario, mensaje, fecha, hora in patrones:
            dialogos.append({
                "Referencia": id_caso,  # Usar directamente el ID del caso desde el DataFrame
                "Dialogo": tabla.strip(),
                "Usuario": usuario.strip(),
                "Mensaje": mensaje.strip(),
                "Fecha": fecha.strip() if fecha else "N/A",
                "Hora": hora.strip() if hora else "N/A"
            })
    else:
        # Si no hay diálogos, devolver la fila con valores "No encontrado"
        dialogos.append({
            "Referencia": id_caso,
            "Dialogo": "No encontrado",
            "Usuario": "No encontrado",
            "Mensaje": "No encontrado",
            "Fecha": "No encontrado",
            "Hora": "No encontrados"
        })

    return dialogos

# Expandir los datos dividiendo múltiples diálogos en filas separadas
data_expandida = []
for _, row in df.iterrows():
    id_caso = row["Referencia"]  # Tomar el ID desde la primera columna
    dialogos = extraer_dialogos(id_caso, row["Detalles"])  # Extraer diálogos correctamente
    data_expandida.extend(dialogos)  # Agregar cada diálogo extraído

# Crear un nuevo DataFrame con los diálogos separados
df_expandido = pd.DataFrame(data_expandida)

# Filtrar mensajes que no contienen información válida
df_expandido = df_expandido[df_expandido["Mensaje"] != "No encontrado"]

# Guardar el archivo limpio con encoding utf-8
df_expandido.to_csv("archivo_limpio.csv", index=False, encoding="utf-8")

print("✅ Archivo procesado correctamente y guardado como 'archivo_limpio.csv'")
 """
import pandas as pd
import re
import json
import os

# Obtiene la ruta del directorio del script actual
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construye la ruta correcta al archivo JSON
file_path = os.path.join(script_dir, "segunda_vista.json")
output_path = os.path.join(script_dir, "archivo_limpio.json")

# Verifica si el archivo existe
if not os.path.exists(file_path):
    print(f"🚨 El archivo {file_path} no existe.")
    exit()

# Intenta leer el JSON como un DataFrame
try:
    df = pd.read_json(file_path, dtype=str, encoding="utf-8")
except ValueError as e:
    print(f"🚨 Error al cargar el JSON: {e}")
    exit()

# Asegurar que la columna "Detalles" no contenga valores nulos
if "Detalles" in df.columns:
    df["Detalles"] = df["Detalles"].fillna("")
    df = df[~df["Detalles"].str.contains("No se encontraron detalles", na=False, case=False)]
else:
    print("🚨 La columna 'Detalles' no se encuentra en el JSON.")
    exit()

# Función para extraer diálogos desde la columna "Detalles"
def extraer_dialogos(id_caso, detalle):
    """
    Extrae los diálogos de la columna 'Detalles' y los estructura en una lista.
    """                                                                                          
    patrones = re.findall(
        r'📌\s*(Tabla\s*\d+):?\s*\|\s*Usuario:\s*([^|]+)\s*\|\s*Mensaje:\s*([^|]+)\s*(?:\|\s*Fecha:\s*([\d/-]+|N/A))?\s*(?:\|\s*Hora:\s*([^|]+|N/A))?', 
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
    print("🚨 La columna 'Referencia' no se encuentra en el JSON.")
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

print(f"✅ Archivo limpio guardado en: {output_path}")