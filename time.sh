#!/bin/sh
SECONDS=0
while [ $((SECONDS)) -lt  3600 ]
do
    t=`date +"%Y_%m_%d_%H_%M_%S"`
    wget -O $t.html http://www.wsj.com/mdc/public/page/2_3021-activnyse-actives.html
    python ./hw9.py $t.html
    sleep 1m
done


