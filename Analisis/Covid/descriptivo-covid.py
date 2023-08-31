#-----------------------------------------------------------
#------------- Analisis Descriptivo ------------------------
#-----        Fuente de datos Covid-19       ---------------
#-----------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#------------------------- Funciones -------------------------

def estadisticas_cantidad(data,columna):
    lista_aux = []
    # Calcular estadísticas básicas
    mean = np.mean(data[columna])          # Media
    median = np.median(data[columna])      # Mediana
    std_dev = np.std(data[columna])        # Desviación estándar
    min_value = np.min(data[columna])      # Valor mínimo
    max_value = np.max(data[columna])      # Valor máximo
    total = np.sum(data[columna])          # Total
    mode = np.argmax(np.bincount(data[columna].astype(int))) # Moda

    # Calcular los cuartiles
    q1 = np.percentile(data[columna], 25)  # Primer cuartil (25%)
    q3 = np.percentile(data[columna], 75)  # Tercer cuartil (75%)

    # Imprimir los resultados
    lista_aux.append(mean),lista_aux.append(median),lista_aux.append(std_dev),lista_aux.append(min_value),lista_aux.append(max_value),lista_aux.append(total),
    lista_aux.append(mode),lista_aux.append(q1),lista_aux.append(q3)

    lista.append(lista_aux)
    lista_aux = []

def transformacion(data):
    # Convertir la columna de fecha a formato de fecha
    data['fecha'] = pd.to_datetime(data['fecha'])

    # Agrupar los datos por día y sumar las cantidades para cada columna
    data_grouped = data.groupby('fecha').sum().reset_index()

    return data_grouped

def exportar_a_Excel():
    cabeceras = ['Estadisticas','Total de Camas','Camas ocupadas', 'Ingresos']
    lista_trans = np.transpose(lista)

    # Crear un DataFrame de pandas con los datos
    df = pd.DataFrame(lista_trans, columns=cabeceras)
    print(df)
    # Crear un archivo de Excel
    #df.to_excel('descriptiva-covid.xlsx', index=False)

    
#------------------------- Se ejecuta el programa -------------------------

lista = [['media','mediana','Desviacion Tipica', 'Valor Minimo', 'Valor Maximo', 'Total', 'Moda', 'Primer Cuartil (Q1)','Tercer Cuartil (Q3)']]

# Cargar los datos en un DataFrame
data = pd.read_excel('ETL\Data\covid.xlsx')

# Exploración inicial de los datos
#print(data.head())
#print(data.info())


data_grouped = transformacion(data)

estadisticas_cantidad(data_grouped,'Total de Camas')
estadisticas_cantidad(data_grouped,'Camas ocupadas')
estadisticas_cantidad(data_grouped,'Ingresos')
exportar_a_Excel()



