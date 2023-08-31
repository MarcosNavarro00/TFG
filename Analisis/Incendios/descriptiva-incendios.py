#-----------------------------------------------------------
#------------- Analisis Descriptivo -----------------------
#-----        Fuente de datos Incendios    ----------------
#-----------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#------------------------- Funciones -------------------------
def grafico_temporal(data):
        # Crear la gráfica temporal
    plt.figure(figsize=(10, 6))  # Tamaño de la figura
    plt.plot(data['Año'], data['Numero de Siniestros'], marker='o', color='b')

    # Etiquetas y título de la gráfica
    plt.xlabel('Año')
    plt.ylabel('Numero de Siniestros')
    plt.title('Numero de Siniestros por Año')

    # Mostrar la gráfica
    plt.grid(True)
    plt.tight_layout()
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

def exportar_a_excel():
    cabeceras = ['Estadisticas','Numero de Siniestros','Numero de siniestros > 500 ha', 'Supercie total (ha) por GIF','Superficie por % por GIF']
    # Transponer la lista
    lista_trans = np.transpose(lista)
    print(lista_trans)
    # Crear un DataFrame de pandas con los datos
    df = pd.DataFrame(lista_trans, columns=cabeceras)

    print(df)

    # Crear un archivo de Excel
    #df.to_excel('descriptiva-incendios.xlsx', index=False)


# ------------------------- Se ejecuta el programa -------------------------
lista = [['media','mediana','Desviacion Tipica', 'Valor Minimo', 'Valor Maximo', 'Total', 'Moda', 'Primer Cuartil (Q1)','Tercer Cuartil (Q3)']]
# Cargar los datos en un DataFrame
data = pd.read_excel('ETL\Data\incendios1996-2015.xlsx')

# Exploración inicial de los datos
#print(data.head())
#print(data.info())

grafico_temporal(data)
# Convertir todos los elementos de la lista 'Cantidad' de str a int

estadisticas_cantidad(data,'Numero de Siniestros' )
estadisticas_cantidad(data,'Numero de siniestros > 500 ha' )
estadisticas_cantidad(data,'Superficie por ha' )
estadisticas_cantidad(data,'Superficie por %' )
exportar_a_excel()







