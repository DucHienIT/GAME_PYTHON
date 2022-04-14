from matplotlib import animation
import pygame
from sympy import randMatrix
from zmq import PLAIN
from obj.define import *
from obj.map import *
from obj.player import *
from multipledispatch import dispatch
from obj.monster import *
import random





class Program:
    def __init__(self):
        #active = true: chương trình hoạt động
        self.active = True

        self.MAP = map('HOME')

        
        self.clock = pygame.time.Clock()
        self.PLAYERs = pygame.sprite.Group()
        self.MONSTERs = pygame.sprite.Group()

        # New Value By Hien
        self.goku_stop = pygame.USEREVENT + 1
 

        self.__key_manager__ = 0

    def main(self): 
        self.create_newPlayer()
        
        while self.active:
            self.active = self.checkEvent()
            self.update()

    def startProcess(self):
        pygame.init()
        self.WORLD = pygame.display.set_mode((WORLD_X, WORLD_Y))    
        self.backdropbox = self.WORLD.get_rect()
        
    

    def endProcess(self):
        pygame.quit()

    def checkEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.PLAYER.isAttack = True
                self.PLAYER.comboCount += 1
                self.PLAYER.animationAttack()
            

            if event.type == pygame.KEYDOWN:
                if event.key == ord('q'):
                    return False
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.PLAYER.control(-Player.steps, 0)
                    self.PLAYER.isRun = True
                    self.PLAYER.isAttack = False
                    self.PLAYER.animationRun()
                    
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.PLAYER.control(Player.steps, 0)
                    self.PLAYER.isRun = True
                    self.PLAYER.isAttack = False
                    self.PLAYER.animationRun()

                if event.key == pygame.K_UP or event.key == ord('w'):
                    self.PLAYER.control(0, -Player.steps)
                    self.PLAYER.isAttack = False
                    self.PLAYER.animationRun()
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.PLAYER.control(0, Player.steps)
                    self.PLAYER.isAttack = False
                    self.PLAYER.animationRun()

                self.__key_manager__ += 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.PLAYER.control(Player.steps, 0)
                    self.PLAYER.isRun = False
                    self.PLAYER.goku_Run_Index = 0

                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.PLAYER.control(-Player.steps, 0)
                    self.PLAYER.isRun = False
                    self.PLAYER.goku_Run_Index = 0

                if event.key == pygame.K_UP or event.key == ord('w'):
                    self.PLAYER.control(0, Player.steps)
                    self.PLAYER.isRun = False
                    self.PLAYER.goku_Run_Index = 0
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.PLAYER.control(0, -Player.steps)
                    self.PLAYER.isRun = False
                    self.PLAYER.goku_Run_Index = 0
                self.__key_manager__ -= 1

            elif self.__key_manager__ == 0:
                self.PLAYER.movex = 0
                self.PLAYER.movey = 0
            
            if event.type == self.goku_stop:
                if self.PLAYER.isAttack == False:
                    if self.PLAYER.isRun == False:
                        self.PLAYER.animationStop()
                        self.PLAYER.isAttack = False
                        self.PLAYER.comboCount = 0
                    else:
                        self.PLAYER.animationRun()
            
                else:
                    self.PLAYER.animationAttack()
        return True

    def player_in_area(self, corn1, corn2):
        
        x = self.PLAYER.rect.centerx
        y = self.PLAYER.rect.centery
        if (corn1[0] < x and x < corn2[0]):
            if (corn1[1] < y and y < corn2[1] ):
                return True
        return False

    def isSwitchMap(self):

        if len(self.MONSTERs) > 0:
            return None
        for key in self.MAP.listSwitchMap:
            if key != None:
                if (self.player_in_area((map.SWITCH_MAP_POSITION[key][0], map.SWITCH_MAP_POSITION[key][1]),\
                    (map.SWITCH_MAP_POSITION[key][0] + map.SWITCH_MAP_POSITION[key][2], \
                        map.SWITCH_MAP_POSITION[key][1] + map.SWITCH_MAP_POSITION[key][3]))):
                    return key
        return None

    def switchMap(self):
        nextMap = self.isSwitchMap()  
        if nextMap:

            self.create_ListMonster(10)
            self.MAP = self.MAP.go_NextMap(nextMap)
            if nextMap == 'TOP':
                self.PLAYER.rect.centerx = PLAYER_START_POS['BOTTOM'][0]
                self.PLAYER.rect.centery = PLAYER_START_POS['BOTTOM'][1]
            elif nextMap == 'RIGHT':
                self.PLAYER.rect.centerx = PLAYER_START_POS['LEFT'][0]
                self.PLAYER.rect.centery = PLAYER_START_POS['LEFT'][1]
            elif nextMap == 'BOTTOM':
                self.PLAYER.rect.centerx = PLAYER_START_POS['TOP'][0]
                self.PLAYER.rect.centery = PLAYER_START_POS['TOP'][1]
            elif nextMap == 'LEFT':
                self.PLAYER.rect.centerx = PLAYER_START_POS['RIGHT'][0]
                self.PLAYER.rect.centery = PLAYER_START_POS['RIGHT'][1]                 

    def update(self):
        #check switch map -> new map, player.new position
        self.switchMap()

        #update map => background, link switch map
        backdrop = self.MAP.update()
        
        #Draw map
        self.WORLD.blit(backdrop, self.backdropbox)

        #draw link switch map
        for key in self.MAP.listSwitchMap:
            #if key: pygame.draw.rect(self.WORLD, (0,0,0), map.SWITCH_MAP_POSITION[key])
            if key:
                self.WORLD.blit(map.SWITCH_MAP_IMG, (map.SWITCH_MAP_POSITION[key][0], map.SWITCH_MAP_POSITION[key][1]))

        #update player => player.rect
        self.PLAYER.update()
        self.MONSTERs.update()
        
        
        self.impact()
        #draw player
        #self.WORLD.blit(self.PLAYER.image, self.PLAYER.rect)
        self.PLAYERs.draw(self.WORLD)
        self.MONSTERs.draw(self.WORLD)
        pygame.time.delay(10)
        
        #update new screena
        pygame.display.flip()
        self.clock.tick(FPS)

    def create_newPlayer(self):
        pygame.time.set_timer(self.goku_stop, 100)
        self.PLAYER = Player("assets/img/goku01.png", [100, 100])
        self.PLAYER.rect.centerx = PLAYER_START_POS['BOTTOM'][0]  # go to x
        self.PLAYER.rect.centery = PLAYER_START_POS['BOTTOM'][1]  # go to y
        self.PLAYERs.add(self.PLAYER)

    def create_ListMonster(self, total):
        for i in range(0, total):
                list_pos_MonsterX = [i for i in range(100, 860)]
                list_pos_MonsterY = [i for i in range(100, 620)]
                new_posX = random.choice(list_pos_MonsterX)
                new_posY = random.choice(list_pos_MonsterY)
                self.create_Monster(new_posX, new_posY)

    def create_Monster(self, x, y):
        self.MONSTER = Monster("assets/img/Bear01.png", [x, y])
        self.MONSTERs.add(self.MONSTER)
        self.MONSTER.update()

    def impact(self):
        for monster in self.MONSTERs:
            if (pygame.sprite.collide_rect(self.PLAYER, monster)):
                if self.PLAYER.isAttack == True:
                    monster.kill()
                else:
                    self.PLAYER.hp -= 1



# import os
# print(os.listdir("./assets/img"))
process = Program()
process.startProcess()
process.main()
process.endProcess()