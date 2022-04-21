import pygame
from obj.define import *

class switch:
    SWITCH_IMG = pygame.transform.scale(pygame.image.load('assets/img/arrow.png'), (SWITCH_SIZE, SWITCH_SIZE))

    def __init__(self, x , y):
        self.x = x
        self.y = y