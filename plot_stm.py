import streamlit as st
import numpy as np
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import io
def plot_stm():

    upload_file = st.sidebar.file_uploader("Upload a .stm format file to  plot", type='stm')
    if upload_file:
        rho_data = upload_file.read().decode('utf-8')
        rho_data_lines = rho_data.split("\n")
    else:
        with open("STM/STM_bias_1.00_spin0_ConsCurrent.stm", "r") as f:
            rho_data = f.read()
            rho_data_lines = rho_data.split("\n")

    rho_data_lines = [s for s in rho_data_lines if '#' not in s]
    nx = int(rho_data_lines[0].split()[0])
    ny = int(rho_data_lines[1].split()[0])

    vec = np.ndarray([2,2], dtype = float)
    for i in range(2):
        for j in range(2):
            vec[i][j] = float(rho_data_lines[i].split()[j+1]) 

    if abs(vec[0][1]) > 1.0e-5 :
        st.markdown("the first vector need to be along x axis, check the .stm file")
        return
    if abs(vec[1][0]) > 1.0e-5 :
        st.markdown("only rectangle shape for xy plane is supported now, check vectors in the .stm file")
        return

    vol_data = ''.join(rho_data_lines[2:]).split()
    rho_1d = np.array(vol_data)


    rho_xy = rho_1d.reshape(nx,ny)

    color_map = st.sidebar.radio("color map", ["hot", "inferno", "plasma"])

    cs, col1, col2,col3 = st.columns([0.1, 1,1,1])
    xcells = col1.number_input("expand in x", 1)
    ycells = col2.number_input("expand in y", 1)
    #spline_type = col3.checkbox("spline interpolation for image", False)
    X = np.ndarray([nx *xcells, ny *ycells], dtype = float)
    Y = np.ndarray([nx *xcells, ny *ycells], dtype = float)
    rho_ext = np.ndarray([nx *xcells,ny *ycells], dtype = float)
    a_length = vec[0][0] * nx
    for j in range(ny * ycells):
        for i in range(nx * xcells):
            X[i][j] = i * vec[0][0] + j * vec[1][0]
            Y[i][j] = i * vec[1][0] + j * vec[1][1]
            rho_ext[i][j] = float(rho_xy[i%nx][j%ny])

    fig, ax = plt.subplots(figsize=(15,15))
    
        #pos = ax.imshow(rho_ext, cmap =color_map, x_ax = X, y_ax = Y)
    pos = ax.pcolormesh(X, Y, rho_ext, cmap =color_map)
    #ax.set_aspect((ymax-ymin)/(xmax-xmin))
    ax.set_aspect("equal")
    ax.set_xlabel('X($\mathrm{\AA}$)')
    ax.set_ylabel('Y($\mathrm{\AA}$)')

    cax = fig.add_axes([ax.get_position().x1+0.01,ax.get_position().y0,0.02,ax.get_position().height])

#    plt.colorbar(pos, cax=cax)


    fn = 'stm.png'
    img = io.BytesIO()
    #plt.tight_layout()
    quality_dpi = st.sidebar.number_input("dpi of image to be saved", 600)    
    plt.savefig(img, format='png', dpi =quality_dpi)
    btn = st.sidebar.download_button(
       label="Download image",
       data=img,
       file_name=fn,
       mime="image/png"
    )

    st.pyplot(fig)

