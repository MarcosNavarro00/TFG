import pandas as pd
import numpy as np
from datetime import datetime



CCAA = []


def getByCCAAByDate(data):
    dt1 = datetime(2020, 8, 1)
    dt2 = datetime(2021, 4, 1)
    for i in range (len(data)):
        if (data[i][0] >= dt1 and data[i][0] <= dt2):
            if (data[i][1] == 13):
                CCAA.append(data[i])
    
    return CCAA

def getData(CCAA):
    fecha = []
    ocupadas_covid = []
    total_camas = []
    ingresos = []
    for i in range (len(CCAA)):
        fecha.append(CCAA[i][0])
        total_camas.append(CCAA[i][5])
        ocupadas_covid.append(CCAA[i][6])
        ingresos.append(CCAA[i][8])   
    return fecha,total_camas,ocupadas_covid, ingresos

def export_xlsx(fechas,total_camas,ocupadas_covid,ingresos ):
    fechas_formateadas = []
    cabecera = ['fecha', 'Total de Camas', 'Camas ocupadas', 'Ingresos']
    
    for fecha in fechas:
    # El objeto Timestamp
        timestamp_obj = pd.Timestamp(fecha)
        # Obtener la fecha en formato 'YYYY-MM-DD'
        fecha_formateada = timestamp_obj.strftime('%Y-%m-%d')
        fechas_formateadas.append(fecha_formateada)


    # Crear la matriz utilizando numpy
    matriz = np.column_stack((fechas_formateadas, total_camas, ocupadas_covid,ingresos ))

    # Nombre del archivo Excel
    nombre_archivo = "ETL\Data\covid.xlsx"

    # Nombre de la hoja en la que deseas insertar la lista
    nombre_hoja = "Sheet1"


    df = pd.DataFrame(matriz, columns=cabecera) #Se introduce la cabecera 
    df.to_excel(nombre_archivo)



# Open the Workbook
df = pd.read_excel(
    'Fuentes de datos\Eulogh\Datos_Capacidad_Asistencial_Historico_03012023.xlsx',
    engine='openpyxl'
)

data = df.values

#print (data)

CCAA = getByCCAAByDate(data) #se obtiene toda la informacion a partir de la ccaa y de la fecha
fechas,total_camas,ocupadas_covid,ingresos = getData(CCAA) 


export_xlsx(fechas,total_camas,ocupadas_covid,ingresos )
