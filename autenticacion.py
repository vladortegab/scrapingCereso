from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
import time

# Configurar el WebDriver
# driver = webdriver.Chrome()  # Asegúrate de que chromedriver está en PATH
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