from asyncio.windows_events import NULL
from itertools import starmap
import pygame
from pygame import *



class Menu():
    hover = False
    def __init__ (self, game) :
        self.game = game
        self.min_width = self.game.WIDTH // 2,
        self.min_height = self.game.HEIGTH // 2
        self.font_color = self.game.WHITE
        self.GRAY = (100, 100, 100)

        # self. run_display = True

        self.cursor_rect = Rect(0, 0, 20, 20)
        self.offset = 100

    def cek_hover(self) :
        if self.hover :
            self.font_color = self.game.RED
            
        else :
            self.font_color = self.game.WHITE

    def draw_rect(self, rect, posx, posy) :
        Rect = rect.get_rect(midtop = (posx, posy))
        return Rect

    def blit_menu(self, text, tetx_rect) :
        self.game.SCREEN.blit(text, tetx_rect)

    def blit_screen(self):
        display.update()


class Main_menu(Menu) :
    def __init__(self, game) :
        Menu.__init__(self, game)
        self.main_menu_rect = NULL
        self.start_rect = NULL
        self.theme_rect = NULL
        self.quit_rect = NULL
        self.state = "main"
        self.startx, self.starty = self.game.WIDTH // 2, 180

        self.themex, self.themey = self.game.WIDTH // 2, 220
        self.quitx, self.quity = self.game.WIDTH // 2, 260

        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def draw_menu(self) :
        
        main_menu = self.game.font_title.render("Main Menu", True, self.font_color)
        start_game = self.game.font_content.render("Start Game", True, self.font_color)
        theme = self.game.font_content.render("Game Theme", True, self.font_color)
        quit_game = self.game.font_content.render("Quit Game", True, self.font_color)

        #rect 
        self.main_menu_rect = self.draw_rect(main_menu, self.game.WIDTH // 2, 100)
        self.start_rect = self.draw_rect(start_game, self.startx, self.starty)
        self.theme_rect = self.draw_rect(theme, self.themex, self.themey)
        self.quit_rect = self.draw_rect(quit_game, self.quitx, self.quity)

        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

        self.blit_menu(main_menu, self.main_menu_rect)
        self.blit_menu(start_game, self.start_rect)
        self.blit_menu(theme, self.theme_rect)
        self.blit_menu(quit_game, self.quit_rect)

    def cursor_move(self) :
        for event in self.game.event_list :
            if event.type == pygame.MOUSE :
                if self.start_rect.collidepoint(event.pos) :
        
                    self.hover = True
                    
                elif Rect(self.theme_rect).collidepoint(event.pos) :
                    self.hover = True
                elif Rect(self.quit_rect).collidepoint(event.pos) :
                    self.hover = True
                else : 
                    self.hover = False

            self.cek_hover()

            

        self.blit_screen()



     
       
    def input_menu(self):
        for event in self.game.event_list :
            if event.type == pygame.MOUSEBUTTONDOWN :
                print(self.game.HEIGTH)
                print(self.min_height)
                print("ok")
        pass

    def update(self) :
        self.draw_menu()
        self.cursor_move()
        self.input_menu()

# class theme(menu):
    # def __init__(self)
