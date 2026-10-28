def es_palindromo(cadena):
    return cadena == cadena[::-1]

def contar_vocales(texto):
    vocales = "aeiouAEIOU"
    total = 0
    for letra in texto:
        if letra in vocales:
            total += 1
    return total
