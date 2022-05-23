import streamlit as st
import py3Dmol
from stmol import showmol
def plot_rho():

    file_op = st.sidebar.radio("use example or upload a cube file", ["C60 example","upload a .cube file"])
    rho_data =""
    rho_data_lines =""
    if file_op == "C60 example":
        with open("C60/density.cube", "r") as f:
            rho_data = f.read()
            rho_data_lines = f.readlines()
    else:
        upload_file = st.sidebar.file_uploader("Upload cube format file to  plot", type='cube')
        if upload_file:
            rho_data = upload_file.read().decode('utf-8')
            rho_data_lines = upload_file.readlines()

    if rho_data:
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
