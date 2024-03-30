import pygame, sys
from scripts.utilities import load_image, load_images, save_map, Animation
from scripts.entities import Player, Soldat, Archer, Player_projectil, Enemie_projectile, Check_obstacle
from scripts.tilemap import TileMap
from scripts.interface import Menu, Transition1, Transition2, End

class Game:

    def __init__(self, master, map_index):
        
        self.master = master
        self.map_index = map_index

        #The assets dictionnary
        self.tile_assets = {
            "background": load_image("plateformer\\ressources\\background\\background.png"),

            "grass" : load_images("plateformer\\ressources\\tiles\\grass"),
            "dirt" : load_images("plateformer\\ressources\\tiles\\dirt"),
            "stone" : load_images("plateformer\\ressources\\tiles\\stone"),

            "trap" : load_images("plateformer\\ressources\\tiles\\traps"),
            "portal" : load_images("plateformer\\ressources\\tiles\\portal"),

            "maps": load_images("plateformer\\ressources\\maps"),
            "texte": load_images("plateformer\\ressources\\Interface\\Texte\\Textes\\tutorial"),
        }
        self.tiles_color_code = {
            "grass": (0,255,0),
            "dirt": (180,90,0),
            "stone": (100,100,100),

            "trap": (50,50,50),
            "portal" : (0,255,255),

            "texte": (255,255,255)
        }
        self.assets = {
            "player": load_image("plateformer\\ressources\\entities\\player\\player_idle.png"),
            "soldat": load_image("plateformer\\ressources\\entities\\enemi\\idle\\enemi_idle.png"),
            "archer": load_image("plateformer\\ressources\\entities\\enemi\\idle\\enemi_idle.png"),

            "player/idle": Animation(load_images("plateformer\\ressources\\entities\\player\\idle"), image_duration=60),
            "player/run": Animation(load_images("plateformer\\ressources\\entities\\player\\run"), image_duration=13),
            "player/jump": Animation(load_images("plateformer\\ressources\\entities\\player\\jump")),
            "enemi/idle": Animation(load_images("plateformer\\ressources\\entities\\enemi\\idle"), image_duration=30),
            "enemi/run": Animation(load_images("plateformer\\ressources\\entities\\enemi\\run"), image_duration=20),
            "player_projectile/idle": Animation(load_images("plateformer\\ressources\\entities\\Projectile\\player"), image_duration=60),
            "enemie_projectile/idle": Animation(load_images("plateformer\\ressources\\entities\\Projectile\\enemie"), image_duration=60),

            "contexte": load_image("plateformer\\ressources\\contexte\\contexte.png")
        }
        self.color_code = {

            "player": (0,0,255),
            "soldat": (255,0,0),
            "archer": (200,0,0)
        }

        #check if there's no next map, then it's the end
        if self.map_index > len(self.tile_assets["maps"])-1:
            self.end = End(self.master)
            self.end.update(surface=self.master.screen)
        
        #make the player spawn where we put the blue square on the map
        for y in range(self.tile_assets["maps"][self.map_index].get_height()):
            for x in range(self.tile_assets["maps"][self.map_index].get_width()):
                if self.tile_assets["maps"][self.map_index].get_at((x,y)) == self.color_code["player"]:
                    self.player = Player(self, (x*32,y*32-32)) #Player creation
                    if self.map_index == 0:
                        self.player.power_flag = False
                    else:
                        self.player.power_flag = True

        self.mouvement = [0,0] #Player mouvement for the right and left
        
        self.soldats = []
        self.archers = []
        self.player_projectiles = []
        self.enemies_projectiles = []

        #check if there is enemi on the map
        for y in range(self.tile_assets["maps"][self.map_index].get_height()):
            for x in range(self.tile_assets["maps"][self.map_index].get_width()):
                if self.tile_assets["maps"][self.map_index].get_at((x,y)) == self.color_code["soldat"]:
                    self.soldats.append(Soldat(self, (x*32, y*32)))
                elif self.tile_assets["maps"][self.map_index].get_at((x,y)) == self.color_code["archer"]:
                    self.archers.append(Archer(self, (x*32, y*32)))
        
        self.map2D = TileMap(self, (32,32)) #Map creation
        self.map2D.mapping() #Call the mapping function

        self.obstacle = False

        self.scroll = [(self.player.rect().centerx - self.master.screen.get_width() / 2), (self.player.rect().centery - self.master.screen.get_height() / 2)] #Make the camera mouving
        self.render_scroll = (self.scroll)

        self.buttons = []
        self.menu = Menu(self.master, "Escape Menu", ("centerx", "centery"), scale=0.5)

        self.transition1 = Transition1(self.master)
        self.transition2 = Transition2(self.master)

        self.running = True

    def run(self):
        pygame.mouse.set_visible(False)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)
        while self.running:
            
            #background
            self.master.screen.blit(pygame.transform.scale(self.tile_assets["background"], (self.master.screen.get_width(),self.master.screen.get_height())), (0,0))
            
            #variables for the mouving camera
            self.scroll[0] += (self.player.rect().centerx - self.master.screen.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.master.screen.get_height() / 2 - self.scroll[1]) / 30

            self.render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            #Tiles
            self.map2D.render(self.master.screen, offset=self.render_scroll)

            #Render the enemis
            for enemi in self.soldats.copy():
                #if the enemi touche the player, we restart the level
                if enemi.rect().colliderect(self.player.rect()):
                    self.player.dead = True
                enemi.update(self.map2D)
                enemi.render(self.master.screen, offset=self.render_scroll)
                
            #Render the enemis
            for enemi in self.archers.copy():
                #if the enemi touche the player, we restart the level
                if enemi.rect().colliderect(self.player.rect()):
                    self.player.dead = True
                if enemi.look_at and not enemi.timer:
                    self.obstacle = Check_obstacle(self, (enemi.position[0], enemi.position[1]), self.player.position, (5,5), "enemie_projectile", 1, enemi.flip)
                    if not self.obstacle.update(self.map2D):
                        self.enemies_projectiles.append(Enemie_projectile(self, ((enemi.position[0]-5, enemi.position[1]) if enemi.flip else (enemi.position[0]+enemi.size[0], enemi.position[1])), (self.player.rect().centerx, self.player.rect().centery-self.player.size[1]//4), (5,5), "enemie_projectile", speed=2.5))
                        enemi.timer = True
                        enemi.can_shoot = True
                    else:
                        enemi.can_shoot = False

                enemi.update(self.map2D)
                enemi.render(self.master.screen, offset=self.render_scroll)

            if not self.player.dead: #render the player if he's not dead
                #Check if the player is mouving, falling, or if there's a collision
                self.player.update(self.map2D, (self.mouvement[1] - self.mouvement[0], 0))
                self.player.render(self.master.screen, offset=self.render_scroll) #Render the player
            else: #else, we restart the level
                self.player.compte_dead += 1
                self.restart()
            
            for projectile in self.player_projectiles.copy():
                #if the enemi touche the player, we restart the level
                projectile.update(self.map2D)
                projectile.render(self.master.screen, offset=self.render_scroll)

                #si il y a une collision avec l'enemi soldat alors supression de l'enemi et du projectile
                for enemi in self.soldats.copy() :
                    if projectile.rect().colliderect(enemi.rect()):
                        projectile.out = True
                        enemi.dead = True
                        self.soldats.remove(enemi)
                #si il y a une collision avec l'enemi archer alors supression de l'enemi et du projectile
                for enemi in self.archers.copy() :
                    if projectile.rect().colliderect(enemi.rect()):
                        projectile.out = True
                        enemi.dead = True
                        self.archers.remove(enemi)

                if projectile.out :
                    self.player_projectiles.remove(projectile)
            
            for projectile in self.enemies_projectiles.copy():
                #if the enemi touche the player, we restart the level
                projectile.update(self.map2D)
                projectile.render(self.master.screen, offset=self.render_scroll)

                if projectile.rect().colliderect(self.player.rect()):
                    self.player.dead = True
                
                if projectile.out :
                    self.enemies_projectiles.remove(projectile)

            #Draw the site
            mouse_pos = (pygame.mouse.get_pos()[0]//2, pygame.mouse.get_pos()[1]//2)
            self.draw_site(mouse_pos)

            #Activation of the player's power
            if self.map_index == 0 and self.player.position[0] <= 256:
                self.player.power_flag = True

            #Events loop
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.quit()
                
                if event.type == pygame.KEYDOWN:
                        
                    if event.key == pygame.K_RIGHT:
                        self.mouvement[1] = 2.1
                    if event.key == pygame.K_LEFT:
                        self.mouvement[0] = 2.1
                    
                    if event.key == pygame.K_ESCAPE:
                        self.escape_menu()
                        
                if event.type == pygame. KEYUP:
                        
                    if event.key == pygame.K_RIGHT:
                        self.mouvement[1] = 0
                    if event.key == pygame.K_LEFT:
                        self.mouvement[0] = 0
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.player.power_flag: 
                        # Lorsqu'on clique avec la souris, crée un projectile
                        self.player_projectiles.append(Player_projectil(self, (self.player.position[0], self.player.position[1]-10), (mouse_pos[0] + self.render_scroll[0], mouse_pos[1] + self.render_scroll[1]), (8,8), "player_projectile"))
                    
                    if event.button == 3 and not self.player.super_jump and not self.player.after_jump and self.player.power_flag:
                        self.player.super_jump = True

            #Keep the jump acive while the Key UP is pressed
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.player.jump()
            
            #Render
            self.master.display.blit(pygame.transform.scale(self.master.screen, ((self.master.screen_size_x, self.master.screen_size_y))), (0,0))
            pygame.display.update()
            self.master.clock.tick(self.master.fps)

    def draw_site(self, mouse_pos):
        pygame.draw.rect(self.master.screen, (0,0,0), (mouse_pos[0]-1, mouse_pos[1]+1, 1, 8))
        pygame.draw.rect(self.master.screen, (0,0,0), (mouse_pos[0]+1, mouse_pos[1]-1, 8, 1))
        pygame.draw.rect(self.master.screen, (0,0,0), (mouse_pos[0]+10, mouse_pos[1]+1, 1, 8))
        pygame.draw.rect(self.master.screen, (0,0,0), (mouse_pos[0]+1, mouse_pos[1]+10, 8, 1))
        pygame.draw.rect(self.master.screen, (0,0,0), (mouse_pos[0]+4, mouse_pos[1]+4, 2, 2))

    def escape_menu(self):
        self.buttons = [("back",self.menu.back),("restart",self.menu.restart),("main_menu", self.menu.main_menu)]
        self.menu.__init__(self.master, "Escape Menu", ("centerx", "centery"), scale=1, buttons=self.buttons)
        self.menu.update()

    def quit(self):
        save_map(self.map_index)
        pygame.quit()
        sys.exit()
    
    def restart(self):
        self.transition2.update_part2(self.master.screen)
        Game.__init__(self, self.master, self.map_index)
        pygame.mouse.set_visible(False)
    
    def new_world(self):
        self.transition2.update_part2(self.master.screen)
        self.map_index += 1
        save_map(map_index=self.map_index)
        Game.__init__(self, self.master, self.map_index)
        pygame.mouse.set_visible(False)