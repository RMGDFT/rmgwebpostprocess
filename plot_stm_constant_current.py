#!/usr/bin/python3

import sys

import math
import numpy as np
import matplotlib.pyplot as plt
import os
import io

if len(sys.argv) > 1:
    with open(sys.argv[1], "r") as f:
        rho_data = f.read()
        rho_data_lines = rho_data.split("\n")
else:
    print("need the stm cube file")  
    exit(0)


rho_iso = 1.0e-4
xcells = 1
ycells = 1

rho_data_lines = [s for s in rho_data_lines if '#' not in s]
num_atoms = int(rho_data_lines[0].split()[0])
real_or_complex = int(rho_data_lines[0].split()[4])
if real_or_complex == 2:
    print("STM data cannot be complex, check the .cube file")
    exit(0)
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
    print("the first vector need to be along x axis")
    exit(0)

zmax = float(max(atom_zpos))
zmin = float(min(atom_zpos))
z_length = vec[2][2] * nz

z_vacuum = z_length -(zmax - zmin)
z_stm_b = float(zmax + 2.0)
z_stm_t = float(zmax + 0.5 * z_vacuum)
iz_start = int(zmax/vec[2][2])
iz_end = int( (z_stm_t)/vec[2][2])
z_stm_ave = (z_stm_b + z_stm_t) * 0.5
vol_data = ''.join(rho_data_lines[num_atoms+4:]).split()
rho_1d = np.array(vol_data, dtype= float)

rho_3d = rho_1d.reshape(nx,ny,nz*real_or_complex)
rho_xy = np.ndarray([nx,ny], dtype = float)


#STM_mode = st.sidebar.radio("STM mode", ["constant current", "constant height"])
STM_mode = "constant current"

if STM_mode == "constant height":
    z_height = st.sidebar.slider("choose the xy plane with z height", z_stm_b, z_stm_t, z_stm_b)
    z_plane = int(z_height/vec[2][2])

    rho_xy = rho_3d[:,:, z_plane]
else:
    rho_iso_min = float(max(rho_3d[:,:, iz_end].reshape(nx*ny)))
    print("rho_isosurface maximum", rho_iso_min)
    print("isosurface: ", rho_iso)
    #print(rho_iso, iz_end)
    for ix in range(nx):
        for iy in range(ny):
           for iz in range(iz_end, 0, -1):
               if float(rho_3d[ix, iy, iz]) > rho_iso:
                  iz_tem = iz
                  break
           height = float(iz_tem) + (rho_3d[ix,iy, iz_tem] - rho_iso)/(rho_3d[ix,iy,iz_tem] - rho_3d[ix,iy,iz_tem+1])       
           rho_xy[ix][iy] = height * vec[2][2]
           #print(ix,iy,iz_tem, rho_xy[ix][iy], rho_3d[ix,iy,iz_tem], rho_3d[ix,iy,iz_tem+1])

 
#color_map = st.sidebar.radio("color map", ["hot", "inferno", "Greys_r"])
color_map = "hot"

#spline_type = col3.checkbox("spline interpolation for image", False)
X = np.ndarray([nx *xcells, ny *ycells], dtype = float)
Y = np.ndarray([nx *xcells, ny *ycells], dtype = float)
rho_ext = np.ndarray([nx *xcells,ny *ycells], dtype = float)
a_length = vec[0][0] * nx
for j in range(ny * ycells):
    for i in range(nx * xcells):
        X[i][j] = i * vec[0][0] + j * vec[1][0]
        Y[i][j] = i * vec[0][1] + j * vec[1][1]
        rho_ext[i][j] = float(rho_xy[i%nx][j%ny])

fig, ax = plt.subplots(figsize=(15,15))

    #pos = ax.imshow(rho_ext, cmap =color_map, x_ax = X, y_ax = Y)
pos = ax.pcolormesh(X, Y, rho_ext, cmap =color_map)
#ax.set_aspect((ymax-ymin)/(xmax-xmin))
ax.set_aspect("equal")
ax.set_xlabel('X($\mathrm{\AA}$)')
ax.set_ylabel('Y($\mathrm{\AA}$)')

cax = fig.add_axes([ax.get_position().x1+0.01,ax.get_position().y0,0.02,ax.get_position().height])

plt.colorbar(pos, cax=cax)


fn=sys.argv[1].replace('cube', 'png')
plt.savefig(fn, format='png', dpi =600)

