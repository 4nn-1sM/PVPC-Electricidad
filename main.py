import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sb
import xlrd
import datetime
from Utils import utils as ut



# Variables a utilizar en las diferentes funciones.

carpeta_origen = "../../../Downloads"
carpeta_destino = "./Data"

# Aplicamos  la función descomprimir_pvpc para extraer de los zip de la carpeta descargas relacionados con el proyecto, todos los archivos en la carpeta Data
ut.descomprimir_pvpc(carpeta_origen, carpeta_destino)

# Aplicamos la función copy_data de utils para que itere por todos los archivos que hay en la carpeta Data y los guarde en el CSV.
df = ut.copy_data()