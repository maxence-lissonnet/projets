#Module's importation
import pygame, sys
from screeninfo import get_monitors
from scripts.Game import Game
from scripts.interface import Button, Transition1, Transition2
from scripts.utilities import load_image, load_images, take_map, save_map
#Main menu classe
class Menu:

    def __init__(self):
        #initialisation of all variables
        pygame.mixer.init()

        # Get all monitors
        monitors = get_monitors()
        
        # Get the primary monitor
        self.primary_monitor = next(iter(monitors), None)

        self.screen_size_x, self.screen_size_y = self.primary_monitor.width, self.primary_monitor.height

        pygame.display.set_caption("Plateformer") #Name of the window
        self.display = pygame.display.set_mode((self.screen_size_x, self.screen_size_y)) #Create the main window
        self.screen = pygame.Surface(((self.screen_size_x//2, self.screen_size_y//2)))#create a sub window for a zomm effect

        self.clock = pygame.time.Clock() #Call the clock function
        self.fps = 60


        #Assets for the main menu
        self.menu_assets = {
            "background": load_image("plateformer\\ressources\\background\\menu_background.jpg"),
            "end_background": load_image("plateformer\\ressources\\background\\end_background.png"),
            "button/play": load_images("plateformer\\ressources\\Interface\\Buttons\\play"),
            "button/quit": load_images("plateformer\\ressources\\Interface\\Buttons\\quit"),
            "button/back": load_images("plateformer\\ressources\\Interface\\Buttons\\Back"),
            "button/restart": load_images("plateformer\\ressources\\Interface\\Buttons\\Restart"),
            "button/main_menu" : load_images("plateformer\\ressources\\Interface\\Buttons\\Main menu"),
            "menu/Escape Menu" : load_image("plateformer\\ressources\\Interface\\Menus\\EscapeMenu\\Menu.Escape.png"),

            "play_button_sound": pygame.mixer.Sound("plateformer\\ressources\\Sound\\Sounds\\buttons\\Play_button_sound.wav"),
            "Default_button_sound": pygame.mixer.Sound("plateformer\\ressources\\Sound\\Sounds\\buttons\\Default.wav"),

            "menu_music": pygame.mixer.music.load("plateformer\\ressources\\Sound\\Musics\\Menu_music.wav")
        }

        #The two buttons for the menu
        self.play_button = Button(self, "play", ("centerx",("centery")), 1, command=self.play_game, sound=self.menu_assets["play_button_sound"])
        self.quit_button = Button(self, "quit",("centerx",("centery","+","50")), 1, command=self.quit, sound=self.menu_assets["Default_button_sound"])
        self.menu_buttons = [self.play_button, self.quit_button] #list of the button

        self.game = Game(self, map_index=0)
        self.transition1 = Transition1(self)
        self.transition2 = Transition2(self)

        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)

    def run(self):

        while True:
            #blit the background on the screen
            self.screen.blit(pygame.transform.scale(self.menu_assets["background"], (self.screen.get_width(),self.screen.get_height())), (0,0))
            #For each button, we apply the update and render fonction
            for button in self.menu_buttons.copy():
                button.update()
                button.render(self.screen)
                if button.trigger:
                    button.call_command()

            #Events loop
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    self.quit()

            #blit the sub window on the main one
            self.display.blit(pygame.transform.scale(self.screen, ((self.screen_size_x, self.screen_size_y))), (0,0))
            pygame.display.update()
            self.clock.tick(self.fps)

    def play_game(self):
        pygame.mixer.music.stop()
        #fonction of the play button
        if take_map() == 0 : #check if the transition have to be with the introduction text
            self.transition1.update_part1(self.screen)
        else: #else we put a simple transition
            self.transition2.update_part2(self.screen)
        #run the game
        self.game.__init__(self, map_index = take_map())
        pygame.mixer.music.unload()
        self.game.assets["game_music"] = pygame.mixer.music.load("plateformer\\ressources\\Sound\\Musics\\Game_music.wav")
        self.game.run()
    
    def quit(self):
        #fonction if the quit button
        save_map(self.game.map_index)
        pygame.quit()
        sys.exit()
        
#call the menu classe
if __name__ == "__main__":
    Menu().run()