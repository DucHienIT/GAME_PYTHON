import pygame
from obj.define import *
from random import randint
from obj.switch import *


class startMap:
    indexChapter = 0
    indexColor = 0
    MAP_IMAGE = MAP_LIST_IMAGE[indexChapter]
    
    

    LIST_SWITCH = []

    def __init__(self):
        self.no_SWITCH = 5

    def createNewSwitch(self):
        self.LIST_SWITCH = [
                switch(LISTSWITCH[0][0], LISTSWITCH[0][1], LISTSWITCH[0][2], LISTSWITCH[0][3]),
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

    def ChangeMap(self):
        self.indexChapter += 1
        self.indexColor += 1
        self.MAP_IMAGE = MAP_LIST_IMAGE[self.indexChapter]
        if self.indexColor > 4:
            self.indexColor = 0
        self.LIST_SWITCH.append(switch(LISTSWITCH[self.indexColor][0], LISTSWITCH[self.indexColor][1], LISTSWITCH[self.indexColor][2], LISTSWITCH[self.indexColor][3]))

        
    