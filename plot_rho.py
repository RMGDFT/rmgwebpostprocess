import streamlit as st
import py3Dmol
from stmol import showmol
def plot_rho():

    upload_file = st.sidebar.file_uploader("Upload a .cube format file to  plot", type='cube')
    if upload_file:
        rho_data = upload_file.read().decode('utf-8')
        rho_data_lines = upload_file.readlines()
        for i in range(len(rho_data_lines)):
            rho_data_lines[i] = rho_data_lines[i].decode('utf-8')
    else:
        with open("C60/density.cube", "r") as f:
            rho_data = f.read()
            rho_data_lines = f.readlines()

    spin = st.sidebar.checkbox('Spin', value = False)
    iso_color = st.sidebar.radio("isosurface color", ['yellow', 'blue', 'red','gold'])
    isosurface_value = st.sidebar.slider("isosurface value", 0.0, 0.2, 0.1)
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
