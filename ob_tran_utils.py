import math
import numpy as np

def Rx(t):
    t *= math.pi / 180
    c = math.cos(t)
    s = math.sin(t)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])

def Ry(t):
    t *= math.pi / 180
    c = math.cos(t)
    s = math.sin(t)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])

def Rz(t):
    t *= math.pi / 180
    c = math.cos(t)
    s = math.sin(t)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

def lonlat_from_xyz(pt):
    # 3D cartesian coordinates (x, y, z) -> spherical coordinates (lon, lat)
    lon = math.atan2(pt[1], pt[0]) * 180 / math.pi
    lat = math.asin(pt[2]) * 180 / math.pi
    return (lon, lat)

def params_from_rotation(r):
    # R = Rz(lon_p) @ Ry(90-lat_p) @ Rz(-lon_0)
    if np.isclose(r[2][2], 1.0):
        # When R[2][2] == 1, the Y axis rotation is 0.
        # Calculate the parameters for the combined Z axis rotation (lon_0 = 0).
        lat_p = 90.0
        lon_p = math.atan2(r[1][0], r[0][0]) * 180 / math.pi
        lon_0 = 0.0
    elif np.isclose(r[2][2], -1.0):
        # When R[2][2] == -1, the Y axis rotation is 180.
        # Calculate the parameters for the combined Z axis rotation (lon_0 = 0).
        # Rz(lon_p) = R @ inv(Ry(180))
        rz = r @ np.array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])
        lat_p = -90.0
        lon_p = math.atan2(rz[1][0], rz[0][0]) * 180 / math.pi
        lon_0 = 0.0
    else:
        # 回転前の北極点が、回転後にどこに位置するか
        # (x)   (R00 R01 R02) (0)
        # (y) = (R10 R11 R12) (0)
        # (z)   (R20 R21 R22) (1)
        new_pole_lonlat = lonlat_from_xyz((r[0][2], r[1][2], r[2][2]))
        lon_p = new_pole_lonlat[0]
        lat_p = new_pole_lonlat[1]

        # 回転後の北極点が、回転前はどこに位置するか
        # (0)   (R00 R01 R02) (x)
        # (0) = (R10 R11 R12) (y)
        # (1)   (R20 R21 R22) (z)
        # which gives,
        # (x)   (R00 R01 R02)^-1 (0)
        # (y) = (R10 R11 R12)    (0)
        # (z)   (R20 R21 R22)    (1)
        ir = np.linalg.inv(r)
        cur_pole_lonlat = lonlat_from_xyz((ir[0][2], ir[1][2], ir[2][2]))
        lon_0 = (cur_pole_lonlat[0] % 360) - 180

    return {'lon_p': lon_p, 'lat_p': lat_p, 'lon_0': lon_0}



