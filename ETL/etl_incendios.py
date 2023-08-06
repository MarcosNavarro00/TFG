
#Aplicar regresion logistica si la superficie supera el 60% 1 sino 0. 

import camelot
import pandas as pd


tables = camelot.read_pdf("Fuentes de datos\Eulogh\incendios-decenio-2006-2015_tcm30-521617.pdf",flavor='stream', pages='32',  strip_text='.')
tabla = tables[0].df
#print(tabla.iloc[0].tolist()) #columnas

tabla= tables[0].df.replace(',','.', regex=True) #cambiar los puntos por comas

tabla = tabla[5:] #elimina el numero de headers de la tabla 

data = tabla.values #se pasa a dataframe

for fila in data:
    fila[-1] = fila[-1].rstrip('%')

#print (data)
cabecera = ['Año', 'Numero de Siniestros', 'Numero de siniestros > 500 ha', 'Supercie total (ha)', 'Superficie por ha', 'Superficie por %']
df = pd.DataFrame(data, columns=cabecera)
#print (df)
df.to_excel("incendios1996-2015.xlsx")