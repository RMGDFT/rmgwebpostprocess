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

    atom_zpos = []
    bohr = 0.529177
    for i in range(num_atoms):
        atom_zpos.append(float(rho_data_lines[i+4].split()[4]) * bohr)
    

    vec = np.ndarray([3,3], dtype = float)
    for i in range(3):
        for j in range(3):
            vec[i][j] = float(rho_data_lines[1+i].split()[j+1]) * bohr

    if abs(vec[0][1]) > 1.0e-5 or abs(vec[0][2]) > 1.0e-5:
        print(vec[0][1], vec[0][2])
        st.markdown("the first vector need to be along x axis")
        return

    zmax = float(max(atom_zpos))
    zmin = float(min(atom_zpos))
    z_length = vec[2][2] * nz

    z_vacuum = z_length -(zmax - zmin)
    z_stm_b = float(zmax + 2.0)
    z_stm_t = float(zmax + 0.5 * z_vacuum)
    z_stm_ave = (z_stm_b + z_stm_t) * 0.5
    vol_data = ''.join(rho_data_lines[num_atoms+4:]).split()
    rho_1d = np.array(vol_data)

    rho_3d = rho_1d.reshape(nx,ny,nz*real_or_complex)


    STM_mode = st.sidebar.radio("STM mode", ["constant height", "constant current"])

    if STM_mode == "constant height":
        z_height = st.sidebar.slider("choose the xy plane with z height", z_stm_b, z_stm_t, z_stm_b)
        z_plane = int(z_height/vec[2][2])
    rho_xy = rho_3d[:,:, z_plane]

     
    cs, col1, col2,col3 = st.columns([0.1, 1,1,1])
    xcells = col1.number_input("expand in x", 1)
    ycells = col2.number_input("expand in y", 1)
    spline_type = col3.checkbox("spline interpolation for image", False)
    X = np.ndarray([ny *ycells,nx *xcells], dtype = float)
    Y = np.ndarray([ny *ycells,nx *xcells], dtype = float)
    rho_ext = np.ndarray([ny *ycells,nx *xcells], dtype = float)
    a_length = vec[0][0] * nx
    for j in range(ny * ycells):
        for i in range(nx * xcells):
            X[j][i] = i * vec[0][0] + j * vec[1][0]
            Y[j][i] = i * vec[0][1] + j * vec[1][1]
            rho_ext[j][i] = rho_xy[i%nx][j%ny]

    xmin = X.min()
    xmax = X.max()
    ymin = Y.min()
    ymax = Y.max()
    
    fig, ax = plt.subplots(figsize=(15,15))
    
    if abs(vec[1][0]) >1.0e-5:
        ax.pcolormesh(X,Y, rho_ext)
    else:
        if spline_type:
            ax.imshow(rho_ext, interpolation="spline16")
        else:
            ax.imshow(rho_ext)
    #ax.set_aspect((ymax-ymin)/(xmax-xmin))
    ax.set_aspect("equal")
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

