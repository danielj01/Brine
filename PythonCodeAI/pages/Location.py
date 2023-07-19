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
openai.api_key = "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"

messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]
st.set_page_config(
    page_title="About",
    initial_sidebar_state='collapsed',
)

st.write("# Input Your Specific Location: ")
st.subheader("Gather Data on Fish Species and Areas...")

input_text = st.text_area(label="Prompt Area" , label_visibility="hidden" , placeholder="Enter your location here...", key=1)

if input_text:
    userInput = input_text
    input_text = "Tell me the latitude and longitude of this location without any extra text and using this format latitude, longitude: " + input_text + " Make sure to only include numbers in your response."
    messages.append(
        {"role": "user", "content": input_text},
    )
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages
    )
    reply = chat.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    reply1 = ""
    for number in reply:
        if number in "0123456789.":
            reply1 = reply1 + number
    reply = reply.split(', ')
    input = [eval(i) for i in reply]
    df = pd.DataFrame(
    [input],
    columns=['lat', 'lon'])
    st.map(df)
    st.write("# Information Regarding your area: ")
    input_text = "Give me information on fishing in theses areas, for example the species of fish that you should release which are close to extinction, and which ones to catch due to their high population. Make sure it is in this format: Endangered Species: species1, species2, species3 \n Non-Endangered Species: species1, species2, species3" + userInput 
    messages.append(
        {"role": "user", "content": input_text},
    )
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages
    )
    reply = chat.choices[0].message.content
    print(reply)
    reply = reply.replace("Endangered Species: ", "")
    reply = reply.replace("Non-","")
    print(reply)
    reply = reply.splitlines()
    print(reply)
    replyInput1 = reply[0].split(', ')
    print(replyInput1)
    replyInput2 = reply[1].split(', ')
    reply = [replyInput1,replyInput2]

    df = pd.DataFrame(
        [reply],
        columns=("Endangered Species: ", "Non-Endangered Species: "))
    st.table(df)

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
