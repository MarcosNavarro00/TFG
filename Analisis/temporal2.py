import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import matplotlib.pyplot as plt

# Leer los datos del archivo XLSX
data = pd.read_excel('ETL\Data\incendios1996-2015.xlsx')

# Preparar los datos
# Utilizaremos solo la columna de "Supercie total (ha)" para la predicción
data = data[['Año', 'Superficie por %']]
data.set_index('Año', inplace=True)

# Escalar los datos para mejorar el rendimiento del modelo
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)

# Preparar las secuencias de tiempo y las etiquetas para entrenamiento
def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    return np.array(X), np.array(y)

sequence_length = 5 # Longitud de la secuencia temporal
X_train, y_train = create_sequences(data_scaled, sequence_length)

# Construir el modelo LSTM
model = Sequential()
model.add(LSTM(50, activation='relu', input_shape=(sequence_length, 1)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

# Entrenar el modelo
model.fit(X_train, y_train, epochs=110, batch_size=4)

# Preparar datos para hacer predicciones
last_sequence = data_scaled[-sequence_length:]
last_sequence = np.reshape(last_sequence, (1, sequence_length, 1))

# Realizar la predicción para los dos años siguientes
num_years_to_predict = 10
predictions = []
for _ in range(num_years_to_predict):
    prediction = model.predict(last_sequence)
    predictions.append(prediction[0, 0])
    last_sequence = np.roll(last_sequence, -1)
    last_sequence[-1] = prediction

# Escalar los valores de predicción nuevamente para obtener los valores reales
predictions = np.array(predictions)
predictions = np.reshape(predictions, (-1, 1))
predictions = scaler.inverse_transform(predictions)


# Calcular los años siguientes para las predicciones
last_year = data.index[-1]
next_years = pd.date_range(start=f"{last_year}-01-01", periods=num_years_to_predict+1, freq='Y').year[1:]

# Imprimir las predicciones para los dos años siguientes
print("Predicciones para los dos años siguientes:")
for year, prediction in zip(next_years, predictions):
    print(f"Año {year}: {int(round(prediction[0]))}")


# Graficar los datos originales y las predicciones
plt.figure(figsize=(10, 6))
plt.plot(pd.to_datetime(data.index, format='%Y'), data['Superficie por %'], label='Datos Originales', marker='o')
plt.plot(pd.to_datetime(next_years, format='%Y'), predictions, label='Predicciones', marker='o')
plt.xlabel('Año')
plt.ylabel('Supercie total (ha)')
plt.legend()
plt.title('Predicciones para los próximos 10 años')
plt.grid(True)
plt.show()
