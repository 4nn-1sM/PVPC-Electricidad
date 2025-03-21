from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
import time
import pandas as pd
from datetime import datetime
from selenium.webdriver.common.keys import Keys
import os

# Aquí podemos modifiar el tipo de búsqueda y las fechas que queremos descargar. Con ello se modificará el link que tiene que introducirse al abrir el driver
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


