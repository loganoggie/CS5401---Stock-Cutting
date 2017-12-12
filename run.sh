#!/bin/bash

export PYTHONHASHSEED=0

pip3 install tqdm >/dev/null

config=$1
problem=$2

. $config

python3 StockCutting.py $problem -lf $log -sf $solution -s $seed -es $strategy -e $evals -r $runs -m $mu -l $lambda -ps $pSelection -pk $pkval -ss $sSelection -sk $skval -mr $mRate -t $term -n $nVal -pc $pCoefficient -sa $selfAdaptive -i $initSeed
