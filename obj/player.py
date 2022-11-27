import string
import pygame
from sympy import false
from obj.define import *
from obj.map import *
from obj.equipment import *
class Player(pygame.sprite.Sprite):
    steps = DEFAULT_STEPS

    clock = pygame.time.Clock()
    def __init__(self, path, info):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.hp = info[0]
        self.mp = info[1]
        self.atk = info[2]
        self.DEF = info[3]
        self.exp = info[4]
        self.level = info[5]
        self.freeValue = 0 # chỉ số tự do người chơi cộng vào các thuộc tính
        self.max_hp = info[0]
        self.max_mp = info[1]
        self.max_atk = info[2]
        self.max_DEF = info[3]
        self.max_exp = info[self.level-1]

        self.totalAtkEquipment = 0

        self.right = True
        self.images = []
        self.imagesRun = []
        self.imagesAttack = []

        self.isRun = False
        self.isAttack = False
        self.goku_Run_Index = 0
        self.goku_Stop_Index = 0
        self.goku_Attack_Index = 0
        
        self.comboCount = 0
        self.room = False


        # Túi đồ nhân vật
        self.Bag = [20, 20, 20]  # Nilon - Thủy tinh - Lon 
        self.listItem = []


        # Trang bị nhân vật
        self.ListEquipmentCanCreate = []
        
        self.mask = None
        self.weapon = None
        self.shoes = None
       
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, (PLAYER_SIZE_X, PLAYER_SIZE_Y))
        
        img.convert_alpha()  # optimise alpha
        img.set_colorkey(ALPHA)  # set alpha
        self.image = img
        self.rect = self.image.get_rect(center = (info[6], info[7]))

        # Image Stop
        
        for i in range(19, 29):
            strImage = "./assets/img/PlayerStand/Untitled-" + str(i) + ".png"
            self.AddImage(strImage, 3)

        # Image Run
        for i in range(1, 33):
            strImage = "./assets/img/PlayerMove/Untitled-" + str(i) + ".png"
            self.AddImage(strImage, 0)
        
        for i in range(12, 43):
            strImag = "./assets/img/PlayerAttack/Untitled-" + str(i) + ".png"
            self.AddImage(strImag, 2)

        
    
    def AddToBag(self, type, total):
      
        if type == 0: 
            self.Bag[0] += total
        elif type == 1: 
            self.Bag[1] += total
        elif type == 2: 
            self.Bag[2] += total
        else:
            pass


    def AddImage(self, path, action):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, (PLAYER_SIZE_X, PLAYER_SIZE_Y))
        img = pygame.transform.flip(img, True, False)
        img.convert_alpha() 
        img.set_colorkey(ALPHA)
        if action == 0: #run
            self.imagesRun.append(img)
        elif action == 1: #jump
            self.imagesJump.append(img)
        elif action == 2: #attack
            self.imagesAttack.append(img)
        else:
            self.images.append(img)

    def control(self, x, y):
        self.movex += x
        self.movey += y

    def isMovableX(self, x):
        if self.room:
            if self.rect.x + x < 0 or self.rect.x + x > WORLD_X - PLAYER_SIZE_X:
                return False
        else:
            if self.rect.x + x < PLAYER_SIZE_X or self.rect.x + x > WORLD_X - PLAYER_SIZE_X*2:
                return False
        return True
    
    def isMovableY(self, y):
        if self.room:
            if self.rect.y + y < 0 or self.rect.y + y > WORLD_Y - PLAYER_SIZE_Y:
                return False
        else:
            if self.rect.y + y < PLAYER_SIZE_Y or self.rect.y + y > WORLD_Y - PLAYER_SIZE_Y*2:
                return False
        return True    

    def animationRun(self):
        self.isRun = True
        if self.goku_Run_Index < 30:
            self.goku_Run_Index += 2
        else:
            self.goku_Run_Index = 0

        new_Image = self.imagesRun[self.goku_Run_Index]
        self.image = pygame.transform.scale(new_Image, (PLAYER_SIZE_X, PLAYER_SIZE_Y))
       
        if self.right == False:
            self.image = pygame.transform.flip(self.image, True, False)

    
    def animationJump(self, index, pos):
        new_Image = self.imagesJump[index]
        self.image = pygame.transform.scale(new_Image, (PLAYER_SIZE_X, PLAYER_SIZE_Y))
        
        if self.right == False:
            self.image = pygame.transform.flip(self.image, True, False)

    def animationStop(self):
        if self.goku_Stop_Index < 9:
            self.goku_Stop_Index += 1
        else:
            self.goku_Stop_Index = 0

        new_Image = self.images[self.goku_Stop_Index]
        self.image = pygame.transform.scale(new_Image, (PLAYER_SIZE_X-50, PLAYER_SIZE_Y))
        
        if self.right == False:
            self.image = pygame.transform.flip(self.image, True, False)

    def animationAttack(self):
        if self.goku_Attack_Index < 29:
            # if self.goku_Attack_Index == 9:
            #     if self.comboCount > 2:
            #         self.goku_Attack_Index += 1
            #     else:
            #         self.goku_Attack_Index = 0
            # else:
            #     self.goku_Attack_Index += 1
            self.goku_Attack_Index += 2
        else:
            self.goku_Attack_Index = 0
        
        new_Image = self.imagesAttack[self.goku_Attack_Index]

        size_tmpX = PLAYER_SIZE_X
        size_tmpY = PLAYER_SIZE_Y
        #if self.goku_Attack_Index in [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]:
            #size_tmpX += 60
            
            # if self.right == True:
            #     if self.isMovableX(10):
            #         self.rect.x += 10
            # else:
            #     if self.isMovableX(-10):
            #         self.rect.x -= 10

        self.image = pygame.transform.scale(new_Image, (size_tmpX + 25, size_tmpY))
        if self.right == False:
            self.image = pygame.transform.flip(self.image, True, False)

    def savePlayer(self):
        string = f'{int(self.hp)} {int(self.mp)} {int(self.atk)} {int(self.DEF)} {int(self.exp)} {int(self.level)} {int(self.rect[0])} {int(self.rect[1])}'
        f = open("./assets/data/player.txt", "w")
        f.write(string)
        f.close()

    def update(self):
        if (self.isMovableX(self.movex)):
            self.rect.x = self.rect.x + self.movex
        if (self.isMovableY(self.movey)):
            self.rect.y = self.rect.y + self.movey
        # moving left => flip player
        if self.movex < 0:
            self.frame += 1
            if self.right == True:
                self.image = pygame.transform.flip(self.image, True, False)
                self.right = False

        # moving right => flip player
        if self.movex > 0:
            self.frame += 1
            if self.right == False:
                self.image = pygame.transform.flip(self.image, True, False)
                self.right = True
        
        if self.exp >= listExpUpLevel[self.level - 1]:
            self.exp = 0
            self.level += 1
            self.freeValue += 5

        if self.hp <= HP:
            self.hp += (0.0005*HP)
        if self.mp <= MP:
            self.mp += (0.01*MP)


    def equipped(self, option, item):
        self.totalAtkEquipment += item.atk
        if option < 3: #Trang bị áo quần
            self.mask = item

        elif option  < 6: # Trang bị vũ khí
            self.weapon = item

        elif option < 9: #Trang bị giày
            self.shoes = item

        

    
    def createEquipment(self, option, total): # total (list): số material cần để tạo trang bị
        
        if self.Bag[0] >= total[0] and self.Bag[1] >= total[1] and self.Bag[2] >= total[2]:
            equip = equipment(EquipmentListImage[option], total, option)
            self.listItem.append(equip)
            
            self.equipped(option, equip)

            self.Bag[0] -= total[0] # Tạo xong phải mất material
            self.Bag[1] -= total[1]
            self.Bag[2] -= total[2]



    def checkEquipment(self):
        
        # Mặt nạ
        if self.Bag[0] >= TotalCanCreateMaskLv1[0] and self.Bag[1] >= TotalCanCreateMaskLv1[1] and self.Bag[2] >= TotalCanCreateMaskLv1[2]:
            self.ListEquipmentCanCreate.append(1)
        if self.Bag[0] >= TotalCanCreateMaskLv2[0] and self.Bag[1] >= TotalCanCreateMaskLv2[1] and self.Bag[2] >= TotalCanCreateMaskLv2[2]:
            self.ListEquipmentCanCreate.append(2)
        if self.Bag[0] >= TotalCanCreateMaskLv3[0] and self.Bag[1] >= TotalCanCreateMaskLv3[1] and self.Bag[2] >= TotalCanCreateMaskLv3[2]:
            self.ListEquipmentCanCreate.append(3)
        
        # Vũ khí
        if self.Bag[0] >= TotalCanCreateWeaponLv1[0] and self.Bag[1] >= TotalCanCreateWeaponLv1[1] and self.Bag[2] >= TotalCanCreateWeaponLv1[2]:
            self.ListEquipmentCanCreate.append(4)
        if self.Bag[0] >= TotalCanCreateWeaponLv2[0] and self.Bag[1] >= TotalCanCreateWeaponLv2[1] and self.Bag[2] >= TotalCanCreateWeaponLv2[2]:
            self.ListEquipmentCanCreate.append(5)
        if self.Bag[0] >= TotalCanCreateWeaponLv3[0] and self.Bag[1] >= TotalCanCreateWeaponLv3[1] and self.Bag[2] >= TotalCanCreateWeaponLv3[2]:
            self.ListEquipmentCanCreate.append(6)

        # Giày
        if self.Bag[0] >= TotalCanCreateShoesLv1[0] and self.Bag[1] >= TotalCanCreateShoesLv1[1] and self.Bag[2] >= TotalCanCreateShoesLv1[2]:
            self.ListEquipmentCanCreate.append(7)
        if self.Bag[0] >= TotalCanCreateShoesLv2[0] and self.Bag[1] >= TotalCanCreateShoesLv2[1] and self.Bag[2] >= TotalCanCreateShoesLv2[2]:
            self.ListEquipmentCanCreate.append(8)
        if self.Bag[0] >= TotalCanCreateShoesLv3[0] and self.Bag[1] >= TotalCanCreateShoesLv3[1] and self.Bag[2] >= TotalCanCreateShoesLv3[2]:
            self.ListEquipmentCanCreate.append(9)




