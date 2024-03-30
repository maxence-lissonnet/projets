import pygame

class TileMap:
   
    def __init__(self, game, tile_size, scale = 1):
        #variable's initialisation
        self.game = game
        self.scale = scale
        self.tile_size = (tile_size[0], tile_size[1])
        self.tilemap = {}
        self.offgrid_tiles = []

        self.NEIGHBOR_OFFSETS = [(0, 0), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]
        #dictionnary who contain some type of tiles
        self.PHYSICS_TILES = {"grass","dirt","stone"}
        self.INTERACT_TRAP = {"trap"}
        self.INTERACT_PORTAL = {"portal"}
    #check if there a solide to a certain position in a type dyctionnary
    def solide_check(self, position, const):
        tile_location = str(int(position[0] // self.tile_size[0])) + ";" + str(int(position[1] // self.tile_size[1]))
        if tile_location in self.tilemap:
            if self.tilemap[tile_location]["type"] in const:
                return self.tilemap[tile_location]
    #check if there's if tile around a certain position
    def tiles_around(self, position):
        tiles = []
        tile_location = (int(position[0] // self.tile_size[0]), int(position[1] // self.tile_size[1]))
        for offset in self.NEIGHBOR_OFFSETS:
            check_loc = str(tile_location[0] + offset[0]) + ";" + str(tile_location[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    #check if there's physics rect around a certain position
    def physics_rects_around(self, position):
        rects = []
        for tile in self.tiles_around(position):
            if tile["type"] in self.PHYSICS_TILES:
                rects.append(pygame.Rect(tile["position"][0] * self.tile_size[0], tile["position"][1] * self.tile_size[1], self.tile_size[0], self.tile_size[1]))
        return rects
    
    def mapping(self):
        #Position, type, variant of the entire tiles of the map
        index = 0
        for y in range(self.game.tile_assets["maps"][self.game.map_index].get_height()):
            for x in range(self.game.tile_assets["maps"][self.game.map_index].get_width()):
                for tile in self.game.tiles_color_code:
                    
                    #Special add of the text
                    if tile == "texte" and self.game.tile_assets["maps"][self.game.map_index].get_at((x,y)) == self.game.tiles_color_code[tile]:
                        self.tilemap[str(x) + ";" + str(y)] = {"type": tile, "variant": index, "position": (x,y)}
                        index += 1
                    
                    #Special add of the portal
                    elif tile == "portal" and self.game.tile_assets["maps"][self.game.map_index].get_at((x,y)) == self.game.tiles_color_code[tile] and\
                        self.solide_check((x*32,y*32-32), const=self.INTERACT_PORTAL) == None:
                        self.tilemap[str(x) + ";" + str(y)] = {"type": tile, "variant": 0, "position": (x,y)}
                        self.tilemap[str(x) + ";" + str(y+1)] = {"type": tile, "variant": 1, "position": (x,y+1)}

                    #All others tiles
                    elif self.game.tile_assets["maps"][self.game.map_index].get_at((x,y)) == self.game.tiles_color_code[tile] and tile != "texte" and tile != "portal":
                        self.tilemap[str(x) + ";" + str(y)] = {"type": tile, "variant": 0, "position": (x,y)}

    def render(self, surface, offset=[0,0]):
        #render all the tiles
        for location in self.tilemap:
            tile = self.tilemap[location]
            surface.blit(self.game.tile_assets[tile["type"]][tile["variant"]], (tile["position"][0] * self.tile_size[0] - offset[0], tile["position"][1] * self.tile_size[1] - offset[1]))