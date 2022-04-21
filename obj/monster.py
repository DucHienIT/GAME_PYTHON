import pygame
from obj.define import *
from obj.map import *
import random

class Monster(pygame.sprite.Sprite):
    steps = DEFAULT_STEPS

    clock = pygame.time.Clock()
    def __init__(self, path, position):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.frame = 0
        
        list_tmp = [True, False, True, False]
        self.right = random.choice(list_tmp)

        self.images = []
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, (PLAYER_SIZE_X, PLAYER_SIZE_Y))

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
        
    def update(self):
        
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

    

