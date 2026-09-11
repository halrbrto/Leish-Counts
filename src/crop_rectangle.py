# Documentation: This code identifies the crop box in
# various Neubauer chamber images

# Status: Lines detected and image segmented.
# Next Step: Fix errors in some images (parameter tuning) /
# Split functions into separate code files
# Final Implementation: Loop-based processing for all images in the folder
# General Comment: Translate the entire code into English

# By: Halerrandro Brito

import cv2 
import numpy as np  
import os
from itertools import combinations

# TESTE DE CONFERÊNCIA DE CAMINHOS
# --------------------------------------------
# print("Diretório atual:", os.getcwd())

# print("\nArquivos nesta pasta:")
# print(os.listdir())

# if os.path.exists("Imagens_teste"):
#     print("\nConteúdo da pasta Imagens_teste:")
#     print(os.listdir("Imagens_teste"))
# else:
#     print("\nA pasta 'Imagens_teste' NÃO existe.")


# CAMINHO DA IMAGEM
# --------------------------------------------

image_path = r"tests\exemplo2.jpg"

# CHECAR SE O CAMINHO EXISTE ANTES DE IMPORTAR
# --------------------------------------------
print("\nFile exists:", os.path.exists(image_path))

# IMPORTAR A IMAGEM 
# --------------------------------------------
img = cv2.imread(image_path)

# TESTE DE FALHAS DE IMPORTAÇÃO E INFORMAÇÕES
# --------------------------------------------
if img is None:
    print("\nErro ao carregar a imagem.")
else:
    print(img.shape)

print(f"Dimensões da imagem (altura (px), largura(px), canais): {img.shape}")
print(f"Tipo de dados da imagem: {img.dtype}")
print(f"Valor máximo de pixel: {np.max(img)}")
print(f"Valor mínimo de pixel: {np.min(img)}")

# ============================================================
# EXECUÇÃO DO ALGORITMO
# ============================================================

# Detecta o retângulo na imagem
retangulo = detectar_retangulo(
    img,
    largura_esperada=1080,
    altura_esperada=548,
    distancia_agrupamento=10
)


# ============================================================
# VERIFICAR SE O RETÂNGULO FOI ENCONTRADO
# ============================================================

if retangulo is None:

    print("\nNenhum retângulo foi encontrado.")

else:

    # --------------------------------------------------------
    # Imprimir informações do retângulo encontrado
    # --------------------------------------------------------

    print("\nRetângulo encontrado:")
    print(f"x1: {retangulo['x1']}")
    print(f"y1: {retangulo['y1']}")
    print(f"x2: {retangulo['x2']}")
    print(f"y2: {retangulo['y2']}")

    print(f"Largura: {retangulo['largura']:.2f} px")
    print(f"Altura: {retangulo['altura']:.2f} px")
    print(f"Erro total: {retangulo['erro']:.4f}")


    # --------------------------------------------------------
    # Obter coordenadas do retângulo
    # --------------------------------------------------------

    x1 = int(retangulo["x1"])
    y1 = int(retangulo["y1"])

    x2 = int(retangulo["x2"])
    y2 = int(retangulo["y2"])


    # --------------------------------------------------------
    # Recortar a imagem original
    # --------------------------------------------------------

    crop = img[
        y1:y2,
        x1:x2
    ]


    # --------------------------------------------------------
    # Verificar se o crop foi gerado corretamente
    # --------------------------------------------------------

    if crop.size == 0:

        print("\nErro: o recorte gerado está vazio.")

    else:

        print(
            f"\nDimensões do recorte: "
            f"{crop.shape[1]} x {crop.shape[0]} px"
        )


        # ----------------------------------------------------
        # Mostrar imagem original com o retângulo detectado
        # ----------------------------------------------------

        imagem_marcada = img.copy()

        cv2.rectangle(
            imagem_marcada,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            3
        )


        # ----------------------------------------------------
        # Abrir janela com a imagem original
        # e o retângulo detectado
        # ----------------------------------------------------

        cv2.imshow(
            "Imagem original - Retangulo detectado",
            imagem_marcada
        )


        # ----------------------------------------------------
        # Abrir janela com a imagem recortada
        # ----------------------------------------------------

        cv2.imshow(
            "Imagem recortada",
            crop
        )


        # ----------------------------------------------------
        # Esperar uma tecla
        # ----------------------------------------------------

        cv2.waitKey(0)

        # Fechar todas as janelas
        cv2.destroyAllWindows()
