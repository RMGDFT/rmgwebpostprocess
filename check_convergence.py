import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import io
def plot_totE():

    upload_file = st.sidebar.file_uploader("Upload a log file to check convergence", type='log')

    if upload_file:
        data = upload_file.readlines()
        for i in range(len(data)):
            data[i] = data[i].decode('utf-8')
    else: 
        with open("C60/C60.rmg.00.log", "r") as f:
            data = f.readlines()
    #print(data)
        
    y = []
    for line in data:
        if '@@ TOTAL E' in line:
            tem = line.split()
            if 'Ha' in tem[len(tem)-1]:
                y.append(float(tem[len(tem) -2]))
    
    x = list(np.arange(0, len(y)))

    x_max = int(max(x))
    x_min = 0
    y_max = max(y)
    y_min = min(y)
    x_range = st.sidebar.slider("Select x range", x_min, x_max, (x_min, x_max))
    y_range = st.sidebar.slider("Select y range", y_min, y_max, (y_min, y_max))

    fig, ax = plt.subplots()
    ax.plot(x,y,linewidth=2.0, color="red", marker='o')
    ax.set_xlim(x_range[0], x_range[1])
    ax.set_ylim(y_range[0], y_range[1])
    plt.title("Total Energy vs SCF steps", fontsize=20)

    ax.set_xlabel('SCF step', fontsize=20)
    ax.set_ylabel('Total Energy (Hatree)', fontsize=20)
    ax.tick_params(direction='in', length=6, width=2, colors='black')
    ax.tick_params(which='minor', direction='in')

    ax.tick_params(axis='x', labelsize=20)
    ax.tick_params(axis='y', labelsize=20)

    fn = 'totE.svg'
    img = io.BytesIO()
    plt.tight_layout()
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2.0)
    quality_dpi = st.sidebar.number_input("dpi of image to be saved", 600)
    plt.savefig(img, format='svg', dpi =quality_dpi)

    btn = st.sidebar.download_button(
       label="Download image",
       data=img,
       file_name=fn,
       mime="image/svg"
    )

    st.pyplot(fig)

def plot_deltaE():

    upload_file = st.sidebar.file_uploader("Upload a log file to check convergence", type='log')

    if upload_file:
        data = upload_file.readlines()
        for i in range(len(data)):
            data[i] = data[i].decode('utf-8')
    else:
        with open("C60/C60.rmg.00.log", "r") as f:
            data = f.readlines()
    #print(data)
        

    y = []
    for line in data:
        if 'error' in line:
            tem = line.split()
            if 'Ha' in tem[len(tem)-1]:
                y.append(float(tem[len(tem) -2]))
    
    x = list(np.arange(1, len(y)+1))

    x_max = int(max(x))
    x_min = 0
    y_max = max(y)
    y_min = min(y)
    x_range = st.sidebar.slider("Select x range", x_min, x_max, (x_min, x_max))
    y_range = st.sidebar.slider("Select y range", y_min, y_max, (y_min, y_max))

    #plt.style.use('_mpl-gallery-nogrid')
    fig, ax = plt.subplots()
    ax.plot(x,y,linewidth=2.0, color="red", marker='o')
    ax.set_xlim(x_range[0], x_range[1])
    ax.set_ylim(y_range[0], y_range[1])
    plt.title("Error in Total Energy", fontsize=20)
    #plt.get_frame().set_linewidth(1.0)
    ax.set_xlabel('SCF step', fontsize=20)
    ax.set_ylabel('$\Delta$E (Hatree)', fontsize=20)
    ax.tick_params(direction='in', length=6, width=2, colors='black')
    ax.tick_params(which='minor', direction='in')

    ax.tick_params(axis='x', labelsize=20)
    ax.tick_params(axis='y', labelsize=20)

    fn = 'deltaE.svg'
    img = io.BytesIO()
    plt.tight_layout()
    plt.yscale("log")
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2.0)
    quality_dpi = st.sidebar.number_input("dpi of image to be saved", 600)
    plt.savefig(img, format='svg', dpi =quality_dpi)

    btn = st.sidebar.download_button(
       label="Download image",
       data=img,
       file_name=fn,
       mime="image/svg"
    )

    st.pyplot(fig)
def plot_rms():

    upload_file = st.sidebar.file_uploader("Upload a log file to check convergence", type='log')

    if upload_file:
        data = upload_file.readlines()
        for i in range(len(data)):
            data[i] = data[i].decode('utf-8')

    else:
        with open("C60/C60.rmg.00.log", "r") as f:
            data = f.readlines()
    #print(data)
        
    y = []
    for line in data:
        if 'RMS' in line:
            tem = line.split()
            y.append(float(tem[len(tem) -2]))
    x = list(np.arange(0, len(y)))

    x_max = int(max(x))
    x_min = int(min(x))
    y_max = max(y)
    y_min = min(y)
    x_range = st.sidebar.slider("Select x range", x_min, x_max, (x_min, x_max))
    y_range = st.sidebar.slider("Select y range", y_min, y_max, (y_min, y_max))

    #plt.style.use('_mpl-gallery-nogrid')
    fig, ax = plt.subplots()
    ax.plot(x,y,linewidth=2.0, color="red", marker='o')
    ax.set_xlim(x_range[0], x_range[1])
    ax.set_ylim(y_range[0], y_range[1])
    plt.title("RMS of total potential", fontsize=20)
    #plt.get_frame().set_linewidth(1.0)
    ax.set_xlabel('SCF step', fontsize=20)
    ax.set_ylabel('RMS[dV]', fontsize=20)
    ax.tick_params(direction='in', length=6, width=2, colors='black')
    ax.tick_params(which='minor', direction='in')

    ax.tick_params(axis='x', labelsize=20)
    ax.tick_params(axis='y', labelsize=20)

    fn = 'rms.svg'
    img = io.BytesIO()
    plt.tight_layout()
    plt.yscale("log")
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2.0)
    quality_dpi = st.sidebar.number_input("dpi of image to be saved", 600)
    plt.savefig(img, format='svg', dpi =quality_dpi)

    btn = st.sidebar.download_button(
       label="Download image",
       data=img,
       file_name=fn,
       mime="image/svg"
    )

    st.pyplot(fig)
