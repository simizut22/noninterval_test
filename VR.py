# -*- coding : utf-8 -*-
"""Vetoris Rips Complex における minimal な model の実験"""

# 基本的には以下のようなもの. ここで, index の自明な purmutation が実際にはかかってくるが, itertools.permutation の制限は特につけないこととする.

# A -- C -- E
# |    |    |
# B -- D -- F

# に 2 点 X, Y を追加する.

# 条件として,
# ```
#           A ------------------- C ------------------ E
#         /  ＼                  /  ＼             ／ /
#        /      ＼              /      ＼       ／   /
#       /          ＼          /          ＼ ／      /
#      /              ＼----+--------------X       /
#     /       Y------------+-----＼               /
#    /     ／  ＼         /         ＼           /
#   /   ／        ＼     /             ＼       /
#  /／              ＼ /                  ＼   /
# B ------------------ D --------------------  F
# ```
# edge を貼る ->
# A --  C -- E
#  |     |     |    より  |AB|, |AC|, |BD|, |CD|, |CE|, |DF|, |EF| ≦ t
# B --  D -- F
# 追加の X, Y が edge をはる
# |AX|, |CX|, |EX| ≦ t
# |BY|, |DY|, |FY| ≦
# |XY| ≦ t

# X--Y--A--B が face を貼る -> min(|XB|, |YA|) ≦ t
# X--Y--C--D が face を貼る -> min(|XF|, |YE|) ≦ t

# これ以外は face を張らない.
# ABCD が face を張らない -> |AD|, |BC| > t
# CDEF が face を張らない -> |CF|, |ED| > t
# XYCD が face を張らない -> |XC|, |YD| > t


import numpy as np
from scipy.spatial import distance_matrix
import itertools


_POINT_NUM = 8
[iA, iB, iC, iD, iE, iF, iX, iY] = list(range(_POINT_NUM))

_CONNECT_CANDIDATEA = [
    # A | B | C | D | E | F | X | Y 
    [ 1 , 1 , 1 , 0 , 0 , 0 , 1 , 1],  # A に接続する(可能性がある)のは A, B, C, X, Y
    [ 1 , 1 , 0 , 1 , 0 , 0 , 1 , 1],  # B に接続する(可能性がある)のは A, B, D, X, Y
    [ 1 , 0 , 1 , 1 , 1 , 0 , 1 , 0],  # C に接続する(可能性がある)のは A, C, D, E, X
    [ 0 , 1 , 1 , 1 , 0 , 1 , 0 , 1],  # Dに接続する(可能性がある)のは B, C, D, F, Y
    [ 0 , 0 , 1 , 0 , 1 , 1 , 1 , 1],  # E に接続する(可能性がある)のは C, E, F, X, Y
    [ 0 , 0 , 0 , 1 , 1 , 1 , 1 , 1],  # Fに接続する(可能性があるのは) D, E, F, X, Y
    [ 1 , 1 , 1 , 0 , 1 , 1 , 1 , 1],  # X に接続する(可能性がある)のは A, B, C, E, F, X, Y
    [ 1 , 1 , 0 , 1 , 1 , 1 , 1 , 1]   # Y に接続する(可能性があるのは) A, B, D, E, F, X, Y
]


def _get_minimal_nonconnect_edge_length(distmatr):
    points_num = len(distmatr)
    mindist = None
    for i in range(points_num):
        for j in range(i+1, points_num):
            if _CONNECT_CANDIDATEA[i][j] == 0:
                    if mindist is None:
                        mindist = distmatr[i, j]
                    else:
                        mindist = min(mindist, distmatr[i, j])
    return mindist


def _get_maximal_connect_edge_length(distmatr):
    """
    |AB|, |AC|, |AX|, |BD|, |BY|, |CD|, |CE|, |CX|, |DF|, |DY|, |EF|, |EX|, |FY|, |XY| ≦ t
    min(|XB|, |YA|), min(|XF|, |YE|) ≦ t
    """
    determined = max([
        distmatr[iA, iB],  # AB
        distmatr[iA, iC],  # AC
        distmatr[iA, iX],  # AX
        distmatr[iB, iD],  # BD
        distmatr[iB, iY],  # BY
        distmatr[iC, iD],  # CD
        distmatr[iC, iE],  # CE
        distmatr[iC, iX],  # CX
        distmatr[iD, iF],  # DF
        distmatr[iD, iY],  # DY
        distmatr[iE, iF],  # EF 
        distmatr[iE, iX],  # EX
        distmatr[iF, iY],  # FY
        distmatr[iX, iY]]  # XY
    )
    xbya = min(distmatr[iX, iB], distmatr[iY, iA])
    xfye = min(distmatr[iX, iF], distmatr[iY, iE])
    return max(determined, xbya, xfye)


def _is_noninterval(pts):
    """
    上の条件を満たすかどうかを確認する.
    """
    dist = distance_matrix(pts, pts)
    nonconnect_min = _get_minimal_nonconnect_edge_length(dist)
    if nonconnect_min is None:
        print ("None!!!!")
        exit(1)
    connect_max = _get_maximal_connect_edge_length(dist)
    ret = connect_max < nonconnect_min
    return (ret, connect_max, nonconnect_min)


def _output_result(count, pts, connect_max, nonconnect_min):
    output_dir = "VR/"
    point_filename = output_dir + "points" + str(count) + ".csv"
    np.savetxt(point_filename, pts, delimiter=",", fmt="%f")
    # up and low file nmae
    thresh_filename = output_dir + "threshold" + str(count) + ".txt"
    with open(thresh_filename, "w") as f:
        f.write("low=" + str(connect_max), + "\n")
        f.write("up=" + str(nonconnect_min) + "\n") 
    # debug mode
    print("connect_max = ", connect_max, ", non_conect_min = ", nonconnect_min)
    print(pts)
        


def _trial_1(count, dim):
    points = np.random.rand(_POINT_NUM, dim)
    (ret, connect_max, nonconnect_min) = _is_noninterval(points)
    if ret:
        _output_result(count, points, connect_max, nonconnect_min)
        return True
    return False

    
def _trial_all(count, dim):
    points = np.random.rand(_POINT_NUM, dim)
    for p in itertools.permutations(points):
        (ret, connect_max, nonconnect_min) = _is_noninterval(p)
        if ret:
            _output_result(count, p, connect_max, nonconnect_min)
            return True
    return False


def main(trycount, dim=3):
    count = 1
    for _ in range(trycount):
        if _trial_all(count, dim):
            count = count + 1
    print("total success count : " , count - 1)


if __name__ == "__main__":
    try_count = 1000000
    dim = 3
    main(try_count, dim)
