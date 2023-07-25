#!/bin/bash

num=`echo $(( $RANDOM % 1000 + 1 ))`
question=`head -n $num "$1" | tail -n 1`

python kendra_retriever_falcon40b_instruct.py "$question"
echo "----"
