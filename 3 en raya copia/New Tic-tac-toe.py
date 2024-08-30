import pygame as p
import Animation
import Rules
import BOTS
import menu_partida as mp

WIDTH = 1100
HEIGHT = 720
DIMENSION = 3
S_SEPARATION_WALL = 50
S_SEPARATION = 10
SS = (HEIGHT - S_SEPARATION_WALL * 2 - S_SEPARATION * 2) // DIMENSION
START_COLUMN = WIDTH - S_SEPARATION_WALL - SS * 3 - S_SEPARATION * 2

FPS = 60

COLORS = {"background grey": (44, 61, 67), "light blue": (140, 200, 222), "white": (255, 255, 255)}

text = [["TicTacToe", 80], ["CLASSIC", 35], ["Turn", 30], ["Player", 30], ["Computer", 30]]  # ["Play against:", 25]
text_pos = [(50, 60, 330, 70), (50, 130, 330, 50), (90, 250, 250, 50), (90, 470, 120, 40), (220, 470, 120, 40)]  # (90, 440, 250, 30)
text_rectangles = []

buttons_pos = [(220, 300, 120, 120), (90, 300, 120, 120), (90, 510, 120, 120), (220, 510, 120, 120)]
buttons_rectangle = []
button_images = []

squares = []


class Board:

    pieces = ['X', 'O']
    turn = "human"
    play_ai = False
    ai_playing = False
    BOTS.max_min = ["O", "X"]

    def __init__(self):
        self.board = [['-' for i in range(DIMENSION)] for j in range(DIMENSION)]
        self.pos = []
        self.moves = 0
        self.playing = True
        self.win = False


def main():
    p.init()
    p.display.set_caption("Tic-tac-toe")
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()

    Animation.load_images(SS)
    exes_and_ohs = p.sprite.Group()

    b = Board()

    load_squares()
    load_buttons_text()
    draw_board(screen, b)
    draw_moves(screen, b)

    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

            if event.type == p.MOUSEBUTTONDOWN:
                clicked_on_square, board_pos, screen_pos = detect_board_click()
                b = detect_button_click(screen, b)

                if clicked_on_square and b.playing and b.turn == "human":

                    if b.board[board_pos[0]][board_pos[1]] == '-':
                        b.pos.append(screen_pos)
                        b.board[board_pos[0]][board_pos[1]] = b.pieces[b.moves % 2]

                        piece = Animation.DrawXO(b.pos[b.moves][0], b.pos[b.moves][1], b.moves)
                        exes_and_ohs.add(piece)
                        piece.animate_draw()

                        b.win = Rules.check_win(b.board)

                        b.moves += 1

                        if b.win:
                            piece.fog(b.pieces[(b.moves-1) % 2] + " WINS")
                            b.playing = False

                        elif b.moves == DIMENSION**2:
                            piece.fog("DRAW")
                            b.playing = False

                        b.turn = "AI" if b.ai_playing else "human"

                        draw_moves(screen, b)

            if event.type == p.KEYDOWN:
                if event.key == p.K_BACKSPACE:
                    cons = b.ai_playing
                    b = Board()
                    b.ai_playing = cons
                    exes_and_ohs.empty()
                    draw_board(screen, b)
                    draw_moves(screen, b)
                if event.key == p.K_ESCAPE:
                    mp.in_game_menu(screen, clock)
                    draw_board(screen, b)
                    draw_moves(screen, b)
                    Animation.print_state(screen, b, squares)

        if b.turn == "AI" and b.play_ai and b.playing:
            bot_pos = BOTS.find_best_move(b)
            b.board[bot_pos[0]][bot_pos[1]] = b.pieces[b.moves % 2]
            screen_pos = squares[bot_pos[0]][bot_pos[1]]
            b.pos.append(screen_pos)

            piece = Animation.DrawXO(b.pos[b.moves][0], b.pos[b.moves][1], b.moves)
            exes_and_ohs.add(piece)
            piece.animate_draw()

            b.moves += 1

            b.win = Rules.check_win(b.board)

            if b.win:
                piece.fog(b.pieces[(b.moves-1) % 2] + " WINS")
                b.playing = False

            b.play_ai = False
            b.turn = "human"

            draw_moves(screen, b)

        exes_and_ohs.draw(screen)
        exes_and_ohs.update(screen, b)
        p.display.flip()
        clock.tick(FPS)


def load_squares():
    for i in range(DIMENSION):
        row = []
        for j in range(DIMENSION):
            square = p.Rect(START_COLUMN + (j*SS + S_SEPARATION*j),
                            i*SS + S_SEPARATION*i + S_SEPARATION_WALL,
                            SS, SS)
            row.append(square)
        squares.append(row)


def load_buttons_text():
    for i in text_pos:
        rectangle = p.Rect(i[0], i[1], i[2], i[3])
        text_rectangles.append(rectangle)

    button_images.append(p.image.load("images/O.png"))
    button_images.append(p.image.load("images/X.png"))
    button_images.append(p.transform.scale(p.image.load("images/Brain.png"), (90, 90)))
    button_images.append(p.image.load("images/Computer.png"))
    for j in buttons_pos:
        rectangle = p.Rect(j[0], j[1], j[2], j[3])
        buttons_rectangle.append(rectangle)


def draw_moves(screen, b):
    p.draw.rect(screen, COLORS["white"], buttons_rectangle[b.moves % 2], 7, 20)
    p.draw.rect(screen, COLORS["light blue"], buttons_rectangle[(b.moves-1) % 2], 7, 20)


def draw_options(screen):
    for i in range(len(text_rectangles)):
        rect_obj = p.draw.rect(screen, COLORS["background grey"], text_rectangles[i])
        my_font = p.font.SysFont("helvetica", text[i][1], bold=True).render(text[i][0], True, COLORS["white"])
        text_rect = my_font.get_rect(center=rect_obj.center)
        screen.blit(my_font, text_rect)

    for j in range(len(buttons_rectangle)):
        rect_obj = p.draw.rect(screen, COLORS["white"], buttons_rectangle[j], 0, 20)
        rect = button_images[j].get_rect(center=rect_obj.center)
        screen.blit(button_images[j], rect)


def draw_board(screen, b):
    screen.fill(COLORS["background grey"])

    for i in range(DIMENSION):
        for j in range(DIMENSION):
            p.draw.rect(screen, COLORS["light blue"], (squares[i][j]), 0, 15)

    draw_options(screen)

    if b.ai_playing:
        p.draw.rect(screen, COLORS["light blue"], buttons_rectangle[3], 7, 20)
    else:
        p.draw.rect(screen, COLORS["light blue"], buttons_rectangle[2], 7, 20)


def detect_board_click():
    lx, ly = p.mouse.get_pos()
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            square = squares[i][j]
            sx = square[0]
            sy = square[1]
            if sx < lx < (sx + SS) and sy < ly < (sy + SS):
                return True, (i, j), (sx, sy)
    return False, None, None


def detect_button_click(screen, b):
    lx, ly = p.mouse.get_pos()
    bx, by, sb = buttons_rectangle[3][0], buttons_rectangle[3][1], buttons_rectangle[3][2]

    if bx < lx < bx + sb and by < ly < by + sb:
        b = Board()
        b.ai_playing = True
        draw_board(screen, b)
        draw_moves(screen, b)

    bx, by, sb = buttons_rectangle[2][0], buttons_rectangle[2][1], buttons_rectangle[2][2]

    if bx < lx < bx + sb and by < ly < by + sb:
        b = Board()
        b.ai_playing = False
        draw_board(screen, b)
        draw_moves(screen, b)
    return b


if __name__ == '__main__':
    main()
