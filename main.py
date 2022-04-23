from pygame import *
from src.game import *


init()
WIDTH = 800
HEIGHT = 600

White = (255, 255, 255)
black = (0, 0, 0)

fps = 60
timer = time.Clock()
# Initialize the screen
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("remaider game")

game = Game()

running = True
while running :
    timer.tick(fps)
    screen.fill(black)

    event_list = event.get()
    for even in event_list :
        if even.type == QUIT:
            running = False
    
    game.update(event_list, HEIGHT, WIDTH, screen)

    display.update()
    display.flip()


quit()

