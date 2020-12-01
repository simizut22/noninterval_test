# -*- coding:utf-8 -*-



#            B
#         ↗ | ↘
#       ↗   |   ↘
#     ↗     |     ↘
#   ↗       |       ↘
# A          |         D
#   ↘       |       ↗
#     ↘     |     ↗
#       ↘   |   ↗
#         ↘ | ↗
#            C 
# に 1 点 X を追加 


# face の状況
# XAB が face を張る -> XAB の外接円の半径 ≦ t
# XAC が face を張る -> XAC の外接円の半径 ≦ t
# XBD が face を張る -> XBD の外接円の半径 ≦ t
# XCD が face を張る -> XCD の外接円の半径 ≦ t
# 辺の接続状況
# |XB|, |XC|, |BC| ≦ 2t 
# <!-- 上の三角形の条件にすでに入っているので以下の辺は不要
# |AB|, |AC| |BD|. |CD|   
# -->
# |AD| > 2t

# ABC が face を張らない -> ABC の外接円の半径 > t
# BCD が face を張らない -> BCD の外接円の半径 > t
# XBC が face を張らない -> XBC の外接円の半径 > t


import numpy as np
from scipy.spatial import distance_matrix
import itertools

_POINT_NUM = 5
[iA, iB, iC, iD, iX] = list(range(_POINT_NUM))


def _get_radius(dist, ix, iy, iz):
    a, b, c = dist[iy, iz], dist[iz, ix], dist[ix, iy]
    a2, b2, c2 = a*a, b*b, c*c
    return a*b*c/np.sqrt(
        2*(a2*b2 + b2*c2 + c2*a2) - (a2*a2 + b2*b2 + c2*c2)
    )


def _get_face_radius_max(dist):
    """XAB, XAC, XBD, XCD の外接円の半径 の最大値を取得"""
    xab = _get_radius(dist, iX, iA, iB)  # XAB
    xac = _get_radius(dist, iX, iA, iC)  # XAC
    xbd = _get_radius(dist, iX, iB, iD)  # XBD
    xcd = _get_radius(dist, iX, iC, iD)  # XCD
    return max(xab, xac, xbd, xcd)

def _get_nonface_radius_min(dist):
    """ABC, BCD, XBC の外接円の半径の最小値を取得"""
    abc = _get_radius(dist, iA, iB, iC)  # ABC
    bcd = _get_radius(dist, iB, iC, iD)  # BCD 
    xbc = _get_radius(dist, iX, iB, iC)  # XBC
    return min(abc, bcd, xbc)

def _get_connect_edge_max(dist):
    """ XB, XC, BC の辺の長さの最大を取得"""
    xb = dist[iX, iB]  # XB
    xc = dist[iX, iC]  # XC
    bc = dist[iB, iC]  # BC
    return max(xb, xc, bc)


def _get_nonconnect_edge_min(dist):
    """AD の長さを取得"""
    return dist[iA, iD]

# def _get_x_minimal_edge(dist):
#     xa = dist[iX, iA]  # XA
#     xb = dist[iX, iB]  # XB
#     xc = dist[iX, iC]  # XC
#     xd = dist[iX, iD]  # XD
#     return min(xa, xb, xc, xd)

# def _get_nonx_max_edge(dist):
#     ab = dist[iA, iB]
#     ac = dist[iA, iC]
#     bc = dist[iB, iC]
#     bd = dist[iB, iD]
#     cd = dist[iC, iD]
#     return max(ab, ac, bc, bd, cd)
    
def _is_noninterval(pts):
    dist = distance_matrix(pts, pts)

    # XAB, XAC, XBD, XCD の外接円の半径 の最大値を取得 (≦ t)
    face_radius_max = _get_face_radius_max(dist)

    # XB, XC, BC の辺の長さの最大値を取得 (≦ 2t)
    connect_edge_max = _get_connect_edge_max(dist)

    t_connect = max(face_radius_max, connect_edge_max/2)

    # ABC, BCD, XBC の外接円の半径の最小値を取得 (> t)
    nonface_radius_min = _get_nonface_radius_min(dist)

    # AD の長さを取得 (> 2t)
    nonconnect_edge_min = _get_nonconnect_edge_min(dist) 

    t_nonconnect = min(nonface_radius_min, nonconnect_edge_min/2)

    # x_min = _get_x_minimal_edge(dist)
    # nonx_max = _get_nonx_max_edge(dist)
    # ret = (t_connect < t_nonconnect)   and (x_min > nonx_max)
    ret = (t_connect < t_nonconnect)
    return (ret, t_connect, t_nonconnect)

def _output_result(count, pts, connect_max, nonconnect_min):
    output_dir = "Cech/"
    point_filename = output_dir + "points" + str(count) + ".csv"
    np.savetxt(point_filename, pts, delimiter=",", fmt="%f")
    # up and low file nmae
    thresh_filename = output_dir+"threshold" + str(count) + ".txt"
    with open(thresh_filename, "w") as f:
        f.write("low=" + str(connect_max) + "\n")
        f.write("up=" + str(nonconnect_min) + "\n") 
    # debug mode
    print("connect_max = ", connect_max, ", non_conect_min = ", nonconnect_min)
    print(pts)


def _trial_all(count, dim):
    points = np.random.rand(_POINT_NUM, dim)
    for p in itertools.permutations(points):
        (ret, t_connect, t_nonconnect) = _is_noninterval(p)
        if ret:
            _output_result(count, p, t_connect, t_nonconnect)
            return True
    return False


def main(trycount, dim=3):
    count = 1
    for _ in range(trycount):
        if _trial_all(count, dim):
            count = count + 1

    print("total success count : " , count - 1)


if __name__ == "__main__":
    trycount = 1000000
    dim = 3
    main(trycount, dim)
