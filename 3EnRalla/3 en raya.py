import pygame as p
import random
import time

WIDTH = 700
HEIGHT = 800
DIMENSION = 3
SS = (WIDTH-100) // DIMENSION
MAX_FPS = 30

IMAGES = {}


def load_images():
    IMAGES["X"] = p.transform.scale(p.image.load("images/X.png"), (SS-SS//3, SS-SS//3))
    IMAGES["O"] = p.transform.scale(p.image.load("images/O.png"), (SS-SS//3, SS-SS//3))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    screen.fill(p.Color("white"))
    p.display.set_caption("3 in row")
    clock = p.time.Clock()
    load_images()
    i = 0

    my_font = p.font.SysFont("algerian", 130)

    board = [["-", "-", "-"],
             ["-", "-", "-"],
             ["-", "-", "-"]
             ]

    moves = 0
    x_to_move = True
    draw_x_o = {True: "X", False: "O"}

    running = True
    playing = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

            elif event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                mouse_in_range = 50 <= location[0] <= 650 and 150 <= location[1] <= 750

                if mouse_in_range and playing:
                    col = (location[0]-50) // SS
                    row = (location[1]-150) // SS

                    if board[row][col] == '-':
                        board[row][col] = draw_x_o[x_to_move]
                        x_to_move = not x_to_move
                        moves += 1

                elif 550 < location[0] < 650 and 760 < location[1] < 790:
                    board, moves, x_to_move, playing = reset(screen)

        keys = p.key.get_pressed()
        if keys[p.K_BACKSPACE]:
            board, moves, x_to_move, playing = reset(screen)

        win = check_win(board)
        if win:
            draw_board(screen)

            color_squares(win[:i], screen)
            i += 1
            if i == 4:
                i = 0

            draw_pieces(screen, board)
            winner = "X" if moves % 2 != 0 else "O"

            p.draw.rect(screen, (255, 255, 255), p.Rect(0, 0, 700, 145))
            text = my_font.render(winner + " WINS!", 1, (255, 0, 0))
            screen.blit(text, (130, 10))

            playing = False

            time.sleep(0.1)

        elif moves == 9:
            abcd = [random.randint(0, 2) for x in range(4)]
            draw_board(screen)
            color_squares([(abcd[0], abcd[1]), (abcd[2], abcd[3])], screen)
            draw_pieces(screen, board)

            p.draw.rect(screen, (255, 255, 255), p.Rect(0, 0, 700, 145))
            text = my_font.render("DRAW", 1, (255, 0, 0))
            screen.blit(text, (170, 10))

            time.sleep(0.2)

        else:
            draw_board(screen)
            draw_pieces(screen, board)
            text = my_font.render("3 in row", 1, (255, 0, 0))
            screen.blit(text, (90, 10))

        draw_button(screen)
        clock.tick(MAX_FPS)
        p.display.flip()


def reset(screen):
    board = [["-", "-", "-"],
             ["-", "-", "-"],
             ["-", "-", "-"]
             ]
    moves = 0
    x_to_move = True
    screen.fill(p.Color("white"))
    playing = True
    return board, moves, x_to_move, playing


def draw_board(screen):
    color1 = (255, 255, 255)
    color2 = (0, 0, 0)
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            p.draw.rect(screen, color1, p.Rect(j*SS+50, i*SS+150, SS, SS))
            p.draw.rect(screen, color2, p.Rect(j*SS+50, i*SS+150, SS, SS), 5, 100)


def color_squares(squares, screen):
    color1 = (255, 0, 0)
    color2 = (0, 0, 0)
    for i in range(len(squares)):
        p.draw.rect(screen, color1, p.Rect(squares[i][1]*SS+50, squares[i][0]*SS+150, SS, SS))
        p.draw.rect(screen, color2, p.Rect(squares[i][1]*SS+50, squares[i][0]*SS+150, SS, SS), 5)


def draw_pieces(screen, board):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if board[i][j] != "-":
                screen.blit(IMAGES[board[i][j]], p.Rect(j*SS+SS//6+50, i*SS+SS//6+150, SS, SS))


def draw_button(screen):
    p.draw.rect(screen, (200, 200, 200), p.Rect(550, 760, 100, 30))
    my_font = p.font.SysFont("algerian", 30)
    text = my_font.render("RESET", True, (255, 255, 255))
    screen.blit(text, (553, 758))


def check_win(matrix):
    col_matrix, diagonals = transform_matrix(matrix)
    for i in range(3):
        if len(set(matrix[i])) == 1 and set(matrix[i]) != {'-'}:
            return (i, 0), (i, 1), (i, 2)
        elif len(set(col_matrix[i])) == 1 and set(col_matrix[i]) != {'-'}:
            return (0, i), (1, i), (2, i)

    if len(set(diagonals[0])) == 1 and set(diagonals[0]) != {'-'}:
        return (0, 0), (1, 1), (2, 2)
    elif len(set(diagonals[1])) == 1 and set(diagonals[1]) != {'-'}:
        return (0, 2), (1, 1), (2, 0)


def transform_matrix(board):
    m = []
    for i in range(len(board)):
        row = []
        for j in range(len(board[i])):
            row.append(board[j][i])
        m.append(row)

    d1 = []
    d2 = []
    for i in range(len(board)):
        d1.append(board[i][i])
        d2.append(board[i][len(board)-1-i])
    return m, [d1, d2]


"""class Circle:
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.CIRCLES = []
        for i in range(1, 13):
            self.CIRCLES.append(p.transform.scale(p.image.load("videos/" + str(i) + ".png"),
                                                  (SS - SS // 3, SS - SS // 3)))
        self.current_sprite = 0
        self.image = self.CIRCLES[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]


    def update(self):"""


if __name__ == "__main__":
    main()
