import streamlit as st
from streamlit_lottie import st_lottie
import torch
import numpy as np
import imageio.v3 as iio
import cv2
from torchvision.io import read_image
from torchvision.models import resnet50, ResNet50_Weights
import torch, torchvision
from torchvision import datasets, models, transforms
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import time
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
from torchsummary import summary
import pandas as pd
import os
import openai
import re
import streamlit_extras as components
openai.api_key = "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"
messages = [ {"role": "system", "content": "You are a intelligent assistant who is knowledgable in Fishing."} ]
st.set_page_config(
    page_title="Fish_Tracking",
    initial_sidebar_state='collapsed',
)
st.write("# Give your Latitude and Longitude ")
st.subheader("Get Data on the Best Fishing Spots...")

number = st.number_input('Insert your Specific Latitude...')
number2 = st.number_input('Insert your Specific Longitude...')
coords = [[number,number2]]
st.divider()
st.write("# Specify Your Fishing Radius")
st.subheader("Give the amount of miles away you want to fish in...")
input = st.number_input('Specify your radiues (in miles)...', min_value=0)
st.divider()
colm1, colm2, colm3 , colm4, colm5 = st.columns(5)
with colm1:
    pass
with colm2:
    pass
with colm4:
    pass
with colm5:
    pass
with colm3 :
    button = st.button('Start')
col1, col2 = st.columns(2)
temp = 0
catchRate = ""
table = []
boolean = False
if button:
    input_text = "Give a list of coordinates in this format [latitude, longitude], that is in the radius of " + str(input) + " miles away from the coordinates " + str(coords) + ", that have the best fishing catch rates/spots, and base it on past information and water depth around the area. Remember to only show the list of coordinates, seperated by commas, without any extra warnings/text, like this: [lat,long], [lat,long], [lat,long]"
    messages.append(
            {"role": "user", "content": input_text},
        )
    chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
    reply = chat.choices[0].message.content
    data_str = reply
    try:
        data_list = eval('[' + data_str + ']')
        print(data_list)
        boolean = True
    except:
        st.error("Input another pair of coordinates and radius, we are not able to recieve information of these.")

with col1:
   if boolean:
       coords = data_list
   st.header("Best Fishing Spot Near You...")
   df = pd.DataFrame(
    coords,
    columns=['lat', 'lon'])
   st.map(df)
   st.write("Coordinates of the points: " + str(coords))
   
   

with col2:
    if button:
        st.header("Information Regarding Your Area...")
        output = "Give general information on this area which is in the format [latitude, longitude]: " + str([number,number2]) + ", about the water depth, average temperature, etc and make in a bullet note/table format"
        messages.append(
                {"role": "user", "content": output},
            )
        chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            )
        output = chat.choices[0].message.content
        st.write(output)

from streamlit.components.v1 import html

def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)

colm1, colm2, colm3 , colm4, colm5 = st.columns(5)
with colm1:
    pass
with colm2:
    pass
with colm4:
    pass
with colm5:
    pass
with colm3 :
    if st.button('Go Back'):
        nav_page("")