import pygame as p
import sys


def in_game_menu(screen, clock):

    s = p.Surface((1100, 720))  # the size of your rect
    s.set_alpha(150)  # alpha level
    s.fill((44, 61, 67))  # this fills the entire surface
    screen.blit(s, (0, 0))
    p.draw.rect(screen, (140, 200, 222), p.Rect(0, 0, 380, 720))
    my_font = p.font.SysFont("arial black", 72)
    text = my_font.render("Menu", True, (255, 255, 255))
    screen.blit(text, (50, 50))

    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if event.type == p.KEYDOWN:
                if event.key == p.K_ESCAPE:
                    running = False

        p.display.flip()
        clock.tick(60)
