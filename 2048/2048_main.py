import pygame as p
import random


WIDTH = HEIGHT = 800
m = 4
SS = 800 // m
FPS = 30
white = (255, 255, 255)
colors = {"lines": (187, 173, 160),
          "num>2": (249, 246, 242),
          "num<2": (119, 110, 101),
          0: (205, 193, 180),
          2: (238, 228, 218),
          4: (238, 225, 201),
          8: (243, 178, 122),
          16: (246, 150, 100),
          32: (247, 124, 95),
          64: (247, 95, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          4096: (62, 57, 51)}


class Board:
    def __init__(self):
        self.board = generate_matrix()


def main():
    p.init()
    p.display.set_caption("2048")
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()

    b = Board()

    draw_board(b, screen)

    counter = 0
    count = False

    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

            if event.type == p.KEYDOWN:

                if event.key == p.K_BACKSPACE:
                    b = Board()
                    draw_board(b, screen)

                elif counter == 0:
                    copy = copy_matrix(b.board)

                    if event.key == p.K_DOWN:
                        b.board = down(b.board)

                    if event.key == p.K_LEFT:
                        left(b.board)

                    if event.key == p.K_RIGHT:
                        right(b.board)

                    if event.key == p.K_UP:
                        b.board = up(b.board)

                    if copy != b.board:
                        count = True
                        draw_board(b, screen)

                    if not is_there_options(b.board):
                        draw_game_over(screen)

        if count:
            counter += 1

        if counter == 5:
            generate_number(b.board)
            draw_board(b, screen)
            counter = 0
            count = False

        p.display.flip()
        clock.tick(FPS)


def draw_board(b, screen):
    screen.fill(colors["lines"])
    for i in range(m):
        for j in range(m):
            text = ""
            if b.board[i][j] != 0:
                text = str(b.board[i][j])

            color = colors["num>2"] if b.board[i][j] > 4 else colors["num<2"]

            rect_obj = p.draw.rect(screen, colors[b.board[i][j]], p.Rect(j*SS+5, i*SS+5, SS-10, SS-10), 0, 10)
            my_font = p.font.SysFont("helvetica", 80, bold=True).render(text, True, color)
            text_rect = my_font.get_rect(center=rect_obj.center)
            screen.blit(my_font, text_rect)


def draw_game_over(screen):
    my_font = p.font.SysFont("helvetica", 80, bold=True).render("GAME OVER!", True, white)
    pos = my_font.get_rect()
    screen.blit(my_font, (WIDTH//2 - pos[2]//2, HEIGHT//2 - pos[3]//2))


def generate_matrix():
    matrix = [[0 for i in range(m)] for j in range(m)]
    generate_number(matrix)
    generate_number(matrix)
    return matrix


def generate_number(matrix):
    i, j = random.randint(0, m-1), random.randint(0, m-1)
    while matrix[i][j] != 0:
        i, j = random.randint(0, m-1), random.randint(0, m-1)
    number = random.randint(0, 10)
    if number <= 2:
        number = 4
    else:
        number = 2
    matrix[i][j] = number
    return matrix


def up(board):
    board = transpose(board)
    compress(board)
    add(board)
    compress(board)
    board = transpose(board)
    return board


def down(board):
    board = transpose(board)
    invert(board)
    compress(board)
    add(board)
    compress(board)
    invert(board)
    board = transpose(board)
    return board


def left(board):
    compress(board)
    add(board)
    compress(board)


def right(board):
    invert(board)
    compress(board)
    add(board)
    compress(board)
    invert(board)


def is_there_options(matrix):
    for i in range(m):
        if 0 in matrix[i]:
            return True

    copy = copy_matrix(matrix)
    copy2 = copy_matrix(matrix)

    copy = up(copy)
    copy = down(copy)
    left(copy)
    right(copy)

    if copy != copy2:
        return True
    return False


def compress(matrix):
    for i in range(m):
        move_position = 0
        for j in range(m):
            if matrix[i][j] != 0:
                if j != move_position:
                    matrix[i][move_position], matrix[i][j] = matrix[i][j], 0
                move_position += 1
    return matrix


def add(matrix):
    for i in range(m):
        for j in range(m-1):
            if matrix[i][j] == matrix[i][j+1]:
                matrix[i][j] *= 2
                matrix[i][j+1] = 0
    return matrix


def invert(matrix):
    for i in range(m):
        for j in range(m//2):
            matrix[i][j], matrix[i][-(j+1)] = matrix[i][-(j+1)], matrix[i][j]
    return matrix


def transpose(matrix):
    matrix2 = [[0 for k in range(m)] for l in range(m)]
    for i in range(m):
        for j in range(m):
            matrix2[i][j] = matrix[j][i]
    return matrix2


def copy_matrix(matrix):
    matrix2 = []
    for i in range(4):
        row = []
        for j in range(4):
            row.append(matrix[i][j])
        matrix2.append(row)
    return matrix2


if __name__ == '__main__':
    main()
