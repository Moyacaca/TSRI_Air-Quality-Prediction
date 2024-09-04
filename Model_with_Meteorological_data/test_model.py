#model name : lstm_v3_test

import pandas as pd
import numpy as np
import keras
import matplotlib.pyplot as plt
import tensorflow as tf

from config import *

def decode(data, channel, time):
    print("data orignal", data)
    data = data.reshape((time*24, 7))
    print("data shape", data.shape)
    print("data", data)
    output = data[:,channel_i]
    return output

# ------------------------------------------------ load dataset and model and inference ------------------------------------------------
past = 3
min = 30
step = int(1440/min)
# load dataset
npz_file = np.load(f'{min}min_dataset_past_{past}day.npz')
x_test, y_test = npz_file['x_test'], npz_file['y_test']

# load model
model = keras.models.load_model(f'./result/{min}min_{feature}_past_{past}.h5')


x_test = tf.concat([
    x_test[:, :, [0]],  # 10th feature
    x_test[:, :, [1]], # 11th feature, ensure this exists
    x_test[:, :, [2]],  # 8th feature
    x_test[:, :, [3]],  # 9th feature
    x_test[:, :, [channel_i]]  # feature at index 'channel_i'
], axis=-1)

# x_test = x_test[:, :, channel_i]
y_test = y_test[:, :, channel_i]

# print shape
print("\nx_test, y_test's shape : ")
print(x_test.shape)
print(y_test.shape)

# x_test = x_test.reshape((x_test.shape[0], past, step))  #(18, 336, 1)->(18, 7, 48)
y_test = y_test.reshape((y_test.shape[0], step))

# print("\nx_test, y_test's shape after reshape: ")
# print(x_test.shape)
# print(y_test.shape)
# print('\n')

average = y_test.sum()/(y_test.shape[0]*step)
standard_deviation = np.std(y_test)
print(f'standard_deviation = {standard_deviation}')
scores = model.evaluate(x_test, y_test)
print(scores)
print(f'average = {average}')
print(average)
print(f'\n{feature} loss value & MAE values : {scores}')

if feature == 'tmp':
    print(f'{feature} accuracy : {(average-scores[1])/average}')
elif feature == 'hum':
    print(f'{feature} accuracy : {(average-scores[1])/average}')
elif feature == 'pm25':
    print(f'{feature} accuracy : {(3*standard_deviation-scores[1])/(3*standard_deviation)}')
elif feature == 'pm1p0':
    print(f'{feature} accuracy : {(3*standard_deviation-scores[1])/(3*standard_deviation)}')
elif feature == 'pm10':
    print(f'{feature} accuracy : {(3*standard_deviation-scores[1])/(3*standard_deviation)}')
elif feature == 'co2':
    print(f'{feature} accuracy : {(average-scores[1])/average}')
elif feature == 'co':
    print(f'{feature} accuracy : {(average-scores[1])/average}')

pred = model.predict(x_test)

print("pred from model: \n")
print(pred.shape)
print(pred)
print("pred ground truth: \n")
print(y_test.shape)
print(y_test)

R_square = 1 - (((pred - y_test)**2).sum()/((average - y_test)**2).sum())
print(f"R_square = {R_square}")

time = int(60/min)

# create xticks label
values = []
for hour in range(24*time*1):
    if hour%2 == 0:
        values.append(f'{int(hour/2)}H')
    else:
        values.append('')

# Plot the prediction graph
plt.title(f'{feature}')
plt.xlabel('time(hour)') # 設定x軸的標籤
if feature == 'tmp':
    plt.ylabel("˚C") # 設定y軸的標籤
elif feature == 'hum':
    plt.ylabel("RH")
elif feature == 'pm25':
    plt.ylabel("μg/m3") # 設定y軸的標籤
elif feature == 'pm1p0':
    plt.ylabel("μg/m3") # 設定y軸的標籤
elif feature == 'pm10':
    plt.ylabel("μg/m3") # 設定y軸的標籤
elif feature == 'co2':
    plt.ylabel("μg/m3") # 設定y軸的標籤
elif feature == 'co':
    plt.ylabel("μg/m3") # 設定y軸的標籤

data_plt = 2 # choose a pair of data to plot.

plt.plot(range(24*time*1), y_test[data_plt][:], label='Today')             # Choose one of the data to plot it out.
plt.plot(range(24*time*1), pred[data_plt][:], label="Today's Prediction")
print("x_test shape", x_test.shape)
plt.plot(range(24*time*1), x_test[data_plt][-48:, 4], label='Yesterday')  # Fixed indexing
plt.xticks(range(24*time*1), values)

# Save the prediction to csv file
csv = []
csv.append(x_test[data_plt][-48:, 4])  # Last 48 time steps for 'Yesterday'
csv.append(pred[data_plt][:])          # Today's prediction
csv.append(y_test[data_plt][:]) 
csv = np.rot90(csv, -1)
# Today,Prediction,Yesterday
np.savetxt(f"./result/{feature}.csv", csv, delimiter=",")

# 繪製網格
plt.grid(alpha=0.4, linestyle=':')
plt.legend()
# 展示
plt.show()