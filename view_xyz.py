import streamlit as st
import py3Dmol
import numpy as np
from stmol import showmol
def view_xyz():

    upload_file = st.sidebar.file_uploader("Upload a .xyz format file to  view the atomic structure", type='xyz')
    if upload_file:
        xyz_data = upload_file.read().decode('utf-8')
    else:
        with open("C60/C60.xyz", "r") as f:
            xyz_data = f.read()

    spin = st.sidebar.checkbox('Spin', value = False)

    xyz_view = py3Dmol.view()
    xyz_view.addModel(xyz_data, "xyz")
                      
    scale = 0.18
    radius = 0.05
    xyz_view.setStyle({'sphere':{'colorscheme':'Jmol','scale':scale},
                       'stick':{'colorscheme':'Jmol', 'radius':radius}})
    xyz_view.zoomTo()
    if spin:
        xyz_view.spin(True)
    else:
        xyz_view.spin(False)
    xyz_view.render()
    showmol(xyz_view,height=500,width=800)
