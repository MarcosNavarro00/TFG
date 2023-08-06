import pandas as pd
import numpy as np
# Gráficos
# ==============================================================================
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns

# Preprocesado y modelado
# ==============================================================================
from scipy.stats import pearsonr
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
import statsmodels.formula.api as smf

#regresion lineal aplicado a metricas de la poblaicon.
tabla_total = []
provincias = []
poblacion = []

años = [2021,2020,2019,2018,2017,2016,2015,2014,2013,2012,2011,2010,2009,2008,2007,2006,2005,2004,2003,2002,2001,2000,1999,1998,1996]

#----------------------------------- Extrae la tabla de totales -------------------------------- 
def extractDta (data):
    provincia = []
    for i in range (len (data)):
        provincia = []
        if ( i >= 8): #porque los datos empiezan a partir de la fila 8
            for j in range (len (data[i])):
                    if (j <= 25):#porque los datos llegan a hasta la columna 26
                        provincia.append(data[i][j])
            tabla_total.append (provincia)
       
    return tabla_total

#----------------------------------- Coloca cada provincia con su info relacionada con los años -------------------------------- 
def cleanData(data):
    for i in range (len (data)):
        provincias.append(data[i][0]) #se crea una lista con todos los nombres de provincias 
        data[i].pop(0)
        poblacion.append(data[i])#se crea una lista con todos los datos poblacionales


   

# Open the Workbook
df = pd.read_excel(
    'Fuentes de datos\Smarcities\poblacionEspaña.xlsx',
    engine='openpyxl'
)


data = df.values

data = extractDta (data)
cleanData(data)


datos = pd.DataFrame({'años': años, 'poblacion': poblacion[0]})

print (datos)