#!/bin/bash
echo "Crawling the file..."

cd web_crawler
python web_interactor.py

cd ..
cd pred_today

echo "Loading the file..."

python build_train_web.py
echo "Start evaluating!"

python lstm_on_web_1to1_3Day_1440.py 
