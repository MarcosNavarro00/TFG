#-----------------------------------------------------------
#--------------- Red Neuronal LSTM -------------------------
#-----        Fuente de datos Incendios     ----------------
#------------ 'Año', 'Superficie por %' -------------------- 
#-----------------------------------------------------------

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import matplotlib.pyplot as plt


#------------------------- Funciones -------------------------
# Cargar datos
def preparacion():
    data = pd.read_excel('ETL\Data\incendios1996-2015.xlsx')
    data2 = data[['Año', 'Superficie por %']]
    data2.set_index('Año', inplace=True)
    return data2,data

# Escalar datos
def escalar_data(data):
    escalar = MinMaxScaler()
    data_scaled = escalar.fit_transform(data)
    return data_scaled, escalar

# Crear secuencias
def sencuecnia(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    return np.array(X), np.array(y)

# Construir modelo
def modelo(forma_de_entrada):
    model = Sequential()
    model.add(LSTM(200, activation='relu', input_shape=forma_de_entrada))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def predicciones(data_scaled,model,data):
    # Hacer predicciones
    ultima_secuencia = data_scaled[-tam_secuencia:]
    ultima_secuencia = np.reshape(ultima_secuencia, (1, tam_secuencia, 1))
    años_predecir = 10
    predictions = model.predict(ultima_secuencia)
    predictions = np.repeat(predictions, años_predecir, axis=0)
    for i in range(1, años_predecir):
        ultima_secuencia = np.roll(ultima_secuencia, -1)
        ultima_secuencia[-1] = predictions[i-1]
        prediction = model.predict(ultima_secuencia)
        predictions[i] = prediction

    # Desescalar predicciones
    predictions = np.reshape(predictions, (-1, 1))
    predictions = scaler.inverse_transform(predictions)

    # Calcular años siguientes
    ultimo_año = 2015
    proximos_años = pd.date_range(start=f"{ultimo_año}-01-01", periods=años_predecir+1, freq='Y').year[1:]
    print(ultimo_año,proximos_años)
    data_aux = data[['Año', 'Superficie por %']]

    return proximos_años,predictions,data_aux

def exportar_a_excel(proximos_años,predictions,data_aux):
    # Imprimir predicciones
    print("Predicciones para los dos años siguientes:")
    for año, prediction in zip(proximos_años, predictions):
        print(f"Año {año}: {int(round(prediction[0]))}")
        new_row = {'Año': año, 'Prediccion': float(prediction)}
        data_aux = data_aux.append(new_row, ignore_index=True)

    # Extraer a un archivo Excel
    #data_aux.to_excel('predicciones_Superficie%.xlsx')   

# ------------------------- Programa Principal -------------------------
data2, data = preparacion()
data_scaled, scaler = escalar_data(data2)

# Crear secuencias
tam_secuencia = 5
X_train, y_train = sencuecnia(data_scaled, tam_secuencia)

# Construir modelo
forma_de_entrada = (tam_secuencia, 1)
model = modelo(forma_de_entrada)

# Entrenar modelo
model.fit(X_train, y_train, epochs=120, batch_size=8)

proximos_años,predictions,data_aux = predicciones(data_scaled,model,data)
exportar_a_excel(proximos_años,predictions,data_aux)





