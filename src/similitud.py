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

def levenshtein_distance(seq1: list[str], seq2: list[str]) -> int:
    m, n = len(seq1), len(seq2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i-1] == seq2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j],       # Borrado
                                   dp[i][j-1],       # Inserción
                                   dp[i-1][j-1])     # Sustitución

    return dp[m][n]

def normalized_levenshtein_similarity(seq1: list[str], seq2: list[str]) -> float:
    max_len = max(len(seq1), len(seq2))
    if max_len == 0:
        return 1.0
    dist = levenshtein_distance(seq1, seq2)
    return 1.0 - (dist / max_len)