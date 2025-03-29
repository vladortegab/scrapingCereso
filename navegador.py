from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
driver = webdriver.Chrome()
def iniciar_navegador():
    """Inicia el navegador y abre la URL."""
    
    print("🔄 Iniciando navegador...")
    driver.get("https://mesadeservicio.ica.gov.co:8090/cereso/Index.aspx")
   

   
    
    
    time.sleep(5)  # Esperar para asegurarse de que la página carga

    print("✅ Navegador iniciado correctamente.")
    
    return driver
