#!/bin/bash


tf_path="/Users/mariograndi/TensorFlow/models/research"

cd $tf_path

protoc -I=./ --python_out=./ ./object_detection/protos/*.proto

export PYTHON_PATH=$PYTHON_PATH:`pwd`:`pwd`/slim

cd -