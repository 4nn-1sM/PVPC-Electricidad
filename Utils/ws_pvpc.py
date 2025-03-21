from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
import time
import pandas as pd
from datetime import datetime
from selenium.webdriver.common.keys import Keys
import os
import calendar

"""

PENDIENTE DE COMPROBAR QUE FUNCIONE LA FUNCIÓN DE OBTENER FECHA FINAL E INICIAL Y HACER AJUSTES PARA PODER ELEGIR SI ES DESCARGA INICIAL, MENSUAL O RANGO DETERMINADO DE FECHA

DESCARGA INICIAL: Tomará la primera fecha desde que hay registro de datos 1/4/2014 hasta el último día del mes anterior al mes en el que estamos haciendo la petición

DESCARGA MENSUAL: Descargará los datos del mes anterior al actual en el que realizamos la petición

DESCARGA RANGO DE FECHA: Solicitará incluir las fechas de las que deseemos realizar la descarga


"""



# Función para obtener la fecha final de las descargas. Toma como base el día de hoy(cuando se corre el código) y devuelve el último día del mes anterior.
def obtener_fecha_final():
    # Obtener la fecha actual
    hoy = datetime.today()
    
    # Determinar el último día del mes anterior
    ultimo_dia_mes_anterior = calendar.monthrange(hoy.year, hoy.month - 1 if hoy.month > 1 else 12)[1]
    
    # Obtener el año y mes del mes anterior
    año = hoy.year if hoy.month > 1 else hoy.year - 1
    mes = hoy.month - 1 if hoy.month > 1 else 12

    # Construir la fecha en formato YYYY-MM-DD
    fecha_final = datetime(ultimo_dia_mes_anterior, mes, año).strftime("%d-%m-%Y")
    
    return fecha_final

# Uso
fecha_final_descarga = obtener_fecha_final()
print("Fecha final de descarga:", fecha_final_descarga)

# Funcion para obtener la fecha inicial de descargas del mes anterior al actual.
def obtener_fecha_inicial():
    # Obtener la fecha actual
    hoy = datetime.today()
    
    # Obtener el año y mes del mes anterior
    año = hoy.year if hoy.month > 1 else hoy.year - 1
    mes = hoy.month - 1 if hoy.month > 1 else 12


    # Construir la fecha en formato YYYY-MM-DD
    fecha_inicial = datetime(1, mes, año).strftime("%d-%m-%Y")
    
    return fecha_inicial

# Uso
fecha_inicial_descarga = obtener_fecha_final()
print("Fecha inicial de descarga:", fecha_inicial_descarga)

# Descarga inicial. La web recoge datos desde el 1/4/2014
start_date_first_dw = "01-04-2014"
end_date_first_dw = fecha_final_descarga


# Aquí podemos modifcar el tipo de búsqueda y las fechas que queremos descargar. Con ello se modificará el link que tiene que introducirse al abrir el driver
search_type = "datos"
search_start_date = datetime.strptime("1/1/2022", "%d/%m/%Y").strftime("%#d-%#m-%Y")
search_end_date = datetime.strptime("31/1/2022", "%d/%m/%Y").strftime("%#d-%#m-%Y")

# Con esto abrimos el driver
cr_dr_path = "../Utils/chromedriver.exe"
service = Service(executable_path=cr_dr_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.get(f"https://www.esios.ree.es/es/descargas?date_type={search_type}&start_date={search_start_date}&end_date={search_end_date}")

# Para aceptar solo las cookies necesarias
loadMore = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/div/div[2]/button[4]')
loadMore.click()

# Con esto buscamos los archivos relativos a la descarga de precios
buscador = driver.find_element(By.XPATH, '/html/body/main/div/div[2]/div/div[4]/div/div[1]/div[2]/div[1]/input')
buscador.send_keys('pvpc')
buscador.submit()


# Aquí se busca el elemento que iniciará la descarga y se le clicará
elemento_descarga = driver.find_element(By.XPATH, '/html/body/main/div/div[2]/div/div[4]/div/div[1]/div[4]/table/tbody/tr[3]/td[1]/a')
elemento_descarga.click()

# Para cerrar el driver
driver.quit()


