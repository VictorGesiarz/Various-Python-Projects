"""Create a 2^n board of squares in which a square is chosen and the
    rest of the board is completed with figures with a L form. """

import pygame as p
import random

HEIGHT = WIDTH = 1024               # Main screen configurations.
MAX_FPS = 30
DIMENSION = 2                       # The dimension of the board, which can be changed.
squares_per_row = 2 ** DIMENSION
ss = HEIGHT // squares_per_row


def main():
    p.init()                                        # Initialize the screen.
    screen = p.display.set_mode((HEIGHT, WIDTH))
    screen.fill((255, 255, 255))                    # Fill the screen whit white.
    p.display.set_caption("L puzzle")
    clock = p.time.Clock()

    colors = {0: (255, 255, 255)}
    board = [[0 for x in range(squares_per_row)] for y in range(squares_per_row)]   # Create the board.
    counter = 1

    select = True

    running = True
    while running:
        for event in p.event.get():

            if event.type == p.QUIT:
                running = False

            elif event.type == p.MOUSEBUTTONDOWN:       # Detect mouse click.
                location = p.mouse.get_pos()            # Get the position of the mouse.
                col = location[0] // ss
                row = location[1] // ss

                if select:
                    select = False
                    board[row][col] = counter           # Select the square clicked.
                    counter += 1

                    # Run the main program which calculates everything.
                    board, counter = program(board, [row, col], counter)
                    colors = make_colors(counter)   # Set a random color to each L figure.

        keys = p.key.get_pressed()  # Detect the backspace key to reset.
        if keys[p.K_BACKSPACE]:
            board = [[0 for i in range(squares_per_row)] for j in range(squares_per_row)]
            colors = {0: (255, 255, 255)}
            select = True
            screen.fill(p.Color("white"))
            counter = 1

        color_squares(screen, board, colors)    # Draw the board.
        draw_squares(screen)
        clock.tick()
        p.display.flip()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


"""def draw_board(screen):
    for k in range(DIMENSION):
        squares_per_row = 2**(DIMENSION-k)
        ss = HEIGHT // squares_per_row
        draw_squares(screen, squares_per_row, ss, k)"""


def draw_squares(screen):
    color = (0, 0, 0)
    for i in range(squares_per_row):
        for j in range(squares_per_row):
            p.draw.rect(screen, color, p.Rect(j*ss, i*ss, ss, ss), 1)


def color_squares(screen, board, colors):
    for i in range(squares_per_row):
        for j in range(squares_per_row):
            p.draw.rect(screen, colors[board[i][j]], p.Rect(j * ss, i * ss, ss, ss))


def make_colors(counter):
    colors = {1: (0, 0, 0)}
    for i in range(2, counter):
        a = random.randint(0, 255)
        b = random.randint(0, 255)
        c = 255
        colors[i] = (a, b, c)
    return colors


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def program(board, sel_sq, counter):
    a = len(board)//2
    quadrants = separate(a, board)
    quadrant = find_quadrant(a, sel_sq)
    quadrants, counter, selected_squares = fill(a, quadrants, quadrant, counter, sel_sq)
    if len(board) == 2:
        return remake(a, quadrants), counter
    else:
        for i in range(4):
            quadrants[i], counter = program(quadrants[i], selected_squares[i], counter)
        return remake(a, quadrants), counter


def fill(a, quadrants, quadrant, counter, sel_sq):
    selected_squares = []
    ass = {True: 0, False: a-1}
    loop = 0
    for i in range(2):
        for j in range(2):
            if (i, j) != quadrant:
                quadrants[loop][-(1-i)][-(1-j)] = counter
                selected_squares.append([ass[1 - i == 0], ass[1 - j == 0]])
            elif a > 1:
                sel_sq[0] -= int(ass[1-i != 0] * (a/(a-1)))
                sel_sq[1] -= int(ass[1-j != 0] * (a/(a-1)))
                selected_squares.append(sel_sq)
            loop += 1
    return quadrants, counter+1, selected_squares


def find_quadrant(a, sel_sq):
    checker = {True: 0, False: 1}
    i, j = sel_sq[0], sel_sq[1]
    return checker[i < a], checker[j < a]


def separate(a, board):
    quadrants = [[], [], [], []]
    for i in range(a):
        quadrants[0].append(board[i][:a])
        quadrants[1].append(board[i][a:a*2])
        quadrants[2].append(board[i+a][:a])
        quadrants[3].append(board[i+a][a:a*2])
    return quadrants


def remake(a, quadrants):
    for i in range(a):
        quadrants[0][i] += quadrants[1][i]
        quadrants[2][i] += quadrants[3][i]
    return quadrants[0] + quadrants[2]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


if __name__ == '__main__':
    main()
