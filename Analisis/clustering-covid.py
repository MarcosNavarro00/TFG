import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

# Cargar los datos desde el archivo xlsx
data = pd.read_excel('ETL\Data\covid.xlsx')

# Convertir la columna de fechas al tipo de dato datetime para facilitar el procesamiento
data['fecha'] = pd.to_datetime(data['fecha'])

# Agrupar los datos por intervalos de dos semanas y calcular el promedio de camas ocupadas para cada intervalo
two_weekly_data = data.resample('1D', on='fecha').mean()

# Crear el modelo de clustering (por ejemplo, usando K-Means con 3 clusters)
n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, random_state=42)

# Entrenar el modelo
kmeans.fit(two_weekly_data[['Camas ocupadas']])

# Obtener las etiquetas del cluster asignadas a cada registro original
cluster_labels = kmeans.predict(two_weekly_data[['Camas ocupadas']])

# Asignar las etiquetas al DataFrame two_weekly_data
two_weekly_data['Cluster'] = cluster_labels

# Visualizar los clusters en función de los intervalos de dos semanas
plt.figure(figsize=(10, 6))
for cluster in range(n_clusters):
    cluster_data = two_weekly_data[two_weekly_data['Cluster'] == cluster]
    plt.scatter(cluster_data.index, cluster_data['Camas ocupadas'], label=f'Cluster {cluster}')

# Ajustar el formato del eje X para mostrar intervalos de dos semanas
date_format = DateFormatter("%Y-%m-%d")
plt.gca().xaxis.set_major_formatter(date_format)

plt.xlabel('Intervalos de dos semanas')
plt.ylabel('Promedio de Camas Ocupadas')
plt.title('Clustering de Camas Ocupadas')
plt.xticks(rotation=45)
plt.legend()
plt.show()
