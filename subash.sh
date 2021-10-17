#!/bin/bash
alpha=$1
L=$2
cd ~/dynamo
. ~/qenv_bilkis/bin/activate
python3 main.py --alpha $alpha --L $L
deactivate
