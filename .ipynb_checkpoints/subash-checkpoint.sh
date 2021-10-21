#!/bin/bash
alpha=$1
L=$2
ch=$3
cd ~/dynamo
. ~/qenv_bilkis/bin/activate
python3 main.py --alpha $alpha --L $L --Npriors 300 --channel_params $ch 1 
deactivate
