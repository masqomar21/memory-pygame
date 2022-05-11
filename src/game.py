from asyncio.windows_events import NULL
from os import *
from time import *
from random import *
import cv2
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

        # leveling and score
        self.level = 1
        self.__score = 0
        self.score_adding = 10
        self.level_complete = False
        self.game_over = False
        self.playing, self.running = False, True
       
       #theme
        self.cek_theme = 1
        self.cek_start = False
    
        #card position
        self.img_w, self.img_h = 100, 100
        self.pad = 15
        self.margin_top = 160
        self.cols = 4
        self.rows = 2

        #flip & timing
        self.flipped = []
        self.frame_count = 0
        self.block_game = False


        #countdown time
        self.time = self.level * 30
        self.back_up_time = 1 * 30
        self.time_counter = 0
        self.end_time = False
        
        self.get_background()
        self.theme_update = False

        #color
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GRY = (128, 128, 128)

        #menu
        self.main_menu = Main_menu(self)
        self.theme_menu = theme(self)
        self.cur_menu = self.main_menu

        #music
        pygame.mixer.music.load("sounds/bg-music.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play()


        self.time_reset()


    def add_score(self):
        self.__score += self.score_adding

    def game_init(self):
        cek = True
        self.check_theme()
        if cek :
            print ("theme : ", self.theme)
            cek = False
        

        #card
        self.card_list = [f for f in listdir("figure/"+self.theme) if path.join("figure/"+self.theme, f)]
        self.card_grup = pygame.sprite.Group()
        self.generete_level(self.level)
     
    def update(self, event_list):
        if self.level == 1 and not self.cek_start :
            self.game_init()
            self.cek_start = True
        # self.time_reset()
        self.draw()
        self.check_theme()
        self.input_user(event_list)
        self.cek_complete(event_list)
        
    def cek_complete(self, event_list):
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
                                        self.add_score()
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
            self.game_reset()

    def game_reset(self):
        self.level = 1
        self.__score = 0
        self.level_complete = False
        self.game_over = False
        self.playing, self.running = False, True

        self.end_time = False

        self.game_init()
        
        
    def input_user(self,event_list):
        for event in event_list :
            if event.type == pygame.MOUSEBUTTONDOWN :
               if self.level_complete :
                    self .time_reset()
                    self.level += 1
                    self.time = self.level * 30
                    if self.level > 5 :
                        self.level = 1
                    self.generete_level(self.level)
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE and self.level_complete :
                    self.playing = False
        self.coundown()

    def generete_level(self, level):
        self.card = self.random_select_card(self.level)
        self.level_complete = False
        self.rows = self.level +1
        self.cols= 4
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
            print (card.name)
            self.card_grup.add(card)
        print ("\n")


    def random_select_card(self, level):
        card = sample(self.card_list, (self.level + self.level +2))
        copy_card = card.copy()
        card.extend(copy_card)
        shuffle(card)
        return card

    def coundown(self):
        self.time_counter += 1
        if not self.level_complete :
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

       
    def check_theme(self) :
        self.theme_update = False
        if self.cek_theme == 1 :
            self.theme = "jhutsu"
            self.theme_update = True
        elif self.cek_theme == 2 :
            self.theme = "ciby"
            self.theme_update = True


    def get_background(self):
        self.check_theme()
        self.img = cv2.imread('figure/bg/' + self.theme + '.png')
        self.img = cv2.resize(self.img,dsize=(self.WIDTH, self.HEIGTH))
        self.success = True
        self.shape = self.img.shape[1::-1]


    def draw_background(self):
        if self.success :
            self.SCREEN.blit(image.frombuffer(self.img.tobytes(), self.shape, 'BGR'), (0, 0))
        else :
            self.get_background()
       


    def draw (self):
       
        self.draw_background()
        #text
        title_text = self.font_title.render("NARUTO REMAIDER", True, self.BLACK)
        title_rect = title_text.get_rect(midtop = (self.WIDTH // 2, 10))

        level_text = self.font_content.render("Level: " + str(self.level), True, (self.BLACK))
        level_rect = level_text.get_rect(midtop = (self.WIDTH // 2 - 200, 80))

        time_text = self.font_content.render(self.time_format, True, (self.BLACK))
        time_rect = time_text.get_rect(midtop = (self.WIDTH // 2 , 80))

        score_text = self.font_content.render("Score: " + str(self.__score), True, (self.BLACK))
        score_rect = score_text.get_rect(midtop = (self.WIDTH // 2 + 200, 80))

        info_text = self.font_content.render("Cari 2 kartui yang sama", True, (self.BLACK))
        info_rect = info_text.get_rect(midtop = (self.WIDTH // 2, 120))

        

        self.SCREEN.blit(title_text, title_rect)
        self.SCREEN.blit(level_text, level_rect)
        self.SCREEN.blit(time_text, time_rect)
        self.SCREEN.blit(score_text, score_rect)
        self.SCREEN.blit(info_text, info_rect)


        if not self.level == 5 :
            next_level_text = self.font_content.render("Level Complete, klik the right button to next level", True, (self.BLACK))
        else :
            next_level_text = self.font_content.render("Game Complete, press space for back to main menu", True, (self.BLACK))
        text_rect = next_level_text.get_rect(midtop = (self.WIDTH // 2, self.HEIGTH - 90))

        #draw card
        self.card_grup.draw(self.SCREEN)
        self.card_grup.update()

        if self.level_complete :
            self.SCREEN.blit(next_level_text, text_rect)

