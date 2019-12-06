#!/bin/bash

if [ -p /dev/stdin ]; then
    while IFS= read line; do
        echo ${line}
        python takehome.py "${line}"
    done
else
        echo "No input was found on stdin!1"
        if [ -f "$1" ]; then
                echo "Filename specified: ${1}"
        else
                echo "No input given!"
        fi
fi
