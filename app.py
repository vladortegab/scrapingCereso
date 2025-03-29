from navegador import iniciar_navegador
from autenticacion import iniciar_sesion
from extraerTabla import extraer_tabla
from extraerDatosCasos import extraer_detalles_tabla

        
if __name__ == "__main__":
    driver = iniciar_navegador()
    
    usuario = "vladimir.ortega"
    contraseña = "Col2024#"  # ⚠️ Usa variables de entorno en producción

    iniciar_sesion(driver, usuario, contraseña)
    extraer_tabla(driver)  # Extraer y guardar la primera vista
    extraer_detalles_tabla(driver)  # Extraer y guardar la segunda vista


    input("Presiona Enter para cerrar el navegador...")
    driver.quit()
