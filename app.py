import yaml
import os
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from ultralytics import YOLO
from clearml import InputModel
from segment import segment
from generateMap import getSatelliteImage

os.environ['CLEARML_CONFIG_FILE'] = "clearml.conf"

# Open Config File
with open("config.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

# Create Sidebar
with st.sidebar:
    st.title("Project 2 - Ponds Estimator") # Sidebar Title
    st.image("efisherylogolandscape.jpg") # Sidebar Logo
    st.divider()
    
    # Create select box to select YOLOv8 model
    st.header("Choose a Model")
    selectModel = st.selectbox("What YOLOv8 model you would like to choose?", 
                               ("YOLOv8 Nano", "YOLOv8 Small", "YOLOv8 Medium","YOLOv8 Large"))

    # If model selected, pick the model from ClearML IDModel
    if selectModel == "YOLOv8 Nano":
        model = InputModel(model_id=cfg["model"]["yolov8n"]) # model_id pickup from config.yaml
        store_model = model.get_local_copy()
        model = YOLO(store_model)

    if selectModel == "YOLOv8 Small":
        model = InputModel(model_id=cfg["model"]["yolov8s"])
        store_model = model.get_local_copy()
        model = YOLO(store_model)

    if selectModel == "YOLOv8 Medium":
        model = InputModel(model_id=cfg["model"]["yolov8m"])
        store_model = model.get_local_copy()
        model = YOLO(store_model)

    if selectModel == "YOLOv8 Large":
        model = InputModel(model_id=cfg["model"]["yolov8l"])
        store_model = model.get_local_copy()
        model = YOLO(store_model)

    # Create an expander which explain more about the models difference
    expander = st.expander("See explanation about the model..", expanded=False)
    expander.write("""Xtreme model give the most accuracy while sacrifice performance speed, Nano is the fastest model but least accurate.
    \nYou can check Yolov8 models comparation by expanding image below..
                   Visit YOLO8 github link for more, https://github.com/ultralytics/ultralytics""")
    expander.image("yolo8_detail.png")

    
# Main Page Container
with st.container():
    st.title("Ponds Detection & Estimation With AI!")
    st.divider()

    # Get input for latitude angd longitude
    st.subheader("Enter Latitude and Longitude Here")
    col1, col2 = st.columns(2)
    with col1:
        latitude = st.text_input(
            "Enter Your Latitude here..",
            placeholder="Example: -7.675039",
        )
    with col2:
        longitude = st.text_input(
            "Enter Your Longitude here..",
            placeholder="Example: 107.769191"
        )
    # Button to process the detection
    if st.button('Process'):
        try:
            image, error, message = getSatelliteImage(float(latitude), float(longitude))
            ponds_dict, countListDetected, img_yolo = segment(image, model, float(latitude), zoomLevel=18)
            st.success('Success!', icon="✅")
            st.subheader("Detection Result")

            col1,col2 = st.columns(2)
            with col1:
                st.image(image)
                st.markdown("<p style='text-align: center; color: white;'>Ponds</p>", unsafe_allow_html=True)
            with col2:
                st.image(img_yolo)
                st.markdown("<p style='text-align: center; color: white;'>Ponds Detected by YOLOv8 Segmentation</p>", unsafe_allow_html=True)
         

            # Create container for result of detection 
            with st.container():
                st.header("Ponds Detection Result")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Ponds Detected", countListDetected[0])

            #   print(ponds_dict)
            ponds_table = pd.DataFrame.from_dict(ponds_dict,orient='index', columns=['Area'])
            st.dataframe(ponds_table)
        except:
            pass
     
    
                
    

  