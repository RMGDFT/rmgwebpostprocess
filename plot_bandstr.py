import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import io
def plot_band():

    upload_file = st.sidebar.file_uploader("", type='xmgr')
    if upload_file:
        data = upload_file.readlines()
        for i in range(len(data)):
            data[i] = data[i].decode('utf-8')
    else:
        with open("diamond_prim/diamond2_band.rmg.00_spin0.bandstructure.xmgr", "r") as f:
            data = f.readlines()
    #print(data)
        
    x = []
    y = []
    #  get xtick and lables for special k points 
    x_tick_pos = []
    x_tick_sym = []
    for line in data:
        if "xaxis  tick major" in line:
            tem_str = line.split()
            x_tick_pos.append(float(tem_str[len(tem_str) -1]))
        if "xaxis  ticklabel" in line:
            tem_str = line.split('"')
            if len(tem_str) > 1:
                x_tick_sym.append(tem_str[1])
        if "yaxis" in line: break

    for i in range(len(x_tick_sym)):
        if x_tick_sym[i] == 'G':
            x_tick_sym[i] = '$\Gamma$'
    header_lines = True
    x1 =[]
    y1 =[]
    for line in data: 
        tem_str = line.split()    
        if "target" in line:
            if not header_lines: 
                x.append(x1)
                y.append(y1)
            header_lines = False
            x1 =[]
            y1 =[]
        elif "type xy" in line: 
            continue
        elif not header_lines and len(tem_str) == 2:
            x1.append(float(tem_str[0]))
            y1.append(float(tem_str[1]))
        else:
            pass
            
    x.append(x1)
    y.append(y1)

    x_max = -1000.0
    x_min = 1000.0
    y_max = -1000.0
    y_min = 1000.0
    for i in range(len(x)):
        x_max = max(x_max, max(x[i]))
        x_min = min(x_min, min(x[i]))
        y_max = max(y_max, max(y[i]))
        y_min = min(y_min, min(y[i]))


    x_range = st.sidebar.slider("Select x range", x_min, x_max, (x_min, x_max))
    y_range = st.sidebar.slider("Select y range", y_min, y_max, (y_min, y_max))

    #plt.style.use('_mpl-gallery-nogrid')
    fig, ax = plt.subplots()
    for i in range(len(x)):
        ax.plot(x[i],y[i],linewidth=2.0, color="black")
    ax.set_xlim(x_range[0], x_range[1])
    ax.set_ylim(y_range[0], y_range[1])
    plt.title("Electronic Band Structure", fontsize=20)
    #plt.get_frame().set_linewidth(1.0)
    #ax.set_xlabel('E (eV)', fontsize=20)
    ax.set_xticks(x_tick_pos, x_tick_sym, fontsize=20)

    for x0 in x_tick_pos:
        ax.plot([x0,x0],y_range, linewidth=1, color="black")
    ax.set_ylabel('E (eV)', fontsize=20)
    ax.tick_params(axis='y', direction='in', length=6, width=2, colors='black')
    ax.tick_params(axis='x', direction='in', length=6, width=1, colors='black')

    ax.tick_params(axis='x', labelsize=20)
    ax.tick_params(axis='y', labelsize=20)

    fn = 'bandstructure.png'
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
