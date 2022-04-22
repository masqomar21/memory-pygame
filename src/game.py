from pygame import *
from random import *
from os import *


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


class Game:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.level_complete = False

    def update(self, event_list, height, width, screen):
        global HEIGHT
        HEIGHT = height
        global WIDTH
        WIDTH = width
        global SCREEN
        SCREEN = screen

        self.input_user(event_list)
        self.draw()
        pass

    def input_user(self, event_list):
        pass


    def generete_level(self):
        pass

    def draw (self):
        #font family
        font_title = font.Font("font/njnaruto.ttf", 44)
        font_content = font.Font("font/njnaruto.ttf", 24)

        #text
        title_text = font_title.render("NARUTO REMAIDER", True, WHITE)
        title_rect = title_text.get_rect(midtop = (WIDTH // 2, 10))

        level_text = font_content.render("Level: " + str(self.level), True, (WHITE))
        level_rect = level_text.get_rect(midtop = (WIDTH // 2 - 200, 80))

        score_text = font_content.render("Score: " + str(self.score), True, (WHITE))
        score_rect = score_text.get_rect(midtop = (WIDTH // 2 + 200, 80))

        info_text = font_content.render("Cari 2 kartui yang sama", True, (WHITE))
        info_rect = info_text.get_rect(midtop = (WIDTH // 2, 120))


        SCREEN.blit(title_text, title_rect)
        SCREEN.blit(level_text, level_rect)
        SCREEN.blit(score_text, score_rect)
        SCREEN.blit(info_text, info_rect)

