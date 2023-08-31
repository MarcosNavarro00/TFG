import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from pmdarima import auto_arima

# Lee los datos desde el archivo xlsx
df = pd.read_excel('ETL\Data\covid.xlsx')

# Convierte la columna 'fecha' en el índice del DataFrame y ordena los datos por fecha
df['fecha'] = pd.to_datetime(df['fecha'])
df.set_index('fecha', inplace=True)
df.sort_index(inplace=True)

#Se juntan todos los datos de un mismo dia
df_daily = df.resample('D').sum()
print(df_daily.head())


# Grafica la serie de tiempo de ingresos
plt.figure(figsize=(12, 6))
plt.plot(df['Ingresos'])
plt.title('Serie de tiempo de ingresos')
plt.xlabel('Fecha')
plt.ylabel('Ingresos')
plt.show()  

ts = df["fecha","Ingresos"]

# Utilizar auto_arima para encontrar los valores óptimos de p, d y q
model = auto_arima(ts, seasonal=False, trace=True, error_action="ignore", suppress_warnings=True)
best_p = model.order[0]
best_d = model.order[1]
best_q = model.order[2]


# Entrenar el modelo ARIMA
modelo_arima = ARIMA(df_daily['Ingresos'], order=(2, 2, 0),trend=None,enforce_stationarity =True , enforce_invertibility =True)
resultado_arima = modelo_arima.fit()

# Realizar predicciones para los próximos 7 días
predicciones = resultado_arima.predict(start='2021-03-01', end='2021-04-1', dynamic=False)

# Verificar las predicciones
print(predicciones)

# Graficar las predicciones junto con la serie de tiempo existente
plt.figure(figsize=(12, 6))
plt.plot(df_daily['Ingresos'], label='Datos existentes')
plt.plot(predicciones, label='Predicciones', color='red')
plt.title('Predicciones de ingresos usando modelo ARIMA')
plt.xlabel('Fecha')
plt.ylabel('Ingresos')
plt.legend()
plt.show()
