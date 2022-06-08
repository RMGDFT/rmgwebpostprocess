import streamlit as st
import py3Dmol
import numpy as np
from stmol import showmol
def plot_rho():

    upload_file = st.sidebar.file_uploader("Upload a .cube format file to  plot", type='cube')
    if upload_file:
        rho_data = upload_file.read().decode('utf-8')
        rho_data_lines = rho_data.split("\n")
        #for i in range(len(rho_data_lines)):
        #    rho_data_lines[i] = rho_data_lines[i].decode('utf-8')
    else:
        with open("C60/density.cube", "r") as f:
            rho_data = f.read()
            rho_data_lines = rho_data.split("\n")


    num_atoms = int(rho_data_lines[2].split()[0])
    real_or_complex = int(rho_data_lines[2].split()[4])
    nx = int(rho_data_lines[3].split()[0])
    ny = int(rho_data_lines[4].split()[0])
    nz = int(rho_data_lines[5].split()[0])
    vol_data_start_line = num_atoms + 6
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

    rho_1d = rho_3d.reshape(nx*ny*nz, real_or_complex)
    rho_max = np.max(rho_1d, axis=0)
    rho_min = np.min(rho_1d, axis=0)
    rho_ave = 0.5 * (float(rho_max[0]) + float(rho_min[0]))

    spin = st.sidebar.checkbox('Spin', value = False)
    iso_color = st.sidebar.radio("isosurface color", ['yellow', 'blue', 'red','gold'])
    isosurface_value = st.sidebar.slider("isosurface value", float(rho_min[0]), float(rho_max[0]), rho_ave)
    #rho_view.setBackgroundColor(bcolor)

    rho_view = py3Dmol.view()
    rho_view.addVolumetricData(rho_data, "cube", {'isoval': isosurface_value, 'color': iso_color, 'opacity': 0.85})
    rho_view.addModel(rho_data, "cube", 'mol')
                      

    #rho_view.setStyle({'stick':{}})
    #rho_view.setStyle({'sphere':{radius~0.2}})
    scale = 0.18
    radius = 0.05
    rho_view.setStyle({'sphere':{'colorscheme':'Jmol','scale':scale},
                       'stick':{'colorscheme':'Jmol', 'radius':radius}})
    rho_view.zoomTo()
    if spin:
        rho_view.spin(True)
    else:
        rho_view.spin(False)
    rho_view.render()
    rho_view.zoomTo()
    showmol(rho_view,height=500,width=800)
