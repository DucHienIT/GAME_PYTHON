#%%
from errno import ESTALE
from random import random
from tkinter import CURRENT
from matplotlib.pyplot import step
import random
import pygame
import sys
import os
from pyparsing import Word

from sympy import false

'''
Variables
'''

WORLD_X = 960
WORLD_Y = 720
PLAYER_SIZE_X = 100
PLAYER_SIZE_Y = 100
START_X = (WORLD_X-PLAYER_SIZE_X)/2
START_Y = (WORLD_Y-PLAYER_SIZE_Y)*2/3
FPS = 40
ANIMATION = 4

BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)
ALPHA = (0, 255, 0)

WORLD = pygame.display.set_mode([WORLD_X, WORLD_Y])
KEY_MANAGER = 0 #Nếu số keyUP == keyDOWN thì dừng nhân vật

RIGHT_MAP_POS = (WORLD_X-50, WORLD_Y/2+10)
MAP = (
    pygame.transform.scale(pygame.image.load('home.png'), (WORLD_X, WORLD_Y)),
    pygame.transform.scale(pygame.image.load('shop.png'), (WORLD_X, WORLD_Y)),
    pygame.transform.scale(pygame.image.load('gym.png'), (WORLD_X, WORLD_Y)),
    pygame.transform.scale(pygame.image.load('N1.png'), (WORLD_X, WORLD_Y)),
    pygame.transform.scale(pygame.image.load('N2.png'), (WORLD_X, WORLD_Y)),
    pygame.transform.scale(pygame.image.load('b1.png'), (WORLD_X, WORLD_Y)),
    pygame.transform.scale(pygame.image.load('b2.png'), (WORLD_X, WORLD_Y)),
    pygame.transform.scale(pygame.image.load('b3.png'), (WORLD_X, WORLD_Y)),
    pygame.transform.scale(pygame.image.load('b4.png'), (WORLD_X, WORLD_Y))
)

'''
Game setup
'''
backdrop = MAP[0]
clock = pygame.time.Clock()
pygame.init()
backdropbox = WORLD.get_rect()
main = True
'''
Objects
'''


class Player(pygame.sprite.Sprite):
    """
    Spawn a player
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.images = []
        for i in range(1, 5):
            img = pygame.image.load('player1.png')
            img = pygame.transform.flip(img, True, False)
            img = pygame.transform.scale(img, (75,75))
            img.convert_alpha()  # optimise alpha
            img.set_colorkey(ALPHA)  # set alpha
            self.images.append(img)
            self.image = self.images[0]
            self.rect = self.image.get_rect()

    '''
    Chuyển map
    '''
    def footMap(self, currentMap):
        return currentMap

    def footRightMap(self, currentMap):
        if self.rect.centerx > RIGHT_MAP_POS[0]-20 and\
    self.rect.centery > RIGHT_MAP_POS[1]-50 and\
        self.rect.centerx < RIGHT_MAP_POS[0]+50 and\
            self.rect.centery < RIGHT_MAP_POS[1]+20:
            self.rect.x = 100
            self.rect.centery = WORLD_Y/2
            currentMap = MAP[3]
        return currentMap

        '''
            Giới hạn vị trí đi
        '''

    def isMovableX(self, x):
        if self.rect.x + x < 0 or self.rect.x + x > WORLD_X - PLAYER_SIZE_X:
            return False
        return True
    
    def isMovableY(self, y):
        if self.rect.y + y < 0 or self.rect.y + y > WORLD_Y - PLAYER_SIZE_Y:
            return False
        return True

    def control(self, x, y):
        """
        control player movement
        """
        self.movex += x
        self.movey += y

    def update(self):
        """
        Update sprite position
        """

        if self.isMovableX(self.movex):
            self.rect.x = self.rect.x + self.movex
        if self.isMovableY(self.movey):
            self.rect.y = self.rect.y + self.movey

        # moving left
        if self.movex < 0:
            self.frame += 1
            if self.frame > 3*ANIMATION:
                self.frame = 0
            self.image = pygame.transform.flip(self.images[self.frame // ANIMATION], True, False)

        # moving right
        if self.movex > 0:
            self.frame += 1
            if self.frame > 3*ANIMATION:
                self.frame = 0
            self.image = self.images[self.frame//ANIMATION]


'''
Setup
'''
player = Player()  # spawn player
player.rect.x = START_X # go to x
player.rect.y = START_Y  # go to y
player_list = pygame.sprite.Group()
player_list.add(player)
steps = 10

'''
Main Loop
'''
while main:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            try:
                sys.exit()
            finally:
                main = False

        if event.type == pygame.KEYDOWN:
            if event.key == ord('q'):
                pygame.quit()
                try:
                    sys.exit()
                finally:
                    main = False
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(-steps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(steps, 0)
            if event.key == pygame.K_UP or event.key == ord('w'):
                player.control(0, -steps)
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                player.control(0, steps)
            KEY_MANAGER += 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(steps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(-steps, 0)
            if event.key == pygame.K_UP or event.key == ord('w'):
                player.control(0, steps)
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                player.control(0, -steps)
            KEY_MANAGER -= 1
        elif KEY_MANAGER == 0:
            player.movex = 0
            player.movey = 0

    backdrop = player.footRightMap(backdrop)
    WORLD.blit(backdrop, backdropbox)
    player.update()
    pygame.draw.circle(WORLD, (0,0,0), RIGHT_MAP_POS, 20)
    player_list.draw(WORLD)
    pygame.display.flip()
    clock.tick(FPS)
# %%
