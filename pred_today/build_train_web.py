#program name : build_train.py
#porpose : Build training data from http://125.227.15.167/download

import pandas as pd
import numpy as np
import csv
import threading
import matplotlib.pyplot as plt
import pandas as pd
import argparse
from datetime import datetime


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

# def print_data():
   
#    sample_data = pd.read_csv("2023-12-05_14-23-19_730.csv")
#   y = list(sample_data['Temperature'])
#   x = list(sample_data['Time'])
#    plt.plot(x, y)
#    plt.ylabel('CO',fontsize=10)
#    plt.xlabel('Time',fontsize=10)
   
#    plt.show()

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
    
    # file_name = f'2023-12-22_2023-12-29.csv'
    with open(full_path, newline='') as csvfile:
    
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
                elif type == 'o3':
                    o3.append(float(row[8]))
                elif type == 'so2':
                    so2.append(float(row[9]))
                elif type == 'no2':
                    no2.append(float(row[10]))
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
                elif type == 'o3':
                    o3.append(float(row[8]))
                elif type == 'so2':
                    so2.append(float(row[9]))
                elif type == 'no2':
                    no2.append(float(row[10]))
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

    pm25, pm1p0, pm10, co2, co, o3, so2, no2, tmp, hum = [], [], [], [], [], [], [], [], [], []

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

    return tmp, hum, pm25, pm10, pm1p0, co2, co

# ------------------------------------------------ build IoT data ------------------------------------------------
def build_year_data(end_y, end_m, end_d):
    
    unavaliabe_data = 0

    year_data = []  # define an empty array (use for store year data)

    year, month, day = year_td, month_td, day_td-3 # Start date

    while True:
        # Read only a day's data and return it's feature
        tmp, hum, pm25, pm10, pm1p0, co2, co = read_day_data(year, month, day) 
        # Combine all the feature to become a single matrix
        day_data = np.concatenate([tmp, hum, pm25, pm1p0, pm10, co2, co])
        #print(day_data)
        day_data = np.reshape(day_data,(7, -1))
        #print(day_data)
        day_data = np.rot90(day_data, -1)
        x, y = day_data.shape
        print('x = ', x)
        if x < 48:
            print(day_data)
        #print('y = ', y)
        #print(day_data)
        print('------------------------------------')
        for i in range(x):
            if day_data[i][2] >= 70:  # Define the threshold of pm2.5
                #print(day_data)
                unavaliabe_data = 1
                break
            else:
                unavaliabe_data = 0
        # Append to year's data
        if unavaliabe_data == 1:
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
    if array.shape == (48, 7):
        return 1
    else:
        return 0

# ------------------------------------------------- build train function -------------------------------------------------
def buildTrain(data, past):

    x_test = []
    # print(data)
        
    break_flag = 0
    # check data's shape is right or not
    for check_i in range(0, past):

        # if the data's shape or value isn't right
        if check_shape(data[check_i]) == 0:
            break_flag = 1
            print(data[check_i].shape)
            print(f"Wrong Shape with {check_i}th day")
            break

    if break_flag:
        return 0
        
    # if all data's shape is correct, append x_train
    x_temp = []
    for x_i in range(0, past):
        x_temp.extend(data[x_i])

    x_test.append(x_temp)

    x_test = np.array(x_test)

    return x_test

# ------------------------------------------------ Data processing ------------------------------------------------
def data_processing():

    # set past
    past = 3

    # Read data from the csv file on http://125.227.15.167/download
    year_data = build_year_data(year_td, month_td, day_td - 1) # Build New data from 2023/12/22 to 2023/12/28 
                                              # please write the end date
    # Build New dataset
    x = buildTrain(year_data, past)

    if buildTrain == 0:
        print("Data missing...")
    else:
        x_pron = np.array(x)
        print("print x shape.")
        print(x.shape)
        print(x_pron.shape)
        
        print("------------------------------------------------ Data (Inside) ------------------------------------------------")
        print("Data's x shape :")
        print(x.shape)

        # print shape
        print("------------------------------------------------ All Data (Inside) ------------------------------------------------")
        print("x_pron shape : ")
        print(x_pron.shape)

        # save the dataset as dataset.npz
        save_file_name = f'evaluate_{past}day.npz'
        np.savez_compressed(save_file_name, x_test = x_pron)
        print(f'Save dataset as {save_file_name}')

def extract_date_from_filename(filename):

    global year_td, month_td, day_td  # Declare the variables as global

    # Splitting the filename to separate the date and time
    date_part, time_part, no_use = filename.split('_')

    # Splitting the date part to get year, month, and day
    year_td, month_td, day_td = date_part.split('-')

    year_td = int(year_td)
    month_td = int(month_td)
    day_td = int(day_td)

    print("Year_td:", year_td)
    print("Month_td:", month_td)
    print("Day_td:", day_td)


if __name__ == '__main__':  

    # parser = argparse.ArgumentParser(description='Process a CSV file with a specified start date.')
    # parser.add_argument("-f", "--filename", type=str, help='Path to the CSV file')
    # parser.add_argument("-d", "--date", type=str, help='Date in the format YYYY-MM-DD')

    # args = parser.parse_args()
    year_td = None
    month_td = None
    day_td = None

    try:
        with open("../web_crawler/downloaded_filename.txt", "r") as file:
            filename = file.read()
        print("Open txt file succefully!")
        print("csv filename:", filename)

        extract_date_from_filename(filename)
        

        print("Extract date succefully!")

        folder_path = '../web_crawler/'
        full_path = folder_path + filename
        # Your code to process the date goes here
        print("Processing date:", year_td, month_td, day_td-1)
        data_processing()
    except ValueError:
        print("Invalid date format.")