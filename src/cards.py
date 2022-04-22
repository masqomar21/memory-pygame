from asyncio.windows_events import NULL
from pygame import *
from random import *


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Cards(sprite.Sprite) :
    def __init__(self) -> None:
        super().__init__()
        self.image = NULL
        self.card_opened = False
    
    def open_card(self, card_image)
        self.image = card_image
        self.card_opened = True
        pass

    def generet_image(self) :
        pass

    def close_card(self) : 
        pass