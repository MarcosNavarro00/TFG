#-----------------------------------------------------------
#------------- Analisis Descriptivo -----------------------
#-----        Fuente de datos Bosque        ----------------
#-----------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



#------------------------- Funciones -------------------------
def histograma(data):
    #Eliminar puntos de los valores y convertirlos a números de punto flotante
    data['Cantidad'] = [float(x.replace(".", "")) for x in data['Cantidad']]

    plt.figure(figsize=(12, 6))  # Tamaño de la figura

    plt.bar(data['Especie'], data['Cantidad'], color='lightblue', edgecolor='black')

    plt.xticks(rotation=90)

    plt.xlabel('Especies')
    plt.ylabel('Cantidad')
    plt.title('Cantidad de especies')

    plt.yticks(range(0, int(max(data['Cantidad'])) + 5000, 5000))

    plt.tight_layout()  # Ajustar el diseño para evitar recorte de etiquetas
    plt.show()

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
    # Convertir todos los elementos de la lista 'Cantidad' de str a int
    data['Cantidad'] = [float(str(x).replace(".", "")) for x in data['Cantidad']]


    data['Captación Contaminación (Kg/Año)'] = [x.replace(".", "") for x in data['Captación Contaminación (Kg/Año)']]
    data['Captación Contaminación (Kg/Año)'] = [x.replace(",", ".") for x in data['Captación Contaminación (Kg/Año)']]
    data['Captación Contaminación (Kg/Año)'] = [float(x) for x in data['Captación Contaminación (Kg/Año)']]

    data['Agua Interceptada (M3/Año)'] = [x.replace(".", "") for x in data['Agua Interceptada (M3/Año)']]
    data['Agua Interceptada (M3/Año)'] = [x.replace(",", ".") for x in data['Agua Interceptada (M3/Año)']]
    data['Agua Interceptada (M3/Año)'] = [float(x) for x in data['Agua Interceptada (M3/Año)']]

    return data

def exportar_a_Excel(data):
    
    cabeceras = ['Estadisticas','Cantidad','Captación Contaminación (Kg/Año)', 'Agua Interceptada (M3/Año)']

    lista_trans = np.transpose(lista)

    # Crear un DataFrame de pandas con los datos
    df = pd.DataFrame(lista_trans, columns=cabeceras)

    print(df)

    # Crear un archivo de Excel
    #df.to_excel('descriptiva-bosque.xlsx', index=False)



# ------------------------- Se ejecuta el programa -------------------------   
lista = [['media','mediana','Desviacion Tipica', 'Valor Minimo', 'Valor Maximo', 'Total', 'Moda', 'Primer Cuartil (Q1)','Tercer Cuartil (Q3)']]
# Cargar los datos en un DataFrame
data = pd.read_excel('ETL\Data\dataBosque.xlsx')

# Exploración inicial de los datos
#print(data.head())
#print(data.info())

data = transformacion(data)

estadisticas_cantidad(data,'Cantidad' )
estadisticas_cantidad(data,'Captación Contaminación (Kg/Año)' )
estadisticas_cantidad(data,'Agua Interceptada (M3/Año)' )

exportar_a_Excel(data)






