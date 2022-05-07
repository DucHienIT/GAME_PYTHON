import pygame
# Size of SCREEN
WORLD_X = 960
WORLD_Y = 720

# Tốc độ khung hình
FPS = 60

# Một số màu
BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)
ALPHA = (0, 255, 0)

# size ô chuyển map
SWITCH_SIZE = 80

# player size
PLAYER_SIZE_X = 75
PLAYER_SIZE_Y = 75

# Vị trí bắt đầu của player
PLAYER_START_POS = {
    'x': WORLD_X/2,
    'y': WORLD_Y - PLAYER_SIZE_Y
}

# key animation
ANIMATION = 4

# Tốc độ di chuyển
DEFAULT_STEPS = 7

list_Image = []
loadGame01 = pygame.transform.scale(pygame.image.load('./assets/img/loadGame_01.png'), (WORLD_X, WORLD_Y))
loadGame02 = pygame.transform.scale(pygame.image.load('./assets/img/loadGame_02.png'), (WORLD_X, WORLD_Y))
loadGame03 = pygame.transform.scale(pygame.image.load('./assets/img/loadGame_03.png'), (WORLD_X, WORLD_Y))
list_Image.append(loadGame01)
list_Image.append(loadGame02)
list_Image.append(loadGame03)
list_Image.append(loadGame01)
list_Image.append(loadGame02)
list_Image.append(loadGame03)
list_Image.append(loadGame01)
list_Image.append(loadGame02)
list_Image.append(loadGame03)
list_Image.append(loadGame01)
list_Image.append(loadGame02)
list_Image.append(loadGame03)
list_Image.append(loadGame01)
list_Image.append(loadGame02)
list_Image.append(loadGame03)


