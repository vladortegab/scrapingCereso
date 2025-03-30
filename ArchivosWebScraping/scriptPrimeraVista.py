from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
import re
import csv
import json

from selenium.common.exceptions import TimeoutException

def iniciar_navegador():
    """Configura y devuelve el driver de Selenium."""
    driver = webdriver.Chrome()  # Asegúrate de que chromedriver está en PATH
    driver.get("https://mesadeservicio.ica.gov.co:8090/cereso/Index.aspx")
    time.sleep(5)  # Espera para evitar que la URL quede en 'data:,' 
    return driver

def iniciar_sesion(driver, usuario, contraseña):
    """Inicia sesión en CERESO con el usuario y contraseña dados."""
    try:
        usuario_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
        )
        usuario_input.send_keys(usuario)
        print("¡Campo de usuario encontrado y llenado!")

        contraseña_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
        )
        contraseña_input.send_keys(contraseña)
        print("¡Campo de contraseña encontrado y llenado!")

        contraseña_input.send_keys(Keys.RETURN)
        print("¡Inicio de sesión exitoso!")
        time.sleep(5)

    except Exception as e:
        print("Error al iniciar sesión:", e)

def extraer_tabla(driver):
    """Extrae datos de la tabla y los guarda en un archivo CSV."""
    try:
        wait = WebDriverWait(driver, 10)
        print("Iniciando extracción de datos...")

        # 1️⃣ Hacer clic en el botón 'Vista' para desplegar opciones
        try:
            boton_vista = wait.until(EC.presence_of_element_located((By.XPATH, "//li[contains(@class, 'ColorTab')]/a[div/div[text()='Vista']]")))
            boton_vista.click()
            print("Se hizo clic en la pestaña 'Vista'.")
            time.sleep(2)
        except Exception as e:
            print("No se pudo abrir la vista de opciones:", e)
            return

        # 2️⃣ Seleccionar 100 en el select
        try:
            select_element = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@class='form-control']")))
            select = Select(select_element)
            select.select_by_value("100")
            print("Se seleccionó '100 filas' en el selector.")

            time.sleep(5)  # Esperar que carguen los datos
        except Exception as e:
            print("No se pudo seleccionar 100 registros por página:", e)
            return
            
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
        # Convertir datos a JSON
            json_data = json.dumps(data, ensure_ascii=False, indent=4)

            # Guardar en archivo JSON
            with open("primera_vista.json", "w", encoding="utf-8") as json_file:
                json_file.write(json_data)

            print("Extracción completada. Datos guardados en 'primera_vista.json'")

            return json_data

        except Exception as e:
            print("Error al extraer la tabla principal:", e)
            
    except Exception as e:
        print("Error general en la extracción:", e)
        return json.dumps([])
       
if __name__ == "__main__":
    driver = iniciar_navegador()
    
    usuario = "vladimir.ortega"
    contraseña = "Col2024#"  # ⚠️ Usa variables de entorno en producción

    iniciar_sesion(driver, usuario, contraseña)
    extraer_tabla(driver)  # Extraer y guardar la primera vista


    driver.quit()
