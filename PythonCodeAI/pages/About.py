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
from streamlit.components.v1 import html
import streamlit.components.v1 as components
st.set_page_config(

    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 0rem;
                    padding-right: 0rem;
                }
        </style>
        """, unsafe_allow_html=True)
components.html(
"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500&display=swap');
*{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Poppins', sans-serif;
  color: #ddd;
}
.features{
  height: 500px;
  width: 100%;
  padding: 90px 0;
  background: #0E1117;
}
.featuresDesc{
  height: 300px;
  width: 100%;
  padding: 90px 0;
  background: #0E1117;
}
.about-us{
  height: 900px;
  width: 100%;
  padding: 150px 0;
  background: #0E1117;
}
.pic{
  height: auto;
  width: 500px;
}
.pic2{
  height: auto;
  width: 500px;
}
.about{
  width: 1130px;
  max-width: 100%;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-around;
}
.text{
  width: 540px;
}
.text h6{
  width: 900px;
  font-size: 90px;
  font-weight: 600;
  margin-left: -150px;
}
.text h1{
  font-size: 90px;
  font-weight: 600;
  margin-bottom: 20px;
}
.text h2{
  font-size: 90px;
  font-weight: 600;
  margin-bottom: 10px;
}
.text h5{
  font-size: 22px;
  font-weight: 500;
  margin-bottom: 20px;
}
.text h3{
  font-size: 22px;
  font-weight: 500;
  margin-top: 20px;
}
span{
  color: #4070f4;
}
.text p{
  font-size: 18px;
  line-height: 25px;
  letter-spacing: 1px;
}
.data{
  margin-top: 50px;
}
</style>
<!DOCTYPE html>
<!-- Coding By CodingNepal - codingnepalweb.com -->
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
 <title> An About Us Page | CoderGirl </title>
  <!---Custom Css File!--->
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <section class="about-us">
    <div class="about">
      <img src="https://files.worldwildlife.org/wwfcmsprod/images/Fishing_Net/story_full_width/9t3d6gqugs_shutterstock_513364243.jpg" class="pic">
      <div class="text">
        <h2>About Us</h2>
        <h5>What drives us & <span>Why we do it...</span></h5>
          <p>We are a passionate team of students participating in a hackathon, driven by a shared concern for the environment. Our Fish Species Detection application utilizes cutting-edge machine learning and computer vision to spread awareness about overfishing. By accurately identifying fish species from images, we empower users with knowledge of sustainable fishing practices and the importance of preserving marine biodiversity. Join us on this journey to make a positive impact and protect our oceans for a sustainable tomorrow.</p>
        <div class="data">
        </div>
      </div>
    </div>
  </section>
  <section class="featureDesc">
    <div class="about">
      <div class="text">
        <h6>Included Features</h6>
        <div class="data">
        </div>
      </div>
    </div>
  </section>
  <section class="features">
    <div class="about">
      <img src="https://erepublic.brightspotcdn.com/dims4/default/e61ab23/2147483647/strip/true/crop/770x374+0+69/resize/1440x700!/quality/90/?url=http%3A%2F%2Ferepublic-brightspot.s3.amazonaws.com%2F21%2F97%2Fd00f65636598110cc7631c7c7736%2Ffish.jpg" class="pic">
      <div class="text">
        <h1>Feature 1</h1>
        <h5>Image <span>Recognition</span></h5>
          <p>Our website's image recognition model boasts a cutting-edge fish species detection feature, accurately identifying various fish species from uploaded images with remarkable precision, aiding enthusiasts and researchers alike in effortlessly identifying aquatic life.</p>
        <div class="data">
        </div>
      </div>
    </div>
  </section>
  <section class="features">
    <div class="about">
      <img src="https://i.stack.imgur.com/YNVyH.jpg" class="pic2">
      <div class="text">
        <h1>Feature 2</h1>
        <h5>Map <span>Management</span></h5>
          <p>Our website's image recognition model boasts a cutting-edge fish species detection feature, accurately identifying various fish species from uploaded images with remarkable precision, aiding enthusiasts and researchers alike in effortlessly identifying aquatic life.</p>
        <div class="data">
        </div>
      </div>
    </div>
  </section>
  <section class="features">
    <div class="about">
      <img src="https://globalfishingwatch.org/wp-content/uploads/3.Global-Fishing-Activity-dark-1030x677.png" class="pic2">
      <div class="text">
        <h1>Feature 3</h1>
        <h5>Fish <span>Tracking</span></h5>
          <p>Our cutting-edge fishing location feature utilizes geospatial data and user-generated inputs to deliver personalized and up-to-date recommendations, guiding you to the prime fishing spots in your vicinity, ensuring an exceptional fishing experience every time you cast your line.</p>
        <div class="data">
        </div>
      </div>
    </div>
  </section>
</body>
</html>
""", width=2000, height=2000, scrolling=True
)
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