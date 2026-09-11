import cv2 
import numpy as np  
import os
from itertools import combinations

def encontrar_retangulo(
    xs,
    ys,
    largura_esperada=1080,
    altura_esperada=548,
    tolerancia_largura=0.10,
    tolerancia_altura=0.10
):

    candidatos = []

    # Todas as combinações de duas linhas verticais
    pares_verticais = combinations(
        sorted(xs),
        2
    )

    for x1, x2 in pares_verticais:

        largura = x2 - x1

        erro_largura = (
            abs(
                largura -
                largura_esperada
            )
            /
            largura_esperada
        )

        # Descarta larguras muito diferentes
        if erro_largura > tolerancia_largura:
            continue

        # Todas as combinações de duas linhas horizontais
        pares_horizontais = combinations(
            sorted(ys),
            2
        )

        for y1, y2 in pares_horizontais:

            altura = y2 - y1

            erro_altura = (
                abs(
                    altura -
                    altura_esperada
                )
                /
                altura_esperada
            )

            # Descarta alturas muito diferentes
            if erro_altura > tolerancia_altura:
                continue

            # Erro total
            erro_total = (
                erro_largura +
                erro_altura
            )

            candidatos.append({

                "x1": x1,
                "y1": y1,

                "x2": x2,
                "y2": y2,

                "largura": largura,
                "altura": altura,

                "erro": erro_total
            })

    # Nenhum retângulo encontrado
    if not candidatos:
        return None

    # Menor erro primeiro
    candidatos.sort(
        key=lambda r: r["erro"]
    )

    return candidatos[0]