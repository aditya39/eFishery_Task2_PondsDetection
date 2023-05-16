# eFishery_Task2_PondsDetection

<div align="center" style="text-align: center">

<p style="text-align: center">
  <img align="center" src="efisherylogolandscape.jpg" alt="eFishery" width="500">
</p>

</div>

# eFishery Task 3 - Vibrio Detection
<p> Hi.. </p>
The purpose of this project is to be able detect, counting, and classifying vibrio bacteria with YOLOv8, well known as one of the DeepLearning object detection algorithm.
This is also part of take home test for applying Machine Learning Computer Vision Engineer in eFishery.

## Problem
Mr. Joshua who is an Aquaculture Expert in the field of microbiology. At this time, he is in need of help to count the number of vibrio colonies because he is used to processing more or less 100 cups per day. Counting one cups consist dozens of different vibrio already a pain, imagine 100 cups. 
Mr. Joshua need an alternative or automatic ways to do this painfull jobs.
  
## Idea & Solution
To make Mr. Joshua live easier, we create a web based platform to be able detect vibrio, classify & count.
Deep learning approach were made to solved this problem, by using YOLOv8 (You Only Look Once version 8) we be able to detect, classify the size also color of the vibrio.

  How it work
  1. Prepare the dataset, annotate the image, and export it into YOLOv8 format (I used Roboflow to do this).
  2. Train the pretrained models of YOLOv8 with our dataset (link train.ipynb).
  3. Use ClearML to tracks and controls the process, performance metrics, and model storing.
  4. Create the platform using streamlit and inference the image using the our trained model.
  
## Installation and Usage
Here is the instruction about how to install and run the program.
<br>
### PYTHON USAGE
1. Clone this git repo, you can download or use commmand below
```
git clone https://github.com/aditya39/eFishery_Task2_PondsDetection.git
```
2. Install depedency (Recommend to create Virtual Environtment first before doing this step)
   Enter the project directory then run this command in CLI like CMD:
```
pip install -r requirements.txt
```
4. To run the program, run this command below on CLI
```
streamlit run app.py
```
5. Browser will automatically open, if not, type localhost:8501 to broweser address. Web application page will be open.

### DOCKER COMPOSE
1. Clone this git repository by run command below.
```
git clone https://github.com/aditya39/eFishery_Task2_PondsDetection.git
```
2. To run the app, open CLI on the directory of the program and run this command.
```
docker-compose up
```
3. Wait to load and install depedency, after done you can go to browser and run localhost:8501, app should be running.
4. To stop the docker, run this command.
```
docker-compose down
```

## Demo
### Input gambar
<p style="text-align: center">
  <img align="center" src="homepage.png" alt="eFishery">
</p>

### Choose model
<p style="text-align: center">
  <img align="center" src="model.png" alt="eFishery">
</p>

### Result
<p style="text-align: center">
  <img align="center" src="result.png" alt="eFishery">
</p>
