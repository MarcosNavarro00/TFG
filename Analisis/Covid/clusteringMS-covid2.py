#-----------------------------------------------------------
#-----Clustering con el algoritmo Mean Shift----------------
#-----        Fuente de datos Covid-19       ---------------
#----- fecha y Camas ocupadas ------------------------------
#-----------------------------------------------------------

import pandas as pd
from sklearn.cluster import MeanShift
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

#------------------------- Funciones -------------------------
def preparacion():
   
    data = pd.read_excel('ETL\Data\covid.xlsx')

    # Se convierte la columna de fechas al tipo de dato datetime para facilitar el procesamiento
    data['fecha'] = pd.to_datetime(data['fecha'])

    # Se agrupan los datos en intervalos de un dia 
    dia_data = data.resample('1D', on='fecha').mean()

    return dia_data, data

def visualizacion():
    # Visualizar los clusters en función de los intervalos de un dia
    plt.figure(figsize=(10, 6))
    for cluster in set(cluster_labels):
        cluster_data = dia_data[dia_data['Cluster'] == cluster]
        plt.scatter(cluster_data['fecha'], cluster_data['Camas ocupadas'], label=f'Cluster {cluster}')

    # Ajustar el formato del eje X para mostrar intervalos de dos semanas
    date_format = DateFormatter("%Y-%m-%d")
    plt.gca().xaxis.set_major_formatter(date_format)

    plt.xlabel('Intervalos de dos semanas')
    plt.ylabel('Promedio de Camas Ocupadas')
    plt.title('Clustering de Camas Ocupadas (Mean Shift)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.show()

def exportar_a_Excel(dia_data):
    output_filename = 'clusteringMS1-covid.xlsx'
    #dia_data.to_excel(output_filename, index=False)


# ------------------------- Se ejecuta el programa -------------------------
dia_data, data = preparacion()

# Se crea el modelo de clustering Mean Shift
meanshift = MeanShift()

# Se entrenar el modelo
meanshift.fit(dia_data[['Camas ocupadas']])

# Se obtienen las etiquetas de cada cluster
cluster_labels = meanshift.labels_

# Se asgina las etiquetas al dataframe dia_data
dia_data['Cluster'] = cluster_labels

# Se guarda las fechas en dataframe
dia_data['fecha'] = dia_data.index

# Ordenar las columnas del DataFrame
dia_data = dia_data[['fecha', 'Camas ocupadas', 'Cluster']]

visualizacion()
exportar_a_Excel(dia_data)


