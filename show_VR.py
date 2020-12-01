# -*- coding: utf-8 -*-

import numpy as np
import gudhi
from mayavi import mlab
import sys


def _get_threshold(filename):
    with open(filename, "r") as f:
        low_line = f.readline()
        up_line = f.readline()
        low_line = low_line[ low_line.find("=")+1:].strip()
        up_line = up_line[ up_line.find("=")+1:].strip()        
        return (float(low_line), float(up_line))
        
def show(count):
    mlab.clf()
    directory = "VR/%02d/" % count
    points = np.loadtxt(directory + "points.csv", delimiter=",")
    (low, up) = _get_threshold(directory+"threshold.txt")
    rc = gudhi.RipsComplex(points, max_edge_length=(low+up)/2)
    st = rc.create_simplex_tree(max_dimension=2)
    triangles = [s[0] for s in st.get_skeleton(2) if len(s[0])== 3]
    edges = []
    for s in st.get_skeleton(1):
        e = s[0]
        if len(e) == 2:
            edges.append(points[[e[0], e[1]]])
                                
    mlab.triangular_mesh(points[:, 0], points[:, 1], points[:, 2], triangles)
    for e in edges:
        mlab.plot3d(e[:, 0], e[:, 1], e[:, 2], tube_radius=None)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : python show_VR.py ${num}")
        sys.exit(1)
    cnt = int(sys.argv[1])
    show(cnt)
