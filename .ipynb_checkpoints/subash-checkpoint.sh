#!/bin/bash
alpha=$1
L=$2
chparam=$3
cd ~/dynamo
. ~/qenv_bilkis/bin/activate
python3 main.py --alpha $alpha --L $L --Npriors 10 --chanel_params $chparam 1 
deactivate
