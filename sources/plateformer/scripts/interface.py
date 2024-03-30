import pygame, sys

class Transition1:

    def __init__(self, master):

        self.master = master
        self.time = 1
        self.alpha = 1
        self.opacity = 0
        self.transition2 = Transition2(self.master)

        self.surface = pygame.Surface((self.master.screen_size_x, self.master.screen_size_y))
    
    def update_part1(self, surface):
        self.opacity = 0
        for i in range(0,60) :
            self.opacity += 2
            self.surface.set_alpha(self.opacity)
            self.master.screen.blit(self.surface, (0,0))
            self.master.display.blit(pygame.transform.scale(self.master.screen, (self.master.screen_size_x, self.master.screen_size_y)), (0,0))
            pygame.display.update()
            pygame.time.delay(15)

        for i in range(0,1500) :
            if self.opacity < -1400 :
                break
            self.opacity -= 5
            self.surface.set_alpha(self.opacity)
            self.master.screen.blit(pygame.transform.scale(self.master.game.assets["contexte"], (self.master.screen.get_width(),self.master.screen.get_height())),(0,0))
            self.master.screen.blit(self.surface, (0,0))
            self.master.display.blit(pygame.transform.scale(self.master.screen, (self.master.screen_size_x, self.master.screen_size_y)), (0,0))
            pygame.display.update()
            pygame.time.delay(15)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE :
                            self.transition2.update_part2(self.master.screen)
                            return
        
        self.opacity = 0

        for i in range(0,100) :
        
            self.opacity += 0.5
            self.surface.set_alpha(self.opacity)
            self.master.screen.blit(self.surface, (0,0))
            self.master.display.blit(pygame.transform.scale(self.master.screen, (self.master.screen_size_x, self.master.screen_size_y)), (0,0))
            pygame.display.update()
    
        self.transition2.update_part2(self.master.screen)

class Transition2:

    def __init__(self, master):

        self.master = master
        self.alpha = 1
        self.opacity = 0
        self.run = True

        self.surface = pygame.Surface((self.master.screen_size_x, self.master.screen_size_y))
    
    def update_part2(self, surface) :
        
            for i in range(0,75) :
                self.opacity += 1.5
                self.surface.set_alpha(self.opacity)
                self.master.screen.blit(self.surface, (0,0))
                self.master.display.blit(pygame.transform.scale(self.master.screen, (self.master.screen_size_x, self.master.screen_size_y)), (0,0))
                pygame.display.update()
                pygame.time.delay(15)
                
            for i in range(0,100) :
                if self.opacity <= 0:
                    return
                self.opacity -= 6
                self.surface.set_alpha(self.opacity)
                self.master.screen.blit(self.surface, (0,0))
                self.master.display.blit(pygame.transform.scale(self.master.screen, (self.master.screen_size_x, self.master.screen_size_y)), (0,0))
                pygame.display.update()

class Button:

    def __init__(self, master, button, position, scale, command=None, sound=None):
        #variables initialisation
        self.master = master
        self.button = button
        self.scale = scale
        self.image = self.master.menu_assets["button/"+str(self.button)][0]
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*self.scale, self.image.get_height()*self.scale))
        #dictionnary with two special positins, the center a of the screen in x and y
        self.positions = {
            "centerx": (self.master.screen.get_width()//2)-(self.image.get_width()//2),
            "centery": (self.master.screen.get_height()//2)-(self.image.get_height()//2)
        }

        self.command = command
        self.sound = sound
        
        #Calcul de la position ------------------------------------------------------------------------------------
        self.position = position
        #position in x
        if self.position[0] in self.positions:
            self.position = (self.positions[self.position[0]], self.position[1])
        elif type(self.position[0]) != int: #check if the position is special
            if self.position[0][0] in self.positions:
                if self.position[0][1] == "+":
                    self.position = (self.positions[self.position[0][0]]+int(self.position[0][2]), self.position[1])
                elif self.position[0][1] == "-":
                    self.position = (self.positions[self.position[0][0]]-int(self.position[0][2]), self.position[1])
        #position in y
        if self.position[1] in self.positions:
            self.position = ( self.position[0], self.positions[self.position[1]])
        elif type(self.position[1]) != int: #check if the position is special
            if self.position[1][0] in self.positions:
                if self.position[1][1] == "+":
                    self.position = (self.position[0], self.positions[self.position[1][0]]+int(self.position[1][2]))
                elif self.position[1][1] == "-":
                    self.position = (self.position[0], self.positions[self.position[1][0]]-int(self.position[1][2]))
        #Calcul de la position --------------------------------------------------------------------------------------
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.position[0], self.position[1])

        self.pressed = False
        self.trigger = False
    
    def update(self):
            #get the mouse position, we divide it by two because of the 2x effect zoom
            mouse_position = (pygame.mouse.get_pos()[0]//2, pygame.mouse.get_pos()[1]//2)
            #if the is collision between the button and the mouse
            if self.rect.collidepoint(mouse_position):
                if pygame.mouse.get_pressed()[0] == True and not self.pressed:
                    self.pressed = True #the button is pressed
                    if self.sound != None:
                        self.sound.play()
                if pygame.mouse.get_pressed()[0] == False and self.pressed:
                    self.pressed = False #the button is no longer pressed
                    self.trigger = not self.trigger
            
            if not self.pressed: #change the button image in fonction of the pressed variable
                self.image = pygame.transform.scale(self.master.menu_assets["button/"+str(self.button)][1], (self.image.get_width(), self.image.get_height()))
            else:
                self.image = pygame.transform.scale(self.master.menu_assets["button/"+str(self.button)][0], (self.image.get_width(), self.image.get_height()))
    
    def call_command(self):
        #if the button is pressed, then we call his command
        if self.command != None:
            self.trigger = False
            self.command()
            return True
        else:
            return False

    def render(self, surface):
        #blit the button on the screen
        surface.blit(self.image, self.position)

class Menu(Button, Transition1):

    def __init__(self, master, title, position, scale, buttons=None):
        pygame.mouse.set_visible(True)
        #variable initialisation
        self.master = master
        self.title = title
        self.scale = scale
        self.image = self.master.menu_assets["menu/"+str(self.title)]
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*self.scale, self.image.get_height()*self.scale))

        self.positions = {
            "centerx": (self.master.screen.get_width()//2)-(self.image.get_width()//2),
            "centery": (self.master.screen.get_height()//2)-(self.image.get_height()//2)
        }
        
        #Calcul de la position ------------------------------------------------------------------------------------
        self.position = position
        if self.position[0] in self.positions:
            self.position = (self.positions[self.position[0]], self.position[1])
        elif type(self.position[0]) != int:
            if self.position[0][0] in self.positions:
                if self.position[0][1] == "+":
                    self.position = (self.positions[self.position[0][0]]+int(self.position[0][2]), self.position[1])
                elif self.position[0][1] == "-":
                    self.position = (self.positions[self.position[0][0]]-int(self.position[0][2]), self.position[1])

        if self.position[1] in self.positions:
            self.position = ( self.position[0], self.positions[self.position[1]])
        elif type(self.position[1]) != int:
            if self.position[1][0] in self.positions:
                if self.position[1][1] == "+":
                    self.position = (self.position[0], self.positions[self.position[1][0]]+int(self.position[1][2]))
                elif self.position[1][1] == "-":
                    self.position = (self.position[0], self.positions[self.position[1][0]]-int(self.position[1][2]))
        #Calcul de la position --------------------------------------------------------------------------------------

        #button adding if there're some
        if buttons != None:    
            self.buttons = list(buttons)
            for button in range(len(self.buttons)): #creat a button class for each in the button list
                self.buttons[button] = Button(self.master, self.buttons[button][0], 
                                            (self.position[0] + self.image.get_width()//2 - self.master.menu_assets["button/"+self.buttons[button][0]][0].get_width()//2*self.scale, 
                                            self.position[1] + self.master.menu_assets["button/"+self.buttons[button][0]][0].get_height()*button*scale + (button*15) + self.image.get_height()//(len(self.buttons)*2)),
                                            self.scale, command=self.buttons[button][1], sound=self.master.menu_assets["Default_button_sound"])

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.position[0], self.position[1])

        self.transition2 = Transition2(self.master)
        self.active = True

    def update(self):
        while self.active:
            #render the menu
            self.render(self.master.screen)
            #render each button in the list
            for button in self.buttons:
                button.update()
                button.render(self.master.screen)
                if button.trigger:
                    button.call_command()
            #check if we want to quit the menu or the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                #the menu is no longer active if we press escape
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.active = False
            #render the menu on the screen
            self.master.display.blit(pygame.transform.scale(self.master.screen, (self.master.screen_size_x, self.master.screen_size_y)), (0,0))
            pygame.display.update()
            self.master.clock.tick(60)

    def render(self, surface):
        surface.blit(self.image, self.position)
    
    def back(self):
        #back fonction for the back button
        pygame.mouse.set_visible(False)
        self.active = False
    
    def restart(self):
        #restart fonction for the restart button
        self.active = False
        self.master.game.restart()
    
    def main_menu(self):
        #back to the main menu fonction for the main menu button
        self.active = False
        self.master.game.running = False
        self.transition2.update_part2(self.master.screen)
        pygame.mixer.music.unload()
        self.master.menu_assets["menu_music"] = pygame.mixer.music.load("plateformer\\ressources\\Sound\\Musics\\Menu_music.wav")
        pygame.mixer.music.play()

class End:

    def __init__(self, master):

        self.master = master

    def update(self, surface):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.master.display.blit(pygame.transform.scale(self.master.menu_assets["end_background"], (self.master.screen_size_x, self.master.screen_size_y)), (0,0))
            pygame.display.update()
            self.master.clock.tick(self.master.fps)