from matplotlib import animation
import pygame
from obj.define import *
from obj.map import *
from random import randint
from random import choice

class Material(pygame.sprite.Sprite):
    steps = DEFAULT_STEPS

    clock = pygame.time.Clock()
    def __init__(self, Image, position):
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0
        self.inDisplay = False
        self.images = []
        img = Image
        img = pygame.transform.scale(img, (ITEM_SIZE_X*2, ITEM_SIZE_Y*2))

        img.convert_alpha()  # optimise alpha
        img.set_colorkey(ALPHA)  # set alpha

        self.image = img
        self.rect = self.image.get_rect(center = (position[0], position[1]))
    
    def AddImage(self, path):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, (ITEM_SIZE_X, ITEM_SIZE_X))
        
        
        img.convert_alpha() 
        img.set_colorkey(ALPHA)
        
        self.images.append(img)


    

