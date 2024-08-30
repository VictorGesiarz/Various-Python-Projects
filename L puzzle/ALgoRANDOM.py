import random
import pygame as p
import time

HEIGHT = WIDTH = 1024
DIMENSION = 4
DIMENSIONY = HEIGHT//DIMENSION
DIMENSIONX = WIDTH//DIMENSION
MAX_FPS = 30
ss = HEIGHT // DIMENSIONY
white = (255, 255, 255)


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    screen.fill(white)
    p.display.set_caption("Random")
    clock = p.time.Clock()

    contador = 0
    board = []
    for i in range(DIMENSIONX):
        row = []
        for j in range(DIMENSIONY):
            row.append(contador)
            contador += 1
        board.append(row)
    print(len(board))

    running = True
    while running:
        for event in p.event.get():

            if event.type == p.QUIT:
                running = False

        keys = p.key.get_pressed()

        colors = make_colors(board)
        color_squares(screen, board, colors)
        draw_squares(screen)

        time.sleep(0.2)

        clock.tick()
        p.display.flip()


def draw_squares(screen):
    color = (0, 0, 0)

    for i in range(DIMENSIONY):
        for j in range(DIMENSIONX):
            p.draw.rect(screen, color, p.Rect(j*ss, i*ss, ss, ss), 1)


def color_squares(screen, board, colors):
    for i in range(DIMENSIONY):
        for j in range(DIMENSIONX):
            p.draw.rect(screen, colors[board[i][j]], p.Rect(j * ss, i * ss, ss, ss))


def make_colors(board):
    colors = {}
    for i in range(len(board)):
        for j in range(len(board[i])):
            a = b = c = random.randint(0, 255)
            colors[board[i][j]] = (a, b, c)
    return colors


if __name__ == '__main__':
    main()
