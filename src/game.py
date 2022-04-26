from asyncio.windows_events import NULL
from pygame import *
import pygame
from random import *
from os import *
from src.menu import *


class Game:
    def __init__(self):
        #font family
      
        self.font_title = font.Font("font/njnaruto.ttf", 44)
        self.font_content = font.Font("font/njnaruto.ttf", 24)

    
        self.level = 1
        self.score = 0
        self.level_complete = False
        self.game_over = False
        self.background = NULL #image.load("img/background.jpg")
        self.HEIGTH = 0
        self.WIDTH = 0
        self.SCREEN = NULL

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)

        #menu
        self.main_menu = NULL



        self.event_list = NULL

        

    def update(self, event_list, heigth, width, screen):

        self.HEIGTH = heigth
        self.WIDTH = width
        self.SCREEN = screen

        self.event_list = event_list
    
        self.main_menu = Main_menu(self)
        self.main_menu.update()
        # self.main_menu.draw_menu()
        # self.main_menu.input_menu()


        # self.input_user()
        # self.draw()
        pass

    def input_user(self,):
        for event in self.event_list :
            if event.type == pygame.MOUSEBUTTONDOWN :
                print("ok")
        pass


    def generete_level(self):
        pass

    def draw (self):
        
        #text
        title_text = self.font_title.render("NARUTO REMAIDER", True, self.WHITE)
        title_rect = title_text.get_rect(midtop = (self.WIDTH // 2, 10))

        level_text = self.font_content.render("Level: " + str(self.level), True, (self.WHITE))
        level_rect = level_text.get_rect(midtop = (self.WIDTH // 2 - 200, 80))

        score_text = self.font_content.render("Score: " + str(self.score), True, (self.WHITE))
        score_rect = score_text.get_rect(midtop = (self.WIDTH // 2 + 200, 80))

        info_text = self.font_content.render("Cari 2 kartui yang sama", True, (self.WHITE))
        info_rect = info_text.get_rect(midtop = (self.WIDTH // 2, 120))


        self.SCREEN.blit(title_text, title_rect)
        self.SCREEN.blit(level_text, level_rect)
        self.SCREEN.blit(score_text, score_rect)
        self.SCREEN.blit(info_text, info_rect)

