# Environment
keras               2.12.0  
selenium            3.141.0  
tensorflow-macos    2.12.0  

****
# Inference
There are two kinds of inference here.

## 1st model prediction process
1st model will print the Ground Truth(GT) out.  
You can give the order to get the result.
```
bash run_GT.sh
```
It will crawl the latest data from the website and inference.


## 2rd model prediction process
It is a realistic prdiction using the latest data.  
You can give the order below to get the result.
```
bash run.sh
```
It will crawl the latest data from the website and inference.  
<ins> Note that the routine should be executed at the start of a day. </ins>  


In the figure folder, there are six files containing data for each air quality prediction.  
In the file(the picture below), the data in the orange box is forcast data.  
The data in the green box is yesterday's data.  
The first line belongs to the time "00:01", the sencod belongs to "00:02", and so on.  
<img width="378" alt="image" src="https://github.com/Moyacaca/TSRI_Air-Quality-Prediction/assets/117159970/c9ca9522-3103-407a-9d4a-be782da6b0b0">

The newest edits are all in the file "pred_today/ lstm_on_web_1to1_3Day_1440.py".
