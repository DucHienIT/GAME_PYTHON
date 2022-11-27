import pygame
from obj.define import *
from obj.map import *
from obj.player import *
from obj.monster import *
from obj.start_map import *
from obj.PlaySound import *
from obj.button import *
from obj.material import *
from obj.equipment import *

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
        self.MATERTIALS = pygame.sprite.Group()
        self.rect_BG_X = 0
        self.rect_BG_Y = 0
        self.i = 0
        # New Value By Hien
        self.goku_stop = pygame.USEREVENT + 1
        self.MonsterInDisplay = False

        self.ListButtonEquipItem = []

        self.MaterialInDisplay = False
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
        if self.PLAYER.hp <= 0:
            self.frmOverGame(0)
        else:
            self.frmOverGame(1)
        pygame.quit()

    def frmOverGame(self, flag):
        myfont = pygame.font.Font("./assets/img/font.ttf", 100)
        
        if len(self.START_MAP.LIST_SWITCH) == 0 and flag == 1:
            label = myfont.render('YOU WIN', True, "#b68f40")
        elif flag == 0:
            label = myfont.render('GAME OVER', True, "#b68f40")
        else:
            return
        label_rect = label.get_rect(center=(WORLD_X/2, WORLD_Y/2))
        count = 200
        while count > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    self.is_start = True
                    if event.key == ord('q') or event.key == pygame.K_ESCAPE:
                        return False
            self.WORLD.fill(BLACK)
            self.WORLD.blit(label, (label_rect))
            pygame.display.flip()
            self.clock.tick(FPS)
            count -= 1

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
                if  event.key == ord('c'):
                    self.click_InfoPlayer()
                
                if  event.key == ord('e'):
                    self.click_PickUpGarbage()

                if event.key == ord('b'):
                    self.click_BagPlayer()


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

    def is_player_in_area(self, row, col):
        
        x = self.rect_BG_X - self.PLAYER.rect.centerx
        y = self.rect_BG_Y - self.PLAYER.rect.centery
        if (row[0] >  x > row[1]):
            if (col[0] > y > col[1] ):
                return True
        return False

    def is_player_in_exit(self):
        x = self.PLAYER.rect.centerx
        y = self.PLAYER.rect.centery
        if (WORLD_X/2 - .5*SWITCH_SIZE < x and x < .5*SWITCH_SIZE + WORLD_X/2):
            if (WORLD_Y-SWITCH_SIZE < y < WORLD_Y):
                return True
        return False

    def switchMap(self):
        # c_map là vị trí đang đứng hiện tại 
        c_map = None
        if self.is_staying_in_startMap:
            c_map = self.START_MAP
            self.PLAYER.room = False
        else:
            c_map = self.MAP
            self.PLAYER.room = True
        
        # Xác định vị trí dungeon
        
        #print(self.rect_BG_X - self.PLAYER.rect.centerx, self.rect_BG_Y - self.PLAYER.rect.centery)
        
        # Nếu đặt chân lên switch thì chuyển map
        for switch in c_map.LIST_SWITCH:
            # Nếu đặt chân lên switch
            if self.is_player_in_area((switch.x, switch.y), (switch.z, switch.t)): 
                self.isSwitchMap = True   
                #Nếu đang ở start map
                if self.is_staying_in_startMap:            
                    del self.MAP
                    self.MAP = map('HOME')
                    #self.create_ListMonster(randint(4,10))
                    self.create_ListMonster(1)

                    self.MonsterInDisplay = True
                    self.is_staying_in_startMap = False  
                
                c_map.removeSwitch(switch)
                c_map.ChangeMap()
            if self.is_player_in_exit() and self.is_staying_in_startMap == False and len(self.MAP.LIST_SWITCH) > 0:  # Nếu đang trong phòng đánh quái
                self.isSwitchMap = True  
                self.is_staying_in_startMap = True
                c_map.removeSwitch(switch) 
                self.MATERTIALS.empty()               
        del c_map 
     
    def update(self):
        #check switch map -> new map, player.new position
        self.switchMap()
        if self.isSwitchMap == True:
            self.loading()
            self.PLAYER.rect.centerx = PLAYER_START_POS['x']
            self.PLAYER.rect.centery = PLAYER_START_POS['y']
        else:
        #update map => background, link switch map
            if self.is_staying_in_startMap:
                backdrop = self.START_MAP.update()
               
                if -3073 < self.rect_BG_X - self.PLAYER.movex <= 0 and -1722 < self.rect_BG_Y - self.PLAYER.movey <= 0:
                    self.rect_BG_X -= self.PLAYER.movex*1.5
                    self.rect_BG_Y -= self.PLAYER.movey*1.5
                self.WORLD.blit(backdrop, (self.rect_BG_X, self.rect_BG_Y))


        
            else: # Đang ở map đánh quái
                backdrop = self.MAP.update()
                self.WORLD.blit(backdrop, self.backdropbox)
                if len(self.MONSTERs) <= 0 and len(self.MAP.LIST_SWITCH) <= 0:
                    self.MAP.createSwitch()
                for switch in self.MAP.LIST_SWITCH:
                    self.WORLD.blit(switch.SWITCH_IMG_Exit, ((WORLD_X-SWITCH_SIZE)/2, WORLD_Y - SWITCH_SIZE))

                

        #update player => player.rect
            self.infoCharaterUpdate()
            self.PLAYER.update()
            self.MONSTERs.update(self.PLAYER.rect.centerx, self.PLAYER.rect.centery)
        
            self.impact()
            self.PLAYERs.draw(self.WORLD) 
            self.MONSTERs.draw(self.WORLD)
            self.MATERTIALS.draw(self.WORLD)

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
        
        self.PLAYER = Player("assets/img/PlayerAttack/Untitled-42.png", info)
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
        self.MONSTER.update(self.PLAYER.rect.x, self.PLAYER.rect.y)
        self.MONSTER.inDisplay = True
        self.MONSTERs.add(self.MONSTER)
        

    def impact(self):
        for monster in self.MONSTERs:
            if (pygame.sprite.collide_rect(self.PLAYER, monster)):
                if self.PLAYER.isAttack == True:
                    self.sound.__Play__Collision__(0)
                    monster.hp -= (self.PLAYER.atk + self.PLAYER.totalAtkEquipment)
                    print(self.PLAYER.totalAtkEquipment)

                    if monster.hp <= 0: # quái chết và rớt item
                        self.creatMatertial(self.PLAYER.rect.x + 100, self.PLAYER.rect.y + 100)
                        monster.kill()
                        self.PLAYER.exp += 100
                        
                if monster.Run_Index in [1, 10 ,20, 30]:
                    self.PLAYER.hp -= 20
                    if self.PLAYER.hp <= 0:
                        self.active = False
                    monster.movex = 0
                    monster.movey = 0
       
    def infoCharaterUpdate(self):
        Font = pygame.font.Font("assets/img/font.ttf", 45)
        OPTIONS_TEXT = Font.render("LV" + str(self.PLAYER.level), True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(300, 200))
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
    
    def click_InfoPlayer(self):

        
        def get_font(size): # Returns Press-Start-2P in the desired size
            return pygame.font.Font("assets/img/font.ttf", size)
        def get_font2(size): # Returns Press-Start-2P in the desired size
            return pygame.font.Font("assets/img/font2.ttf", size)
        while True:
            MOUSE_POS = pygame.mouse.get_pos()

            self.WORLD.blit(pygame.transform.scale(pygame.image.load("./assets/img/BG_Info_Player02.png"), (WORLD_X, WORLD_Y)), (0, 0))
            

            TEXT = get_font2(60).render("Thông tin nhân vật", True, "White")
            OPTIONS_RECT = TEXT.get_rect(center=(720, 80))
            self.WORLD.blit(TEXT, OPTIONS_RECT)

            ATK_TEXT = Button(image=None, pos=(1155, 190), text_input="ATK", font=get_font(30), base_color="Black", hovering_color="Green")
            ATK_TEXT.update(self.WORLD)
            DEF_TEXT = Button(image=None, pos=(1155,WORLD_Y - 130), text_input="DEF", font=get_font(30), base_color="Black", hovering_color="Green")
            DEF_TEXT.update(self.WORLD)
            HP_TEXT = Button(image=None, pos=(870, WORLD_Y/2 + 30), text_input="HP", font=get_font(30), base_color="Black", hovering_color="Green")
            HP_TEXT.update(self.WORLD)
            MP_TEXT = Button(image=None, pos=(1450, WORLD_Y/2 + 30), text_input="MP", font=get_font(30), base_color="Black", hovering_color="Green")
            MP_TEXT.update(self.WORLD)

            sumATK_Btn = Button(image=None, pos=(1060, 260), text_input="+", font=get_font(30), base_color="Black", hovering_color="Green")
            sumATK_Btn.update(self.WORLD)
            subATK_Btn = Button(image=None, pos=(1240, 260), text_input="-", font=get_font(30), base_color="Black", hovering_color="Green")
            subATK_Btn.update(self.WORLD)

            sumDEF_Btn = Button(image=None, pos=(1060, WORLD_Y - 220), text_input="+", font=get_font(30), base_color="Black", hovering_color="Green")
            sumDEF_Btn.update(self.WORLD)
            subDEF_Btn = Button(image=None, pos=(1240, WORLD_Y - 220), text_input="-", font=get_font(30), base_color="Black", hovering_color="Green")
            subDEF_Btn.update(self.WORLD)

            sumHP_Btn = Button(image=None, pos=(985, WORLD_Y/2 - 60), text_input="+", font=get_font(30), base_color="Black", hovering_color="Green")
            sumHP_Btn.update(self.WORLD)
            subHP_Btn = Button(image=None, pos=(985, WORLD_Y/2 + 100), text_input="-", font=get_font(30), base_color="Black", hovering_color="Green")
            subHP_Btn.update(self.WORLD)
            
            sumMP_Btn = Button(image=None, pos=(1365, WORLD_Y/2 - 60), text_input="+", font=get_font(30), base_color="Black", hovering_color="Green")
            sumMP_Btn.update(self.WORLD)
            subMP_Btn = Button(image=None, pos=(1365, WORLD_Y/2 + 100), text_input="-", font=get_font(30), base_color="Black", hovering_color="Green")
            subMP_Btn.update(self.WORLD)



            Total_ATK = get_font(20).render(str(self.PLAYER.atk), True, "White")
            self.WORLD.blit(Total_ATK, (1140, 260))
            Total_DEF = get_font(20).render(str(self.PLAYER.DEF), True, "White")
            self.WORLD.blit(Total_DEF, (1140, WORLD_Y - 240))
            Total_HP = get_font(20).render(str(self.PLAYER.hp), True, "White")
            self.WORLD.blit(Total_HP, (935, WORLD_Y/2 + 20))
            Total_MP = get_font(20).render(str(self.PLAYER.mp), True, "White")
            self.WORLD.blit(Total_MP, (1315, WORLD_Y/2 + 20))


            Total_Free_Value = get_font(20).render(str(self.PLAYER.freeValue), True, "Black")
            self.WORLD.blit(Total_Free_Value, (1060, WORLD_Y - 90))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and self.PLAYER.freeValue > 0:
                    if sumATK_Btn.checkForInput(MOUSE_POS):
                        self.PLAYER.atk += 1
                        Total_ATK = get_font(20).render(str(self.PLAYER.atk), True, "White")
                        self.WORLD.blit(Total_ATK, (1140, 260))
                        self.PLAYER.freeValue -= 1
                    if subATK_Btn.checkForInput(MOUSE_POS):
                        if self.PLAYER.atk > 10:
                            self.PLAYER.atk -= 1
                            Total_ATK = get_font(20).render(str(self.PLAYER.atk), True, "White")
                            self.WORLD.blit(Total_ATK, (1140, 260))
                            self.PLAYER.freeValue += 1
                    if sumDEF_Btn.checkForInput(MOUSE_POS):
                        self.PLAYER.DEF += 1
                        Total_DEF = get_font(20).render(str(self.PLAYER.DEF), True, "White")
                        self.WORLD.blit(Total_DEF, (1140, WORLD_Y - 240))
                        self.PLAYER.freeValue -= 1
                    if subDEF_Btn.checkForInput(MOUSE_POS):
                        if self.PLAYER.DEF > 10:
                            self.PLAYER.DEF -= 1
                            Total_DEF = get_font(20).render(str(self.PLAYER.DEF), True, "White")
                            self.WORLD.blit(Total_DEF, (1140, WORLD_Y - 240))
                            self.PLAYER.freeValue += 1

                    if sumHP_Btn.checkForInput(MOUSE_POS):
                        self.PLAYER.hp += 100
                        Total_HP = get_font(20).render(str(self.PLAYER.hp), True, "White")
                        self.WORLD.blit(Total_HP, (935, WORLD_Y/2 + 20))
                        self.PLAYER.freeValue -= 1
                        
                    if subHP_Btn.checkForInput(MOUSE_POS):
                        if self.PLAYER.hp > 1000:
                            self.PLAYER.hp -= 100
                            Total_HP = get_font(20).render(str(self.PLAYER.hp), True, "White")
                            self.WORLD.blit(Total_HP, (935, WORLD_Y/2 + 20))
                            self.PLAYER.freeValue += 1
                    if sumMP_Btn.checkForInput(MOUSE_POS):
                        self.PLAYER.mp += 10
                        Total_MP = get_font(20).render(str(self.PLAYER.mp), True, "White")
                        self.WORLD.blit(Total_MP, (1315, WORLD_Y/2 + 20))
                        self.PLAYER.freeValue -= 1
                    if subMP_Btn.checkForInput(MOUSE_POS):
                        if self.PLAYER.mp > 100:
                            self.PLAYER.mp -= 10
                            Total_MP = get_font(20).render(str(self.PLAYER.mp), True, "White")
                            self.WORLD.blit(Total_MP, (1315, WORLD_Y/2 + 20))
                            self.PLAYER.freeValue += 1

                    Total_Free_Value = get_font(20).render(str(self.PLAYER.freeValue), True, "Black")
                    self.WORLD.blit(Total_Free_Value, (1060, WORLD_Y - 90))
                if event.type == pygame.KEYDOWN:
                    if event.key == ord('c'):
                        return
 
            pygame.display.update()

    def click_BagPlayer(self):

        self.WORLD.blit(pygame.transform.scale(pygame.image.load("./assets/img/BG_Info_Player03.png"), (WORLD_X, WORLD_Y)), (0, 0))
        
        def get_font(size): # Returns Press-Start-2P in the desired size
            return pygame.font.Font("assets/img/font.ttf", size)
        def get_font2(size): # Returns Press-Start-2P in the desired size
            return pygame.font.Font("assets/img/font2.ttf", size)

        
        while True:
            MOUSE_POS = pygame.mouse.get_pos()

            TEXT = get_font2(60).render("Túi đồ nhân vật", True, "White")
            OPTIONS_RECT = TEXT.get_rect(center=(720, 80))
            self.WORLD.blit(TEXT, OPTIONS_RECT)

            if len(self.PLAYER.listItem) > 0:
                self.loadListItem()
                self.loadButton()

            

            ButonCreateEquip = Button(image=None, pos=(1304, 688), text_input="Tạo trang bị", font=get_font2(35), base_color="White", hovering_color="Green")
            ButonCreateEquip.update(self.WORLD)

            Total_Flatis = get_font(20).render(str(self.PLAYER.Bag[0]), True, "White")
            self.WORLD.blit(Total_Flatis, (198, 765))
            Total_Glass = get_font(20).render(str(self.PLAYER.Bag[1]), True, "White")
            self.WORLD.blit(Total_Glass, (438, 765))
            Total_Cans = get_font(20).render(str(self.PLAYER.Bag[2]), True, "White")
            self.WORLD.blit(Total_Cans, (630, 765))


            self.loadEquidment()

            #----------------------------------------------------------------------

           
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == ord('b'):
                        return
                   
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if ButonCreateEquip.checkForInput(MOUSE_POS):
                        print("Tạo trang bị")
                        self.click_CreateEquipment()

 
            pygame.display.update()
    def loadListItem(self):
        x = 0
        y = 0
        for i in range(0, len(self.PLAYER.listItem)):
            if y <= 3:
                if x <= 3:
                    rectx = 896 +  (x * 144)
                    recty = 222 + (y * 144)
                    self.WORLD.blit(self.PLAYER.listItem[i].img, (rectx, recty))
                    x += 1
                else:
                    x = 0
                    y += 1
    def loadEquidment(self):
        if self.PLAYER.mask:
            self.WORLD.blit(self.PLAYER.mask.img, (548, 212))
        if self.PLAYER.weapon:
            self.WORLD.blit(self.PLAYER.weapon.img, (548, 384))
        if self.PLAYER.shoes:
            self.WORLD.blit(self.PLAYER.shoes.img, (548, 545))
        
    def loadButton(self):
        def get_font2(size): # Returns Press-Start-2P in the desired size
            return pygame.font.Font("assets/img/font2.ttf", size)

        x = 0
        y = 0
        for i in range(0, len(self.PLAYER.listItem)):
            if y <= 3:
                if x <= 3:
                    rectx = 944 +  (x * 144)
                    recty = 318 + (y * 144)
                    ButonCreateEquip = Button(image=None, pos=(rectx, recty), text_input="Trang bị", font=get_font2(10), base_color="White", hovering_color="Green")
                    ButonCreateEquip.update(self.WORLD)
                    self.ListButtonEquipItem.append(ButonCreateEquip)
                    
                    x += 1
                else:
                    x = 0
                    y += 1


    def click_PickUpGarbage(self):
        if len(self.MATERTIALS) > 0:
            self.MATERTIALS.empty()
            listTotal = [1, 2, 3, 4]
            self.PLAYER.AddToBag(0, random.choice(listTotal))
            self.PLAYER.AddToBag(1, random.choice(listTotal))
            self.PLAYER.AddToBag(2, random.choice(listTotal))
        else:
            print("Trống")


    def click_CreateEquipment(self): #Form tạo trang bị

        self.PLAYER.checkEquipment()
        print(len(self.PLAYER.ListEquipmentCanCreate))

        optionCreate = 0
        totalCreate = [99, 99, 99]
        
        def get_font(size): # Returns Press-Start-2P in the desired size
            return pygame.font.Font("assets/img/font.ttf", size)
        def get_font2(size): # Returns Press-Start-2P in the desired size
            return pygame.font.Font("assets/img/font2.ttf", size)

        self.WORLD.blit(pygame.transform.scale(pygame.image.load("./assets/img/BG_Info_Player04.png"), (WORLD_X, WORLD_Y)), (0, 0))
        while True:
            MOUSE_POS = pygame.mouse.get_pos()
            
            TEXT = get_font2(60).render("Tạo trang bị", True, "White")
            OPTIONS_RECT = TEXT.get_rect(center=(720, 80))
            self.WORLD.blit(TEXT, OPTIONS_RECT)

            
            MaskLV1 = Button(image=None, pos=(984, 328), text_input="MaskLV1", font=get_font(10), base_color="White", hovering_color="Red")
            MaskLV1.update(self.WORLD)

            MaskLV2 = Button(image=None, pos=(1157, 328), text_input="MaskLV2", font=get_font(10), base_color="White", hovering_color="Red")
            MaskLV2.update(self.WORLD)

            MaskLV3 = Button(image=None, pos=(1328, 328), text_input="MaskLV3", font=get_font(10), base_color="White", hovering_color="Red")
            MaskLV3.update(self.WORLD)


            WeaponLV1 = Button(image=None, pos=(984, 494), text_input="WeaponLV1", font=get_font(10), base_color="White", hovering_color="Red")
            WeaponLV1.update(self.WORLD)

            WeaponLV2 = Button(image=None, pos=(1157, 494), text_input="WeaponLV2", font=get_font(10), base_color="White", hovering_color="Red")
            WeaponLV2.update(self.WORLD)

            WeaponLV3 = Button(image=None, pos=(1328, 494), text_input="WeaponLV3", font=get_font(10), base_color="White", hovering_color="Red")
            WeaponLV3.update(self.WORLD)

            ShoeLV1 = Button(image=None, pos=(984, 660), text_input="WeaponLV1", font=get_font(10), base_color="White", hovering_color="Red")
            ShoeLV1.update(self.WORLD)

            ShoeLV2 = Button(image=None, pos=(1157, 660), text_input="WeaponLV2", font=get_font(10), base_color="White", hovering_color="Red")
            ShoeLV2.update(self.WORLD)

            ShoeLV3 = Button(image=None, pos=(1328, 660), text_input="WeaponLV3", font=get_font(10), base_color="White", hovering_color="Red")
            ShoeLV3.update(self.WORLD)


            Total_Flatis = get_font(20).render(str(self.PLAYER.Bag[0]), True, "White")
            self.WORLD.blit(Total_Flatis, (971, 740))
            Total_Glass = get_font(20).render(str(self.PLAYER.Bag[1]), True, "White")
            self.WORLD.blit(Total_Glass, (1210, 740))
            Total_Cans = get_font(20).render(str(self.PLAYER.Bag[2]), True, "White")
            self.WORLD.blit(Total_Cans, (1404, 740))

            #----------------------------------------------------------------------
            ButonCreateEquip = Button(image=None, pos=(388, 764), text_input="Tạo", font=get_font2(35), base_color="White", hovering_color="Green")
            ButonCreateEquip.update(self.WORLD)
          
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == ord('q'):
                        self.WORLD.blit(pygame.transform.scale(pygame.image.load("./assets/img/BG_Info_Player03.png"), (WORLD_X, WORLD_Y)), (0, 0))
                        return
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ButonCreateEquip.checkForInput(MOUSE_POS):
                        self.PLAYER.createEquipment(optionCreate, totalCreate)
                        self.WORLD.blit(pygame.transform.scale(pygame.image.load("./assets/img/BG_Info_Player04.png"), (WORLD_X, WORLD_Y)), (0, 0))


                    if MaskLV1.checkForInput(MOUSE_POS):
                        self.LoadItemInScreen(EquipmentListImage[0], 1, InfoEquidmentListImage[0])
                        optionCreate = 0
                        totalCreate = TotalCanCreateMaskLv1

                    if MaskLV2.checkForInput(MOUSE_POS):
                        self.LoadItemInScreen(EquipmentListImage[1], 2, InfoEquidmentListImage[1])
                        optionCreate = 1
                        totalCreate = TotalCanCreateMaskLv2

                    if MaskLV3.checkForInput(MOUSE_POS):
                        self.LoadItemInScreen(EquipmentListImage[2], 3, InfoEquidmentListImage[2])
                        optionCreate = 2
                        totalCreate = TotalCanCreateMaskLv3

                    if WeaponLV1.checkForInput(MOUSE_POS):
                        self.LoadItemInScreen(EquipmentListImage[3], 4, InfoEquidmentListImage[3])
                        optionCreate = 3
                        totalCreate = TotalCanCreateWeaponLv1

                    if WeaponLV2.checkForInput(MOUSE_POS):
                        self.LoadItemInScreen(EquipmentListImage[4], 5, InfoEquidmentListImage[4])
                        optionCreate = 4
                        totalCreate = TotalCanCreateWeaponLv2
                    if WeaponLV3.checkForInput(MOUSE_POS):
                        self.LoadItemInScreen(EquipmentListImage[5], 6, InfoEquidmentListImage[5])
                        optionCreate = 5
                        totalCreate = TotalCanCreateWeaponLv3
                    if ShoeLV1.checkForInput(MOUSE_POS):
                        self.LoadItemInScreen(EquipmentListImage[6], 7, InfoEquidmentListImage[6])
                        optionCreate = 6
                        totalCreate = TotalCanCreateShoesLv1
                    if ShoeLV2.checkForInput(MOUSE_POS):
                        self.LoadItemInScreen(EquipmentListImage[7], 8, InfoEquidmentListImage[7])
                        optionCreate = 7
                        totalCreate = TotalCanCreateShoesLv2
                    if ShoeLV3.checkForInput(MOUSE_POS):
                        self.LoadItemInScreen(EquipmentListImage[8], 9, InfoEquidmentListImage[8])
                        optionCreate = 8
                        totalCreate = TotalCanCreateShoesLv3

                    
             
            
            pygame.display.update()
    def LoadItemInScreen(self, itemInScreen, option, itemInScreen2):
        def get_font(size): # Returns Press-Start-2P in the desired size
            return pygame.font.Font("assets/img/font.ttf", size)
        self.WORLD.blit(pygame.transform.scale(pygame.image.load("./assets/img/BG_Info_Player04.png"), (WORLD_X, WORLD_Y)), (0, 0))
        self.WORLD.blit(itemInScreen, (156, 316))
        self.WORLD.blit(itemInScreen2, (271, 289))


        
        if option == 1:
            Total_Flatis = get_font(20).render(str(TotalCanCreateMaskLv1[0]), True, "White")
            self.WORLD.blit(Total_Flatis, (210, 549))
            Total_Glass = get_font(20).render(str(TotalCanCreateMaskLv1[1]), True, "White")
            self.WORLD.blit(Total_Glass, (425, 549))
            Total_Cans = get_font(20).render(str(TotalCanCreateMaskLv1[2]), True, "White")
            self.WORLD.blit(Total_Cans, (588, 549))
        if option == 2:
            Total_Flatis = get_font(20).render(str(TotalCanCreateMaskLv2[0]), True, "White")
            self.WORLD.blit(Total_Flatis, (210, 549))
            Total_Glass = get_font(20).render(str(TotalCanCreateMaskLv2[1]), True, "White")
            self.WORLD.blit(Total_Glass, (425, 549))
            Total_Cans = get_font(20).render(str(TotalCanCreateMaskLv2[2]), True, "White")
            self.WORLD.blit(Total_Cans, (588, 549))
        if option == 3:
            Total_Flatis = get_font(20).render(str(TotalCanCreateMaskLv3[0]), True, "White")
            self.WORLD.blit(Total_Flatis, (210, 549))
            Total_Glass = get_font(20).render(str(TotalCanCreateMaskLv3[1]), True, "White")
            self.WORLD.blit(Total_Glass, (425, 549))
            Total_Cans = get_font(20).render(str(TotalCanCreateMaskLv3[2]), True, "White")
            self.WORLD.blit(Total_Cans, (588, 549))

        if option == 4:
            Total_Flatis = get_font(20).render(str(TotalCanCreateWeaponLv1[0]), True, "White")
            self.WORLD.blit(Total_Flatis, (210, 549))
            Total_Glass = get_font(20).render(str(TotalCanCreateWeaponLv1[1]), True, "White")
            self.WORLD.blit(Total_Glass, (425, 549))
            Total_Cans = get_font(20).render(str(TotalCanCreateWeaponLv1[2]), True, "White")
            self.WORLD.blit(Total_Cans, (588, 549))
        if option == 5:
            Total_Flatis = get_font(20).render(str(TotalCanCreateWeaponLv2[0]), True, "White")
            self.WORLD.blit(Total_Flatis, (210, 549))
            Total_Glass = get_font(20).render(str(TotalCanCreateWeaponLv2[1]), True, "White")
            self.WORLD.blit(Total_Glass, (425, 549))
            Total_Cans = get_font(20).render(str(TotalCanCreateWeaponLv2[2]), True, "White")
            self.WORLD.blit(Total_Cans, (588, 549))
        if option == 6:
            Total_Flatis = get_font(20).render(str(TotalCanCreateWeaponLv3[0]), True, "White")
            self.WORLD.blit(Total_Flatis, (210, 549))
            Total_Glass = get_font(20).render(str(TotalCanCreateWeaponLv3[1]), True, "White")
            self.WORLD.blit(Total_Glass, (425, 549))
            Total_Cans = get_font(20).render(str(TotalCanCreateWeaponLv3[2]), True, "White")
            self.WORLD.blit(Total_Cans, (588, 549))
        if option == 7:
            Total_Flatis = get_font(20).render(str(TotalCanCreateShoesLv1[0]), True, "White")
            self.WORLD.blit(Total_Flatis, (210, 549))
            Total_Glass = get_font(20).render(str(TotalCanCreateShoesLv1[1]), True, "White")
            self.WORLD.blit(Total_Glass, (425, 549))
            Total_Cans = get_font(20).render(str(TotalCanCreateShoesLv1[2]), True, "White")
            self.WORLD.blit(Total_Cans, (588, 549))
        
        if option == 8:
            Total_Flatis = get_font(20).render(str(TotalCanCreateShoesLv2[0]), True, "White")
            self.WORLD.blit(Total_Flatis, (210, 549))
            Total_Glass = get_font(20).render(str(TotalCanCreateShoesLv2[1]), True, "White")
            self.WORLD.blit(Total_Glass, (425, 549))
            Total_Cans = get_font(20).render(str(TotalCanCreateShoesLv2[2]), True, "White")
            self.WORLD.blit(Total_Cans, (588, 549))
        if option == 9:
            Total_Flatis = get_font(20).render(str(TotalCanCreateShoesLv3[0]), True, "White")
            self.WORLD.blit(Total_Flatis, (210, 549))
            Total_Glass = get_font(20).render(str(TotalCanCreateShoesLv3[1]), True, "White")
            self.WORLD.blit(Total_Glass, (425, 549))
            Total_Cans = get_font(20).render(str(TotalCanCreateShoesLv3[2]), True, "White")
            self.WORLD.blit(Total_Cans, (588, 549))
        

    def creatMatertial(self, x, y):
        self.MATERTIAL = Material(MaterialListImage[0], [x, y])
        self.MATERTIAL.inDisplay = True
        self.MATERTIALS.add(self.MATERTIAL)
