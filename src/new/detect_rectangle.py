import cv2
import numpy as np


def detect_rectangle(
    img,
    width=1080,
    height=548,
    distance=10
):

    # ============================================
    # 1. CONVERTER PARA ESCALA DE CINZA
    # ============================================

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )


    # ============================================
    # 2. DETECTAR BORDAS
    # ============================================

    edges = cv2.Canny(
        gray,
        40,
        120
    )


    # ============================================
    # 3. DETECTAR LINHAS
    # ============================================

    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=50,
        minLineLength=900,
        maxLineGap=150
    )

    # 3. To separate the lines into vertical and horizontal, 
    # we can use the slope of the lines.
    
''' PRECISO CUIDAR DO SEPARATE LINES 
    verticals, horizontal = separate_lines(
        lines
    )

    # ---------------------------------
    # 5. Agrupar lines próximas
  

    xs = group_coordinates(
        verticals,
        distance=distance
    )

    ys = group_coordinates(
        horizontal,
        distance=distance
    )

    # ---------------------------------
    # 6. Procurar retângulo
    # ---------------------------------

    rectangle = encontrar_rectangle(
        xs,
        ys,
        expected_width=width,
        expected_height=height
    )

    return rectangle
    '''