import streamlit as st
import pandas as pd
import numpy as np
import os
st.title('RMG Postprocess User Interface')
st.markdown("Welcome to use rmg package! This interface will help you plot some resutls from RMG")
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: left}<style>',
        unsafe_allow_html=True)

st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("")

uploaded_file = st.sidebar.file_uploader("Choose a file to plot")
