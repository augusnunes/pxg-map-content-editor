import numpy as np
from config_obj import ConfigurationPXGFile

def _na_aresta(px, py, x1, y1, x2, y2):
    cruz = (px - x1) * (y2 - y1) - (py - y1) * (x2 - x1)
    if cruz != 0:
        return False
    return min(x1, x2) <= px <= max(x1, x2) and min(y1, y2) <= py <= max(y1, y2)


def verify_point_in_poligono(poligono, coord, incluir_borda=True):
    """
    poligono is a list of points em R3 [(x1, y1, z1), (x2, y2, z2), ..., (xn, yn, zn)]
    coord -> (xi, yi, zi)
    """
    dentro = False
    n = len(poligono)
    # print(coord)
    x = coord["position"]["x"]
    y = coord["position"]["y"]
    
    for i in range(n):
        x1, y1, _ = poligono[i]
        x2, y2, _ = poligono[(i + 1) % n]
        if incluir_borda and _na_aresta(x, y, x1, y1, x2, y2):
            return True
        if (y1 > y) != (y2 > y):
            x_int = (y - y1) * (x2 - x1) / (y2 - y1) + x1
            if x < x_int:
                dentro = not dentro
    # print(coord if dentro else "")
    return dentro


def get_poligonal_points(config, poligono):
    return [
        coord 
        for coord in config.config_dict["minimap"]
        if verify_point_in_poligono(poligono, coord, incluir_borda=True)
    ]

def shift_new_points(points, delta_coord):
    x, y, z = delta_coord
    for i in range(len(points)):
        points[i]["position"]["x"]+=x
        points[i]["position"]["y"]+=y
        points[i]["position"]["z"]+=z
    return points 


def main(path, poligono, ponto_original, ponto_novo):
    delta = get_delta(ponto_original, ponto_novo)
    conf = ConfigurationPXGFile(path)
    conf.config_dict["minimap"]
    new_points = get_poligonal_points(conf, poligono)
    new_points = shift_new_points(new_points, delta)
    print(new_points)
    conf.incluir_marcadores(new_points)
    conf.export_config_file(f"novo/{path}")

def get_delta(ponto_original, ponto_novo):
    return list(np.array(ponto_novo) - np.array(ponto_original))

main(
    "settings.otml",
    [
        [5709, 26548, 5],
        [6225, 26543, 5],
        [6249, 26955, 5],
        [5669, 26955, 5],
    ],
    [6130, 26619, 5],
    [6875, 26619, 5],
)
