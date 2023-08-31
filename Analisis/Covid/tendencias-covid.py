import pandas as pd
import matplotlib.pyplot as plt

# Cargar los datos desde el archivo xlsx
data = pd.read_excel('ETL\Data\covid.xlsx')

# Convertir la columna de fechas al tipo de dato datetime
data['fecha'] = pd.to_datetime(data['fecha'])

# Agrupar los datos por fecha y calcular la suma de las camas ocupadas y los ingresos para cada fecha
time_series_data = data.groupby('fecha').sum()

# Visualizar los datos en un gráfico de líneas
plt.figure(figsize=(10, 6))
plt.plot(time_series_data.index, time_series_data['Total de Camas'], label='Camas ocupadas')

plt.xlabel('Fecha')
plt.ylabel('Cantidad')
plt.title('Análisis de Series de Tiempo - Camas Ocupadas e Ingresos COVID-19')
plt.xticks(rotation=45)
plt.legend()
plt.show()
