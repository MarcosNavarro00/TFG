import pandas as pd


# Open the Workbook
df = pd.read_excel(
    'Fuentes de datos\Eulogh\ConcesionesNacionalidadResidencia_2019.xlsx',
    sheet_name="1", #Se accede a la primera pagina
    engine='openpyxl'
)
# Extraer el rango de filas y columnas especificado
values = df.iloc[84:161, 0:11] 
data = df.values
data = values.values #se pasa a dataframe
cabecera = ['País', '2019', '2018', '2017', '2016', '2015','2014', '2013', '2012', '2011', '2010']
df = pd.DataFrame(data, columns=cabecera) #Se introduce la cabecera 
#print (df)
df.to_excel("nacionalidad-Hombres.xlsx")