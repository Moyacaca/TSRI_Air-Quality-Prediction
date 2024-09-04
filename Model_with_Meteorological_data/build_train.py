#program name : build_train.py
#porpose : Build training data from http://125.227.15.167/download

import pandas as pd
import numpy as np
import csv
import threading
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split

import calendar


pm25, pm1p0, pm10, co2, co, o3, so2, no2, tmp, hum,  = [], [], [], [], [], [], [], [], [], []
# ------------------------------------------------- Next day function -------------------------------------------------
def next_day(year, month, day):
    if month == 2 and day == 28:
        if(leap(year)):
            day = 29
            month = 2
        else:
            day = 1
            month = 3
    elif month == 2 and day == 29:
        day = 1
        month = 3
    elif (month == 4 or month == 6 or month == 9 or month == 11) and day == 30:
        day = 1
        month += 1
    elif day == 31 :
        if month == 12:
            year += 1
            month = 1
            day = 1
        else:
            day = 1
            month += 1
    else:
        day += 1
        month = month
    
    return year, month, day
    
# ------------------------------------------------- Leap or not function -------------------------------------------------
def leap(year):
    leap = 0
    if year%4 == 0:
        leap = 1            
    if year%100 == 0:
        leap = 0            
    if year%400 == 0:
        leap = 1           
    return leap

def Encode_Cyclical_Features(data, max_val):
    data_sin = np.sin(2 * np.pi * data/max_val)
    data_cos = np.cos(2 * np.pi * data/max_val)
    return data_sin, data_cos

def get_days_in_month(year, month):
    return calendar.monthrange(year, month)[1]


# ------------------------------------------------- Read pm25 or tmp or hum or else data function -------------------------------------------------
def read_data(year, month, day, type):

    global pm25
    global tmp
    global hum
    global pm1p0
    global pm10
    global co2
    global co
    global o3
    global so2
    global no2
    global time_m_sin
    global time_m_cos
    global time_d_sin
    global time_d_cos

    days_in_month = get_days_in_month(year, month)

    file_name = f'./2022-10-6_2023-10-6/2022-10-6_2023-10-6.csv'
    with open(file_name, newline='') as csvfile:
    
        rows = csv.reader(csvfile)
        state = 0
        hour = 0
        for row in rows:  # search the csv file from top to end

            # Find the first data of each half hour and add to the array
            # ex: time = "2023-02-12_13:"
            time = f'{str(year).zfill(2)}-{str(month).zfill(2)}-{str(day).zfill(2)}_{str(hour).zfill(2)}:'
            if state == 0 and (time+'00' in row[0] or time+'01' in row[0] or time+'02' in row[0] or time+'03' in row[0] or time+'04' in row[0] or time+'05' in row[0] or time+'06' in row[0] or time+'07' in row[0]  or time+'08' in row[0] or time+'09' in row[0]
                               or time+'10' in row[0] or time+'11' in row[0] or time+'12' in row[0] or time+'13' in row[0] or time+'14' in row[0] or time+'15' in row[0] or time+'16' in row[0] or time+'17' in row[0]  or time+'18' in row[0] or time+'19' in row[0]
                               or time+'20' in row[0] or time+'21' in row[0] or time+'22' in row[0] or time+'23' in row[0] or time+'24' in row[0] or time+'25' in row[0] or time+'26' in row[0] or time+'27' in row[0]  or time+'28' in row[0] or time+'29' in row[0]):  #整點01分、02分、03分、04分、05分
                state = 1
                if type == 'temperature':
                    tmp.append(float(row[1]))
                elif type == 'humidity':
                    hum.append(float(row[2]))
                elif type == 'pm1.0':
                    pm1p0.append(float(row[3]))
                elif type == 'pm25':
                    pm25.append(float(row[4]))
                elif type == 'pm10':
                    pm10.append(float(row[5]))
                elif type == 'co2':
                    co2.append(float(row[6]))
                elif type == 'co':
                    co.append(float(row[7]))
                # elif type == 'o3':
                #     o3.append(float(row[8]))
                # elif type == 'so2':
                #     so2.append(float(row[9]))
                # elif type == 'no2':
                #     no2.append(float(row[10]))
                elif type == 'time':
                    m_sin, m_cos = Encode_Cyclical_Features(month, 12)
                    d_sin, d_cos = Encode_Cyclical_Features(day, days_in_month)
                    time_m_sin.append(float(m_sin))
                    time_m_cos.append(float(m_cos))
                    time_d_sin.append(float(d_sin))
                    time_d_cos.append(float(d_cos))
                
            elif state == 1 and (time+'30' in row[0] or time+'31' in row[0] or time+'32' in row[0] or time+'33' in row[0] or time+'34' in row[0] or time+'35' in row[0] or time+'36' in row[0] or time+'37' in row[0]  or time+'38' in row[0] or time+'39' in row[0]
                               or time+'40' in row[0] or time+'41' in row[0] or time+'42' in row[0] or time+'43' in row[0] or time+'44' in row[0] or time+'45' in row[0] or time+'46' in row[0] or time+'47' in row[0]  or time+'48' in row[0] or time+'49' in row[0]
                               or time+'50' in row[0] or time+'51' in row[0] or time+'52' in row[0] or time+'53' in row[0] or time+'54' in row[0] or time+'55' in row[0] or time+'56' in row[0] or time+'57' in row[0]  or time+'58' in row[0] or time+'59' in row[0]):
                state = 0
                if type == 'temperature':
                    tmp.append(float(row[1]))
                elif type == 'humidity':
                    hum.append(float(row[2]))
                elif type == 'pm1.0':
                    pm1p0.append(float(row[3]))
                elif type == 'pm25':
                    pm25.append(float(row[4]))
                elif type == 'pm10':
                    pm10.append(float(row[5]))
                elif type == 'co2':
                    co2.append(float(row[6]))
                elif type == 'co':
                    co.append(float(row[7]))
                # elif type == 'o3':
                #     o3.append(float(row[8]))
                # elif type == 'so2':
                #     so2.append(float(row[9]))
                # elif type == 'no2':
                #     no2.append(float(row[10]))
                elif type == 'time':
                    m_sin, m_cos = Encode_Cyclical_Features(month, 12)
                    d_sin, d_cos = Encode_Cyclical_Features(day, days_in_month)
                    time_m_sin.append(float(m_sin))
                    time_m_cos.append(float(m_cos))
                    time_d_sin.append(float(d_sin))
                    time_d_cos.append(float(d_cos))
                hour += 1

                if hour == 24:  # there will be no hour larger than 23 
                    break
            # else :
            #     print(f"There are some data missed on {year}, {month}, {day}.")

# ------------------------------------------------- Read one day data function -------------------------------------------------
def read_day_data(year, month, day):

    global pm25
    global tmp
    global hum
    global pm1p0
    global pm10
    global co2
    global co
    global o3
    global so2
    global no2
    global time_m_sin
    global time_m_cos
    global time_d_sin
    global time_d_cos

    pm25, pm1p0, pm10, co2, co, o3, so2, no2, tmp, hum = [], [], [], [], [], [], [], [], [], []
    time_m_sin, time_m_cos, time_d_sin, time_d_cos = [], [], [], [] 

    # search for data using multithreading
    t_hum = threading.Thread(target = read_data, args = (year, month, day, 'humidity'))
    t_tmp = threading.Thread(target = read_data, args = (year, month, day, 'temperature'))
    t_pm25 = threading.Thread(target = read_data, args = (year, month, day, 'pm25'))
    t_pm1p0 = threading.Thread(target = read_data, args = (year, month, day, 'pm1.0'))
    t_pm10 = threading.Thread(target = read_data, args = (year, month, day, 'pm10'))
    t_co2 = threading.Thread(target = read_data, args = (year, month, day, 'co2'))
    t_co = threading.Thread(target = read_data, args = (year, month, day, 'co'))
    # t_o3 = threading.Thread(target = read_data, args = (year, month, day, 'o3'))
    # t_so2 = threading.Thread(target = read_data, args = (year, month, day, 'so2'))
    # t_no2 = threading.Thread(target = read_data, args = (year, month, day, 'no2'))
    t_time = threading.Thread(target = read_data, args = (year, month, day, 'time'))

    # 執行該子執行緒
    t_hum.start()
    t_tmp.start()
    t_pm25.start()
    t_pm1p0.start()
    t_pm10.start()
    t_co2.start()
    t_co.start()
    # t_o3.start()
    # t_so2.start()
    # t_no2.start()
    t_time.start()


    # wait for all thread are finish
    t_hum.join()
    t_tmp.join()
    t_pm25.join()
    t_pm1p0.join()
    t_pm10.join()
    t_co2.join()
    t_co.join()
    # t_o3.join()
    # t_so2.join()
    # t_no2.join()
    t_time.join()

    return tmp, hum, pm25, pm10, pm1p0, co2, co, time_m_sin, time_m_cos, time_d_sin, time_d_cos

# ------------------------------------------------ build IoT data ------------------------------------------------
sum_pm1p0 = 0
sum_pm25 = 0
sum_pm10 = 0
total_amount = 0

pm1p0_data = [] 
pm25_data = []
pm10_data = []
count = 0

def build_year_data(end_y, end_m, end_d):
    
    global sum_pm1p0
    global sum_pm25
    global sum_pm10
    global total_amount

    global pm1p0_data
    global pm25_data
    global pm10_data

    global count
    unavaliabe_data = 0

    

    year_data = []  # define an empty array (use for store year data)

    year, month, day = 2022, 10, 6 # Start date

    while True:
        # Read only a day's data and return it's feature
        tmp, hum, pm25, pm10, pm1p0, co2, co, time_m_sin, time_m_cos, time_d_sin, time_d_cos = read_day_data(year, month, day) 
        # Combine all the feature to become a single matrix
        day_data = np.concatenate([tmp, hum, pm25, pm1p0, pm10, co2, co, time_m_sin, time_m_cos, time_d_sin, time_d_cos])
        #print(day_data)
        day_data = np.reshape(day_data,(11, -1))
        np.set_printoptions(suppress=True, precision=2)
        print("day_data = ", day_data)
        #print(day_data)
        day_data = np.rot90(day_data, -1)
        x, y = day_data.shape
        print('x = ', x)

        for i in range(x):
            
            if day_data[i][8] >= 120:  # Define the threshold of pm2.5
                #print(day_data)
                unavaliabe_data = 1
                print("unavaliabe_data = 1")
                break
            else:
                unavaliabe_data = 0
        # Append to year's data
        if unavaliabe_data == 1:
            print(day_data)
            if year == end_y and month == end_m and day == end_d: # End date
                break
            else:
                year, month, day = next_day(year, month, day)
            continue
        else:
            print('------------------------------------')
            year_data.append(day_data)
            print(day_data.shape)

        #----------------count the next day-------------------
        print(f'\rprocessing {month}/{day}...', end = '')
        #print("\n")

        if year == end_y and month == end_m and day == end_d: # End date
            break
        else:
            year, month, day = next_day(year, month, day)

    # print(year_data)
    # year_data = np.array(year_data)
    
    return year_data

# ------------------------------------------------- check shape function -------------------------------------------------
def check_shape(array):
    if array.shape == (48, 11):
        return 1
    else:
        return 0

# ------------------------------------------------- build train function -------------------------------------------------
def buildTrain(data, past):

    x_train, y_train = [], []
    serial_number = 0

    for i in range(past, len(data), 1): # from 7th data to the last data.
        
        break_flag = 0
        # check data's shape is right or not
        for check_i in range(i-past, i+1):

            # if the data's shape or value isn't right
            if check_shape(data[check_i]) == 0:
                break_flag = 1
                print(data[check_i].shape)
                print(f"Wrong Shape with {check_i}th day")
                break

        if break_flag:
            continue
        
        # if all data's shape is correct, append x_train
        x_temp = []
        for x_i in range(i-past, i):
            x_temp.extend(data[x_i])

        x_train.append(x_temp)
        y_train.append(data[i])
        print(data[i])

        print(f"serial_number {serial_number} is {i}th day")
        serial_number = serial_number+1

    x_train = np.array(x_train)
    y_train = np.array(y_train)

    return x_train, y_train

# ------------------------------------------------ Data processing ------------------------------------------------
def data_processing():

    # set past
    past = 3

    # set train/test/validation rate
    train_rate = 0.8      # this mean 80% of the data will be training data
    test_rate = 0.1       # 10%
    validation_rate = 0.1 # 10%

    # Dataset
    x_train, y_train = [], []   # x is input data(the previous 7 days data)
                                # y is output data(the next day data)
    x_test, y_test = [], []
    x_validation, y_validation = [], []


    #print_data()
    # Read data from the csv file on http://125.227.15.167/download
    year_data = build_year_data(2023, 10, 6) # End date
    # Build New dataset
    x, y = buildTrain(year_data, past)
    x_pron = np.array(x)
    y_pron = np.array(y)
    print(x_pron.shape)
    print(y_pron.shape)
    #a = np.concatenate((x_pron, y_pron))
    save_file_name = f'./full_data.npz'
    np.savez_compressed(save_file_name, x_pron = x_pron, y_pron = y_pron)
    print(f'Save dataset as {save_file_name}')
    print("------------------------------------------------ Data (Inside) ------------------------------------------------")
    print("Data's x,y shape :")
    print(x.shape, y.shape)

    # set train/test/validation rate
    train_rate = 0.8      # 80% of the data will be training data
    validation_rate = 0.2 # 20% will be validation data
    # Split into training, validation and testing data
    size = x.shape[0]

    # Split the data: last 10% for testing, first 90% for training and validation
    split_index = int(size * 0.9)

    # Test data is the last 10%
    x_test = x[split_index:]
    y_test = y[split_index:]

    # Training and validation data come from the first 90%
    x_train_val = x[:split_index]
    y_train_val = y[:split_index]

    # Randomly split the first 90% into training and validation sets
    x_train, x_validation, y_train, y_validation = train_test_split(
        x_train_val, y_train_val, test_size=validation_rate, random_state=42
    )

    # for i in range(size):
    #     # Split into training
    #     if i < (size*train_rate):
    #         x_train.append(x[i])
    #         y_train.append(y[i])
    #     # Split into validation
    #     elif (i < (size*(train_rate+validation_rate))) and (i >= (size*train_rate)):
    #         x_validation.append(x[i])
    #         y_validation.append(y[i])
    #     # Split into testing
    #     else:
    #         x_test.append(x[i])
    #         y_test.append(y[i])

    # convert to ndarray
    x_train = np.array(x_train)
    y_train = np.array(y_train)
    x_test = np.array(x_test)
    y_test = np.array(y_test)
    x_validation = np.array(x_validation)
    y_validation = np.array(y_validation)

    # print shape
    print("------------------------------------------------ All Data (Inside) ------------------------------------------------")
    print("x_train, y_train's shape : ")
    print(x_train.shape)
    print(y_train.shape)
    print("x_test, y_test's shape : ")
    print(x_test.shape)
    print(y_test.shape)
    print("x_validation, y_validation's shape : ")
    print(x_validation.shape)
    print(y_validation.shape)

    # save the dataset as dataset.npz
    save_file_name = f'./30min_dataset_past_{past}day.npz'
    np.savez_compressed(save_file_name, x_train = x_train, 
                                        y_train = y_train, 
                                        x_test = x_test,
                                        y_test = y_test,
                                        x_validation = x_validation,
                                        y_validation = y_validation)
    print(f'Save dataset as {save_file_name}')


if __name__ == '__main__':  
    data_processing()
