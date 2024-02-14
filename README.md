# Vescicle ML Detection
## Introduction
In this project I attempt to train and use a RCNN to identify dyed brain vescicles from images taken using an electron microsope at different magnification levels.  
Due to the sensitive nature of the images, only the pre-trained models have been pushed to this gitspace without the full set of training images, but only a small number of them are provided for testing. The untrained models can be found in the `models` folder, which is a submodule to the Tensorflow Model garden.

The idea for this project, rather than present a final tool for this task, is to provide a proof of concept that a general RCNN use normally to identify the differences between cats and dogsm can be used towards the automatisartion of this task with high enough identification efficiency. 

I is iportant to note that this task only require **~80% identification efficiency** as the nature of the images makes perfect identification near impossible even for humans. 

## Code Breakdown
- input
- output
- models
- trained_models
- utils
## How to run
### Setup
Firstly, the correct python environment needs to be setup in order to run the scripts.

> conda env create env_setup.yml --name vesc

then the trained models protos need to be added to the python path so that they can be used in code. 
To do so just run the setup.sh script from terminal:

> source setup.sh

### Runme 
# mg380.github.io
