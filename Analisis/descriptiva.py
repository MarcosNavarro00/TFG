
import pandas as pd
from statistics import median, mode,mean, stdev
import statistics 
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

lista_final =[]
anios = [1996, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]

#------------------- Se extrae la informacion del xlsl ------------------------
def extrac():
    
    # Open the Workbook
    df = pd.read_excel(
        'ETL\Data\poblacion-Espana.xlsx',
        engine='openpyxl'
    )

    return df

#------------------- calculamos la mediana, moda y media------------------------
def estadististicos (fila):

    nueva_lista = fila[2:]
    lista_invertida = nueva_lista[::-1]
    
    
    counter = Counter(lista_invertida)
    max_count = max(counter.values())
    modes = [value for value, count in counter.items() if count == max_count]

    # Calculamos el rango
    rango = max(lista_invertida) - min(lista_invertida)
    # Calculamos el rango intercuartil
    q1 = np.percentile(lista_invertida, 25)
    q3 = np.percentile(lista_invertida, 75)

    # Calculamos el rango intercuartil (RI)
    rango_intercuartil = q3 - q1
    
    return median(lista_invertida), mean(lista_invertida), stdev(lista_invertida), rango, q1,q3,rango_intercuartil

def grafico(fila):
    provincia = fila[1]
    nueva_lista = fila[2:]
    lista_invertida = nueva_lista[::-1]
    
    
    # Crear el gráfico de líneas
    plt.figure(figsize=(10, 6))
    plt.plot(anios, lista_invertida, marker='o', linestyle='-')
    plt.xlabel('Año')
    plt.ylabel('Valor')
    plt.title(provincia)
    plt.grid(True)

    
    plt.xticks(anios)

    plt.show()

def load(lista_final):
    # Crear un DataFrame de pandas a partir de la matriz
    nombres_columnas = ['Provincia', 'Mediana', 'Media','Desviacion','Rango','Pimer Quartil (0.25%)', 'Tercer Cuartil (0.75%)', 'Rango Intercuartil']
    df = pd.DataFrame(lista_final, columns=nombres_columnas)

    # Exportar el DataFrame a Excel
    df.to_excel('descriptiva.xlsx', index=False)


def prog_principal():
    lista_aux = []
    lista_final = []
    df = extrac()
    data = df.values

    for fila in data:
        lista_aux.append(fila[1])
        mediana, media, desviacion, rango,q1,q3, rango_intercuartil =  estadististicos(fila)
        lista_aux.append(mediana),lista_aux.append(media),lista_aux.append(desviacion),lista_aux.append(rango),lista_aux.append(q1),lista_aux.append(q3),
        lista_aux.append(rango_intercuartil)
        
        lista_final.append(lista_aux)
        lista_aux = []

        #grafico(fila)

    print(lista_final)
    load(lista_final)
    
prog_principal()


