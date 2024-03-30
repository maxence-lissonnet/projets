import pygame, math

class PhysicsEntity:

    def __init__(self, game, entity_type, position, size, gravity=9.81):
        self.game = game
        self.type = entity_type
        self.position = list(position)
        self.size = list(size)
        self.velocity = [0,0]
        self.gravity = gravity
        self.collisions = {"up": False, "down": False, "right": False, "left": False}

        self.action = ""
        self.anim_offset = (0, 0) #padding on the x side of the image
        self.flip = False
        self.set_action("idle")
    
    def rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + "/" + self.action].copy()

    def update(self, tilemap, mouvement=(0,0)):
        
        self.collisions = {"up": False, "down": False, "right": False, "left": False}

        frame_mouvement = (mouvement[0] + self.velocity[0], mouvement[1] + self.velocity[1]) #Player mouvements

        self.position[0] += frame_mouvement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.position):
            if entity_rect.colliderect(rect): #Check if there's a collision on the right or left
                if frame_mouvement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions["right"] = True
                if frame_mouvement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions["left"] = True
                self.position[0] = entity_rect.x
        
        self.position[1] += frame_mouvement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.position):
            if entity_rect.colliderect(rect): #Check if there's a collision on top or the bottom
                if frame_mouvement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions["down"] = True
                if frame_mouvement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions["up"] = True
                self.position[1] = entity_rect.y
        
        if mouvement[0] > 0:
            self.flip = False
        if mouvement[0] < 0:
            self.flip = True
 
        #gravity
        self.velocity[1] = round(min(self.gravity, self.velocity[1] + 0.2),1)

        #stop the jump or the fall of the player if ther's collision
        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0
        
        self.animation.update()
        
    def render(self, surface, offset=[0,0]):
        surface.blit(pygame.transform.flip(self.animation.image(), self.flip, False), (self.position[0] - offset[0] + self.anim_offset[0], self.position[1] - offset[1] + self.anim_offset[1]))

class Projectile(PhysicsEntity):

    def __init__(self, game, start_pos, end_pos, size, projectile_type, speed=5):

        self.game = game
        self.speed = speed
        self.start_position = start_pos
        self.finish_position = end_pos
        self.size = size
        self.projectile_type = projectile_type
        self.out = False

        delta_x = self.finish_position[0] - self.start_position[0]
        delta_y = self.finish_position[1] - self.start_position[1]

        self.angle = math.atan2(-delta_y, delta_x)

        super().__init__(self.game, self.projectile_type, start_pos, self.size, gravity=0)

    def update(self, tilemap, mouvement=(0, 0)):
        mouvement = (self.speed * math.cos(self.angle), -self.speed * math.sin(self.angle))

        super().update(tilemap, mouvement)

        if self.collisions["up"] or self.collisions["down"] or self.collisions["right"] or self.collisions["left"]:
            self.out = True
        
        if self.rect().x < -self.game.master.display.get_width() or self.rect().x > self.game.tile_assets["maps"][self.game.map_index].get_width()*32 + self.game.master.display.get_width() or \
            self.rect().y < -self.game.master.display.get_height() or self.rect().y > self.game.tile_assets["maps"][self.game.map_index].get_height()*32 + self.game.master.display.get_height():
            self.out = True

    def render(self, surface, offset=[0, 0]):
        super().render(surface, offset)

class Check_obstacle(Projectile):

    def __init__(self, game, start_pos, end_pos, size, projectile_type, speed, side):
        self.side = side
        super().__init__(game, start_pos, end_pos, size, projectile_type, speed)
    
    def update(self, tilemap, mouvement=(0, 0)):
        
        while (self.position[1] >= self.finish_position[1] if self.start_position[1] >= self.finish_position[1] else self.position[1] <= self.finish_position[1]):
            super().update(tilemap, mouvement)
            
            if self.collisions["up"] or self.collisions["down"] or self.collisions["right"] or self.collisions["left"]:
                return True
        
        return False

class Player_projectil(Projectile):

    def __init___(self, game, start_pos, end_pos, size, projectile_type):
        super().__init__(game, start_pos, end_pos, size, projectile_type)

    def update(self, tilemap, mouvement=(0, 0)):

        super().update(tilemap, mouvement)
    
    def render(self, surface, offset=[0, 0]):
        super().render(surface, offset)

class Enemie_projectile(Projectile):

    def __init__(self, game, start_pos, end_pos, size, projectile_type, speed=2.5):
        super().__init__(game, start_pos, end_pos, size, projectile_type, speed=speed)

    def update(self, tilemap, mouvement=(0, 0)):
        super().update(tilemap, mouvement)

    def render(self, surface, offset=[0, 0]):
        super().render(surface, offset)

class Player(PhysicsEntity):
    
    def __init__(self, game, position):

        self.game = game

        self.size = (16,32)
        self.jumps = 1
        self.air_time = 0
        self.coyote_time_value = 0.6 #0.6, no coyote time, 1.6, a little
        self.dead = False

        self.power_flag = False
        self.compte_dead = 0

        self.height_jump = 5.5
        self.super_jump = False
        self.after_jump = False
        self.super_jump_timer = 5*self.game.master.fps
        self.super_jump_timer_save = self.super_jump_timer
        self.super_jump_reset = 10*self.game.master.fps
        self.super_jump_reset_save = self.super_jump_reset

        self.line_size = (20,4)
        self.jump_line = pygame.Surface(self.line_size)

        super().__init__(self.game, "player", position, self.size)

    def jump(self): #jump function

        if self.jumps:
            if self.super_jump:
                self.velocity[1] = -self.height_jump*1.5
            else:
                self.velocity[1] = -self.height_jump
            
            self.jumps -= 1
            self.air_time = 5
    
    def update(self, tilemap, mouvement=(0,0)):

        super().update(tilemap, mouvement)

        #Check if the player touche a trap
        if tilemap.solide_check((self.position), const = tilemap.INTERACT_TRAP) or \
        tilemap.solide_check((self.position[0] + self.size[0], self.position[1]), const = tilemap.INTERACT_TRAP) or \
        tilemap.solide_check((self.position[0], self.position[1] + self.size[1]), const = tilemap.INTERACT_TRAP) or \
        tilemap.solide_check((self.position[0] + self.size[0], self.position[1] + self.size[1]), const = tilemap.INTERACT_TRAP) :
            self.dead = True
        
        #check if the player is entering the portal
        if tilemap.solide_check(self.rect().center, const = tilemap.INTERACT_PORTAL) :
            self.game.new_world() 
        
        #timer for the super jump delay
        if self.super_jump:
            self.super_jump_timer -=1
            if self.super_jump_timer <= 0:
                self.super_jump = False
                self.after_jump = True
                self.super_jump_timer = 5*self.game.master.fps
        #timer for the super jump reset
        if self.after_jump:
            self.super_jump_reset -=1
            if self.super_jump_reset <= 0:
                self.after_jump = False
                self.super_jump_reset = 10*self.game.master.fps
        #drax the timer of the dely and the reset
        self.draw_timer(self.game.master.screen)

        #set the player action in order to his mouvement
        self.air_time += 1
        if self.collisions["down"]:
            self.air_time = 0
        if self.air_time > 4:
            self.set_action("jump")
        elif mouvement[0] != 0:
            self.set_action("run")
        else:
            self.set_action("idle")

        #check if the player is touching the ground, if it's true, then he can jump
        if self.collisions["down"]:
            self.jumps = 1
        
        #check if the fall speed player is superior to 0.6, it means that he's falling
        if self.velocity[1] > self.coyote_time_value:
            self.jumps = 0
        
        #check if the player is falling, but out the screen
        if self.position[1] > (self.game.tile_assets["maps"][self.game.map_index].get_height())*32:
            self.game.player.dead = True

    def draw_timer(self, surface):
        
        #timer for the super jump delay
        if self.super_jump and self.power_flag:
            self.jump_line.fill((0,0,0))
            pygame.draw.rect(self.jump_line, (255,180,0), (1, 1, self.super_jump_timer/(self.super_jump_timer_save/self.line_size[0])-2, self.line_size[1]-2))
            surface.blit(self.jump_line, (self.position[0]+self.size[0]//2-self.line_size[0]//2-self.game.render_scroll[0], self.position[1]-self.game.render_scroll[1]-self.line_size[1]*2))
        
        #Timer for the reset of the super jump
        elif not self.super_jump and self.power_flag and self.after_jump:
            self.jump_line.fill((0,0,0))
            pygame.draw.rect(self.jump_line, (255,0,0), (1, 1, self.super_jump_reset/(self.super_jump_reset_save/self.line_size[0])-2, self.line_size[1]-2))
            surface.blit(self.jump_line, (self.position[0]+self.size[0]//2-self.line_size[0]//2-self.game.render_scroll[0], self.position[1]-self.game.render_scroll[1]-self.line_size[1]*2))
        
        #else, nothing
        else:
            pass

    def render(self, surface, offset=[0,0]):
        super().render(surface, offset)

class Enemi(PhysicsEntity):

    def __init__(self, game, position, detection_radius, speed):

        self.size = (16,32)
        self.walking = 1
        self.dead = False
        self.speed = speed
        self.detection_radius = detection_radius
        self.look_at = False

        super().__init__(game, "enemi", position, self.size)
    
    def update(self, tilemap, mouvement=(0,0)):

        if self.walking:
            #check if the tile in front of and below the ennemi is physic or not
            if tilemap.solide_check((self.rect().centerx + (-self.size[0]//2 if self.flip else self.size[0]//2), self.position[1] + self.size[1]), const = tilemap.PHYSICS_TILES):
                if self.flip:
                    mouvement = (mouvement[0] -self.speed, mouvement[1])
                else:
                    mouvement = (mouvement[0] +self.speed, mouvement[1])
            else:
                self.flip = not self.flip
            #Check if the enemie tcouhe a wall, if true, he go back
            if tilemap.solide_check((self.rect().x + (-1 if self.flip else self.size[0]), self.rect().centery), const = tilemap.PHYSICS_TILES):
                self.flip = not self.flip
                if self.flip:
                    mouvement = (mouvement[0] -self.speed, mouvement[1])
                else:
                    mouvement = (mouvement[0] +self.speed, mouvement[1])

        if self.game.player.position[1] >= self.position[1]-self.detection_radius*self.game.map2D.tile_size[1] and self.game.player.position[1] <= self.position[1]+self.detection_radius*self.game.map2D.tile_size[1] \
            and self.game.player.position[0] < self.position[0] and self.flip and self.position[0]-self.game.player.position[0] <= self.detection_radius*self.game.map2D.tile_size[0] \
            or self.game.player.position[0]> self.position[0] and not self.flip and self.game.player.position[0]-self.position[0] <= self.detection_radius*self.game.map2D.tile_size[0]:
                self.look_at = True
        else :
            self.look_at = False

        super().update(tilemap, mouvement)

        if mouvement[0] != 0:
            self.set_action("run")
        else:
            self.set_action("idle")
    
    def render(self, surface, offset=[0,0]):
        super().render(surface, offset)

class Soldat(Enemi):

    def __init__(self, game, position):
        self.game = game
        self.position = position
        self.detection_radius = 4

        super().__init__(self.game, self.position, self.detection_radius, speed=0.75)

    def update(self, tilemap, mouvement=(0, 0)):

        if self.look_at:
            self.speed = 1.5
        else:
            self.speed = 0.75

        super().update(tilemap, mouvement)
    
    def render(self, surface, offset=[0, 0]):
        super().render(surface, offset)

class Archer(Enemi):

    def __init__(self, game, position):
        
        self.game = game
        self.position = position
        self.detection_radius = 12

        self.can_shoot = False
        self.timer = False
        self.shoot_delay = 60

        super().__init__(self.game, self.position, self.detection_radius, speed=0.5)

    def update(self, tilemap, mouvement=(0, 0)):
        
        #If the enemie can shoot, then he's not moving
        if self.can_shoot:
            self.speed = 0
        else:
            self.speed = 0.5

        #Delay for the projectile
        if self.timer:
            self.shoot_delay -=1
            if self.shoot_delay <= 0:
                self.timer = False
                self.shoot_delay = 60
        
        super().update(tilemap, mouvement)
    
    def render(self, surface, offset=[0, 0]):
        super().render(surface, offset)