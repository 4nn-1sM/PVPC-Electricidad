import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sb
import xlrd
import datetime
import zipfile
import re




# Función para descomprimir los archivos zip descargados de la página de i-de.
def descomprimir_pvpc(carpeta_origen, carpeta_destino):
    # Verificar si la carpeta de destino existe, si no, crearla
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    # Buscar archivos ZIP que contengan "pvpc" en su nombre
    archivos_zip = [f for f in os.listdir(carpeta_origen) if re.search(r'pvpc', f, re.IGNORECASE) and f.endswith('.zip')]

    if not archivos_zip:
        print("No se encontraron archivos ZIP con 'pvpc' en el nombre.")
        return

    # Extraer los archivos encontrados
    for archivo_zip in archivos_zip:
        ruta_zip = os.path.join(carpeta_origen, archivo_zip)
        with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
            zip_ref.extractall(carpeta_destino)
        print(f"Extraído: {archivo_zip} en {carpeta_destino}")
    

carpeta_origen = "../../../Downloads"
carpeta_destino = "./Data"


# Abrimos uno de los archivos excel de los precios diarios para ver cómo está organizado
book = xlrd.open_workbook("./Data/PVPC_DETALLE_DD_20240302.xls")

# Definimos la variable con la que trabajaremos la hoja que nos interesa. En este caso la primera hoja
sh = book.sheet_by_index(0)


def copy_data():
    print(os.getcwd())
    # Defininimos el path absoluto de la carpeta "Data"
    data_path = os.path.join(os.path.dirname(__file__), "../Data")

    # Verificar si la carpeta existe
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"No se encontró la carpeta: {data_path}")

    # Creamos el dataframe que guardará todos los datos recogidos de los archivos diarios de los precios
    df = pd.DataFrame(columns=['Día',
    'Hora',
    'Peaje',
    'Periodo',
    'Término energía PVPC\nFEU = TEU + TCU\n€/MWh consumo',
    'Peajes y cargos TEU\n€/MWh consumo',
    'Precio producción\nTCU=CP x(1+PERD/100)\n€/MWh consumo'])
    # Definimos el tipo de dato que contendrá cada columna
    df = df.astype({
        'Hora': 'float',
        'Peaje': 'object',
        'Periodo': 'object',
        'Término energía PVPC\nFEU = TEU + TCU\n€/MWh consumo': 'float',
        'Peajes y cargos TEU\n€/MWh consumo': 'float',
        'Precio producción\nTCU=CP x(1+PERD/100)\n€/MWh consumo': 'float'
        })

    df['Día'] = pd.to_datetime(df['Día'], errors='coerce')

    print(f"Procesando archivos en: {data_path}")

    # Iteramos por todos los archivos contenidos en la carpeta Data
    for i in os.listdir(data_path):
        print(i)
        if i.endswith('.xls'):
            file_path = os.path.join(data_path, i)
            print(f"Procesando: {i}")
            # Cargamos el archivo Excel
            book = xlrd.open_workbook(file_path)
            sh = book.sheet_by_index(0)


        for rx in range(5,sh.nrows):
            row = []        
            for cx in range(7):
                row.append("{0}".format(sh.cell_value(rowx=rx, colx=cx)))
            row_df = pd.DataFrame([row], columns=df.columns)
            # Convertir texto a número
            for col in row_df.columns[:2]:
                row_df[col] = pd.to_numeric(row_df[col])
            for col in row_df.columns[4:]:
                row_df[col] = pd.to_numeric(row_df[col])

            # Convertir texto a fecha
            row_df["Día"] = pd.to_datetime(row_df["Día"], origin="1899-12-30", unit="D", errors="coerce").dt.date

            # Convertir texto a hora. Aquí vamos a tener problema en octubre con el cambio de hora, ya que 
            row_df["Hora"] = row_df["Hora"].astype(int)
            row_df["Hora"] = row_df["Hora"].apply(lambda x: "00:00:00" if x == 24 else f"{x}:00:00")
            row_df["Hora"] = pd.to_datetime(row_df["Hora"], format="%H:%M:%S").dt.time
        
            # Concatenar los datos al dataframe
            df = pd.concat([df, row_df], ignore_index=True)
    # Guardamos este dataframe en un nuevo csv que va a recoger todos los precios de los diferentes excel diarios        
    output_path = os.path.join(os.path.dirname(__file__), "../PVPC_diarios.csv")
    df.to_csv(output_path, index=False)
    print(f"Datos guardados en {output_path}")
    return df

