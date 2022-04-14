from json import load
import string
from numpy import delete
import pygame
from obj.define import *
from obj.monster import *

class map:
    SWITCH_MAP_POSITION = {
        'TOP': ((WORLD_X-SWITCHMAP_SIZE)/2   , 0                         , SWITCHMAP_SIZE, SWITCHMAP_SIZE),
        'RIGHT': (WORLD_X-SWITCHMAP_SIZE     , (WORLD_Y-SWITCHMAP_SIZE)/2, SWITCHMAP_SIZE, SWITCHMAP_SIZE),
        'BOTTOM': ((WORLD_X-SWITCHMAP_SIZE)/2, WORLD_Y - SWITCHMAP_SIZE  , SWITCHMAP_SIZE, SWITCHMAP_SIZE),
        'LEFT': (0                           , (WORLD_Y-SWITCHMAP_SIZE)/2, SWITCHMAP_SIZE, SWITCHMAP_SIZE)
    } #define vị trí các ô chuyển map
    #Nếu ko có, nhớ add 0, vd: ["TOP", 0, 0, "LEFT"]
    MAP_IMAGE = {
        'HOME': pygame.transform.scale(pygame.image.load('./assets/img/bgn01.png'), (WORLD_X, WORLD_Y)),
        'SHOP': pygame.transform.scale(pygame.image.load('./assets/img/bgn01.png'), (WORLD_X, WORLD_Y)),
        'GYM': pygame.transform.scale(pygame.image.load('./assets/img/bgn01.png'), (WORLD_X, WORLD_Y)),
        'N1': pygame.transform.scale(pygame.image.load('./assets/img/bgn01.png'), (WORLD_X, WORLD_Y)),
        'N2': pygame.transform.scale(pygame.image.load('./assets/img/bgn01.png'), (WORLD_X, WORLD_Y)),
        'B1': pygame.transform.scale(pygame.image.load('./assets/img/bgn01.png'), (WORLD_X, WORLD_Y)),
        'B2': pygame.transform.scale(pygame.image.load('./assets/img/bgn01.png'), (WORLD_X, WORLD_Y)),
        'B3': pygame.transform.scale(pygame.image.load('./assets/img/bgn01.png'), (WORLD_X, WORLD_Y)),
        'B4': pygame.transform.scale(pygame.image.load('./assets/img/bgn01.png'), (WORLD_X, WORLD_Y))
    } #define giá trị map

    SWITCH_MAP_IMG = pygame.transform.scale(pygame.image.load('./assets/img/arrow.png'), (SWITCHMAP_SIZE, SWITCHMAP_SIZE))

    def __init__(self, currentMap_string):
        #Map hiện tại
        self.currentMap = self.MAP_IMAGE[currentMap_string]

        #List các ô chuyển map (top right bot left), có thể miss vài ô
        self.listSwitchMap = [] 
        #Nếu không có, ghi None

        # địa chỉ map tiếp theo.
        self.nextMap = {}
        #define vị trí các ô chuyển map
        #Nếu ko có, nhớ add 0, vd: ["TOP", 0, 0, "LEFT"]
        
        self.getNextMap(currentMap_string)

    def fill_nextMap(self, top, right, bot, left):
        self.nextMap = {
                'TOP' : top, 
                'RIGHT': right, 
                'BOTTOM': bot, 
                'LEFT': left}
        if top: 
            self.listSwitchMap.append('TOP') 
        else: 
            self.listSwitchMap.append(None)
        if right: 
            self.listSwitchMap.append('RIGHT') 
        else: 
            self.listSwitchMap.append(None)
        if bot: 
            self.listSwitchMap.append('BOTTOM') 
        else: 
            self.listSwitchMap.append(None)
        if left: 
            self.listSwitchMap.append('LEFT') 
        else: 
            self.listSwitchMap.append(None)


    def getNextMap(self, currentMap_string):
        if (currentMap_string == 'HOME'):
            self.fill_nextMap('GYM', 'B1', 'N1', 'SHOP')

        if (currentMap_string == 'SHOP'):
            self.fill_nextMap(0 , 'HOME', 0, 0)
        if (currentMap_string == 'GYM'):
            self.fill_nextMap(0, 0, 'HOME', 0)
        if (currentMap_string == 'N1'):
            self.fill_nextMap('HOME', 0, 'N2', 0)
        if (currentMap_string == 'N2'):
            self.fill_nextMap('N1', 0, 0, 0)
        if (currentMap_string == 'B1'):
            self.fill_nextMap(0, 'B2', 0, 'HOME')
        if (currentMap_string == 'B2'):
            self.fill_nextMap(0, 'B4', 'B3', 'B1')
        if (currentMap_string == 'B3'):
            self.fill_nextMap('B2', 0, 0, 0)
        if (currentMap_string == 'B4'):
            self.fill_nextMap(0, 0, 0, 'B1')


    def go_NextMap(self, nextMap_string:str):
        return map(self.nextMap[nextMap_string])

    def update(self):
        #Nếu player chạm swith map thì chuyển map
        return self.currentMap

