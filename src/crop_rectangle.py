# Documentation: 
# Status: 
# Next Step: 
# By: Halerrandro Brito

import cv2
import numpy as np

# Modules
from new import detect_rectangle

# ============================================
# Image Path & import
image_path = r"tests\exemple1.jpg"
img = cv2.imread(image_path)

# Import test image
if img is None:
    print("\nErro ao carregar a imagem:", image_path)
    raise SystemExit

# Image information (metadata)
print(f"Dimensions (height, width, channels): {img.shape}")
print(f"Data type: {img.dtype}")
print(f"Maximum pixel value: {np.max(img)}")
print(f"Minimum pixel value: {np.min(img)}")

# Show the original image
cv2.imshow("Original Image", img)




# ============================================
# Algorithm to detect rectangle
# ============================================

lines = detect_rectangle(img)


# ============================================
# RESULTADO
# ============================================

if lines is None:
    print("Nenhuma linha foi detectada.")
else:
    print(f"Linhas detectadas: {len(lines)}")

cv2.imshow("canny image: ", lines[2])
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
# ============================================================
# VERIFICAR SE O RETÂNGULO FOI ENCONTRADO
# ============================================================

if rectangle is None:

    print("\nNenhum retângulo foi encontrado.")

else:

    # --------------------------------------------------------
    # Imprimir informações do retângulo encontrado
    # --------------------------------------------------------

    print("\nRetângulo encontrado:")
    print(f"x1: {rectangle['x1']}")
    print(f"y1: {rectangle['y1']}")
    print(f"x2: {rectangle['x2']}")
    print(f"y2: {rectangle['y2']}")

    print(f"Largura: {rectangle['largura']:.2f} px")
    print(f"Altura: {rectangle['altura']:.2f} px")
    print(f"Erro total: {rectangle['erro']:.4f}")


    # --------------------------------------------------------
    # Obter coordenadas do retângulo
    # --------------------------------------------------------

    x1 = int(rectangle["x1"])
    y1 = int(rectangle["y1"])

    x2 = int(rectangle["x2"])
    y2 = int(rectangle["y2"])


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
'''