import streamlit as st
import numpy as np
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import io
def plot_stm():

    upload_file = st.sidebar.file_uploader("Upload a .cube format file to  plot", type='cube')
    if upload_file:
        rho_data = upload_file.read().decode('utf-8')
        rho_data_lines = rho_data.split("\n")
        for i in range(len(rho_data_lines)):
            rho_data_lines[i] = rho_data_lines[i].decode('utf-8')
    else:
        with open("graphene/STM_bias_1.00_spin0.cube", "r") as f:
            rho_data = f.read()
            rho_data_lines = rho_data.split("\n")

    rho_data_lines = [s for s in rho_data_lines if '#' not in s]
    num_atoms = int(rho_data_lines[0].split()[0])
    real_or_complex = int(rho_data_lines[0].split()[4])
    if real_or_complex == 2:
        st.markdown("STM data cannot be complex, check the .cube file")
        return
    nx = int(rho_data_lines[1].split()[0])
    ny = int(rho_data_lines[2].split()[0])
    nz = int(rho_data_lines[3].split()[0])
    
    vec = np.ndarray([3,3], dtype = float)
    for i in range(3):
        for j in range(3):
            vec[i][j] = float(rho_data_lines[1+i].split()[j+1])

    if abs(vec[0][1]) > 1.0e-5 or abs(vec[0][2]) > 1.0e-5:
        print(vec[0][1], vec[0][2])
        st.markdown("the first vector need to be along x axis")
        return

    vol_data_start_line = num_atoms + 4
    num_lines_per_z = (nz*real_or_complex)//6 +1

    rho_3d = np.ndarray([nx,ny,nz*real_or_complex], dtype = float)
    for ix in range(nx):
        for iy in range(ny):
            line_index = (ix * ny + iy) * num_lines_per_z + vol_data_start_line
            z_count = 0
            for iz_line in range(line_index, line_index+num_lines_per_z):
                if z_count == nz * real_or_complex:
                    break
                tem_str = rho_data_lines[iz_line].split()
                for s in tem_str:
                    rho_3d[ix][iy][z_count] = float(s)
                    z_count += 1

    rho_1d = rho_3d.reshape(nx*ny*nz)


    STM_mode = st.sidebar.radio("STM mode", ["constant height", "constant current"])

    if STM_mode == "constant height":
        z_height = st.sidebar.slider("choose the xy plane with z height", 0, nz, nz//2)
    rho_xy = rho_3d[:,:, z_height]

     
    cs, col1, col2 = st.columns([0.1, 1,1])
    xcells = col1.number_input("expand in x", 1)
    ycells = col2.number_input("expand in y", 1)
    X = np.ndarray([nx *xcells,ny *ycells], dtype = float)
    Y = np.ndarray([nx *xcells,ny *ycells], dtype = float)
    rho_ext = np.ndarray([nx *xcells,ny *ycells], dtype = float)
    a_length = vec[0][0] * nx
    for i in range(nx * xcells):
        for j in range(ny * ycells):
            X[i][j] = i * vec[0][0] + j * vec[1][0]
            #if X[i][j] > a_length - 1.0e-10:
            #    X[i][j] -= a_length
            #if X[i][j] < 1.0e-10:
            #    X[i][j] += a_length
            Y[i][j] = i * vec[0][1] + j * vec[1][1]
            rho_ext[i][j] = rho_xy[i%nx][j%ny]

    xmin = X.min()
    xmax = X.max()
    ymin = Y.min()
    ymax = Y.max()
    
    fig, ax = plt.subplots(figsize=(15,15))
    ax.pcolormesh(X,Y, rho_ext)
    ax.set_aspect((ymax-ymin)/(xmax-xmin))
    #ax.contour(X,Y, rho_xy)
    #ax.tripcolor(X,Y, rho_xy)
    #ax.image(rho_xy)

    fn = 'stm.png'
    img = io.BytesIO()
    plt.tight_layout()
    quality_dpi = st.sidebar.number_input("dpi of image to be saved", 600)    
    plt.savefig(img, format='png', dpi =quality_dpi)
    btn = st.sidebar.download_button(
       label="Download image",
       data=img,
       file_name=fn,
       mime="image/png"
    )

    st.pyplot(fig)

