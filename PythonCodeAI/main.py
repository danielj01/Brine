import streamlit as st
import torch
import numpy as np
import imageio.v3 as iio
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

st.set_page_config(
    page_title="main",
    page_icon="🧠",
    initial_sidebar_state='collapsed',
)
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
video_html = """
    <style>

    #myVideo {
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%; 
        min-height: 100%;
    }

    .content {
        position: fixed;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        color: #f1f1f1;
        width: 100%;
        padding: 20px;
    }

    </style>	
    <video autoplay muted loop id="myVideo">
        <source src="https://dl.dropboxusercontent.com/scl/fi/9hm544wx2pmxss9y9yh1q/userVideo-2.mp4?rlkey=5kvi2ckkuhfqbwte27p5uwrtw&dl=0")>
        Your browser does not support HTML5 video.
    </video>
    """

st.markdown(video_html, unsafe_allow_html=True)
image = Image.open(r'C:\Users\danje\Downloads\brine-low-resolution-logo-color-on-transparent-background.png')
st.image(image)

components.html(
    """
    <script type="text/javascript">
    function console() {
        console.log("Hello");
    }
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
           
    var snippet = [].slice.call(document.querySelectorAll('.hover'));
    
    if (snippet.length) {
    snippet.forEach(function (snippet) {
        snippet.addEventListener('mouseout', function (event) {
        if (event.target.parentNode.tagName === 'figure') {
            event.target.parentNode.classList.remove('hover')
        } else {
            event.target.parentNode.classList.remove('hover')
        }
        });
    });
    }

    </script>
    <style>
    @import url(https://fonts.googleapis.com/css?family=Roboto:100,700;);
    .snip1585 {
    background-color: rgb(41, 46, 57);
    color: #fff;
    display: inline-block;
    font-family: 'Roboto', sans-serif;
    font-size: 24px;
    margin: 10px;
    max-width: 700;
    min-width: 700px;
    overflow: hidden;
    position: relative;
    text-align: center;
    width: 100%;
    }

    .snip1585 * {
    -webkit-box-sizing: border-box;
    box-sizing: border-box;
    -webkit-transition: all 0.45s ease;
    transition: all 0.45s ease;
    }

    .snip1585:before,
    .snip1585:after {
    background-color: rgba(46, 52, 64,  0.5);
    border-top: 50px solid rgba(46, 52, 64, 0.5);
    border-bottom: 50px solid rgba(46, 52, 64, 0.5);
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    content: '';
    -webkit-transition: all 0.3s ease;
    transition: all 0.3s ease;
    z-index: 1;
    opacity: 0;
    }
    h1 {
    text-align: center;
    font-family: Verdana;
    font-size: 10;
    font-weight: 400;
    letter-spacing: 1px;
    margin: 0;
    }
    .snip1585:before {
    -webkit-transform: scaleY(2);
    transform: scaleY(2);
    }

    .snip1585:after {
    -webkit-transform: scaleY(2);
    transform: scaleY(2);
    }

    .snip1585 img {
    vertical-align: top;
    max-width: 100%;
    backface-visibility: hidden;
    }

    .snip1585 figcaption {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    align-items: center;
    z-index: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    line-height: 1.1em;
    opacity: 0;
    z-index: 2;
    -webkit-transition-delay: 0s;
    transition-delay: 0s;
    }
    @import url(https://fonts.googleapis.com/css?family=Raleway:400);
.snip1479 {
  font-family: 'Raleway', Arial, sans-serif;
  border: none;
  background-color: #5666a5;
  border-radius: 5px;
  color: #ffffff;
  cursor: pointer;
  padding: 0px 30px;
  display: inline-block;
  margin: 15px 30px;
  text-transform: uppercase;
  line-height: 46px;
  font-weight: 400;
  font-size: 1em;
  outline: none;
  position: relative;
  overflow: hidden;
  font-size: 16px;
  border-radius: 23px;
  letter-spacing: 2px;
  -webkit-transform: translateZ(0);
  -webkit-transition: all 0.35s ease;
  transition: all 0.35s ease;
  -webkit-box-sizing: border-box;
  box-sizing: border-box;
}
    .snip1479:after {
  position: absolute;
  top: 0px;
  bottom: 0px;
  left: 0px;
  right: 0px;
  border: 5px solid #5666a5;
  content: '';
  border-radius: inherit;
}
.snip1479:hover,
.snip1479.hover {
  background-color: #5666a5;
  color: #ffffff;
}
.snip1479:hover:before,
.snip1479.hover:before {
  -webkit-transform: translateY(0%);
  transform: translateY(0%);
  opacity: 0.25;
}
    .snip1479:before {
  opacity: 0;
  content: "";
  position: absolute;
  top: 0px;
  bottom: 0px;
  left: 0px;
  right: 0px;
  border-radius: inherit;
  background-color: #ffffff;
  -webkit-transition: all 0.3s;
  transition: all 0.3s;
  -webkit-transform: translateY(-100%);
  transform: translateY(-100%);
}
    .snip1585 h3 {
    font-size: 1em;
    font-weight: 400;
    letter-spacing: 1px;
    margin: 0;
    text-transform: uppercase;
    }

    .snip1585 h3 span {
    display: block;
    font-weight: 700;
    }

    .snip1585 a {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 3;
    }

    .snip1585:hover > img,
    .snip1585.hover > img {
    opacity: 0.7;
    }

    .snip1585:hover:before,
    .snip1585.hover:before,
    .snip1585:hover:after,
    .snip1585.hover:after {
    -webkit-transform: scale(1);
    transform: scale(1);
    opacity: 1;
    }

    .snip1585:hover figcaption,
    .snip1585.hover figcaption {
    opacity: 1;
    -webkit-transition-delay: 0.1s;
    transition-delay: 0.1s;
    }
    </style>
</figure>
    <figure class="snip1585">
  <img src="https://divemagazine.com/wp-content/uploads/fishial_id_shot_2.jpg" alt="sample70" onclick="attempt_nav_page('Scan', 0, 3)" />
  <figcaption>
    <div id="h3" onClick="attempt_nav_page('Scan', 0, 3)"> <h3>Image <span>Recognition</span></h3> </div>
  </figcaption>
</figure>

<figure class="snip1585"><img src="https://profishingrigs.com/wp-content/uploads/2021/09/fishingspots1.png" />
  <figcaption>
  <div id="h3" onClick="attempt_nav_page('Location', 0, 3)"> <h3>Location <span>Scouting</span></h3> </div>
  </figcaption>

</figure>
<figure class="snip1585">
  <img src="https://scx2.b-cdn.net/gfx/news/2020/2-newstudyreve.jpg" alt="sample70"/>
  <figcaption>
    <div id="h3" onClick="attempt_nav_page('FishTracking', 0, 3)"> <h3>Fish <span>Tracking</span></h3> </div>
  </figcaption>
</figure>
<figure class="snip1585">
  <img src="https://kinsta.com/wp-content/uploads/2021/11/about-us-page-1200x675.png" alt="sample70" onclick="attempt_nav_page('Scan', 0, 3)" />
  <figcaption>
    <div id="h3" onClick="attempt_nav_page('About', 0, 3)"> <h3>About <span>Us</span></h3> </div>
  </figcaption>
  </figure>
    """,
    height=2100,
)

col1, col2, col3 , col4, col5 = st.columns(5)
with col1:
    pass
with col2:
    pass
with col4:
    pass
with col5:
    pass
with col3 :
    pass






