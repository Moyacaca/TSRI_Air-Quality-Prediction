# Setup
* tensorflow-macos 2.12.0
* python 3.10.12 
* pandas 2.0.3
* matplotlib 3.7.2
* keras 2.12.0
* numpy 1.23.5

Executing on the linux or Unix system will be better.  
However, it is also possible to execute on Windows system.   
Download BASH and tensorflow for windows might be fine to execute it too!  

# Prediction
There are two kinds of prediction here.

Simply to get the result, you can give the order to get the <ins>line chart with ground truth.</ins>
```
bash run_GT.sh 2023-12-26_2023-12-29.csv 2023-12-26
```

To get the <ins>line chart without ground truth</ins>, please give the order below.
```
bash run.sh 2023-12-26_2023-12-28.csv 2023-12-26
```

****

For detail information or customized data for prediction, please read the guide below. 
</br>


## 1st model prediction process
The one with ground truth(GT) will plot the ground truth out like the picture shown below.  

You can give the order to get the result.  
```
bash run_GT.sh <csv filename> <start date>
```
Please note that the information in "csv filename" should only contain 4 dates of data(including a ground truth). It is necessary to put your csv file into the pred_today_GT folder.  
And the format of "start date" should be "YYYY-MM-DD".  

For example,  
```
bash run_GT.sh 2023-12-26_2023-12-29.csv 2023-12-26
```
The 2023-12-26_2023-12-29.csv file is already included in the pred_today_GT folder.   
You can give the order above directly to get the line charts and the average numbers.  

## 2rd model prediction process
The one without ground truth is for the purpose of realistic prediction.  
You can give the order below to get the result.  
```
bash run.sh <csv filename> <start date>
```
Please note that the information in "csv filename" should only contain 3 dates of data. It is necessary to put your csv file into the pred_today folder.  
And the format of "start date" should be "YYYY-MM-DD".  

For example,  
```
bash run.sh 2023-12-26_2023-12-28.csv 2023-12-26
```
The 2023-12-26_2023-12-28.csv file is already included in the pred_today folder.   
You can give the order above directly to get the line charts and the average numbers.  
