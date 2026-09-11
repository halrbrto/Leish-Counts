# Documentação: Este código serve para encontrar a caixa de crop em 
# diferentes imagens de câmara de Neubaner

# Status: Encontrou as linhas e separou na imagem.
# Próximo Passo: Corrigir o erro de algumas imagens (parametrização) / 
# Separar as funções em diversos códigos
# Implementação final: Implementação em Loop de todas as imagens da pasta
# Comentário geral: traduzir o código inteiro para Inglês

# Por: Halerrandro Brito

import cv2 
import numpy as np  
import os

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

image_path = r"tests\Q4_P1_EstoqueA_01_02_2026.jpg"

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

#print(f"Dimensões da imagem (altura (px), largura(px), canais): {img.shape}")
#print(f"Tipo de dados da imagem: {img.dtype}")
#print(f"Valor máximo de pixel: {np.max(img)}")
#print(f"Valor mínimo de pixel: {np.min(img)}")

# precisa documentar!!!!
# --------------------------------------------
import cv2
import numpy as np
from itertools import combinations


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
