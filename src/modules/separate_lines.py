import numpy as np
import cv2
import os

def separar_linhas(linhas, angulo_tolerancia=10):

    verticais = []
    horizontais = []

    # Verifica se nenhuma linha foi detectada
    if linhas is None:
        return verticais, horizontais

    for linha in linhas:

        # Converte o segmento para um array 1D
        linha = np.asarray(linha).reshape(-1)

        # Garante que o segmento possui exatamente 4 coordenadas
        if linha.size != 4:
            print(
                f"Aviso: segmento ignorado. "
                f"Formato encontrado: {linha.shape}"
            )
            continue

        # Coordenadas dos pontos inicial e final
        x1, y1, x2, y2 = linha.astype(float)

        # Diferenças entre os pontos
        dx = x2 - x1
        dy = y2 - y1

        # Calcula o ângulo da linha
        angulo = np.degrees(
            np.arctan2(dy, dx)
        )

        # Converte o ângulo para o intervalo [0, 180)
        angulo = angulo % 180

        # --------------------------------------------------
        # LINHA VERTICAL
        # --------------------------------------------------

        if abs(angulo - 90) <= angulo_tolerancia:

            # Coordenada X média
            x = (x1 + x2) / 2

            verticais.append(x)

        # --------------------------------------------------
        # LINHA HORIZONTAL
        # --------------------------------------------------

        elif (
            angulo <= angulo_tolerancia
            or abs(angulo - 180) <= angulo_tolerancia
        ):

            # Coordenada Y média
            y = (y1 + y2) / 2

            horizontais.append(y)

    return verticais, horizontais
