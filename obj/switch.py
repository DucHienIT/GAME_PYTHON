import pygame
from obj.define import *

class switch:
    SWITCH_IMG_Exit = pygame.transform.scale(pygame.image.load('assets/img/arrow.png'), (SWITCH_SIZE, SWITCH_SIZE))
    SWITCH_IMG_Dungeon = pygame.transform.scale(pygame.image.load('assets/img/dungeon.png'), (SWITCH_SIZE, SWITCH_SIZE))

    
    def __init__(self, x , y):
        self.x = x
        self.y = y