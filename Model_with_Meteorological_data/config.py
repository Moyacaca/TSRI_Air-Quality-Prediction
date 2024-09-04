

mode_option = ['1i1o', '5i1o', '7i1o']
mode = mode_option[1] 

model_option = ['LSTM_attention', 'CNN_LSTM', 'LSTM', 'LSTM_autoencoder']
model_used = model_option[2] 

# choose one of the feature to training
feature = 'tmp'

if feature == 'tmp':
    channel_i = 10
elif feature == 'hum':
    channel_i = 9
elif feature == 'pm25':
    channel_i = 8
elif feature == 'pm1p0':
    channel_i = 7
elif feature == 'pm10':
    channel_i = 6
elif feature == 'co2':
    channel_i = 5
elif feature == 'co':
    channel_i = 4

# if feature == 'tmp':
#     channel_i = 6
# elif feature == 'hum':
#     channel_i = 5
# elif feature == 'pm25':
#     channel_i = 4
# elif feature == 'pm1p0':
#     channel_i = 3
# elif feature == 'pm10':
#     channel_i = 2
# elif feature == 'co2':
#     channel_i = 1
# elif feature == 'co':
#     channel_i = 0


if mode == '1i1o':
    if model_used == 'LSTM_attention':
        if feature == 'tmp':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0005
        elif feature == 'hum':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0005
        elif feature == 'pm25':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0005
        elif feature == 'pm1p0':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0005
        elif feature == 'pm10':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0005
        elif feature == 'co2':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0005
        elif feature == 'co':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.001
        
    elif model_used == 'CNN_LSTM':
        if feature == 'tmp':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'hum':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'pm25':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'pm1p0':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'pm10':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'co2':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'co':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
    elif model_used == 'LSTM':
        if feature == 'tmp':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'hum':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'pm25':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'pm1p0':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'pm10':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'co2':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'co':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002

elif mode == '5i1o':
    if model_used == 'LSTM_attention':
        if feature == 'tmp':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'hum':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'pm25':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'pm1p0':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'pm10':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'co2':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'co':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
    elif model_used == 'CNN_LSTM':
        if feature == 'tmp':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'hum':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'pm25':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'pm1p0':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'pm10':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'co2':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'co':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002

    elif model_used == 'LSTM':
        if feature == 'tmp':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'hum':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0005
        elif feature == 'pm25':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'pm1p0':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'pm10':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'co2':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'co':
            epochs = 50
            batch_size = 8
            initial_learning_rate = 0.0002



elif mode == '7i1o':
    if model_used == 'LSTM_attention':
        if feature == 'tmp':
            epochs = 150
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'hum':
            epochs = 150
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'pm25':
            epochs = 150
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'pm1p0':
            epochs = 150
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'pm10':
            epochs = 150
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'co2':
            epochs = 150
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'co':
            epochs = 150
            batch_size = 8
            initial_learning_rate = 0.0002
    elif model_used == 'CNN_LSTM':
        if feature == 'tmp':
            epochs = 150
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'hum':
            epochs = 150
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'pm25':
            epochs = 150
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'pm1p0':
            epochs = 150
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'pm10':
            epochs = 150
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'co2':
            epochs = 150
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'co':
            epochs = 150
            batch_size = 8
            initial_learning_rate = 0.0002
    elif model_used == 'LSTM':
        if feature == 'tmp':
            epochs = 150
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'hum':
            epochs = 150
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'pm25':
            epochs = 150
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'pm1p0':
            epochs = 150
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'pm10':
            epochs = 150
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'co2':
            epochs = 150
            batch_size = 8
            initial_learning_rate = 0.0002
        elif feature == 'co':
            epochs = 150
            batch_size = 8
            initial_learning_rate = 0.0002