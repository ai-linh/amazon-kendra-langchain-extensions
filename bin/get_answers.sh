#!/bin/bash

while read -r line; do
    python kendra_retriever_falcon40b_instruct.py "$line"
    echo "----"
    done < "$1"

