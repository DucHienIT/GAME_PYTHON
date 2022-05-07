import pygame
from obj.define import *
from random import randint
from obj.switch import *

class startMap:
    MAP_IMAGE = pygame.image.load('assets/img/WorldMap.png')
    MAP_IMAGE = pygame.transform.scale(MAP_IMAGE, (960, 720))
    LIST_SWITCH = []

    def __init__(self):
        self.no_SWITCH = 5
        self.createSwitch()

    def createSwitch(self):
        unit = int(WORLD_X/self.no_SWITCH)
        for i in range(0, self.no_SWITCH):
            x = randint(unit*i, unit*(i+1)-SWITCH_SIZE)
            y = randint(0, WORLD_Y-SWITCH_SIZE*2)
            self.LIST_SWITCH.append(switch(x,y))

    def removeSwitch(self, switch:switch):
        self.LIST_SWITCH.remove(switch)

    def update(self):
        return self.MAP_IMAGE

    def delay_ChangeMap():
        pass