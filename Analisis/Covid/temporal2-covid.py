import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller

# Lee los datos desde el archivo xlsx
df = pd.read_excel('ETL\Data\covid.xlsx')

# Convierte la columna 'fecha' en el índice del DataFrame y ordena los datos por fecha
df['fecha'] = pd.to_datetime(df['fecha'])
df.set_index('fecha', inplace=True)

# Usar la columna 'Camas_Ocupadas' como serie temporal para el modelo ARIMA
ts = df['Camas ocupadas']

# Plot de la serie temporal
plt.figure(figsize=(12, 6))
plt.plot(ts)
plt.title('Serie Temporal - Camas Ocupadas')
plt.xlabel('Fecha')
plt.ylabel('Camas Ocupadas')
plt.show()

# Prueba de estacionariedad
def test_stationarity(timeseries):
    # Realizar la prueba de Dickey-Fuller:
    result = adfuller(timeseries, autolag='AIC')
    print('Resultados de la Prueba de Dickey-Fuller:')
    print('ADF Statistic:', result[0])
    print('p-value:', result[1])
    print('Valores Críticos:')
    for key, value in result[4].items():
        print('\t', key, ':', value)

test_stationarity(ts)

# Descomposición de la serie temporal
from statsmodels.tsa.seasonal import seasonal_decompose

decomposition = seasonal_decompose(ts, model='additive', period=7)
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

plt.figure(figsize=(12, 8))
plt.subplot(411)
plt.plot(ts, label='Original')
plt.legend(loc='best')
plt.subplot(412)
plt.plot(trend, label='Tendencia')
plt.legend(loc='best')
plt.subplot(413)
plt.plot(seasonal, label='Estacionalidad')
plt.legend(loc='best')
plt.subplot(414)
plt.plot(residual, label='Residual')
plt.legend(loc='best')
plt.tight_layout()
plt.show()

# Gráficos ACF y PACF para determinar parámetros ARIMA
plot_acf(ts)
plot_pacf(ts)
plt.show()

# Ajuste del modelo ARIMA
# (p, d, q) = (2, 1, 2) basado en los gráficos ACF y PACF
model = ARIMA(ts, order=(2, 1, 2), method='ywm')
model_fit = model.fit(disp=0)
print(model_fit.summary())

# Predicciones
forecast_steps = 30  # Cambia el número de pasos hacia adelante que deseas predecir
forecast, stderr, conf_int = model_fit.forecast(steps=forecast_steps, alpha=0.05)

# Plot de las predicciones
plt.figure(figsize=(12, 6))
plt.plot(ts, label='Observado')
plt.plot(pd.date_range(start=ts.index[-1], periods=forecast_steps, freq='D'), forecast, color='r', label='Predicción')
plt.fill_between(pd.date_range(start=ts.index[-1], periods=forecast_steps, freq='D'), conf_int[:, 0], conf_int[:, 1], color='pink')
plt.title('Predicciones ARIMA')
plt.xlabel('Fecha')
plt.ylabel('Camas Ocupadas')
plt.legend()
plt.show()
print ("HOLA")