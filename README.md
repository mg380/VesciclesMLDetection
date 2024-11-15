# Vescicle ML Detection
## Project Overview
In this project, I developed and trained a Region-based Convolutional Neural Network (RCNN) to identify dyed brain vesicles in electron microscope images taken at varying magnification levels. This project serves as a proof of concept, demonstrating the feasibility of adapting an RCNN—typically used for object detection tasks like distinguishing between cats and dogs—to automate vesicle detection with high accuracy. While not a fully operational tool, the project illustrates the potential of RCNNs in addressing complex challenges in biomedical imaging.

## Data and Models
Due to the sensitive nature of the images, the full training dataset is not included in this repository. Instead, I have provided a small subset of the images for testing purposes, along with the pre-trained models. The untrained models are located in the models folder, which is linked to the TensorFlow Model Garden as a submodule.

It's important to note that achieving ~80% identification efficiency is sufficient for this task, as the complexity of the images makes perfect identification nearly impossible, even for human experts.

## Functionality
The code provided enables the identification of the vesicles in the test images, drawing bounding boxes around them and supporting post-processing analysis. Additionally, users can generate summary plots for further insights. Below are examples of the expected output from the tool.

<img src="data/assets/example_image.jpeg" width="window.innerWidth" height="auto">
<img src="data/assets/example_boxes.png" width="window.innerWidth" height="auto">
<img src="data/assets/example_drawing.png" width="window.innerWidth" height="auto">
<!-- ![image](data/assets/example_image.jpeg | width=100) -->
<!-- ![image2](data/assets/example_boxes.png | w) -->
<!-- ![image3](data/assets/example_drawing.png) -->

## Code Breakdown
- input: Contains the input electron microscope images for vesicle identification.
- output: Stores the results, including images with bounding boxes drawn around the detected vesicles.
- models: Includes untrained models and a submodule linked to the TensorFlow Model Garden.
- data: A small subset of sample images for testing, due to the sensitive nature of the full dataset.
- trained_models: Contains pre-trained models used for the task.
- utils: Utility scripts for pre- and post-processing tasks.

## Setup
To run the scripts, you need to set up the correct Python environment.
1. Create the Conda environment:
```bash
conda env create env_setup.yml --name vesc
```
2. Add trained model protos to the Python path: Run the setup.sh script:
```bash
source setup.sh
```
3. If the Conda environment needs to be created: Run the following command:
```bash
source setup.sh conda create 
```
4. If the Conda environment is already set up: Activate it by running:
```bash
source setup.sh conda activate
```

## How to run
You can run the individual source scripts or use the runme.sh file, which ensures all steps are executed properly. There are three main steps in the pipeline:

1. Run the ML box finder:
```bash
Copy code
source runme.sh --run finder
```
2. Perform post-processing using the drawing application:
```bash
Copy code
source runme.sh --run draw
```
3. Run the analysis script:
```bash
Copy code
source runme.sh --run analysis
```

The runme.sh script is the recommended method as it handles the correct sequence of script execution.
