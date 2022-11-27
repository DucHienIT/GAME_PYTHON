import pygame, sys
import obj.define

class Sound:
    #Khởi tạo và add file âm thanh
    pygame.mixer.pre_init(frequency=44100, size= -16, channels=2, buffer=512)
    pygame.mixer.init()
    Intro_sound = pygame.mixer.Sound('./assets/sound/Sound_Intro.wav')
    Collision_sound = pygame.mixer.Sound('./assets/sound/Sound_Collision.wav')
    Battle_sound = pygame.mixer.Sound('./assets/sound/Sound_Battle.wav')
    Gameover_sound = pygame.mixer.Sound('./assets/sound/Sound_Gameover.wav')
    Attack_sound = pygame.mixer.Sound('./assets/sound/Sound_Attack_02.wav')  


    def __Play__Intro__(self, loop):
        self.Intro_sound.set_volume(0)
        self.Intro_sound.play(loops = loop)

    def __Play__Attack__(self, loop):
        
        self.Attack_sound.set_volume(0)
        self.Attack_sound.play(loops = loop)

    def __Play__Collision__(self, loop):
        self.Collision_sound.set_volume(0)
        self.Collision_sound.play(loops = loop)
        

    

