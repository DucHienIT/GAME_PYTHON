from hashlib import new
from re import S
from tkinter import CENTER
from numpy import imag
import pygame
from sympy import centroid
from obj.define import *
from obj.map import *
from multipledispatch import dispatch

class Player(pygame.sprite.Sprite):
    steps = DEFAULT_STEPS

    clock = pygame.time.Clock()
    def __init__(self, path, position):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.frame = 0

        self.hp = 100

        self.right = True
        self.images = []
        self.imagesRun = []
        self.imagesJump = []
        self.imagesAttack = []

        self.isRun = False
        self.isAttack = False
        self.goku_Run_Index = 0
        self.goku_Stop_Index = 0
        self.goku_Attack_Index = 0
        
        self.comboCount = 0
       
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, (PLAYER_SIZE_X, PLAYER_SIZE_Y))
        
        img.convert_alpha()  # optimise alpha
        img.set_colorkey(ALPHA)  # set alpha
        self.image = img
        self.rect = self.image.get_rect(center = (position[0], position[1]))

        # Image Stop
        self.AddImage("assets/img/goku01.png", 3)
        self.AddImage("assets/img/goku02.png", 3)
        self.AddImage("assets/img/goku03.png", 3)
        self.AddImage("assets/img/goku04.png", 3)
        self.AddImage("assets/img/goku05.png", 3)
        self.AddImage("assets/img/goku06.png", 3)

        # Image Run
        self.AddImage("assets/img/goku_run01.png", 0)
        self.AddImage("assets/img/goku_run02.png", 0)
        self.AddImage("assets/img/goku_run03.png", 0)
        self.AddImage("assets/img/goku_run04.png", 0)
        self.AddImage("assets/img/goku_run05.png", 0)
        self.AddImage("assets/img/goku_run06.png", 0)
        self.AddImage("assets/img/goku_run07.png", 0)
        self.AddImage("assets/img/goku_run08.png", 0)

        self.AddImage("assets/img/goku_atk01.png", 2)
        self.AddImage("assets/img/goku_atk02.png", 2)
        self.AddImage("assets/img/goku_atk03.png", 2)
        self.AddImage("assets/img/goku_atk04.png", 2)
        self.AddImage("assets/img/goku_atk05.png", 2)
        self.AddImage("assets/img/goku_atk06.png", 2)
        self.AddImage("assets/img/goku_atk07.png", 2)
        self.AddImage("assets/img/goku_atk08.png", 2)
        self.AddImage("assets/img/goku_atk09.png", 2)
        self.AddImage("assets/img/goku_atk10.png", 2)
        self.AddImage("assets/img/goku_atk11.png", 2)
        self.AddImage("assets/img/goku_atk12.png", 2)
        self.AddImage("assets/img/goku_atk13.png", 2)
        self.AddImage("assets/img/goku_atk14.png", 2)
        self.AddImage("assets/img/goku_atk15.png", 2)
        self.AddImage("assets/img/goku_atk16.png", 2)
        self.AddImage("assets/img/goku_atk17.png", 2)
    
    def AddImage(self, path, action):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, (PLAYER_SIZE_X, PLAYER_SIZE_Y))
        
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
        if self.rect.x + x < 0 or self.rect.x + x > WORLD_X - PLAYER_SIZE_X:
            return False
        return True
    
    def isMovableY(self, y):
        if self.rect.y + y < 0 or self.rect.y + y > WORLD_Y - PLAYER_SIZE_Y:
            return False
        return True    


    def animationRun(self):
        self.isRun = True
        if self.goku_Run_Index < 7:
            self.goku_Run_Index += 1
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
        if self.goku_Stop_Index < 5:
            self.goku_Stop_Index += 1
        else:
            self.goku_Stop_Index = 0

        new_Image = self.images[self.goku_Stop_Index]
        self.image = pygame.transform.scale(new_Image, (PLAYER_SIZE_X, PLAYER_SIZE_Y))
        
        if self.right == False:
            self.image = pygame.transform.flip(self.image, True, False)

    def animationAttack(self):
        if self.goku_Attack_Index < 16:
            if self.goku_Attack_Index == 9:
                if self.comboCount > 2:
                    self.goku_Attack_Index += 1
                else:
                    self.goku_Attack_Index = 0
            else:
                self.goku_Attack_Index += 1
        else:
            self.goku_Attack_Index = 0
        
        new_Image = self.imagesAttack[self.goku_Attack_Index]

        size_tmpX = PLAYER_SIZE_X
        size_tmpY = PLAYER_SIZE_Y
        if self.goku_Attack_Index in [13, 14, 15, 16]:
            size_tmpX += 60
            
            if self.right == True:
                if self.isMovableX(10):
                    self.rect.x += 10
            else:
                if self.isMovableX(-10):
                    self.rect.x -= 10

        self.image = pygame.transform.scale(new_Image, (size_tmpX, size_tmpY))
           

        if self.right == False:
            self.image = pygame.transform.flip(self.image, True, False)
        


    def update(self):
        if self.hp <= 0:
            self.rect.x = 500
            self.rect.y = 500
            self.hp = 100

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

    def infomationPlayer_InScreen(self):
        pass

        

