from asyncio.windows_events import NULL
from itertools import starmap
import pygame
from pygame import *
from abc import ABC, abstractmethod, ABCMeta


class Menu( ABC):
    hover = False
    def __init__ (self, game) :
        self.font_menu = font.Font("font/njnaruto.ttf", 100)
        self.font_menu_content = font.Font("font/njnaruto.ttf", 60)
        self.GRAY = (100, 100, 100)
        self.sky_blue = (135, 206, 250)
        self.game = game
        self.min_width = self.game.WIDTH / 2
        self.min_height = self.game.HEIGTH / 2
        self.font_color = self.game.WHITE
        self.rect_color = self.GRAY
        self.state = 'main'


    def get_rect(self, rect, posx, posy) :
        Rect = rect.get_rect(midtop = (posx, posy))
        return Rect

    def blit_menu(self, text, tetx_rect) :
        self.game.SCREEN.blit(text, tetx_rect)

    def blit_screen(self):
        display.update()

    def draw_rect(self,color, posx, posy, w, h, border_raduis) :
        return draw.rect(self.game.SCREEN, color, (posx, posy, w, h), border_radius= border_raduis)

    
    def cek_hover(self) :
        if self.hover :
            self.rect_color = self.sky_blue
            
        else :
            self.rect_color = self.GRAY

   


class Main_menu(Menu) :
    def __init__(self, game) :
        Menu.__init__(self, game)
        self.w, self.h = 140, 30
        self.off = self.w / 2

        self.startx, self.starty = (self.min_width - self.off), 180
        self.themex, self.themey = (self.min_width - self.off), 230
        self.quitx, self.quity = (self.min_width - self.off), 280

    def draw_menu(self) :
        # text
        main_menu = self.font_menu.render("Main Menu", True, self.font_color)
        start_game = self.font_menu_content.render("Start Game", True, self.font_color)
        theme = self.font_menu_content.render("Game Theme", True, self.font_color)
        quit_game = self.font_menu_content.render("Quit Game", True, self.font_color)

        #rect 
        self.main_menu_rect = self.get_rect(main_menu, self.min_width, 100)
        self.start_rect = self.draw_rect(self.rect_color, self.startx, self.starty, self.w, self.h, 8 )
        self.theme_rect = self.draw_rect(self.rect_color, self.themex, self.themey, self.w, self.h, 8 )
        self.quit_rect =  self.draw_rect(self.rect_color, self.quitx, self.quity, self.w, self.h, 8 )

        #blit
        self.blit_menu(main_menu, self.main_menu_rect)
        self.blit_menu(start_game, self.start_rect)
        self.blit_menu(theme, self.theme_rect)
        self.blit_menu(quit_game, self.quit_rect)


    def cursor_move(self) :
        for event in self.game.event_list :
            if event.type == pygame.MOUSEMOTION and not self.hover :
                if self.start_rect.collidepoint(event.pos) :
                    self.hover = True
                elif Rect(self.theme_rect).collidepoint(event.pos) :
                    self.hover = True
                elif Rect(self.quit_rect).collidepoint(event.pos) :
                    self.hover = True
                self.blit_screen()
            else : 
                self.hover = False
            self.blit_screen()
    
    def input_menu(self, event_list) :
        for event in event_list :
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
                if self.start_rect.collidepoint(mouse.get_pos()) :
                    self.state = 'game'
                elif self.theme_rect.collidepoint(mouse.get_pos()) :
                    self.state = "theme"
                elif self.quit_rect.collidepoint(mouse.get_pos()) :
                    self.state = "quit"
                self.cek_state(event_list)

    def cek_state(self, event_list) :
        print(self.state)
        if self.state == 'main' :
            self.update(event_list)
        elif self.state == 'theme' :
            self.game.cur_menu = self.game.theme_menu
        elif self.state == 'game' :
            self.game.playing = True
        elif self.state == 'quit' :
            self.game.playing = False
            self.game.running = False

    def update(self, event_list) :
        self.draw_menu()
        self.input_menu(event_list)

class theme(Menu):
    def __init__(self, game) :
        Menu.__init__(self, game)
        self.game = game
        # rect pos
        self.rect_color = self.game.WHITE
        self.w, self.h = 150, 150
        self.theme1x = self.min_width - 200
        self.theme2x = self.min_width + 65
        # quit pos
        self.quitx, self.quity = self.min_width - 65/2, self.min_height +100

    def draw_menu(self) :
        # text
        game_theme = self.game.font_title.render("Game Theme", True, self.font_color)
        quit = self.game.font_content.render("Quit", True, self.font_color)

        #rect
        self.theme_rect = self.get_rect(game_theme, self.min_width, 100)
        self.theme1_rect = self.draw_rect(self.rect_color, self.theme1x, self.min_height-105, self.w, self.h, 8 )
        self.theme2_rect = self.draw_rect(self.rect_color, self.theme2x, self.min_height-105, self.w, self.h, 8 )
        self.quit_rect = self.draw_rect(self.GRAY, self.quitx, self.quity, 65, 30, 8 )

        #blit
        self.blit_menu(game_theme, self.theme_rect)
        self.blit_menu(quit, self.quit_rect)


    def input_menu(self, event_list) :
        for event in event_list :
            if event.type == pygame.MOUSEBUTTONDOWN :
                if Rect(self.theme1_rect).collidepoint(event.pos) :
                    self.game.theme = 1
                elif Rect(self.theme2_rect).collidepoint(event.pos) :
                    self.game.theme = 2
                if Rect(self.quit_rect).collidepoint(event.pos) :
                    self.game.cur_menu = self.game.main_menu

    def update(self,event_list) :
        self.draw_menu()
        self.input_menu(event_list)




