from turtle import back
from pygame import *

def screen_init(width, height):
    
    White = (255, 255, 255)
    black = (0, 0, 0)

    fps = 60
    timer = time.Clock()
    # Initialize the screen
    screen = display.set_mode((width, height))
    display.set_caption("Game")

    running = True
    while running :
        timer.tick(fps)
        screen.fill(White)

        for even in event.get():
            if even.type == QUIT:
                running = False


        display.flip()
