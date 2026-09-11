import cv2 
import numpy as np  
import os
from itertools import combinations

def detectar_retangulo(
    img,
    largura_esperada=1080,
    altura_esperada=548,
    distancia_agrupamento=10
):

    # ---------------------------------
    # 1. Pré-processamento
    # ---------------------------------

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    # ---------------------------------
    # 2. Canny
    # ---------------------------------

    edges = cv2.Canny(
        gray,
        40,
        120
    )

    # ---------------------------------
    # 3. HoughLinesP
    # ---------------------------------

    linhas = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 90,
        threshold=50,
        minLineLength=900,
        maxLineGap=150
    )

    if linhas is None:
        return None

    # ---------------------------------
    # 4. Separar horizontais e verticais
    # ---------------------------------

    verticais, horizontais = separar_linhas(
        linhas
    )

    # ---------------------------------
    # 5. Agrupar linhas próximas
    # ---------------------------------

    xs = agrupar_coordenadas(
        verticais,
        distancia=distancia_agrupamento
    )

    ys = agrupar_coordenadas(
        horizontais,
        distancia=distancia_agrupamento
    )

    # ---------------------------------
    # 6. Procurar retângulo
    # ---------------------------------

    retangulo = encontrar_retangulo(
        xs,
        ys,
        largura_esperada=largura_esperada,
        altura_esperada=altura_esperada
    )

    return retangulo