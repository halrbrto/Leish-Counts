import cv2 
import numpy as np  
import os
from itertools import combinations


def agrupar_coordenadas(coordenadas, distancia=10):

    if len(coordenadas) == 0:
        return []

    coordenadas = sorted(coordenadas)

    grupos = []

    grupo_atual = [
        coordenadas[0]
    ]

    for valor in coordenadas[1:]:

        centro = np.mean(
            grupo_atual
        )

        if abs(valor - centro) <= distancia:

            grupo_atual.append(valor)

        else:

            grupos.append(
                grupo_atual
            )

            grupo_atual = [
                valor
            ]

    grupos.append(
        grupo_atual
    )

    # Representa cada grupo pelo seu centro
    centros = [
        np.mean(grupo)
        for grupo in grupos
    ]

    return centros