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
        self.LIST_SWITCH = [
                switch(-800, -1000, -900, -1100),
                switch(-1000, -1200, -160, -360),
                switch(-1600, -1800, -1161, -1361),
                switch(-3170, -3390, -750, -1000),
                switch(-2140, -2360, -211, -411),
                switch(-2075, -2300, -1300, -1500)
            ]

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