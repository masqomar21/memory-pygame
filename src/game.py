from asyncio.windows_events import NULL
from os import *
from time import *
from random import *
from tkinter import mainloop
from traceback import print_tb

import pygame
from pygame import *

from src.cards import *
from src.menu import *


class Game:
    def __init__(self):
        #font family
        self.WIDTH, self.HEIGTH = 1180, 700
        self.FPS = 60
        self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGTH))

        self.font_title = font.Font("font/njnaruto.ttf", 44)
        self.font_content = font.Font("font/njnaruto.ttf", 24)


        self.level = 1
        self.score = 0
        self.level_complete = False
        self.game_over = False
        # self.background = NULL
        self.playing, self.running = False, True
        self.theme = "jhutsu"
        
        
        #card
        self.card_list = [f for f in listdir("figure/"+self.theme) if path.join("figure/"+self.theme, f)]

        self.img_w, self.img_h = 128, 128
        self.pad = 20
        self.margin_top = 160
        self.cols = 4
        self.rows = 2

        self.card_grup = pygame.sprite.Group()
        #flip & timing
        self.flipped = []
        self.frame_count = 0
        self.block_game = False

        self.time = self.level * 30
        self.back_up_time = 1 * 10
        self.time_counter = 0
        self.end_time = False
        self.generete_level(self.level)
        # self.coundown()
        


        #color
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GRY = (128, 128, 128)

        #menu
        self.main_menu = Main_menu(self)
        self.theme_menu = theme(self)
        self.cur_menu = self.main_menu



    def update(self, event_list):
        self.draw()
        self.input_user(event_list)
        # self.coundown()
        self.cek_complete(event_list)

    def cek_complete(self, event_list):
        # self.coundown()
        if not self.end_time :
            if not self.block_game :
                for event in event_list :
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
                        for card in self.card_grup :
                            if card.rect.collidepoint(event.pos)  :
                                self.flipped.append(card.name)
                                card.show()
                                if len(self.flipped) == 2 :
                                    if self.flipped[0] != self.flipped[1] :
                                        self.block_game = True
                                    else :
                                        self.flipped = [] 
                                        for card in self.card_grup :
                                            if card.shown :
                                                self.level_complete = True
                                                self.time_reset()
                                            else :
                                                self.level_complete = False
                                                break
            else :
                self.frame_count += 1
                # print (self.frame_count)
                if self.frame_count == self.FPS :
                    self.frame_count = 0
                    self.block_game = False

                    for card in self.card_grup :
                        if card.name in self.flipped :
                            card.hide()
                    self.flipped = []
        else :
            self.game_over = True
            self.playing = False
            


    def input_user(self,event_list):
        for event in event_list :
            # self.coundown()
            if event.type == pygame.MOUSEBUTTONDOWN :
               if self.level_complete :
                   self .time_reset()
                   self.level += 1
                   self.time = self.level * 10
                   if self.level > 5 :
                        self.level = 1
                   self.generete_level(self.level)

            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE and self.level_complete :
                    self.playing = False

    def generete_level(self, level):
        self.card = self.random_select_card(self.level)
        self.level_complete = False
        self.rows = self.level +1
        self.cols= 4
        self.coundown()
        self.generate_card(self.card)
    
    def generate_card(self, cards):
        self.cols = self.rows = self.cols if self.cols >= self.rows else self.rows
        
        CARD_W = (self.img_w * self. cols + self.pad *3)
        LEFT_MARGIN = RIGHT_MARGIN = (self.WIDTH - CARD_W) // 2

        self.card_grup.empty()
        
        for i in range(len(cards)) :
            posx = LEFT_MARGIN + ((self.img_w + self.pad) * (i % self.cols))
            posy = self.margin_top + (i // self.rows * (self.img_h + self.pad))
            card  = Cards(cards[i], posx, posy, self.theme)
            self.card_grup.add(card)


    def random_select_card(self, level):
        card = sample(self.card_list, (self.level + self.level +2))
        copy_card = card.copy()
        card.extend(copy_card)
        shuffle(card)
        return card

    def coundown(self):
        
        self.time_counter += 1
        if self.time_counter % self.FPS == 0 :
            self.time -= 1
            mins, secs = divmod(self.time, 60)
            self.time_format = "%02d:%02d" % (mins, secs)
            print("time left : ",self.time_format, end = "\r")
            self.time_counter = 0
            if self.time == 0 :
                self.time_counter = 0
                self.end_time = True
                self.time = self.back_up_time

    def time_reset(self):
        self.time_counter = 0
        self.time_format = "%02d:%02d" % (0, 0)
        self.end_time = False





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

        

        if not self.level == 5 :
            next_level_text = self.font_content.render("Level Complete, klik the right button to next level", True, (self.WHITE))
        else :
            next_level_text = self.font_content.render("Game Complete, press space for back to main menu", True, (self.WHITE))
        text_rect = next_level_text.get_rect(midtop = (self.WIDTH // 2, self.HEIGTH - 90))

        #draw card
        self.card_grup.draw(self.SCREEN)
        self.card_grup.update()

        if self.level_complete :
            self.SCREEN.blit(next_level_text, text_rect)

