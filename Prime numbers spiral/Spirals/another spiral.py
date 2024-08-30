import pygame as p
import math as m

WIDTH = HEIGHT = 900
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def main():
    p.init()
    p.display.set_caption("Prime numbers spiral")
    screen = p.display.set_mode((WIDTH, HEIGHT))
    screen.fill(WHITE)
    clock = p.time.Clock()

    spiral(screen)

    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

        p.display.flip()
        clock.tick(30)


def spiral(screen):

    n = 100000
    numbers = [x for x in range(n)]
    primes = hallar_primos_mejor([x for x in range(2, 2*n)], 2*n)
    j = 0

    for i in range(n):
        #if numbers[i] == primes[j]:
            vt = i / 1000 * m.pi
            x = round((vt * 2) * m.cos(vt))
            y = round((vt * 2) * m.sin(vt))
            j += 1
            p.draw.rect(screen, BLACK, p.Rect(WIDTH // 2 + x, WIDTH // 2 + y, 1, 1))


def hallar_primos_mejor(lista, n):
    for i in range(m.ceil(m.sqrt(n))):
        if lista[i]:
            for j in range(1, m.ceil(n/lista[i])-1):
                lista[i + lista[i] * j] = False
    return [x for x in lista if x]


if __name__ == '__main__':
    main()
