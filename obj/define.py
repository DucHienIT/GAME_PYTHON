import pygame
from win32api import GetSystemMetrics


# Size of SCREEN
WORLD_X = GetSystemMetrics(0) # 1536
WORLD_Y = GetSystemMetrics(1) # 864

# unit 
u = WORLD_X/1536

# Tốc độ khung hình
FPS = 120
listExpUpLevel = [i*100 for i in range(1, 100)]


LISTSWITCH = [[-859, -1296, -593, -1149], [-1370, -1510, -1898, -1916], [-2112, -2444, -1076, -1538], [-2444, -3368, -610, -1065], [-3540, -3785, -1597, -1825]]

listExpUpLevel.append(999999999)
# Một số màu
BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)
ALPHA = (0, 255, 0)

# size ô chuyển map
SWITCH_SIZE = 200 * u

# player size
PLAYER_SIZE_X = 150
PLAYER_SIZE_Y = 200

MONSTER_SIZE_X = 300
MONSTER_SIZE_Y = 300
# item size
ITEM_SIZE_X = 100
ITEM_SIZE_Y = 100

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

lockImage = pygame.image.load("./assets/img/lock.png")

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
for i in range (1, 34):
    strImage = "./assets/img/Monter/Untitled-" + str(i) + ".png"
    tmp = pygame.image.load(strImage)
    MaracaListImageAttach.append(tmp)
    
def checkForInput(position):
	if position[0] in range(Info_Charater_Rect.left, Info_Charater_Rect.right) and position[1] in range(Info_Charater_Rect.top, Info_Charater_Rect.bottom):
		return True
	return False



MaterialListImage = []
for i in range (1, 2):
    strImage = "./assets/img/Material0" + str(i) + ".png"
    tmp = pygame.image.load(strImage)
    MaterialListImage.append(tmp)
    

EquipmentListImage = []
for i in range (1, 10):
    strImage = "./assets/img/equipment/equip_" + str(i) + ".png"
    tmp = pygame.image.load(strImage)
    tmp = pygame.transform.scale(tmp, (100, 100))
    EquipmentListImage.append(tmp)

InfoEquidmentListImage = []
for i in range (1, 10):
    strIma = "./assets/img/InfoEquidment/" + str(i) + ".png"
    tm = pygame.image.load(strIma)
    tm = pygame.transform.scale(tm, (416, 208))
    InfoEquidmentListImage.append(tm)


MAP_LIST_IMAGE = []
for i in range (0, 16):
    strImage = "./assets/img/WorldMap/" + str(i) + ".jpg"
    tmp = pygame.image.load(strImage)
    tmp = pygame.transform.scale(tmp, (WORLD_X*3, WORLD_Y*3))
    MAP_LIST_IMAGE.append(tmp)



# Số lượng vật tư để tạo ra trang bị 
AttributeEquidList = []

TotalCanCreateMaskLv1 = [3, 3, 3]
AttributeMaskLv1 = [12, 14, 20] #atk, def, hp
AttributeEquidList.append(AttributeMaskLv1)

TotalCanCreateMaskLv2 = [9, 9, 9]
AttributeMaskLv2 = [21, 22, 30] #atk, def, hp
AttributeEquidList.append(AttributeMaskLv2)


TotalCanCreateMaskLv3 = [27, 27, 27]
AttributeMaskLv3 = [32, 33, 40] #atk, def, hp
AttributeEquidList.append(AttributeMaskLv3)


TotalCanCreateWeaponLv1 = [4, 4, 4]
AttributeWeaponLv1 = [12, 12, 20] #atk, def, hp
AttributeEquidList.append(AttributeWeaponLv1)


TotalCanCreateWeaponLv2 = [12, 11, 10]
AttributeWeaponLv2 = [22, 32, 31] #atk, def, hp
AttributeEquidList.append(AttributeWeaponLv2)


TotalCanCreateWeaponLv3 = [30, 32, 31]
AttributeWeaponLv3 = [32, 42, 31] #atk, def, hp
AttributeEquidList.append(AttributeWeaponLv3)


TotalCanCreateShoesLv1 = [4, 4, 4]
AttributeShoeLv1 = [10, 20, 25] #atk, def, hp
AttributeEquidList.append(AttributeShoeLv1)

TotalCanCreateShoesLv2 = [12, 11, 10]
AttributeShoeLv2 = [12, 31, 29] #atk, def, hp
AttributeEquidList.append(AttributeShoeLv2)


TotalCanCreateShoesLv3 = [30, 32, 31]
AttributeShoeLv3 = [15, 50, 40] #atk, def, hp
AttributeEquidList.append(AttributeShoeLv3)
