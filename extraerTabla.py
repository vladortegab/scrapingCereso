from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


def extraer_tabla(driver):
    """Extrae datos de la tabla y los guarda en un archivo CSV."""
    try:
        # Esperar a que la tabla cargue
        wait = WebDriverWait(driver, 10)
        table_element = wait.until(EC.presence_of_element_located((By.ID, "StackPanel_VclStackPanelContentMemTable_0_0")))

        # Extraer filas de la tabla
        rows = table_element.find_elements(By.TAG_NAME, "tr")
        data = []

        for row in rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            row_data = [col.text.strip() for col in columns]
            if row_data:
                data.append(row_data)

        # Convertir a DataFrame y guardar en CSV
        df = pd.DataFrame(data)
        df.to_csv("primera_vista.csv", index=False)
        print("Extracción completada. Datos guardados en 'datos_extraidos.csv'")

    except Exception as e:
        print("❌ Error al extraer la tabla principal:", e)