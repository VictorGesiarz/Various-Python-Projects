import pygame as p

SCREEN_HEIGHT = 900
SCREEN_WIDTH = 800
BOARD_HEIGHT = 600
BOARD_WIDTH = 700
UPPER_HEIGHT_DIFF = (SCREEN_HEIGHT - BOARD_HEIGHT) * 2 // 3
LOWER_HEIGHT_DIFF = (SCREEN_HEIGHT - BOARD_HEIGHT) // 3
WIDTH_DIFF = (SCREEN_WIDTH - BOARD_WIDTH) // 2
dim_y = 6
dim_x = 7
SS = BOARD_WIDTH // dim_x
MAX_FPS = 30

player_move = [0, 1]
player_colors = ((255, 0, 0), (255, 200, 0))


def main():
    p.init()
    screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill((100, 100, 100))
    p.display.set_caption("Connect 4")
    text(screen, "Connect 4", (50, 60), p.font.SysFont("college", 130))
    clock = p.time.Clock()

    b = Board()

    running = True
    while running:

        location = p.mouse.get_pos()
        is_in_range = (WIDTH_DIFF < location[0] < (SCREEN_WIDTH - WIDTH_DIFF)) and \
                      (UPPER_HEIGHT_DIFF < location[1] < (SCREEN_HEIGHT - LOWER_HEIGHT_DIFF))

        for event in p.event.get():

            if event.type == p.QUIT:
                running = False

            elif event.type == p.MOUSEBUTTONDOWN:

                if is_in_range:
                    col = (location[0] - WIDTH_DIFF) // SS
                    row = possible_squares(b, col)

                    if row and b.playing:
                        b.board[row-1][col] = player_move[b.moves % 2]
                        b.col_board[col][row-1] = player_move[b.moves % 2]

                        if check_win(b, row-1, col):
                            draw_winner(screen, player_colors[b.moves % 2])
                            b.playing = False

                        b.moves += 1

                        if b.playing and b.moves == 42:
                            p.draw.rect(screen, (50, 50, 50), p.Rect(525, 60, 225, 100))
                            text(screen, "DRAW", (530, 75), p.font.SysFont("college", 100))

        keys = p.key.get_pressed()
        if keys[p.K_BACKSPACE]:
            b = Board()
            screen.fill((100, 100, 100))
            text(screen, "Connect 4", (50, 60), p.font.SysFont("college", 130))

        draw_board(screen, b.board)

        if b.playing and is_in_range:
            draw_circle_mouse(b, screen, location)

        clock.tick()
        p.display.flip()


def draw_winner(screen, color):
    p.draw.rect(screen, color, p.Rect(550, 60, 200, 90))
    display_text = "WINS"
    font = p.font.SysFont("college", 100)
    pos = (555, 75)
    text(screen, display_text, pos, font)


def text(screen, display_text, pos, font):
    display_text = font.render(display_text, 1, (255, 255, 255))
    screen.blit(display_text, pos)


def draw_board(screen, board):
    dark_gray = (50, 50, 50)

    for i in range(dim_y):
        for j in range(dim_x):
            if board[i][j] != "-":
                color = player_colors[board[i][j]]
            else:
                color = (200, 200, 200)

            p.draw.rect(screen, dark_gray, p.Rect((j * SS + WIDTH_DIFF, i * SS + UPPER_HEIGHT_DIFF, SS, SS)))
            circle_x = j*SS + SS//2 + WIDTH_DIFF
            circle_y = i*SS + SS//2 + UPPER_HEIGHT_DIFF
            p.draw.circle(screen, color, (circle_x, circle_y), SS//3)


def draw_circle_mouse(b, screen, location):
    col = (location[0] - WIDTH_DIFF) // SS
    row = possible_squares(b, col)

    if row:
        color = player_colors[b.moves % 2]
        circle_x = col * SS + SS // 2 + WIDTH_DIFF
        circle_y = (row - 1) * SS + SS // 2 + UPPER_HEIGHT_DIFF
        p.draw.circle(screen, color, (circle_x, circle_y), SS // 3)
        p.draw.circle(screen, (255, 255, 255), (circle_x, circle_y), SS // 3, 3)


def possible_squares(b, col):
    column = b.col_board[col]
    if "-" in column:
        for i in range(1, 7):
            if column[-i] == "-":
                return 7-i
    else:
        return False


def check_win(b, row, col):
    diagonal1, diagonal2 = get_diagonals(b, row, col)
    rows = [b.col_board[col], b.board[row], diagonal1, diagonal2]

    for i in range(4):
        if len(rows[i]) >= 4:
            for j in range(len(rows[i])-3):
                if rows[i][j] == rows[i][j+1] == rows[i][j+2] == rows[i][j+3] != "-":
                    return True
    return False


def get_diagonals(b, row, col):
    diagonal1 = []
    j = (col - row) if (col - row > 0) else 0
    i = (row - col) if (row - col > 0) else 0
    while i < dim_y and j < dim_x:
        diagonal1.append(b.board[i][j])
        i += 1
        j += 1

    diagonal2 = []
    j2 = (col + row) if (col + row < dim_x) else dim_x-1
    i2 = (col + row - dim_y) if (col + row - dim_y >= 0) else 0
    while i2 < dim_y and j2 >= 0:
        diagonal2.append(b.board[i2][j2])
        i2 += 1
        j2 -= 1

    return diagonal1, diagonal2


class Board:

    def __init__(self):
        self.board = [["-" for i in range(dim_x)] for j in range(dim_y)]
        self.col_board = [["-" for i in range(dim_y)] for j in range(dim_x)]
        self.moves = 0
        self.playing = True


if __name__ == '__main__':
    main()
