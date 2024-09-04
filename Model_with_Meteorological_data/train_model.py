#model name : lstm_v4

import pandas as pd
import numpy as np
from keras.layers import SimpleRNN, TimeDistributed, Activation, BatchNormalization, Bidirectional, RepeatVector
# from keras.layer.normalization import LayerNormalization
from keras.models import Sequential
from tensorflow.keras.layers import Input, LSTM, Dense, Concatenate, LayerNormalization, Dropout, Reshape, Flatten, Layer, Conv1D, MaxPooling1D
from tensorflow.keras.models import Model
from keras.utils import Sequence
from keras.callbacks import EarlyStopping, ModelCheckpoint
import matplotlib.pyplot as plt
import tensorflow as tf
from pandas import read_csv
from keras.layers import LeakyReLU
from tensorflow.keras.callbacks import EarlyStopping

from config import *

# ------------------------------------------------ Data processing ------------------------------------------------
print("---------------------------------------------------------------------------")
print("mode: ", mode)
print("model_used: ", model_used)

past = 3
min = 30 # time step
step = int(1440/min) # 48
# load dataset
npz_file = np.load(f'./{min}min_dataset_past_{past}day.npz')
print(npz_file)
x_train, y_train = npz_file['x_train'], npz_file['y_train']
x_test, y_test = npz_file['x_test'], npz_file['y_test']
x_validation, y_validation = npz_file['x_validation'], npz_file['y_validation']
# print("x_validation = ", x_validation)
print(x_validation.shape)


print("\nBefore choosing the feature.")
print("\nx_train, y_train's shape : ")
print(x_train.shape)
print(y_train.shape)
print("\nx_test, y_test's shape : ")
print(x_test.shape)
print(y_test.shape)
print("\nx_validation, y_validation's shape : ")
print(x_validation.shape)
print(y_validation.shape)


features_train = tf.concat([
    x_train[:, :, [0]],  # 10th feature
    x_train[:, :, [1]], # 11th feature, ensure this exists
    x_train[:, :, [2]],  # 8th feature
    x_train[:, :, [3]],  # 9th feature
    x_train[:, :, [channel_i]]  # feature at index 'channel_i'
], axis=-1)

features_valid = tf.concat([
    x_validation[:, :, [0]],  # 10th feature
    x_validation[:, :, [1]], # 11th feature, ensure this exists
    x_validation[:, :, [2]],  # 8th feature
    x_validation[:, :, [3]],  # 9th feature
    x_validation[:, :, [channel_i]]  # feature at index 'channel_i'
], axis=-1)

features_test = tf.concat([
    x_test[:, :, [0]],  # 10th feature
    x_test[:, :, [1]], # 11th feature, ensure this exists
    x_test[:, :, [2]],  # 8th feature
    x_test[:, :, [3]],  # 9th feature
    x_test[:, :, [channel_i]]  # feature at index 'channel_i'
], axis=-1)

x_train = x_train[:, :, channel_i]
x_test = x_test[:, :, channel_i]
x_validation = x_validation[:, :, channel_i]
y_train = y_train[:, :, channel_i]
y_test = y_test[:, :, channel_i]
y_validation = y_validation[:, :, channel_i]




print("--------------------------------------------------------------------------------------")
# print shape
print("\nBefore reshape")
print("\nfeatures_train: ", features_train.shape)
print("features_test: ", features_test.shape)
print("features_valid: ", features_valid.shape)

print("\nx_train, y_train's shape : ")
print(x_train.shape)
print(y_train.shape)
print("\nx_test, y_test's shape : ")
print(x_test.shape)
print(y_test.shape)
print("\nx_validation, y_validation's shape : ")
print(x_validation.shape)
print(y_validation.shape)

# # features_train = features_train.reshape((features_train.shape[0], past, step*5))
# features_train = tf.reshape(features_train, (features_train.shape[0], past, step * 5))
# features_test = tf.reshape(features_test, (features_test.shape[0], past, step * 5))
# features_valid = tf.reshape(features_valid, (features_valid.shape[0], past, step * 5))

# # Input Shape 為 (輸入時間跨度, 每天的採樣數*7個特徵)
# x_train = x_train.reshape((x_train.shape[0], past, step))
# x_test = x_test.reshape((x_test.shape[0], past, step))
# x_validation = x_validation.reshape((x_validation.shape[0], past, step))

# # Output Shape 為 (輸入時間跨度, 每天的採樣數*1個特徵)
# y_train = y_train.reshape((y_train.shape[0], step))
# y_test = y_test.reshape((y_test.shape[0], step))
# y_validation = y_validation.reshape((y_validation.shape[0], step))

# print("--------------------------------------------------------------------------------------")
# # print shape
# print("\nAfter reshape")
# print("\nfeatures_train: ", features_train.shape)
# print("features_test: ", features_test.shape)
# print("features_valid: ", features_valid.shape)
# print("\nx_train, y_train's shape : ")
# print(x_train.shape)
# print(y_train.shape)
# print("\nx_test, y_test's shape : ")
# print(x_test.shape)
# print(y_test.shape)
# print("\nx_validation, y_validation's shape : ")
# print(x_validation.shape)
# print(y_validation.shape)

# x_train_time = x_train_time.reshape((x_train_time.shape[0], past, step*4))
# x_test_time = x_test_time.reshape((x_test_time.shape[0], past, step*4))
# x_validation_time = x_validation_time.reshape((x_validation_time.shape[0], past, step*4))

# print("\nx_train_time's shape : ")
# print(x_train_time.shape)
# print("\nx_test_time's shape : ")
# print(x_test_time.shape)
# print("\nx_validation_time's shape : ")
# print(x_validation_time.shape)
# print("--------------------------------------------------------------------------------------")

# These two array should have the same value
# print(x_train[0][1])
# print(x_train[1][0])


class DotProductAttention_one2one(Layer):
    def __init__(self, use_scale=True, **kwargs):
        super(DotProductAttention_one2one, self).__init__(**kwargs)
        self.use_scale = use_scale

    def build(self, input_shape):
        # Input shapes for query, key, and value respectively
        query_shape, key_shape, value_shape = input_shape
        self.query_dense = Dense(query_shape[-1])
        self.key_dense = Dense(key_shape[-1])
        self.value_dense = Dense(value_shape[-1])

        if self.use_scale:
            self.scale = 1 / tf.sqrt(tf.cast(key_shape[-1], tf.float32))
        else:
            self.scale = None

    def call(self, inputs):
        query_input, key_input, value_input = inputs
        query = self.query_dense(query_input)
        key = self.key_dense(key_input)
        value = self.value_dense(value_input)

        score = tf.matmul(query, key, transpose_b=True)
        if self.scale is not None:
            score *= self.scale
        
        attention_weights = tf.nn.softmax(score, axis=-1)
        return tf.matmul(attention_weights, value)
    
def buildModel(shape, output):
    global adam
    
    lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
        initial_learning_rate, # please edit in the config.py
        decay_steps=100000,
        decay_rate=0.96,
        staircase=True)

    if mode == '1i1o':
            
        if model_used == 'LSTM_attention':
            
            adam = tf.keras.optimizers.legacy.Adam(learning_rate=lr_schedule, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
            
            # Define inputs
            seq_input = Input(shape=(shape[1], shape[2]))
            additional_input = Input(shape=(shape[1], shape[2]))

            # LSTM layers
            lstm_out = LSTM(128, return_sequences=True, activation="sigmoid")(seq_input)
            lstm_out = LSTM(128, return_sequences=True, activation="sigmoid")(lstm_out)
            lstm_out = Flatten()(lstm_out)

            # Configurable use of scale
            use_scale = True  # Set this to False if you don't want to use scaling

            # DotProductAttention with separate inputs and configurable scale
            attention_out = DotProductAttention_one2one(use_scale=use_scale)([lstm_out, lstm_out, lstm_out])

            # Further processing
            layer_norm = LayerNormalization()(attention_out)
            dropout = Dropout(0.2)(layer_norm)
            output_layer = Dense(output, activation='linear')(dropout)

            # Create the model
            model = Model(inputs=[seq_input], outputs=output_layer)
            model.compile(loss="mean_squared_error", optimizer='adam', metrics=['mae'])
            model.summary()

        elif model_used == 'CNN_LSTM':
            
            adam = tf.keras.optimizers.legacy.Adam(learning_rate=lr_schedule, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
            model = Sequential()
            model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(shape[1], shape[2])))
            model.add(Conv1D(filters=64, kernel_size=3, activation='relu'))
            model.add(LSTM(128, return_sequences=True, activation="sigmoid"))
            model.add(LSTM(128, return_sequences=True, activation="sigmoid"))
            model.add(Flatten())
            model.add(LayerNormalization())
            model.add(Dropout(0.2))
            model.add(Dense(output, activation = 'linear'))
            model.compile(loss = "mean_squared_error", optimizer = adam, metrics = ['mae'])
            model.summary()


        elif model_used == 'LSTM':
            
            adam = tf.keras.optimizers.legacy.Adam(learning_rate=lr_schedule, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
            model = Sequential()
            model.add(LSTM(128, return_sequences = True, activation = "sigmoid", input_shape=(shape[1], shape[2])))
            # model.add(LSTM(128, return_sequences = True, activation = "sigmoid"))
            model.add(LSTM(128, return_sequences = False, activation = "sigmoid"))
            model.add(LayerNormalization())
            model.add(Dropout(0.2))
            model.add(Dense(output, activation = 'linear'))
            model.compile(loss = "mean_squared_error", optimizer = adam, metrics = ['mae'])
            model.summary()
        
    elif mode == '5i1o':
        if model_used == 'LSTM_attention':

            adam = tf.keras.optimizers.legacy.Adam(learning_rate=lr_schedule, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
            
            # Define inputs
            seq_input = Input(shape=(shape[1], shape[2]))
            additional_input = Input(shape=(shape[1], shape[2]))

            # LSTM layers
            lstm_out = LSTM(128, return_sequences=True, activation="sigmoid")(seq_input)
            lstm_out = LSTM(128, return_sequences=False, activation="sigmoid")(lstm_out)
            lstm_out = Flatten()(lstm_out)
            # lstm_out = Dense(512)(lstm_out)
            # Configurable use of scale
            use_scale = True  # Set this to False if you don't want to use scaling

            # DotProductAttention with separate inputs and configurable scale
            attention_out = DotProductAttention_one2one(use_scale=use_scale)([lstm_out, lstm_out, lstm_out])

            # Further processing
            layer_norm = LayerNormalization()(attention_out)
            dropout = Dropout(0.3)(layer_norm)
            output_layer = Dense(output, activation='linear')(dropout)

            # Create the model
            model = Model(inputs=[seq_input], outputs=output_layer)
            model.compile(loss="mean_squared_error", optimizer='adam', metrics=['mae'])
            model.summary()

        elif model_used == 'CNN_LSTM':

            adam = tf.keras.optimizers.legacy.Adam(learning_rate=lr_schedule, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
            model = Sequential()
            model.add(Conv1D(filters=32, kernel_size=3, activation='relu', input_shape=(shape[1], shape[2])))
            model.add(Conv1D(filters=32, kernel_size=3, activation='relu'))
            model.add(MaxPooling1D(pool_size=2))
            model.add(LSTM(128, return_sequences=True, activation="sigmoid"))
            model.add(LSTM(128, return_sequences=True, activation="sigmoid"))
            model.add(Flatten())
            model.add(Dropout(0.3))
            model.add(Dense(output, activation = 'linear'))
            model.compile(loss = "mean_squared_error", optimizer = adam, metrics = ['mae'])
            model.summary()


        elif model_used == 'LSTM':
            adam = tf.keras.optimizers.legacy.Adam(learning_rate=lr_schedule, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
            model = Sequential()
            model.add(LSTM(128, return_sequences = True, activation = "sigmoid", input_shape=(shape[1], shape[2])))
            # model.add(LSTM(128, return_sequences = True, activation = "sigmoid"))
            model.add(LSTM(128, return_sequences = False, activation = "sigmoid"))
            model.add(LayerNormalization())
            model.add(Dropout(0.2))
            model.add(Dense(output, activation = 'linear'))
            model.compile(loss = "mean_squared_error", optimizer = adam, metrics = ['mae'])
            model.summary()

    elif mode == '7i1o': # pm2.5, month_sin. month_cos, day_sin, day_cos, hour_sin, hour_cos

        if model_used == 'LSTM_attention':

            adam = tf.keras.optimizers.legacy.Adam(learning_rate=lr_schedule, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
            
            # Define inputs
            seq_input = Input(shape=(shape[1], shape[2]))
            additional_input = Input(shape=(shape[1], shape[2]))

            # LSTM layers
            lstm_out = LSTM(128, return_sequences=True, activation="sigmoid")(seq_input)
            lstm_out = LSTM(128, return_sequences=False, activation="sigmoid")(lstm_out)
            lstm_out = Flatten()(lstm_out)
            # lstm_out = Dense(512)(lstm_out)
            # Configurable use of scale
            use_scale = True  # Set this to False if you don't want to use scaling

            # DotProductAttention with separate inputs and configurable scale
            attention_out = DotProductAttention_one2one(use_scale=use_scale)([lstm_out, lstm_out, lstm_out])

            # Further processing
            layer_norm = LayerNormalization()(attention_out)
            dropout = Dropout(0.2)(layer_norm)
            output_layer = Dense(output, activation='linear')(dropout)

            # Create the model
            model = Model(inputs=[seq_input], outputs=output_layer)
            model.compile(loss="mean_squared_error", optimizer='adam', metrics=['mae'])
            model.summary()

        elif model_used == 'CNN_LSTM':
            
            adam = tf.keras.optimizers.legacy.Adam(learning_rate=lr_schedule, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
            model = Sequential()
            model.add(Conv1D(filters=64, kernel_size=5, activation='relu', input_shape=(shape[1], shape[2])))
            model.add(LSTM(256, return_sequences=True, activation="sigmoid"))
            model.add(LSTM(128, return_sequences=True, activation="sigmoid"))
            model.add(Flatten())
            model.add(LayerNormalization())
            model.add(Dropout(0.5))
            model.add(Dense(output, activation = 'linear'))
            model.compile(loss = "mean_squared_error", optimizer = adam, metrics = ['mae'])
            model.summary()

        elif model_used == 'LSTM':
            
            adam = tf.keras.optimizers.legacy.Adam(learning_rate=lr_schedule, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
            model = Sequential()
            model.add(LSTM(128, return_sequences = True, activation = "sigmoid", input_shape=(shape[1], shape[2])))
            # model.add(LSTM(128, return_sequences = True, activation = "sigmoid"))
            model.add(LSTM(128, return_sequences = False, activation = "sigmoid"))
            model.add(LayerNormalization())
            model.add(Dropout(0.2))
            model.add(Dense(output, activation = 'linear'))
            model.compile(loss = "mean_squared_error", optimizer = adam, metrics = ['mae'])
            model.summary()

    return model

print("features_train.shape", features_train.shape)
print("features_test.shape", features_test.shape)
print("features_valid.shape", features_valid.shape)
model = buildModel(features_train.shape, step)
# early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
record = model.fit(x=features_train, y=y_train, epochs=epochs, batch_size=batch_size, validation_data = (features_valid, y_validation))#/, callbacks=[early_stopping])
scores = model.evaluate(features_test, y_test)
print(f'\n{feature} loss value & MAE values : {scores}')

# plot the loss and MAE figure
epochs=range(len(record.history['mae']))
plt.figure()
plt.plot(epochs,record.history['mae'],'b',label='Training MAE')
plt.plot(epochs,record.history['val_mae'],'r',label='Validation MAE')
plt.title('Training and Validation MAE')
plt.legend()
plt.savefig(f'./result/figure/{min}min_{feature}_mae_past_{past}.jpg')

plt.figure()
plt.plot(epochs,record.history['loss'],'b',label='Training loss')
plt.plot(epochs,record.history['val_loss'],'r',label='Validation loss')
plt.title('Training and Validation loss')
plt.legend()
plt.savefig(f'./result/figure/{min}min_{feature}_loss_past_{past}.jpg')

# save model
model.save(f'./result/{min}min_{feature}_past_{past}.h5')  # Creates a HDF5 file 'mode_name.h5'
