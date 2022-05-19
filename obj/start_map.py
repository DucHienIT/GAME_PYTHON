import pygame
from obj.define import *
from random import randint
from obj.switch import *


class startMap:
    MAP_IMAGE = pygame.image.load('assets/img/WorldMap02.png')
    MAP_IMAGE = pygame.transform.scale(MAP_IMAGE, (WORLD_X*3, WORLD_Y*3))
    LIST_SWITCH = []

    def __init__(self):
        self.no_SWITCH = 5

    def createNewSwitch(self):
        
        self.loadSwitch()

    def randomSwitch(self):
        unit = int(WORLD_X/self.no_SWITCH)
        switchs = []
        for i in range(0, self.no_SWITCH):
            x = randint(unit*i, unit*(i+1)-SWITCH_SIZE)
            y = randint(0, WORLD_Y-SWITCH_SIZE*2)
            switchs.append(switch(x,y,z,t))
        return switchs

    def loadSwitch(self):
        f = open("./assets/data/switch.txt", 'r')
        string = f.read()
        f.close()
        if len(string) < 1: return
        string = string.split("\n")
        for i in string:
            temp = i.split(" ")
            self.LIST_SWITCH.append(switch(int(temp[0]), int(temp[1]), int(temp[2]), int(temp[3])))

    def removeSwitch(self, switch:switch):
        self.LIST_SWITCH.remove(switch)

    def saveSwitch(self, switchs):
        string = ''
        for i in switchs:
            string += f"{i.x} {i.y} {i.z} {i.t}\n"
        string = string[:-1]
        f = open("./assets/data/switch.txt" ,'w')
        f.write(string)
        f.close()

    def update(self):
        return self.MAP_IMAGE

    def delay_ChangeMap():
        pass