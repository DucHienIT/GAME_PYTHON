from matplotlib import animation
import pygame
from obj.define import *
from obj.map import *
from obj.material import *
from random import randint
from random import choice

class equipment(pygame.sprite.Sprite):
    steps = DEFAULT_STEPS

    clock = pygame.time.Clock()
    def __init__(self, Image, materialList, type):
        pygame.sprite.Sprite.__init__(self)

        self.atk = AttributeEquidList[type][0]
        self.defen = AttributeEquidList[type][1]
        self.hp = AttributeEquidList[type][2] 
        
        self.type = type

        self.img = pygame.transform.scale(Image, (100, 100))

    def AddImage(self, path, action):
        pass

    
        
    def update(self, pos_PlayerX, pos_PlayerY):
        pass

		
    

