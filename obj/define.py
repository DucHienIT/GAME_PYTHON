import pygame
from win32api import GetSystemMetrics

# Size of SCREEN
WORLD_X = GetSystemMetrics(0)
WORLD_Y = GetSystemMetrics(1)

# unit 
u = WORLD_X/1536

# Tốc độ khung hình
FPS = 60
listExpUpLevel = [i*100 for i in range(1, 100)]


listExpUpLevel.append(999999999)
# Một số màu
BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)
ALPHA = (0, 255, 0)

# size ô chuyển map
SWITCH_SIZE = 200 * u

# player size
PLAYER_SIZE_X = 75
PLAYER_SIZE_Y = 75

# Vị trí bắt đầu của player
PLAYER_START_POS = {
    'x': int(WORLD_X/2),
    'y': int(WORLD_Y/2)
}

# key animation
ANIMATION = 4
HP = 1000
MP = 100
ATK = 10
# Tốc độ di chuyển
DEFAULT_STEPS = 7


Info_Charater = pygame.transform.scale(pygame.image.load('./assets/img/Info_Charater.png'), (286*1.5, 113*1.5))
Info_Charater_Rect = Info_Charater.get_rect(center = (286*1.5, 113*1.5))
Hp_Bar = pygame.image.load('./assets/img/HP_Bar.png')
Mp_Bar = pygame.image.load('./assets/img/Mana_Bar.png')
Exp_Bar = pygame.image.load("./assets/img/EXP_Bar.png")
#Load image
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


MaracaListImageAttach = []
for i in range (1, 10):
    strImage = "./assets/img/Maraca0" + str(i) + ".png"
    tmp = pygame.image.load(strImage)
    MaracaListImageAttach.append(tmp)
def checkForInput(position):
	if position[0] in range(Info_Charater_Rect.left, Info_Charater_Rect.right) and position[1] in range(Info_Charater_Rect.top, Info_Charater_Rect.bottom):
		return True
	return False