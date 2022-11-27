from matplotlib import animation
import pygame
from obj.define import *
from obj.map import *
from random import randint
from random import choice

class Monster(pygame.sprite.Sprite):
    steps = DEFAULT_STEPS

    clock = pygame.time.Clock()
    def __init__(self, Image, position):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.inDisplay = False
        self.hp = randint(3, 10) * 200
        self.Run_Index = 0
        list_tmp = [True, False, True, False]
        self.right = choice(list_tmp)

        self.images = []
        img = Image
        img = pygame.transform.scale(img, (MONSTER_SIZE_X, MONSTER_SIZE_Y))

        if self.right == False:
            img = pygame.transform.flip(img, True, False)
            self.movex = 3
        else:
            self.movex = -3
        
        img.convert_alpha()  # optimise alpha
        img.set_colorkey(ALPHA)  # set alpha

        self.image = img
        self.rect = self.image.get_rect(center = (position[0], position[1]))
    
    def AddImage(self, path, action):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, (MONSTER_SIZE_X, MONSTER_SIZE_Y))
        
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
        if self.rect.x + x < 0 or self.rect.x + x > WORLD_X - MONSTER_SIZE_X:
            return False
        return True
    
    def isMovableY(self, y):
        if self.rect.y + y < 0 or self.rect.y + y > WORLD_Y - MONSTER_SIZE_Y:
            return False
        return True    
    
    def animationRun(self):
        self.isRun = True
        if self.Run_Index < 32:
            self.Run_Index += 1
        else:
            self.Run_Index = 0  

        new_Image = MaracaListImageAttach[self.Run_Index]
        self.image = pygame.transform.scale(new_Image, (MONSTER_SIZE_X, MONSTER_SIZE_Y))
       
        if self.right == False:
            self.image = pygame.transform.flip(self.image, True, False)
        
    def update(self, pos_PlayerX, pos_PlayerY):
        
        if self.rect.centerx < pos_PlayerX - MONSTER_SIZE_X/2 :
            self.movex = 2
        elif self.rect.centerx > pos_PlayerX  + MONSTER_SIZE_X/2:
            self.movex = -2
        else:
            self.movex = 0

        if self.rect.centery < pos_PlayerY :
            self.movey = 2
        elif self.rect.centery > pos_PlayerY:
            self.movey = -2
        else:
            self.movey = 0
        
        if (self.isMovableX(self.movex)):
            self.rect.x = self.rect.x + self.movex
        else:
            self.movex = - self.movex
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

    

