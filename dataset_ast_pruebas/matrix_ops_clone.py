def transponer(matriz):
    return [[matriz[col][fila] for col in range(len(matriz))] for fila in range(len(matriz[0]))]
