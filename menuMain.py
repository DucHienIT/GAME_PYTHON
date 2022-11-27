import pygame, sys
from obj.button import Button
import newGame
from obj.define import *
from obj.map import *
from obj.player import *
from obj.monster import *
from obj.start_map import *

def init():
    pygame.init()
    SCREEN = pygame.display.set_mode((WORLD_X, WORLD_Y))
    pygame.display.set_caption("Destroy And Protect")
    BG = pygame.transform.scale(pygame.image.load("assets/img/Backgound002.jpg"), (WORLD_X, WORLD_Y))
    return SCREEN, BG

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/img/font.ttf", size)
def get_font2(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/img/font2.ttf", size)
def play():
    game = newGame.Program()
    game.START_MAP.createNewSwitch()
    game.startProcess()
    game.newPlayer()
    game.main()
    game.endProcess()    
    
def continue_(SCREEN, type):
    if type == 0:
        while True:
            CONTINUE_MOUSE_POS = pygame.mouse.get_pos()

            SCREEN.fill("white")

            CONTINUE_TEXT = get_font(45).render("There is no data.", True, "Black")
            CONTINUE_RECT = CONTINUE_TEXT.get_rect(center=(WORLD_X/2, 260))
            SCREEN.blit(CONTINUE_TEXT, CONTINUE_RECT)

            CONTINUE_BACK = Button(image=None, pos=(WORLD_X/2, 460), 
                                text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

            CONTINUE_BACK.changeColor(CONTINUE_MOUSE_POS)
            CONTINUE_BACK.update(SCREEN)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if CONTINUE_BACK.checkForInput(CONTINUE_MOUSE_POS):
                        main_menu()
            pygame.display.flip()
    else:
        game = newGame.Program()
        game.startProcess()
        game.START_MAP.loadSwitch()
        game.main()
        game.endProcess()
        print(game.START_MAP.LIST_SWITCH)
        del game

def main_menu():
    SCREEN, BG = init()
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font2(100).render("Destroy And Protect", True, "#F0C61B")
        MENU_RECT = MENU_TEXT.get_rect(center=(WORLD_X/2, 150*u))
        PLAY_BUTTON = Button(image=pygame.image.load("./assets/img/Play Rect.png"), pos=(WORLD_X/2, 350*u), 
                            text_input="PLAY", font=get_font2(100), base_color="#d7fcd4", hovering_color="White")
        CONTINUE_BUTTON = Button(image=pygame.image.load("./assets/img/options Rect.png"), pos=(WORLD_X/2, 500*u), 
                            text_input="CONTINUE", font=get_font2(100), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("./assets/img/Quit Rect.png"), pos=(WORLD_X/2, 650), 
                            text_input="QUIT", font=get_font2(100), base_color="#d7fcd4", hovering_color="White")
        
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        for button in [PLAY_BUTTON, CONTINUE_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                    SCREEN, BG = init()
                elif CONTINUE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    f = open("./assets/data/continue.txt")
                    string = int(f.read())
                    f.close()
                    continue_(SCREEN, string)
                    SCREEN, BG = init()
                elif QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.flip()
main_menu()