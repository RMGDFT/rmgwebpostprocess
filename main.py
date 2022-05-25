import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import io
from plot_dos import *
from check_convergence import *
from plot_rho import *
from plot_bandstr import *
from view_xyz import *
st.title('RMG Postprocess User Interface')
st.markdown("Welcome to use rmg package! This interface will help you plot some resutls from RMG")
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: left}<style>',
        unsafe_allow_html=True)


st.sidebar.header("By default, the interface will show example plots. For charge density, density of states, and convergence check, C60 molecule is used. For band structure plot, we use the primitive diamond cell")
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("")

what_to_plot = st.sidebar.radio("what to plot", ['Charge Density', 'DOS', 'Band Structure', 'Check Convergence', 'view xyz'])
if what_to_plot == 'DOS':
    plot_dos()
elif what_to_plot == 'Check Convergence':
    what_to_check = st.sidebar.radio("RMS or Total energy", ['RMS', 'error in Total Energy', 'Total Energy'])
    if what_to_check == 'RMS':
        plot_rms()
    if what_to_check == 'error in Total Energy':
        plot_deltaE()
    if what_to_check == 'Total Energy':
        plot_totE()
elif what_to_plot == "Charge Density":
   # pass
    plot_rho()
elif what_to_plot == "Band Structure":
    plot_band()
elif what_to_plot == "view xyz":
    view_xyz()
