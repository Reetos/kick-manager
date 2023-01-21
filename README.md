# Kick-Manager
## Video Demo:
https://youtu.be/yi69QxH2e30
# Description
## Introduction
   Kick-Manager is a desktop application that utilizes a deep learning model to sort kick samples (in .wav format) into their corresponding genres so that users can choose the kick sound suitable for the music genre they want to make.


## How Kick-Manager Works
By pressing the button "Select directory", a file dialog is prompted, where you can choose a directory that contains the kick samples that you want to sort into genres.

After a while, you can see that all of your kick samples have been sorted into their corresponding genres as you can see by clicking the name of the genres.

Once the sorting process is done, Kick-Manager creates a new directory called "Kick-Manager" under the same directory as the directory you selected is located at.
So you can add the path of this directory e.g. "Kick-Manager" to your DAW or any other software that hundles wav files to select the kick samples based on the music genre you want to make.


## The Buillding Files of Kick-Manager
### 1. clean.py
This file preprocesses the audio data before passing them into the deep learning model.
#### The role of each module is:
・ envelope: Eliminate some parts of the audio file with loudness below a threshold value.
・ downsample_mono: Downsample stereo samples into mono samples.

### 2. predict.py
This file is to predict the genre that each kick sample is suitable for by using a deep learning model.

### 3. custom_gui.py
This is the file that generates the GUI of Kick-Manager.

### 4. models.py
Three deep learning models are built and saved as .h5 files: 1D convolutional neural network, 2D convolutional neural network, recurrent neural network

### 5. conv1d.h5
This is a 1D convolutional neural network used in 'predict.py'
#### Among 1D convolutional network, 2D convolutional network and recurrent neural network, 1D convolutional network was chosen based on the prediction accuracy.

### 6. predictions.csv
This is a csv file that contains the result of prediction is stored.

