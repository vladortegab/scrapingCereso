from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
from selenium.common.exceptions import TimeoutException


def extraer_detalles_tabla(driver):
    """Extrae detalles de la segunda vista y los guarda en 'segunda_vista.csv'."""
    try:
        wait = WebDriverWait(driver, 10)
        print("⏳ Buscando la tabla de la segunda vista...")

        def obtener_filas():
            """Devuelve la lista actualizada de filas de la tabla."""
            table_element = wait.until(EC.presence_of_element_located((By.ID, "StackPanel_VclStackPanelContentMemTable_0_0")))
            return table_element.find_elements(By.TAG_NAME, "tr")

        data_segunda_vista = []
        actions = ActionChains(driver)
        total_filas = len(obtener_filas())  # 🔹 Obtener cantidad total de filas

        index = 0  # 🔹 Control manual del índice
        while index < total_filas:
            try:
                filas = obtener_filas()  # 🔹 Siempre obtener la tabla actualizada
                if index >= len(filas):  
                    print("⚠️ Se alcanzó el final de la tabla.")
                    break  

                fila = filas[index]
                celdas = fila.find_elements(By.TAG_NAME, "td")
                if len(celdas) < 3:
                    index += 1  # 🔹 Avanzar al siguiente caso
                    continue  

                referencia = celdas[1].text.strip()
                if not referencia:
                    index += 1  # 🔹 Avanzar si la celda está vacía
                    continue  

                print(f"[{index}] Doble clic en: {referencia}")
                actions.double_click(celdas[1]).perform()
                time.sleep(3)

                # 🔹 Extraer datos de la segunda vista
                detalles_vista = []
                try:
                    elementos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "chat-box-body")))
                    for elem in elementos:
                        detalles_vista.append(elem.text.strip())

                    detalle_completo = " | ".join(detalles_vista)  
                except:
                    detalle_completo = "No se pudo extraer detalle"

                print(f"Detalles extraídos: {detalle_completo[:200]}")

                # 🔹 Extraer otro elemento antes de regresar
                try:
                    time.sleep(5)  
                    elementos_extra = driver.find_elements(By.XPATH, "//div[@id='StackPanel_h1_1_0']")
                    if elementos_extra:
                        elemento_extra = elementos_extra[0]  
                        detalles_vista.append(f"📌 Número de Caso: {elemento_extra.text.strip()}")
                    else:
                        print(f"⚠️ No se encontró 'Número de Caso' en la fila {index}.")
                        detalles_vista.append("📌 Número de Caso: No disponible")
                except Exception as e:
                    print(f"⚠️ Error al extraer el 'Número de Caso' en la fila {index}: {e}")
                    detalles_vista.append("📌 Número de Caso: Error")


                detalle_completo = " | ".join(detalles_vista)   
                data_segunda_vista.append([referencia, detalle_completo])

              # 🔹 Volver a la tabla principal
                try:
                    time.sleep(5)  # Espera breve antes de buscar el botón
                    
                    boton_volver = wait.until(
                       EC.presence_of_element_located((By.CSS_SELECTOR, "a[title='Inicio']"))
                        #EC.presence_of_element_located((By.XPATH, "//a[@title='Consola']"))
                    )
                    
                    
                    print("Validar un salto")
                    """
                    boton_volver = wait.until(
                       # EC.presence_of_element_located((By.CLASS_NAME, "ion-reply.btn-close-all"))
                        #EC.presence_of_element_located((By.XPATH, "//a[@title='Consola']"))
                    )
                    """
                    print("Validar un salto2 ")
                    if boton_volver.is_displayed() and boton_volver.is_enabled():
                        print("Validar un salto3 ")
                        boton_volver.click()
                        print(f"🔙 Se hizo clic en el botón de volver en la fila {index}.")
                    else:
                        print("Validar un salto4 ")
                        raise Exception("El botón de volver no está interactuable.")
                except Exception as e:
                    print(f"⚠️ Validar error de : {e}")
                    print(f"⚠️ No se encontró el botón de volver en la fila {index}. Intentando con `driver.back()`")
                    driver.back()



                index += 1  # 🔹 Avanzar al siguiente caso correctamente
                total_filas = len(obtener_filas())  # 🔹 Recalcular total de filas por si la tabla cambia

            except Exception as e:
                print(f"❌ Error en la fila {index}: {e}")
                index += 1  # 🔹 Continuar con el siguiente caso si hay error

        # 🔹 Guardar segunda vista en CSV solo si hay datos
        if data_segunda_vista:
            df_segunda = pd.DataFrame(data_segunda_vista, columns=["Referencia", "Detalles"])
            df_segunda.to_csv("segunda_vista.csv", index=False)
            print("✅ Segunda vista guardada en 'segunda_vista.csv'.")
        else:
            print("⚠️ No se extrajo ningún dato para la segunda vista.")

    except Exception as e:
        print("❌ Error general en la extracción:", e)
