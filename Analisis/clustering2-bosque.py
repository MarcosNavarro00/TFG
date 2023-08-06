
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Cargar los datos desde el archivo xlsx
data = pd.read_excel('ETL\Data\dataBosque.xlsx')

# Seleccionar las columnas "Especie", "Agua Interceptada (M3/Año)" y "Captación Contaminación (Kg/Año)"
selected_data = data[['Especie', 'Agua Interceptada (M3/Año)', 'Captación Contaminación (Kg/Año)']]

# Eliminar filas con valores faltantes
selected_data.dropna(inplace=True)

# Convertir el valor en la columna "Agua Interceptada (M3/Año)" de texto a número decimal
selected_data['Agua Interceptada (M3/Año)'] = selected_data['Agua Interceptada (M3/Año)'].apply(lambda x: float(x.replace(',', '')))

# Convertir el valor en la columna "Captación Contaminación (Kg/Año)" de texto a número decimal
selected_data['Captación Contaminación (Kg/Año)'] = selected_data['Captación Contaminación (Kg/Año)'].apply(lambda x: float(x.replace(',', '')))

# Asignar un número único a cada especie
selected_data['Especie ID'] = pd.factorize(selected_data['Especie'])[0]

# Crear un DataFrame con las variables de interés
X = selected_data[['Agua Interceptada (M3/Año)', 'Captación Contaminación (Kg/Año)', 'Especie ID']]

# Crear el modelo de clustering (por ejemplo, usando K-Means con 3 clusters)
n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, random_state=42)

# Entrenar el modelo
kmeans.fit(X)

# Obtener las etiquetas del cluster asignadas a cada registro
selected_data['Cluster'] = kmeans.labels_

# Visualizar los clusters en función de las tres variables
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

for cluster in range(n_clusters):
    cluster_data = selected_data[selected_data['Cluster'] == cluster]
    ax.scatter(cluster_data['Agua Interceptada (M3/Año)'], cluster_data['Captación Contaminación (Kg/Año)'], cluster_data['Especie ID'], label=f'Cluster {cluster}')

ax.set_xlabel('Agua Interceptada (M3/Año)')
ax.set_ylabel('Captación Contaminación (Kg/Año)')
ax.set_zlabel('Especie')
ax.set_title('Clustering de Especies por Agua Interceptada y Captación de Contaminación')
plt.legend()
plt.show()

data['Cluster'] = kmeans.labels_
data.to_excel('resultados_clustering.xlsx', index=False)  # Para guardar en Excel