#!/bin/bash
echo "Crawling the file..."

cd web_crawler
python web_interactor.py

cd ..

cd pred_today_GT

echo "Loading the file..."

python build_train_e2e.py
echo "Start evaluating!"

python lstm_on_web_1to1_3Day.py 
