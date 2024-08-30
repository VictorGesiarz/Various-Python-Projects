import pygame as p
import random

HEIGHT = WIDTH = 1024
DIMENSION = 6
MAX_FPS = 30
squares_per_row = 2 ** DIMENSION
ss = HEIGHT // squares_per_row

white = (255, 255, 255)

player_move = [0, 1]


def main():
    p.init()
    screen = p.display.set_mode((HEIGHT, WIDTH))
    screen.fill(white)
    p.display.set_caption("L puzzle")
    clock = p.time.Clock()

    colors = {0: (255, 255, 255)}
    board = [[0 for x in range(squares_per_row)] for y in range(squares_per_row)]
    counter = 1

    select = True

    running = True
    while running:
        for event in p.event.get():

            if event.type == p.QUIT:
                running = False

            elif event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // ss
                row = location[1] // ss

                if select:
                    select = False
                    board[row][col] = counter
                    counter += 1
                    print(counter)

                    board, counter = program(board, (row, col), counter)

                    colors = make_colors(counter)

        keys = p.key.get_pressed()
        if keys[p.K_BACKSPACE]:
            board, colors, select, counter = reset(board, colors, select, counter, screen)

        color_squares(screen, board, colors)
        draw_squares(screen)
        clock.tick()
        p.display.flip()


"""def draw_board(screen):
    for k in range(DIMENSION):
        squares_per_row = 2**(DIMENSION-k)
        ss = HEIGHT // squares_per_row
        draw_squares(screen, squares_per_row, ss, k)"""


def reset(board, colors, select, counter, screen):
    board = [[0 for i in range(squares_per_row)] for j in range(squares_per_row)]
    colors = {0: (255, 255, 255)}
    select = True
    screen.fill(p.Color("white"))
    counter = 1
    return board, colors, select, counter


def draw_squares(screen):
    color = (0, 0, 0)

    for i in range(squares_per_row):
        for j in range(squares_per_row):
            p.draw.rect(screen, color, p.Rect(j*ss, i*ss, ss, ss), 1)


def color_squares(screen, board, colors):
    for i in range(squares_per_row):
        for j in range(squares_per_row):
            p.draw.rect(screen, colors[board[i][j]], p.Rect(j * ss, i * ss, ss, ss))


def program(board, selected_square, counter):
    if len(board) == 2:
        return complete_square(board, counter), counter+1
    else:
        Q1, Q2, Q3, Q4 = make_quadrants(board)
        boards_to_change = find_quadrant(board, [Q1, Q2, Q3, Q4], selected_square)
        Q1, Q2, Q3, Q4, counter, selected_squares = L_quadrants(Q1, Q2, Q3, Q4, boards_to_change, counter,
                                                                selected_square)
        Q1, counter = program(Q1, selected_squares[0], counter)
        Q2, counter = program(Q2, selected_squares[1], counter)
        Q3, counter = program(Q3, selected_squares[2], counter)
        Q4, counter = program(Q4, selected_squares[3], counter)
        return remake_board(Q1, Q2, Q3, Q4), counter


def make_colors(counter):
    colors = {1: (255, 0, 0)}
    for i in range(2, counter):
        a, b, c = random.randint(0, 255), random.randint(0, 255), 255
        colors[i] = (a, b, c)
    return colors


def print_matrix(board):
    for i in range(len(board)):
        print(board[i])
    print()


def remake_board(Q1, Q2, Q3, Q4):
    for i in range(len(Q1)):
        Q1[i] += Q3[i]
        Q2[i] += Q4[i]
    return Q1 + Q2


def L_quadrants(Q1, Q2, Q3, Q4, boards_to_change, counter, selected_square):
    selected_squares = []
    a = len(Q1)
    if Q1 in boards_to_change:
        Q1[-1][-1] = counter
        selected_squares.append((a-1, a-1))
    else:
        selected_squares.append(selected_square)
    if Q2 in boards_to_change:
        Q2[0][-1] = counter
        selected_squares.append((0, a-1))
    else:
        selected_squares.append((selected_square[0], selected_square[1]-a//2))
    if Q3 in boards_to_change:
        Q3[-1][0] = counter
        selected_squares.append((a-1, 0))
    else:
        selected_squares.append((selected_square[0]-a//2, selected_square[1]))
    if Q4 in boards_to_change:
        Q4[0][0] = counter
        selected_squares.append((0, 0))
    else:
        selected_squares.append((selected_square[0]-a//2, selected_square[1]-a//2))
    return Q1, Q2, Q3, Q4, counter+1, selected_squares


def find_quadrant(board, boards, selected_square):
    i, j = selected_square[0], selected_square[1]
    a = len(board)
    if i < a//2 and j < a//2:
        boards.remove(boards[0])
    elif i >= a//2 > j:
        boards.remove(boards[1])
    elif i < a//2 <= j:
        boards.remove(boards[2])
    elif i >= a//2 and j >= a//2:
        boards.remove(boards[3])
    return boards


def make_quadrants(board):
    Q1 = []
    Q2 = []
    Q3 = []
    Q4 = []
    a = len(board)
    for i in range(a//2):
        r1 = []
        r2 = []
        r3 = []
        r4 = []
        for j in range(a//2):
            r1.append(board[i][j])
            r2.append(board[i+a//2][j])
            r3.append(board[i][j+a//2])
            r4.append(board[i+a//2][j+a//2])
        Q1.append(r1)
        Q2.append(r2)
        Q3.append(r3)
        Q4.append(r4)
    return Q1, Q2, Q3, Q4


def complete_square(board, counter):
    a, b = 0, 0
    for i in range(2):
        for j in range(2):
            if board[i][j] != 0:
                a, b = i, j
                break
    a = abs(a-1)
    board[a][b] = counter
    b = abs(b-1)
    board[a][b] = counter
    a = abs(a-1)
    board[a][b] = counter
    return board


if __name__ == '__main__':
    main()
