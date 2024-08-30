import pygame as p
from math import ceil, sqrt, floor
import random, time


WIDTH = HEIGHT = 1000
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(0, 0, 200), (0, 200, 0)]
DIM = 1000
SS = WIDTH // DIM


def main():
    p.init()
    p.display.set_caption("Prime numbers spiral")
    screen = p.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BLACK)
    clock = p.time.Clock()

    """numbers = [x for x in range(2, DIM ** 2)]
    primes = hallar_primos_mejor(numbers, DIM ** 2)
    primes.append(0)
    set_board(screen, primes)"""

    arr = set_board_romek(DIM)

    for i in range(len(arr)):
        for j in range(len(arr)):
            if arr[i][j]:
                p.draw.rect(screen, COLORS[1], p.Rect(j*SS, i*SS, SS, SS))

    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

        p.display.flip()
        clock.tick(30)


def set_board_romek(width):
    start = time.time()

    prime = get_primes(width**2)
    arr = [[0 for x in range(width)] for z in range(width)]
    center = (width - 1) // 2
    steps = [[0, 1], [-1, 0], [0, -1], [1, 0]]

    x = center
    y = center

    temp = 0
    value = 1

    for i in range(1, width+1):
        for j in range(2):
            for k in range(i):
                if x < 0 or y < 0 or x > width - 1 or y > width - 1:
                    break
                arr[x][y] = prime[value]
                value += 1
                x += steps[temp % 4][0]
                y += steps[temp % 4][1]
            temp += 1
        if value > width**2:
            break
    end = time.time()
    print(end - start)
    return arr


def get_primes(n):
    prime = [True for i in range(n + 1)]

    prime[0] = False
    prime[1] = False
    for p in range(2, int(sqrt(n)) + 1):
        if prime[p]:
            for i in range(p**2, n+1, p):
                prime[i] = False
    return prime


def set_board(screen, primes):
    start = time.time()
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    pos = [DIM // 2, DIM // 2]
    moves = 1
    direction = 0
    counter = 1
    prime = 0

    board = [[0 for x in range(DIM)] for y in range(DIM)]

    p.draw.circle(screen, (255, 0, 0), (pos[0]*SS, pos[1]*SS), SS)

    for i in range(DIM*2 - 1):
        for j in range(moves):
            board[pos[0]][pos[1]] = counter

            if counter == primes[prime]:
                rect_obj = p.Rect(pos[1] * SS, pos[0] * SS, SS, SS)
                p.draw.rect(screen, COLORS[0], rect_obj)
                prime += 1

            pos[0] += directions[direction % 4][0]
            pos[1] += directions[direction % 4][1]
            counter += 1
        direction += 1
        if i % 2 == 1:
            moves += 1
    end = time.time()
    print(end-start)


def hallar_primos_mejor(lista, n):
    for i in range(ceil(sqrt(n))):
        if lista[i]:
            for j in range(1, ceil(n/lista[i])-1):
                lista[i + lista[i] * j] = False
    return [x for x in lista if x]


if __name__ == '__main__':
    main()