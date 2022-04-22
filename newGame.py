import pygame
from obj.define import *
from obj.map import *
from obj.player import *
from obj.monster import *
from obj.start_map import *
import random






class Program:
    def __init__(self):
        #active = true: chương trình hoạt động
        self.active = True

        self.START_MAP = startMap()
        self.MAP = None

        
        self.clock = pygame.time.Clock()
        self.PLAYERs = pygame.sprite.Group()
        self.MONSTERs = pygame.sprite.Group()

        # New Value By Hien
        self.goku_stop = pygame.USEREVENT + 1
 
        # Cờ chỉ vị trí đang đứng (start map hay phòng đánh quái)
        self.is_staying_in_startMap = True

        # Cờ quản lý số key đang nhấn 
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
                    self.PLAYER.isAttack = False
                    self.PLAYER.animationRun()
                    self.__key_manager__ += 1
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.PLAYER.control(Player.steps, 0)
                    self.PLAYER.isAttack = False
                    self.PLAYER.animationRun()
                    self.__key_manager__ += 1
                if event.key == pygame.K_UP or event.key == ord('w'):
                    self.PLAYER.control(0, -Player.steps)
                    self.PLAYER.isAttack = False
                    self.PLAYER.animationRun()
                    self.__key_manager__ += 1
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.PLAYER.control(0, Player.steps)
                    self.PLAYER.isAttack = False
                    self.PLAYER.animationRun()
                    self.__key_manager__ += 1


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.PLAYER.control(Player.steps, 0)
                    self.PLAYER.goku_Run_Index = 0
                    self.__key_manager__ -= 1
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.PLAYER.control(-Player.steps, 0)
                    self.PLAYER.goku_Run_Index = 0
                    self.__key_manager__ -= 1
                if event.key == pygame.K_UP or event.key == ord('w'):
                    self.PLAYER.control(0, Player.steps)
                    self.PLAYER.goku_Run_Index = 0
                    self.__key_manager__ -= 1
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.PLAYER.control(0, -Player.steps)
                    self.PLAYER.goku_Run_Index = 0
                    self.__key_manager__ -= 1

            elif self.__key_manager__ > 0: 
                self.PLAYER.isRun = True
            elif self.__key_manager__ == 0:
                self.PLAYER.movex = 0
                self.PLAYER.movey = 0
                self.PLAYER.isRun = False
            
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

    def is_player_in_area(self, corn1, corn2):
        
        x = self.PLAYER.rect.centerx
        y = self.PLAYER.rect.centery
        if (corn1[0] < x and x < corn2[0]):
            if (corn1[1] < y and y < corn2[1] ):
                return True
        return False

    def switchMap(self):
        # c_map là vị trí đang đứng hiện tại 
        c_map = None
        if self.is_staying_in_startMap:
            c_map = self.START_MAP
        else:
            c_map = self.MAP
        
        # Nếu đặt chân lên switch thì chuyển map
        for switch in c_map.LIST_SWITCH:
            # Nếu đặt chân lên switch
            if self.is_player_in_area((switch.x, switch.y), (switch.x + SWITCH_SIZE, switch.y+SWITCH_SIZE)):     
                #Nếu đang ở start map
                if self.is_staying_in_startMap:
                    del self.MAP
                    self.MAP = map('HOME')
                    self.create_ListMonster(randint(1,5))
                    self.is_staying_in_startMap = False  
                else:  # Nếu đang trong phòng đánh quái
                    self.is_staying_in_startMap = True
                c_map.removeSwitch(switch)
        del c_map 
     
    def update(self):
        #check switch map -> new map, player.new position
        self.switchMap()

        #update map => background, link switch map
        if self.is_staying_in_startMap:
            backdrop= self.START_MAP.update()
            self.WORLD.blit(backdrop, self.backdropbox)
            for switch in self.START_MAP.LIST_SWITCH:
                self.WORLD.blit(switch.SWITCH_IMG, (switch.x, switch.y))
        
        else: # Đang ở map đánh quái
            backdrop = self.MAP.update()
            self.WORLD.blit(backdrop, self.backdropbox)
            if len(self.MONSTERs) <= 0 and len(self.MAP.LIST_SWITCH) <= 0:
                self.MAP.createSwitch()
            for switch in self.MAP.LIST_SWITCH:
                self.WORLD.blit(switch.SWITCH_IMG, (switch.x, switch.y))
            

        #update player => player.rect
        self.PLAYER.update()
        self.MONSTERs.update()
        
        
        self.impact()
        #draw player
        #self.WORLD.blit(self.PLAYER.image, self.PLAYER.rect)
        self.PLAYERs.draw(self.WORLD)
        self.MONSTERs.draw(self.WORLD)
        pygame.time.delay(20)
        
        #update new screena
        pygame.display.flip()
        self.clock.tick(FPS)

    def create_newPlayer(self):
        pygame.time.set_timer(self.goku_stop, 100)
        self.PLAYER = Player("assets/img/goku01.png", [100, 100])
        self.PLAYER.rect.x = PLAYER_START_POS['x']  # go to x
        self.PLAYER.rect.y = PLAYER_START_POS['y']  # go to y
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