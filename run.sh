#!/bin/bash
cd pred_today

echo "Loading the file..."

python build_train_web.py -f "${1}" -d "${2}"
echo "Start evaluating!"

python lstm_on_web_1to1_3Day.py
