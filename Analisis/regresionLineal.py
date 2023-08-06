
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

def analisisRegresion():



    # Gráfico
    # ==============================================================================
    plt.plot(años,poblacion[0], ":",color="y")
    plt.show()


    corr_test = pearsonr(x = datos['años'], y =  datos['poblacion'])
    print("Coeficiente de correlación de Pearson: ", corr_test[0])
    print("P-value: ", corr_test[1])

    X = datos['años']
    y = datos['poblacion']

    X_train, X_test, y_train, y_test = train_test_split(
                                            X.values.reshape(-1,1),
                                            y.values.reshape(-1,1),
                                            train_size   = 0.8,
                                            random_state = 1234,
                                            shuffle      = True
                                        )

    # Creación del modelo utilizando matrices como en scikitlearn
    # ==============================================================================
    # A la matriz de predictores se le tiene que añadir una columna de 1s para el intercept del modelo
    X_train = sm.add_constant(X_train, prepend=True)
    modelo = sm.OLS(endog=y_train, exog=X_train,)
    modelo = modelo.fit()
    print(modelo.summary())

    # Intervalos de confianza para los coeficientes del modelo
    # ==============================================================================
    modelo.conf_int(alpha=0.05)

    # Predicciones con intervalo de confianza del 95%
    # ==============================================================================
    predicciones = modelo.get_prediction(exog = X_train).summary_frame(alpha=0.05)
    predicciones['x'] = X_train[:, 1]
    predicciones['y'] = y_train
    predicciones = predicciones.sort_values('x')

    fig, ax = plt.subplots(figsize=(6, 3.84))

    ax.scatter(predicciones['x'], predicciones['y'], marker='o', color = "gray")
    ax.plot(predicciones['x'], predicciones["mean"], linestyle='-', label="OLS")
    ax.plot(predicciones['x'], predicciones["mean_ci_lower"], linestyle='--', color='red', label="95% CI")
    ax.plot(predicciones['x'], predicciones["mean_ci_upper"], linestyle='--', color='red')
    ax.fill_between(predicciones['x'], predicciones["mean_ci_lower"], predicciones["mean_ci_upper"], alpha=0.05)
    ax.legend()
    plt.show()

