from math import ceil, sqrt


def hallar_primos_mejor(lista, n):
    for i in range(ceil(sqrt(n))):
        if lista[i]:
            for j in range(1, ceil(n/lista[i])-1):
                lista[i + lista[i] * j] = False
    return [x for x in lista if x]


primes = hallar_primos_mejor([x for x in range(2, 100000)], 100000)
print(primes)
print(len(primes))
