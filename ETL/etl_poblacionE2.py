import pandas as pd




def clean(data):
    for fila in range(len(data)):
        provincia= data[fila][0]
        nombre = provincia[3:]
        data[fila][0] = nombre
    
    return data


# Open the Workbook
df = pd.read_excel(
    'Fuentes de datos\Smarcities\poblacionEspaña.xlsx',
    engine='openpyxl'
)
# Extraer el rango de filas y columnas especificado
values = df.iloc[8:64, 0:26] 
data = values.values #se pasa a dataframe
cabecera = ['Provincia', '2021', '2020','2019', '2018', '2017', '2016', '2015','2014', '2013', '2012', '2011', '2010','2009', '2008', '2007', '2006', 
            '2005','2004', '2003', '2002', '2001', '2000', '1999', '1998', '1996']

data2 = clean(data) #Funcion Clean, se procede a limpiar los datos
df = pd.DataFrame(data2, columns=cabecera) #Se introduce la cabecera 
#print (df)
df.to_excel("poblacion-Espana.xlsx") #Se crea y se introduce al archivo xlsx



