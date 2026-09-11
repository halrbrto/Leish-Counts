from itertools import combinations

def encontrar_retangulo(
    xs,
    ys,
    largura_esperada=1080,
    altura_esperada=548,
    tolerancia_largura=0.10,
    tolerancia_altura=0.10
):
    """Find the rectangle whose dimensions best match the expected values.

    Args:
        xs: X-coordinates of candidate vertical lines.
        ys: Y-coordinates of candidate horizontal lines.
        largura_esperada: Expected rectangle width in pixels.
        altura_esperada: Expected rectangle height in pixels.
        tolerancia_largura: Maximum relative width error allowed.
        tolerancia_altura: Maximum relative height error allowed.

    Returns:
        A dictionary describing the best matching rectangle, or ``None`` if
        no pair satisfies both tolerances.
    """

    candidatos = []

    # Generate every possible pair of vertical lines.
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

        # Ignore widths that are outside the allowed tolerance.
        if erro_largura > tolerancia_largura:
            continue

        # Generate every possible pair of horizontal lines.
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

            # Ignore heights that are outside the allowed tolerance.
            if erro_altura > tolerancia_altura:
                continue

            # Combine the width and height errors into one score.
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

    # Return None when no candidate meets both tolerances.
    if not candidatos:
        return None

    # Sort candidates from the smallest error to the largest.
    candidatos.sort(
        key=lambda r: r["erro"]
    )

    # The first candidate is the best match.
    return candidatos[0]