# -*- coding: utf-8 -*-

import numpy as np
import gudhi
from mayavi import mlab

def _get_threshold(filename):
    with open(filename, "r") as f:
        low_line = f.readline()
        up_line = f.readline()
        low_line = low_line[ low_line.find("=")+1:].strip()
        up_line = up_line[ up_line.find("=")+1:].strip()        
        return (float(low_line), float(up_line))


def show(count):
    mlab.clf()
    directory = "Cech/%02d/" % count
    points = np.loadtxt(directory + "points.csv", delimiter=",")
    (low, up) = _get_threshold(directory+"threshold.txt")
    ac = gudhi.AlphaComplex(points)
    st = ac.create_simplex_tree(max_alpha_square = (low*low+up*up)/2)
    [iA, iB, iC, iD, iX] = list(range(5))
    triangles = []
    triangles.append([iA, iB, iX]) # ABX
    triangles.append([iA, iC, iX]) # ACX
    triangles.append([iB, iD, iX]) # BDX
    triangles.append([iC, iD, iX]) # CDX
    # triangles = [s[0] for s in st.get_skeleton(2) if len(s[0])== 3]
    # print([s[0] for s in st.get_skeleton(2)])
    # edges = []
    # for s in st.get_skeleton(1):
    #     e = s[0]
    #     if len(e) == 2:
    #         edges.append(points[[e[0], e[1]]])

    edges = []
    edges.append(points[[iA, iB]]) # AB
    edges.append(points[[iB, iC]]) # BC
    edges.append(points[[iC, iA]]) # CA
    edges.append(points[[iA, iX]]) # AX
    edges.append(points[[iX, iD]]) # XD
    edges.append(points[[iD, iC]]) # DC
    edges.append(points[[iC, iX]]) # CX
    edges.append(points[[iX, iB]]) # XB
    edges.append(points[[iB, iD]]) # BD
    
    mlab.triangular_mesh(points[:, 0], points[:, 1], points[:, 2], triangles)
    for e in edges:
        mlab.plot3d(e[:, 0], e[:, 1], e[:, 2], tube_radius=None)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : python show_Cech.py ${num}")
        sys.exit(1)
    cnt = int(sys.argv[1])
    show(cnt)

