# Environment
keras               2.12.0  
selenium            3.141.0  
tensorflow-macos    2.12.0  

****
# Inference
There are two kinds of inference here.

## 1st model prediction process
The one with ground truth(GT) will plot the ground truth out like the picture shown below.
<img width="586" alt="image" src="https://github.com/Moyacaca/TSRI_Air-Quality-Prediction/assets/117159970/fe9502ad-3c4c-42f6-9b0f-06f00f1c9e93">

You can give the order to get the result.
```
bash run_GT.sh
```
It will crawl the latest data from the website and inference.


## 2rd model prediction process
The one without ground truth is for the purpose of realistic prediction.
<img width="572" alt="image" src="https://github.com/Moyacaca/TSRI_Air-Quality-Prediction/assets/117159970/36cf50c9-9b3c-4b84-b806-cbbcedc64878">

You can give the order below to get the result.
```
bash run.sh
```
It will crawl the latest data from the website and inference.  
<ins> Note that the routine should be executed at the start of a day. </ins>


