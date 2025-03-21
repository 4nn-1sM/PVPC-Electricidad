import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sb
import xlrd
import datetime
from Utils import utils as ut


# Aplicamos la función copy_data de utils para que itere por todos los archivos que hay en la carpeta Data y los guarde en el CSV.
df = ut.copy_data()
