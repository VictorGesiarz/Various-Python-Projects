import pygame as p

images = [[], []]


def load_images(ss):
    for i in range(1, 14):
        if i != 13:
            images[1].append(
                p.transform.scale(p.image.load("videos/Circle/" + str(i) + ".png"), (ss, ss)))
        images[0].append(
            p.transform.scale(p.image.load("videos/Cruz/" + str(i) + ".png"), (ss, ss)))


def make_fog(screen, text):
    text_pos = (600, 300)
    if text == "DRAW":
        text_pos = (620, 300)
    s = p.Surface((720, 720))  # the size of your rect
    s.set_alpha(150)  # alpha level
    s.fill((44, 61, 67))  # this fills the entire surface
    screen.blit(s, (380, 0))  # (0,0) are the top-left coordinate
    my_font = p.font.SysFont("arial black", 72)
    text = my_font.render(text, True, (255, 255, 255))
    screen.blit(text, text_pos)


def print_state(screen, b, squares):
    for i in range(3):
        for j in range(3):
            if b.board[i][j] == "O":
                screen.blit(images[1][-1], squares[i][j])
            if b.board[i][j] == "X":
                screen.blit(images[0][-1], squares[i][j])


class DrawXO(p.sprite.Sprite):
    def __init__(self, pox_x, pos_y, moves):
        super().__init__()
        self.turn = moves % 2
        self.is_animating = False
        self.counter = 0

        self.is_fog = False
        self.display_text = ""

        self.current_sprite = 0
        self.array = images[self.turn]
        self.image = self.array[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pox_x, pos_y]

    def animate_draw(self):
        self.is_animating = True
        self.counter = 0

    def fog(self, text):
        self.is_fog = True
        self.display_text = text

    def update(self, screen, b):
        if self.is_animating:
            self.counter += 1
            self.current_sprite += 1

            if self.counter >= len(self.array):
                self.current_sprite = 0

            if self.counter == 45:
                self.counter = 0
                self.is_animating = False

                if b.ai_playing and self.turn == 0:
                    b.play_ai = True

            self.image = self.array[int(self.current_sprite)]

            if self.is_fog and not self.is_animating:
                make_fog(screen, self.display_text)
