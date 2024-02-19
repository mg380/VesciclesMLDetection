#!/bin/bash


tf_path="models/research"

cd $tf_path

protoc -I=./ --python_out=./ ./object_detection/protos/*.proto

export PYTHON_PATH=$PYTHON_PATH:`pwd`:`pwd`/slim

cd -

# setting up conda environment

if [[ "$1" == "conda" ]]; then 
    
    which conda &> /dev/null
    
    [[ $? -ne 0 ]] && echo "conda not found, please install conda or setup environment to run with conda" && exit

    if [[ "$2" == "create" ]]; then 

        conda create --name vesc --file data/spec-file.txt

        conda activate vesc
    elif [[ "$2" == "activate" ]];then
        
        conda activate vesc
    fi
fi
