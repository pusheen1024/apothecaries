from math import cos, radians, sqrt
     

def distance(point_1, point_2):
    lon_1, lat_1 = map(float, point_1)
    lon_2, lat_2 = map(float, point_2)
    deg_to_m = 111 * 1000
    dlt = (lat_2 - lat_1) * deg_to_m
    dlg = (lon_2 - lon_1) * deg_to_m * cos(radians((lat_1 + lat_2) / 2))
    return sqrt(dlt ** 2 + dlg ** 2)