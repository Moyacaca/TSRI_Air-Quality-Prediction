#model name : lstm_v3_test

import pandas as pd
import numpy as np
import keras
import matplotlib.pyplot as plt

def decode(data, channel, time):

    if channel == 'tmp':
        channel_i = 6
    elif channel == 'hum':
        channel_i = 5
    elif channel == 'pm25':
        channel_i = 4
    elif channel == 'pm1p0':
        channel_i = 3
    elif channel == 'pm10':
        channel_i = 2
    elif channel == 'co2':
        channel_i = 1
    elif channel == 'co':
        channel_i = 0

    # data = data.reshape((time*24, 7))
    print("data shape", data.shape)
    print("data", data)
    output = data[:,channel_i]
    return output

def model_prediction(feature):
# ------------------------------------------------ load dataset and model and inference ------------------------------------------------
    past = 3
    min = 30
    step = int(1440/min)
    # load dataset
    npz_file = np.load(f'evaluate_{past}day.npz')
    x_test = npz_file['x_test']

    # # choose one of the feature to predict
    # feature = 'tmp'

    # load model
    model = keras.models.load_model(f'../1to1_3Day_model/{min}min_{feature}_past_{past}.h5')

    if feature == 'tmp':
        channel_i = 6
    elif feature == 'hum':
        channel_i = 5
    elif feature == 'pm25':
        channel_i = 4
    elif feature == 'pm1p0':
        channel_i = 3
    elif feature == 'pm10':
        channel_i = 2
    elif feature == 'co2':
        channel_i = 1
    elif feature == 'co':
        channel_i = 0

    x_test = x_test[:, :, channel_i]
    # y_test = y_test[:, :, channel_i]

    # print shape
    print("\nx_test shape : ")
    print(x_test.shape)

    x_test = x_test.reshape((x_test.shape[0], past, step))  #(18, 336, 7)->(18, 7, 336) 
                                                            # 18 units of datasets, 336(7*48) everyday, 7 days
                                                            # 18 units of datasets, 7 days, 336(7 kinds*48) units of data everyday. 
                                                            # make sure again
                                                            # put 7 datasets at the same time, iterate 336 times, this may cause gradient decent.
                                                            # put 336 datasets at the same time, iterate 7 times, this will train faster.

    print("\nx_test shape after reshape: ")
    print(x_test.shape)
    print('\n')



    # # Calculate the average value
    # average = y_test.sum()/(y_test.shape[0]*step)

    pred = model.predict(x_test)
    print("---------------------------------------------------------------------------")
    print("predict value")
    print(pred)
    print(pred.shape)
    print("---------------------------------------------------------------------------")

    average = pred.sum()/(pred.shape[0]*step)
    # print("average = ", average)

    time = int(60/min)

    # create xticks label
    values = []
    for hour in range(24*time*1):
        if hour%2 == 0:
            values.append(f'{int(hour/2)}H')
        else:
            values.append('')

    # Plot the prediction graph
    # plt.title(f'{feature}')
    # plt.xlabel('time(hour)') # 設定x軸的標籤
    # if feature == 'tmp':
    #     plt.ylabel("˚C") # 設定y軸的標籤
    # elif feature == 'hum':
    #     plt.ylabel("RH")
    # elif feature == 'pm25':
    #     plt.ylabel("μg/m3") # 設定y軸的標籤
    # elif feature == 'pm1p0':
    #     plt.ylabel("μg/m3") # 設定y軸的標籤
    # elif feature == 'pm10':
    #     plt.ylabel("μg/m3") # 設定y軸的標籤
    # elif feature == 'co2':
    #     plt.ylabel("CO2e") # 設定y軸的標籤
    # elif feature == 'co':
    #     plt.ylabel("mg/m3") # 設定y軸的標籤

    # data_plt = 5

    # plt.plot(range(24*time*1), y_test[data_plt][:], label='Today')             # Choose one of the data to plot it out.
    # plt.plot(range(24*time*1), pred[0][:], label="Today's Prediction")
    print("x_test shape", x_test.shape)
    print("x_test", x_test)
    # Yesterday = decode(x_test[:], feature, time)
    # print("x_test[0][6][:]", x_test[0][past-1][:])
    # plt.plot(range(24*time*1), x_test[0][past-1][:], label='Yesterday')
    # plt.xticks(range(24*time*1), values)

    # Save the prediction to csv file
    csv = []
    
    arr_yesterday = np.concatenate(([x_test[0][past-2][47]], x_test[0][past-1][:])) # To fill the data with last midnight 
    arr_today = np.concatenate(([x_test[0][past-1][47]], pred[0][:]))               # which include 49 datas.
    yesterday_1440 = extend_data(arr_yesterday)
    today_1440 = extend_data(arr_today)
    csv.append(yesterday_1440)
    csv.append(today_1440)
    
    csv = np.rot90(csv, -1)
    # Today,Prediction,Yesterday
    np.savetxt(f"./figure/{feature}.csv", csv, delimiter=",")

    # 繪製網格
    # plt.grid(alpha=0.4, linestyle=':')
    # plt.legend()
    # 展示
    # plt.show()
    return average

def extend_data(original_data):
    # Number of values to be generated between each pair of original data points
    # Since the original data represents every 30 minutes, and we need to fill for every minute,
    # we need to generate 29 values between each pair of original data points.
    values_to_generate = 30  # 29 + 1 for the next original data point
    
    # Initialize the list to store the extended data
    extended_data = []
    
    # Iterate through the original data
    for i in range(len(original_data) - 1):
        # Calculate the step to increment between the current and the next data point
        step = (original_data[i+1] - original_data[i]) / values_to_generate
        
        # Fill the values between the current and the next data point
        for j in range(values_to_generate):
            extended_data.append(original_data[i] + step * j)
    
    # Add the last original data point to the extended data list
    extended_data.append(original_data[-1])
    
    extended_data.pop(0)

    return extended_data

if __name__ == '__main__':
    info = ["co2", "pm10", "pm1p0", "pm25", "hum", "tmp"]
    # for i in info:
    #     model_prediction(i)

    num_plots = len(info)
    num_cols = 2  # You can adjust the number of columns as needed
    num_rows = (num_plots + num_cols - 1) // num_cols

    # Create subplots
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 8))
    axes = axes.flatten()

    averages_dict = {}

    # Plot each data in a separate subplot
    for i, data in enumerate(info):
        print(data)
        # plt.sca(axes[i])
        average = model_prediction(data)
        averages_dict[data] = average
        # print("average =", average)

    for i, data in enumerate(info):
        print(data, "average =", averages_dict[data])

    # # Adjust layout
    # plt.tight_layout()

    # # Show the plots
    # plt.show()

    
