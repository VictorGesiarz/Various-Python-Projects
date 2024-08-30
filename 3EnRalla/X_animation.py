import pygame as p


class X(p.sprite.Sprite):
    def __init__(self, pox_x, pos_y, ss):
        super().__init__()
        self.images = []
        self.is_animating = False
        for i in range(1, 14):
            self.images.append(p.transform.scale(p.image.load("videos/Cruz/" + str(i) + ".png"), (ss-ss//3, ss-ss//3)))
        self.current_sprite = 0
        self.image = self.images[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pox_x, pos_y]

    def animate(self):
        self.is_animating = True

    def update(self):
        if self.is_animating:
            self.current_sprite += 1

            if self.current_sprite >= len(self.images):
                self.current_sprite = 0
                self.is_animating = False

            self.image = self.images[int(self.current_sprite)]
