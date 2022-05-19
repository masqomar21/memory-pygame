from os import *
from time import *
from random import *
import cv2


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

        self.cek = False
        self.h = 240
        self.w = 470

        self.img_level_complete = pygame.image.load("figure/level_complete.png")
        self.cek_page_complete = False

    def add_score(self):
        self.__score += self.score_adding

    def min_score(self):
        if self.__score <= 0 :
            self.__score = 0
        else :
            self.__score -= 1

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
                                if self.cek_page_complete :
                                    self.cek_page_complete = False
                                else :
                                    if not card.shown :
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
                                                        self.cek = True
                                                        self.time_reset()
                                                    else :
                                                        self.level_complete = False
                                                        self.cek = False
                                                        break
            else :
                self.frame_count += 1
                if self.frame_count == self.FPS :
                    self.min_score()
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
                    if self.btn_next_level.collidepoint(event.pos) :
                        self.cek = True
                        self .time_reset()
                        self.level += 1
                        self.time = self.level * 30
                        if self.level > 5 :
                            self.level = 1
                            self.game_reset()
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
        
        CARD_W = (self.img_w * self. cols + self.pad *(self.cols - 1))
        LEFT_MARGIN = RIGHT_MARGIN = (self.WIDTH - CARD_W) // 2

        self.card_grup.empty()
        
        for i in range(len(cards)) :
            posx = LEFT_MARGIN + ((self.img_w + self.pad) * (i % self.cols))
            posy = self.margin_top + (i // self.rows * (self.img_h + self.pad))
            card  = Cards(cards[i], posx, posy, self.theme)
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


    def level_complete_page(self):
        posx, posy = self.WIDTH // 2, 50
        self.level_complete_page_rect = self.img_level_complete.get_rect(midtop = (posx, posy))
        self.btn_next_level = draw.rect(self.SCREEN, (0, 0, 0), ((self.WIDTH // 2)-150, (self.HEIGTH // 2) + 85, 135, 60), border_radius=15)
        self.SCREEN.blit(self.img_level_complete, self.level_complete_page_rect)


    def draw (self):
        if self.cek :
            if self.level == 2 :
                self.h = 350
            elif self.level == 3 :
                self.h = 465
            elif self.level == 4 :
                self.w = 580
            elif self.level == 5 :
                self.w = 690

            print(self.level)
            self.cek = False

        self.draw_background()

        self.card_backgrund = draw.rect(self.SCREEN, self.GRY, ((self.WIDTH - self.w)/2, 150, self.w, self.h), border_radius= 15)
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

        if self.level == 5 :
            self.img_level_complete = image.load('figure/game_complete.png')

        #draw card
        self.card_grup.draw(self.SCREEN)
        # self.card_backgrund = draw.rect(self.SCREEN, self.GRY, ((self.WIDTH - self.w)/2, 150, self.w, self.h), border_radius= 15)
        self.card_grup.update()

        if self.level_complete :
            self.level_complete_page()
            self.cek_page_complete = True

