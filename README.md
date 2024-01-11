# Setup
* tensorflow-macos 2.12.0
* python 3.10.12 
* pandas 2.0.3
* matplotlib 3.7.2
* keras 2.12.0
* numpy 1.23.5

Executing on the linux or Unix system will be better.  
However, it is also possible to execute on Windows system.   
Download <ins>BASH</ins> and <ins>tensorflow</ins> for windows might be fine to do it!  

****

# Prediction
There are two kinds of prediction here.  
Simply to get the result, you can give the order to get the <ins>line chart with ground truth(GT).</ins>
```
bash run_GT.sh 2023-12-26_2023-12-29.csv 2023-12-26
```
![1to1_3Day](https://github.com/Moyacaca/TSRI_Air-Quality-Prediction/assets/117159970/8beb161b-f88d-4203-9d50-b12032975836)

****

To get the <ins>line chart without ground truth</ins>, please give the order below.  
```
bash run.sh 2023-12-26_2023-12-28.csv 2023-12-26
```
![1to1_3Day_noGT](https://github.com/Moyacaca/TSRI_Air-Quality-Prediction/assets/117159970/e5594ab5-36d8-437f-838e-b77560e3b447)


****

For detail information or customized data for prediction, please read the guideline below. 

<br>

## Prediction with ground truth
The one with ground truth(GT) will plot the ground truth in the line chart.  

You can give the order to get the result.  
```
bash run_GT.sh <csv filename> <start date>
```
Please note that the information in "csv filename" should only contain <ins>4 dates</ins> of data(including a ground truth). It is necessary to put your csv file into the pred_today_GT folder.  
And the format of "start date" should be "YYYY-MM-DD".  
<br>
For example,  
```
bash run_GT.sh 2023-12-26_2023-12-29.csv 2023-12-26
```
The 2023-12-26_2023-12-29.csv file is already included in the pred_today_GT folder.   
You can give the order above directly to get the line charts and the average numbers.  

****

## Prediction without ground truth
The one without ground truth is for the purpose of realistic prediction. 

You can give the order below to get the result.  
```
bash run.sh <csv filename> <start date>
```
Please note that the information in "csv filename" should only contain <ins>3 dates</ins>ins of data. It is necessary to put your csv file into the pred_today folder.  
And the format of "start date" should be "YYYY-MM-DD".  
<br>
For example,  
```
bash run.sh 2023-12-26_2023-12-28.csv 2023-12-26
```
The 2023-12-26_2023-12-28.csv file is already included in the pred_today folder.   
You can give the order above directly to get the line charts and the average numbers.  
