## About the Project


## Getting Started
### Prerequisites
The program mainly run on python, ensure you have python3 on your device to run the program without problem,

These following python library are mandatory to run the program. 
os
json
numpy
pandas
random
scipy.interpolate 
pprint
matplotlib.pyplot 
matplotlib.animation 
tensorflow
scikitlearn

### Running the Program
The program are written in notebook (ipynb) format, so that you can run every segment/cell independently. To run the desired shell simply press `Super/Windows/Mac + Enter` on your notebook (jupyter, colab, vscode, etc). 

#### Section List
##### Data Acquisition
In the file *'data-manual-input.ipynb'*, contain an application to record the hand gesture from your device's camera, and store the data as json format, here are the command on using the app.

t   : store the recorded gesture as 'rotate-left' class \
y   : store the recorded gesture as 'rotate-right' class \
u   : store the recorded gesture as 'zoom-in' class \
i   : store the recorded gesture as 'zoom-out' class \
o   : store the recorded gesture as 'slide-left' class \
p   : store the recorded gesture as 'slide-right' class\
esc : exit the application

Note that if you have more than one camera plugged in your device, change the camera index accordingly. 


##### Data Processing

In the *'data-processor.ipynb'*, there are few segment to augment the data based on some input of authentic data, including adding noises, scaling, rotating, and translating the previous record. This section is used to handle various cases without redundantly record the data manually. 

Lastly we have the machine learning model using LSTM. This section is to build our model and show the training result. 
