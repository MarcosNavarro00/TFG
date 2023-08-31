#-----------------------------------------------------------
#----- Series Temporales con el algoritmo ARIMA ------------
#-----        Fuente de datos Covid-19        --------------
#------------ fecha y camas ocupadas -----------------------
#-----------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from pmdarima import auto_arima
import pmdarima as pm
from statsmodels.tsa.stattools import adfuller

#------------------------- Funciones -------------------------

def prepararar_datos():
    # Lee los datos desde el archivo xlsx
    df = pd.read_excel('ETL\Data\covid.xlsx')
    # Convierte la columna 'fecha' en el índice del DataFrame y ordena los datos por fecha
    df['fecha'] = pd.to_datetime(df['fecha'])
    df.set_index('fecha', inplace=True)
    df_daily = df.resample('D').sum()
    return df_daily

def prueba_estacionaria(ts):
    # Prueba de estacionariedad
    # Realizar la prueba de Dickey-Fuller:
    result = adfuller(ts, autolag='AIC')
    print('Resultados de la Prueba de Dickey-Fuller:')
    print('ADF Statistic:', result[0])
    print('p-value:', result[1])
    print('Valores Críticos:')
    for key, value in result[4].items():
        print('\t', key, ':', value)
        if result[1] <= 0.05:
            print("Se rechaza la hipótesis nula, los datos son estacionarios")
        else:
            print("Se acepta la hipótesis nula, los datos no son estacionarios")

def crear_entrenar(ts):
    # Utilizar auto_arima para encontrar los valores óptimos de p, d y q
    model = auto_arima(ts, seasonal=False, trace=True, error_action="ignore", suppress_warnings=True)
    best_p = model.order[0]
    best_d = model.order[1]
    best_q = model.order[2]

    print('Best p,d,q values are: ', best_p, best_d, best_q)

    mod = sm.tsa.ARIMA(ts,
                    order=(best_p, best_d, best_q), #1,1,1
                    enforce_stationarity=False)

    results = mod.fit()

    print(results.summary().tables[1])

    results.plot_diagnostics(figsize=(15, 12))
    plt.show()

    return results

def predicciones(ts, result):
    start_date = pd.to_datetime('2021-02-01')

    pred = results.get_prediction(start=start_date, dynamic=False)
    pred_ci = pred.conf_int()

    ax = ts['2020-08-01':].plot(label='observed')
    pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7)

    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.2)

    ax.set_xlabel('Date')
    ax.set_ylabel('Camas ocupadas')
    plt.legend()

    plt.show()

    # Crear un DataFrame con las predicciones y las fechas
    predictions_df = pd.DataFrame({
        'Fecha': pred.predicted_mean.index,
        'Prediccion': pred.predicted_mean.values,
        'Intervalo Inferior': pred_ci.iloc[:, 0].values,
        'Intervalo Superior': pred_ci.iloc[:, 1].values
    })
    # Unificar los DataFrames por la columna 'Fecha'
    DFunificados = pd.merge(ts, predictions_df, left_index=True, right_on='Fecha', how='outer')
    #Se envia a un archivo excel
    #DFunificados.to_excel('ARIMA.xlsx')   

    return pred, pred_ci, start_date

#------------------------- Se ejecuta el programa -------------------------
df = prepararar_datos()
# Usar la columna 'Camas_Ocupadas' como serie temporal para el modelo ARIMA
ts = df['Camas ocupadas']
prueba_estacionaria(ts)
results = crear_entrenar(ts)
pred, pred_ci,start_date = predicciones(ts, results)

# Plot de la serie temporal
plt.figure(figsize=(12, 6))
plt.plot(ts)
plt.title('Serie Temporal - Camas ocupadas')
plt.xlabel('Fecha')
plt.ylabel('Camas ocupadas')
plt.show()


           




y_forecasted = pred.predicted_mean
y_truth = ts['2021-02-01':]

# Compute the mean square error
mse = ((y_forecasted - y_truth) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))

pred_dynamic = results.get_prediction(start=start_date, dynamic=True,full_results=True)
pred_dynamic_ci = pred_dynamic.conf_int()

ax = ts['2020-08-01':].plot(label='observed', figsize=(20, 15))
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7)

ax.fill_between(pred_dynamic_ci.index,
                pred_dynamic_ci.iloc[:, 0],
                pred_dynamic_ci.iloc[:, 1], color='k', alpha=.25)

ax.set_xlabel('Date')
ax.set_ylabel('Camas ocupadas')

plt.legend()
plt.show()

# Extract the predicted and true values of our time series
y_forecasted = pred_dynamic.predicted_mean
y_truth = ts[start_date:]

# Compute the mean square error
mse = ((y_forecasted - y_truth) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))
# Generar un rango de fechas para el próximo mes
next_month = pd.date_range(start=ts.index[-1], periods=30, freq='D')

# Realizar las predicciones para el próximo mes
forecast = results.get_forecast(steps=30)

# Obtener los valores predichos y el intervalo de confianza
forecasted_values = forecast.predicted_mean
forecasted_ci = forecast.conf_int()

# Crear un DataFrame para las predicciones
forecast_df = pd.DataFrame({
    'Fecha': next_month,
    'Predicción': forecasted_values,
    'Intervalo Inferior': forecasted_ci.iloc[:, 0],
    'Intervalo Superior': forecasted_ci.iloc[:, 1]
})

# Plot de las predicciones para el próximo mes
plt.figure(figsize=(12, 6))
plt.plot(ts, label='Observado')
plt.plot(forecast_df['Fecha'], forecast_df['Predicción'], label='Predicción', color='red')
plt.fill_between(forecast_df['Fecha'], forecast_df['Intervalo Inferior'], forecast_df['Intervalo Superior'], color='gray', alpha=0.2)
plt.title('Predicción para el próximo mes')
plt.xlabel('Fecha')
plt.ylabel('Camas ocupadas')
plt.legend()
plt.show()









