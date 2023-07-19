
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



st.set_page_config(
    page_title="Scan",
    initial_sidebar_state='collapsed',
)
dataset = r'C:\Users\danje\Downloads\Fish_Dataset'
best_epoch = 0
model = torch.load("{}_model_{}.pt".format(dataset, best_epoch))

idx_to_class = {0: 'Black Sea Sprat', 1: 'Gilt-Head Bream', 2: 'Hourse Mackarel', 3: 'Red Mullet', 4: 'Red Sea Bream', 5: 'Sea Bass', 6: 'Shrimp', 7: 'Striped Red Mullet', 8: 'Trout'}
image_transforms = { 
    'train': transforms.Compose([
        transforms.RandomResizedCrop(size=256, scale=(0.8, 1.0)),
        transforms.RandomRotation(degrees=15),
        transforms.RandomHorizontalFlip(),
        transforms.CenterCrop(size=224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ]),
    'valid': transforms.Compose([
        transforms.Resize(size=256),
        transforms.CenterCrop(size=224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ]),
    'test': transforms.Compose([
        transforms.Resize(size=256),
        transforms.CenterCrop(size=224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])
}

def predict(model, test_image_name):
    '''
    Function to predict the class of a single test image
    Parameters
        :param model: Model to test
        :param test_image_name: Test image

    '''
    
    transform = image_transforms['test']


    test_image = Image.open(test_image_name)
    plt.imshow(test_image)
    
    test_image_tensor = transform(test_image)
    test_image_tensor = test_image_tensor.clone().detach()
    if torch.cuda.is_available():
        test_image_tensor = test_image_tensor.view(1, 3, 224, 224).cuda()
    else:
        test_image_tensor = test_image_tensor.view(1, 3, 224, 224)
    
    with torch.no_grad():
        model.eval()
        # Model outputs log probabilities
        out = model(test_image_tensor)
        ps = torch.exp(out)

        topk, topclass = ps.topk(3, dim=1)
        cls = idx_to_class[topclass.cpu().numpy()[0][0]]
        score = topk.cpu().numpy()[0][0]

        for i in range(3):
            print("Predcition", i+1, ":", idx_to_class[topclass.cpu().numpy()[0][i]], ", Score: ", topk.cpu().numpy()[0][i])
        return cls
st.write("# Scan your Fish Here: ")
picture = st.camera_input(label="Video Area", label_visibility="hidden", key=2)

if picture is not None:
    bytes_data = picture.getvalue()
    torch_img = torch.ops.image.decode_image(
        torch.from_numpy(np.frombuffer(bytes_data, np.uint8)), 3
    )
    prediction = predict(model, picture)
    st.markdown("<h1 style='text-align: center; color: white;'> Detected: " + prediction + "</h1>", unsafe_allow_html=True)
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