import pygame as p
import time

WIDTH = HEIGHT = 1000
DIMENSION = 100
SS = WIDTH // DIMENSION
FPS = 60
COLORS = [(255, 255, 255), (0, 0, 0)]


def main():
    p.init()
    p.display.set_caption("Juego de la vida")
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()

    board = [[0 for i in range(DIMENSION)] for j in range(DIMENSION)]
    for z in range(DIMENSION):
        for x in range(DIMENSION):
            if z == x:
                board[z][x] = 1
            if z + x == DIMENSION:
                board[z][x] = 1
    save = []

    clicked = False
    pause = True
    running = True
    while running:

        time.sleep(0.1)

        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

            if event.type == p.KEYDOWN:
                if event.key == p.K_SPACE:
                    pause = not pause

                if event.key == p.K_BACKSPACE:
                    pause = True
                    board = [[0 for i in range(DIMENSION)] for j in range(DIMENSION)]

                if event.key == p.K_s:
                    save = copy(board)

                if event.key == p.K_p:
                    if len(save) > 0:
                        board = save

            if event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                xi = location[1] // SS
                yi = location[0] // SS
                board[xi][yi] = 0 if board[xi][yi] == 1 else 1
                clicked = True

            if event.type == p.MOUSEBUTTONUP:
                clicked = False

            if event.type == p.MOUSEMOTION and clicked:
                location = p.mouse.get_pos()
                x = location[1] // SS
                y = location[0] // SS
                board[x][y] = 0 if board[xi][yi] == 0 else 1

        screen.fill(COLORS[0])

        c = copy(board)

        for i in range(DIMENSION):
            for j in range(DIMENSION):
                if not pause:
                    neighbours = board[(i-1) % DIMENSION][(j-1) % DIMENSION] + \
                                 board[(i-1) % DIMENSION][j % DIMENSION] + \
                                 board[(i-1) % DIMENSION][(j+1) % DIMENSION] + \
                                 board[i % DIMENSION][(j-1) % DIMENSION] + \
                                 board[i % DIMENSION][(j+1) % DIMENSION] + \
                                 board[(i+1) % DIMENSION][(j-1) % DIMENSION] + \
                                 board[(i+1) % DIMENSION][j % DIMENSION] + \
                                 board[(i+1) % DIMENSION][(j+1) % DIMENSION]

                    if board[i][j] == 0 and neighbours == 3:
                        c[i][j] = 1
                    elif board[i][j] == 1 and 2 > neighbours or neighbours > 3:
                        c[i][j] = 0

                p.draw.rect(screen, COLORS[1], p.Rect(SS * j, SS * i, SS, SS), abs(c[i][j] - 1))

        if not pause:
            board = copy(c)

        p.display.flip()
        clock.tick(FPS)


def copy(board):
    c = []
    for i in range(DIMENSION):
        r = []
        for j in range(DIMENSION):
            r.append(board[i][j])
        c.append(r)
    return c


if __name__ == '__main__':
    main()
