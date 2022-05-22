import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import io
def plot_dos():

    file_op = st.sidebar.radio("use an example or upload a file by yourself", ["upload a .dat file", "C60 example"])
    data =""
    if file_op == "C60 example":
        with open("C60/dos_tot_spin0.dat", "r") as f:
            data = f.readlines()
    else:
        upload_file = st.sidebar.file_uploader("Upload dos_tot_spin*.dat to  plot", type='dat')
        if upload_file:
            data = upload_file.readlines()
    #print(data)
        
    if data:    
        x = []
        y = []
        for line in data:
            x.append(float(line.split()[0]))
            y.append(float(line.split()[1]))

        x_max = max(x)
        x_min = min(x)
        y_max = max(y)
        y_min = min(y)
        x_range = st.sidebar.slider("Select x range", x_min, x_max, (x_min, x_max))
        y_range = st.sidebar.slider("Select y range", y_min, y_max, (y_min, y_max))

        #plt.style.use('_mpl-gallery-nogrid')
        fig, ax = plt.subplots()
        ax.plot(x,y,linewidth=2.0, color="red")
        ax.set_xlim(x_range[0], x_range[1])
        ax.set_ylim(y_range[0], y_range[1])
        plt.title("Electronic Density of States", fontsize=20)
        #plt.get_frame().set_linewidth(1.0)
        ax.set_xlabel('E (eV)', fontsize=20)
        ax.set_ylabel('Density of States', fontsize=20)
        ax.tick_params(direction='in', length=6, width=2, colors='black')

        ax.tick_params(axis='x', labelsize=20)
        ax.tick_params(axis='y', labelsize=20)

        fn = 'tot_dos.png'
        img = io.BytesIO()
        plt.tight_layout()
        plt.figure(dpi=600)
        for axis in ['top','bottom','left','right']:
            ax.spines[axis].set_linewidth(2.0)
        quality_dpi = st.sidebar.number_input("dpi of image to be saved", 600)    
        plt.savefig(img, format='png', dpi =quality_dpi)

        btn = st.sidebar.download_button(
           label="Download image",
           data=img,
           file_name=fn,
           mime="image/png"
        )

        st.pyplot(fig)
