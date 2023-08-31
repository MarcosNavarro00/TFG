#-----------------------------------------------------------
#-----Clustering con el algoritmo Mean Shift----------------
#-----        Fuente de datos Bosque        ----------------
#-----Columnas Agua Interceptada (M3/Año) y Captación Contaminación (Kg/Año)
#-----------------------------------------------------------


import pandas as pd
from sklearn.cluster import MeanShift
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


#------------------------- Funciones -------------------------
def preparacion():
    data = pd.read_excel('ETL\Data\dataBosque.xlsx')

    # Seleccionar las columnas "Especie", "Agua Interceptada (M3/Año)" y "Captación Contaminación (Kg/Año)"
    selected_data = data[['Especie', 'Agua Interceptada (M3/Año)', 'Captación Contaminación (Kg/Año)']]

    selected_data.dropna(inplace=True)

    # Convierte las columnas "Agua Interceptada (M3/Año)" y "Captación Contaminación (Kg/Año)"  de texto a float
    selected_data['Agua Interceptada (M3/Año)'] = selected_data['Agua Interceptada (M3/Año)'].apply(lambda x: float(x.replace(',', '')))
    selected_data['Captación Contaminación (Kg/Año)'] = selected_data['Captación Contaminación (Kg/Año)'].apply(lambda x: float(x.replace(',', '')))

    # Asignar un número único a cada especie
    selected_data['Especie ID'] = pd.factorize(selected_data['Especie'])[0]

    # Se crea el DataFrame 
    x = selected_data[['Agua Interceptada (M3/Año)', 'Captación Contaminación (Kg/Año)', 'Especie ID']]

    return x,selected_data,data

def visualizacion(selected_data,meanshift):
    # Obtener las etiquetas del cluster asignadas a cada registro
    selected_data['Cluster'] = meanshift.labels_

    # Visualizar los clusters en función de las tres variables
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    for cluster in set(meanshift.labels_):
        cluster_data = selected_data[selected_data['Cluster'] == cluster]
        ax.scatter( cluster_data['Especie ID'],cluster_data['Agua Interceptada (M3/Año)'], cluster_data['Captación Contaminación (Kg/Año)'], label=f'Cluster {cluster}')

    ax.set_xlabel('Especie')
    ax.set_ylabel('Captación Contaminación (Kg/Año)')
    ax.set_zlabel('Agua Interceptada (M3/Año)')
    ax.set_title('Clustering de Especies por Agua Interceptada y Captación de Contaminación')
    plt.legend()
    plt.show()

def exportar_a_Excel(data):
    data['Cluster'] = meanshift.labels_
    #data.to_excel('resultados_clustering_mean_shift.xlsx', index=False)  # Para guardar en Excel


# ------------------------- Programa Principal -------------------------
x,selected_data,data = preparacion()

#Se crea el modelo  Mean Shift
meanshift = MeanShift()
#Se entrena
meanshift.fit(x)

#Se visualiza el resultado
visualizacion(selected_data,meanshift)
exportar_a_Excel(data)


