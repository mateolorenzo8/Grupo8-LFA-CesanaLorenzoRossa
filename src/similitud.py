from collections import Counter


def generar_ngramas(sequencia: list[str], n: int = 3) -> list[tuple[str, ...]]:
    if len(sequencia) < n:
        return [tuple(sequencia)]
    return [tuple(sequencia[i:i + n]) for i in range(len(sequencia) - n + 1)]


def similiridad_jaccard_ngramas(sec1: list[str], sec2: list[str], n: int = 3) -> float:
    ngramas1 = set(generar_ngramas(sec1, n))
    ngramas2 = set(generar_ngramas(sec2, n))

    interseccion = ngramas1.intersection(ngramas2)
    union = ngramas1.union(ngramas2)

    if not union:
        return 0.0
    return len(interseccion) / len(union)