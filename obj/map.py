import pygame
from obj.define import *
from obj.switch import *

class map:
    MAP_IMAGE = {
        'HOME': pygame.transform.scale(pygame.image.load('./assets/img/bgn01.png'), (WORLD_X, WORLD_Y)),
    }

    LIST_SWITCH = []

    def __init__(self, currentMap_string):
        self.currentMap = self.MAP_IMAGE[currentMap_string]
        

    def createSwitch(self):
        self.LIST_SWITCH.append(switch((WORLD_X-PLAYER_SIZE_X)/2,WORLD_Y-PLAYER_SIZE_Y*2, 0, 0))

    def removeSwitch(self, switch:switch):
        self.LIST_SWITCH.remove(switch)

    def update(self):
        return self.currentMap

  
        
    

            

    


