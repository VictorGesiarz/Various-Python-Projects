import pygame as p


class Circle(p.sprite.Sprite):
    def __init__(self, pox_x, pos_y, ss):
        super().__init__()
        self.images = []
        self.is_animating = False
        for i in range(1, 13):
            self.images.append(p.transform.scale(p.image.load("videos/" + str(i) + ".png"), (ss-ss//3, ss-ss//3)))
        self.current_sprite = 12
        self.image = self.images[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pox_x, pos_y]

    def animate(self):
        self.is_animating = True

    def update(self):
        if self.is_animating:
            self.current_sprite -= 1

            if self.current_sprite >= len(self.images):
                self.current_sprite = 0
                self.is_animating = False

            self.image = self.images[int(self.current_sprite)]


HEIGHT = 800
WIDTH = 800
SS = 400

FPS = 60

colors = {"white": (255, 255, 255), "black": (0, 0, 0)}


def main():
    p.init()
    p.display.set_caption("Sprites")
    screen = p.display.set_mode((HEIGHT, WIDTH))
    screen.fill(colors["black"])
    clock = p.time.Clock()

    circle = Circle(50, 50, SS)

    circles = p.sprite.Group()
    circles.add(circle)

    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

            if event.type == p.MOUSEBUTTONDOWN:
                circle.animate()

        circles.draw(screen)
        circle.update()
        p.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
