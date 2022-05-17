import pygame
from obj.define import *
from obj.map import *
from obj.player import *
from obj.monster import *
from obj.start_map import *
from obj.PlaySound import *
import random

class Program:
    def __init__(self):
        #active = true: chương trình hoạt động
        self.active = True

        self.START_MAP = startMap()
        self.MAP = None

        self.sound = Sound()
        self.isSwitchMap = False
        self.clock = pygame.time.Clock()
        self.PLAYERs = pygame.sprite.Group()
        self.MONSTERs = pygame.sprite.Group()
        
        self.i = 0
        # New Value By Hien
        self.goku_stop = pygame.USEREVENT + 1
        self.MonsterInDisplay = False
        # Cờ chỉ vị trí đang đứng (start map hay phòng đánh quái)
        self.is_staying_in_startMap = True

        # Cờ quản lý số key đang nhấn 
        self.__key_manager__ = 0

    def main(self): 
        self.sound.__Play__Intro__(-1)
        self.loadPlayer()
        while self.active:
            self.active = self.checkEvent()    
            self.update()

    def startProcess(self):
        pygame.init()
        self.WORLD = pygame.display.set_mode((WORLD_X, WORLD_Y))  
        pygame.display.set_caption("Dragon Boy Advertune", "Game") 
        self.backdropbox = self.WORLD.get_rect()
        self.isSwitchMap = True

    def endProcess(self):
        self.saveInfo()
        f = open('./assets/data/continue.txt', 'w')
        if self.PLAYER.hp <= 0:
            f.write('0')
        else:
            f.write('1')
        f.close()


        while self.i < 10:
            self.loading()
            pygame.display.flip()
        pygame.quit()

    def checkEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.PLAYER.mp >= 10:
                    self.PLAYER.isAttack = True
                    self.PLAYER.animationAttack()
                    self.PLAYER.mp -= 10
                    self.PLAYER.comboCount += 1
                    self.sound.__Play__Attack__(0)

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
                if self.MonsterInDisplay:
                    for monster in self.MONSTERs:
                        monster.animationRun()
                        
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
                self.isSwitchMap = True   
                #Nếu đang ở start map
                if self.is_staying_in_startMap:
                    
                    del self.MAP
                    self.MAP = map('HOME')
                    self.create_ListMonster(randint(4,10))
                    self.MonsterInDisplay = True
                    self.is_staying_in_startMap = False  
                else:  # Nếu đang trong phòng đánh quái
                    self.is_staying_in_startMap = True
                    
                c_map.removeSwitch(switch)
        del c_map 
     
    def update(self):
        #check switch map -> new map, player.new position
        self.switchMap()
        if self.isSwitchMap == True:
            self.loading()
        else:
        #update map => background, link switch map
            if self.is_staying_in_startMap:
                backdrop = self.START_MAP.update()
                self.WORLD.blit(backdrop, self.backdropbox)
                for switch in self.START_MAP.LIST_SWITCH:
                    self.WORLD.blit(switch.SWITCH_IMG_Dungeon, (switch.x, switch.y))
        
            else: # Đang ở map đánh quái
                backdrop = self.MAP.update()
                self.WORLD.blit(backdrop, self.backdropbox)
                if len(self.MONSTERs) <= 0 and len(self.MAP.LIST_SWITCH) <= 0:
                    self.MAP.createSwitch()
                for switch in self.MAP.LIST_SWITCH:
                    self.WORLD.blit(switch.SWITCH_IMG_Exit, (switch.x, switch.y))
            

        #update player => player.rect
            self.infoCharaterUpdate()
            self.PLAYER.update()
            self.MONSTERs.update(self.PLAYER.rect.centerx, self.PLAYER.rect.centery)
        
            self.impact()
            self.PLAYERs.draw(self.WORLD) 
            self.MONSTERs.draw(self.WORLD)
            pygame.time.delay(10)
        
        #update new screena
        pygame.display.flip()
        self.clock.tick(FPS)

    def loading(self):
        self.WORLD.blit(list_Image[self.i], self.backdropbox)
        if self.i < 10:
            self.i += 1
        else:
            self.i = 0
            self.isSwitchMap = False
        pygame.time.delay(75)

    def newPlayer(self):
        string = f'{HP} {MP} {ATK} {10} {0} {1} {PLAYER_START_POS["x"]} {PLAYER_START_POS["y"]}'
        f = open("./assets/data/player.txt", "w")
        f.write(string)
        f.close()    

    def loadPlayer(self): 
        f = open("./assets/data/player.txt", "r")
        string = f.read()
        f.close()
        '''
        string:
        hp mp atk def exp level pos_x pos_y
        '''
        string = string.split(" ")
        info = []
        for i in string:
            info.append(int(i))

        pygame.time.set_timer(self.goku_stop, 150)
        self.PLAYER = Player("assets/img/goku01.png", info)
        self.PLAYERs.add(self.PLAYER)

    def create_ListMonster(self, total):
        for i in range(0, total):
                list_pos_MonsterX = [i for i in range(100, 860)]
                list_pos_MonsterY = [i for i in range(100, 620)]
                new_posX = random.choice(list_pos_MonsterX)
                new_posY = random.choice(list_pos_MonsterY)
                self.create_Monster(new_posX, new_posY)

    def create_Monster(self, x, y):
        self.MONSTER = Monster(MaracaListImageAttach[0], [x, y])
        self.MONSTER.update(self.PLAYER.rect.x, self.PLAYER.rect.x)
        self.MONSTER.inDisplay = True
        self.MONSTERs.add(self.MONSTER)
        

    def impact(self):
        
        for monster in self.MONSTERs:
            if (pygame.sprite.collide_rect(self.PLAYER, monster)):
                if self.PLAYER.isAttack == True:
                    self.sound.__Play__Collision__(0)
                    monster.hp -= self.PLAYER.atk
                    if monster.hp <= 0:
                        monster.kill()
                        self.PLAYER.exp += 100
                elif monster.Run_Index in [7, 8]:
                    self.PLAYER.hp -= 100
                    if self.PLAYER.hp <= 0: 
                        self.active = False
                    monster.movex = 0
                    monster.movey = 0
       
    def infoCharaterUpdate(self):
        Font = pygame.font.Font("assets/img/font.ttf", 45)
        OPTIONS_TEXT = Font.render("LV " + str(self.PLAYER.level), True, "Blue")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(300, 100))
        self.WORLD.blit(OPTIONS_TEXT, OPTIONS_RECT)

        Hp_Ba = pygame.transform.scale(Hp_Bar, (450*(self.PLAYER.hp)/HP, 125*1.5))
        Mp_Ba = pygame.transform.scale(Mp_Bar, (450*(self.PLAYER.mp)/MP, 125*1.5))
        EXP_Ba = pygame.transform.scale(Exp_Bar, (415*(self.PLAYER.exp/listExpUpLevel[self.PLAYER.level-1]), 125))
        
        self.WORLD.blit(Info_Charater, (0, 0))
        self.WORLD.blit(Hp_Ba, (149, 12))
        self.WORLD.blit(Mp_Ba, (165, 34))
        self.WORLD.blit(EXP_Ba, (170, 57))

    def saveInfo(self):
        # save player
        self.PLAYER.savePlayer()
        # save switch
        self.START_MAP.saveSwitch(self.START_MAP.LIST_SWITCH)
