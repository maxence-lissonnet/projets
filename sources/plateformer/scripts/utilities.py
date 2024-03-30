import os
import pygame
#take an image to a path
def load_image(path):
    image = pygame.image.load(path).convert_alpha()
    return image
#take some images to a path
def load_images(path):
    images = []
    for name in sorted(os.listdir(path)):
        images.append(load_image(path + "\\" + name))
    return images
#get the map_index in the save file
def take_map():
    with open("plateformer\\scripts\\save\\save.txt", "r") as text:
        lines = text.readlines()
        return int(lines[1][0])
#write the map_index in the save file
def save_map(map_index):
    with open("plateformer\\scripts\\save\\save.txt", "w") as text:
        text.seek(0)
        text.write("map_index:\n"+str(map_index))
        return None

#class for player and enemis animations
class Animation:

    def __init__(self, images, image_duration=5, loop=True):

        self.images = images
        self.image_duration = image_duration
        self.loop = loop
        self.done = False
        self.frame = 0
    
    def copy(self):
        return Animation(self.images, self.image_duration, self.loop)

    def update(self):
        if self.loop: #check if the animation is finish
            self.frame = (self.frame + 1 ) % (self.image_duration * len(self.images))
        
        else: #if not, we update the frames
            self.frame = min(self.frame + 1, self.image_duration * len(self.images) -1)
            if self.frame >= self.image_duration / len(self.images) -1:
                self.done = True
    
    def image(self):
        return self.images[int(self.frame / self.image_duration)]