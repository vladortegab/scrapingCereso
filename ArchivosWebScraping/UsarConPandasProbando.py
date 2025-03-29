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



def extraer_detalles_caso(driver, wait, index):
    """Extrae los detalles de un caso individual sin agregar información vacía."""
    detalles_vista = []
    caso = "N/A"
    
    # Extraer número de caso
    """ try:
        time.sleep(5)
        elementos_extra = driver.find_elements(By.XPATH, "//div[@id='StackPanel_h1_1_0']")
        for elem in elementos_extra:
            if elem.text.strip():
                caso = elem.text.strip()
                detalles_vista.append(f"📌 Número de Caso: {caso}")
                break  # Tomar el primer número válido
    except Exception as e:
        detalles_vista.append(f"📌 Número de Caso: Error ({e})") """
    #Extraccion de informacion conversación con Funcionario
    try:
        elementos = driver.find_elements(By.CSS_SELECTOR, ".cont-aten .chat-box-body .chat-box-body-elem")
        detalles_tabla1 = []

        for elemento in elementos:
            usuario = elemento.find_element(By.CSS_SELECTOR, ".item-user-name.font-1").text.strip() if elemento.find_elements(By.CSS_SELECTOR, ".item-user-name.font-1") else None
            mensaje = elemento.find_element(By.CSS_SELECTOR, ".item-msg-lbl.font-3").text.strip() if elemento.find_elements(By.CSS_SELECTOR, ".item-msg-lbl.font-3") else None
            hora = elemento.find_element(By.CSS_SELECTOR, ".item-fecha-lbl.font-3").text.strip() if elemento.find_elements(By.CSS_SELECTOR, ".item-fecha-lbl.font-3") else None
            fecha_elemento = elemento.find_element(By.CSS_SELECTOR, ".title-cont-title label") if elemento.find_elements(By.CSS_SELECTOR, ".title-cont-title label") else None
            fecha = fecha_elemento.text.strip() if fecha_elemento else "N/A"
            
            mensajes = elemento.find_elements(By.CSS_SELECTOR, ".item-cont-main")

            for mensaje_elem in mensajes:
                usuario = mensaje_elem.find_element(By.CSS_SELECTOR, ".item-user-name.font-1").text.strip() if mensaje_elem.find_elements(By.CSS_SELECTOR, ".item-user-name.font-1") else None
                mensaje = mensaje_elem.find_element(By.CSS_SELECTOR, ".item-msg-lbl.font-3").text.strip() if mensaje_elem.find_elements(By.CSS_SELECTOR, ".item-msg-lbl.font-3") else None
                hora = mensaje_elem.find_element(By.CSS_SELECTOR, ".item-fecha-lbl.font-3").text.strip() if mensaje_elem.find_elements(By.CSS_SELECTOR, ".item-fecha-lbl.font-3") else None

            # Solo agrega la entrada si hay al menos un dato válido
            if usuario or mensaje or hora:
                detalles_tabla1.append(f"📌 Tabla 1: | Usuario: {usuario or 'N/A'} | Mensaje: {mensaje or 'N/A'} | Fecha: {fecha} | Hora: {hora or 'N/A'}")
        # Agregar solo si hay contenido válido
        if detalles_tabla1:
            detalles_vista.append(f"{' || '.join(detalles_tabla1)}")
    except Exception as e:
        detalles_vista.append(f"📌 Tabla 1: Error ({e})")
    
    #Extraccion de informacion conversación con Usuarios
    try:
        elementos = driver.find_elements(By.CSS_SELECTOR, ".cont-messages .chat-box-body .chat-box-body-elem")
        detalles_tabla1 = []

        for elemento in elementos:
            usuario = elemento.find_element(By.CSS_SELECTOR, ".item-user-name.font-1").text.strip() if elemento.find_elements(By.CSS_SELECTOR, ".item-user-name.font-1") else None
            mensaje = elemento.find_element(By.CSS_SELECTOR, ".item-msg-lbl.font-3").text.strip() if elemento.find_elements(By.CSS_SELECTOR, ".item-msg-lbl.font-3") else None
            hora = elemento.find_element(By.CSS_SELECTOR, ".item-fecha-lbl.font-3").text.strip() if elemento.find_elements(By.CSS_SELECTOR, ".item-fecha-lbl.font-3") else None
            fecha_elemento = elemento.find_element(By.CSS_SELECTOR, ".title-cont-title label") if elemento.find_elements(By.CSS_SELECTOR, ".title-cont-title label") else None
            fecha = fecha_elemento.text.strip() if fecha_elemento else "N/A"
            
            mensajes = elemento.find_elements(By.CSS_SELECTOR, ".item-cont-main")

            for mensaje_elem in mensajes:
                usuario = mensaje_elem.find_element(By.CSS_SELECTOR, ".item-user-name.font-1").text.strip() if mensaje_elem.find_elements(By.CSS_SELECTOR, ".item-user-name.font-1") else None
                mensaje = mensaje_elem.find_element(By.CSS_SELECTOR, ".item-msg-lbl.font-3").text.strip() if mensaje_elem.find_elements(By.CSS_SELECTOR, ".item-msg-lbl.font-3") else None
                hora = mensaje_elem.find_element(By.CSS_SELECTOR, ".item-fecha-lbl.font-3").text.strip() if mensaje_elem.find_elements(By.CSS_SELECTOR, ".item-fecha-lbl.font-3") else None

            # Solo agrega la entrada si hay al menos un dato válido
            if usuario or mensaje or hora:
                detalles_tabla1.append(f"📌 Tabla 2: | Usuario: {usuario or 'N/A'} | Mensaje: {mensaje or 'N/A'} | Fecha: {fecha} | Hora: {hora or 'N/A'}")
        # Agregar solo si hay contenido válido
        if detalles_tabla1:
            detalles_vista.append(f"{' || '.join(detalles_tabla1)}")
    except Exception as e:
        detalles_vista.append(f"📌 Tabla 2: Error ({e})")
        
        
    return " | ".join(detalles_vista) if detalles_vista else "No se encontraron detalles"
def extraer_detalles_tabla(driver):
    """Extrae detalles de la segunda vista y los guarda en 'segunda_vista.csv'."""
    try:
        wait = WebDriverWait(driver, 10)
        print("⏳ Iniciando extracción de datos...")

        # 1️⃣ Hacer clic en el botón 'Vista' para desplegar opciones
        try:
            boton_vista = wait.until(EC.presence_of_element_located((By.XPATH, "//li[contains(@class, 'ColorTab')]/a[div/div[text()='Vista']]")))
            boton_vista.click()
            print("✅ Se hizo clic en la pestaña 'Vista'.")
            time.sleep(2)
        except Exception as e:
            print("⚠️ No se pudo abrir la vista de opciones:", e)
            return

        # 2️⃣ Seleccionar 100 en el select
        try:
            select_element = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@class='form-control']")))
            select = Select(select_element)
            select.select_by_value("100")
            print("✅ Se seleccionó '100 filas' en el selector.")

            time.sleep(5)  # Esperar que carguen los datos
        except Exception as e:
            print("⚠️ No se pudo seleccionar 100 registros por página:", e)
            return

        data_segunda_vista = []
        actions = ActionChains(driver)

        def obtener_filas():
            """Devuelve la lista actualizada de filas de la tabla."""
            table_element = wait.until(EC.presence_of_element_located((By.ID, "StackPanel_VclStackPanelContentMemTable_0_0")))
            return table_element.find_elements(By.TAG_NAME, "tr")

        total_filas = len(obtener_filas())
        index = 0

        while index < total_filas:
            try:
                filas = obtener_filas()
                if index >= len(filas):  
                    print("⚠️ Se alcanzó el final de la tabla.")
                    break  
                
                fila = filas[index]
                celdas = fila.find_elements(By.TAG_NAME, "td")
                if len(celdas) < 3:
                    index += 1
                    continue  
                
                referencia = celdas[1].text.strip()
                if not referencia:
                    index += 1  
                    continue  
                
                print(f"[{index}] Doble clic en: {referencia}")
                actions.double_click(celdas[1]).perform()
                time.sleep(3)
                
                detalle_completo = extraer_detalles_caso(driver, wait, index)
                print(f"Detalles extraídos: {detalle_completo[:200]}")
                data_segunda_vista.append([referencia, detalle_completo])
                
                try:
                    time.sleep(5)
                    boton_volver = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[title='Inicio']")))
                    if boton_volver.is_displayed() and boton_volver.is_enabled():
                        boton_volver.click()
                        print(f"🔙 Se hizo clic en el botón de volver en la fila {index}.")
                    
                        """
                        # Este codigo es por si quiere pasar por paginas los casos #Edicion 1
                        # Volver a la página correcta
                        for _ in range(pagina_actual - 1):
                            try:
                                siguiente_pagina = driver.find_element(By.XPATH, "//ul[@id='myPager']/li[not(contains(@class, 'active'))]/a[@class='page_link']")
                                siguiente_pagina.click()
                                print(f"➡️ Volviendo a la página {pagina_actual}...")
                                time.sleep(5)
                            except Exception:
                                print("⚠️ No se pudo regresar a la página correcta. Verificar navegación.")
                                break    
                    """         
                    else:
                        raise Exception("El botón de volver no está interactuable.")
                except Exception as e:
                    print(f"⚠️ Validar error de : {e}")
                    print(f"⚠️ No se encontró el botón de volver en la fila {index}. Intentando con `driver.back()`")
                    driver.back()
                
                index += 1
                total_filas = len(obtener_filas())  
            
            except Exception as e:
                print(f"❌ Error en la fila {index}: {e}")
                index += 1
            """ 
                    #Este codigo es por si quiere pasar por paginas los casos #Edicion 1
            try:
                siguiente_pagina = driver.find_element(By.XPATH, "//ul[@id='myPager']/li[not(contains(@class, 'active'))]/a[@class='page_link']")
                if siguiente_pagina.is_displayed() and siguiente_pagina.is_enabled():
                    siguiente_pagina.click()
                    pagina_actual += 1  # Actualizar la página actual
                    print(f"➡️ Avanzando a la página {pagina_actual}...")
                    time.sleep(5)  # Esperar a que la página se cargue completamente
                else:
                    print("✅ No hay más páginas disponibles.")
                    break  # Salir del bucle si no hay más páginas
            except NoSuchElementException:
                print("✅ No se encontró el botón de siguiente página. Finalizando extracción.")
                break """
                                
        if data_segunda_vista:
            df_segunda = pd.DataFrame(data_segunda_vista, columns=["Referencia", "Detalles"])
            df_segunda.to_csv("segunda_vista.csv", index=False)
            print("✅ Segunda vista guardada en 'segunda_vista.csv'.")
        else:
            print("⚠️ No se extrajo ningún dato para la segunda vista.")
    
    except Exception as e:
        print("❌ Error general en la extracción:", e)


       
if __name__ == "__main__":
    driver = iniciar_navegador()
    
    usuario = "vladimir.ortega"
    contraseña = "Col2024#"  # ⚠️ Usa variables de entorno en producción

    iniciar_sesion(driver, usuario, contraseña)
    extraer_tabla(driver)  # Extraer y guardar la primera vista
    extraer_detalles_tabla(driver)  # Extraer y guardar la segunda vista


    input("Presiona Enter para cerrar el navegador...")
    driver.quit()
