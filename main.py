from email.header import Header
from pygame import *
from src.screen import *

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

running = True
while running :
    timer.tick(fps)
    screen.fill(White)

    for even in event.get():
        if even.type == QUIT:
            running = False


    display.flip()


quit()

