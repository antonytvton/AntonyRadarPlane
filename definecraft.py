#definecraft
import pygame
from extra_libraries import *
import math
from numpy import *
global Foxtrot
Foxtrot = {"maxspeed": 2750, "turnrate": 30, "acceleration": 600, "image": "foxtrot1.png", "missiles": [1], "smallhardpoint": 0, "gunhardpoint": 0, "highlighted_image": "foxtrothighlighted1.png", "highlightoverlay" : "outline.png", "radcone" : "transparencytest.png"}

def rot_center(image, angle, cent):
    """rotate a Surface, maintaining position."""
    
    loc = cent.get_rect().center  #rot_image is not defined 
    rot_sprite = pygame.transform.rotate(image, angle)
    rot_sprite.get_rect().center = loc
    return rot_sprite



class Plane(pygame.sprite.Sprite):
    def __init__(self, type):
        super(Plane, self).__init__()
        self.surf = pygame.image.load(type["image"]).convert_alpha()


        self.surf.set_colorkey((255, 255, 255), pygame.RLEACCEL)

        self.surf = pygame.transform.smoothscale(self.surf, (40, 40))
        

class Craft:


      def __init__(self, type, team, name, startx = 0, starty = 0):
            #defining each craft type


            #inital data about craft
            self.maxspeed = type["maxspeed"]
            self.type = type
            self.acceleration = type["acceleration"]
            self.turnrate = type["turnrate"]
            self.name = name
            self.team = team
            self.target_angle = 0
            self.target = [0, 0]

            #positional and movement data about craft
            self.xpos = startx
            self.ypos = starty
            self.curspeed = self.maxspeed
            self.angle = -130
            #init craft sprite
            self.sprite = Plane(type)


      def time_tick(self, selectedobjects, screen, timeish):
            self.ypos = (sin(deg2rad(self.angle)))*(self.curspeed/200000)*70 + self.ypos
            self.xpos = -(cos(deg2rad(self.angle)))*(self.curspeed/200000)*70 + self.xpos
            if (self.xpos - self.target[0]) > 0:
                  self.target_angle = -(rad2deg(real(math.atan((self.ypos - self.target[1])/(self.xpos - self.target[0])))))

            if (self.xpos - self.target[0]) < 0:
                  self.target_angle = -(rad2deg(real(math.atan((self.ypos - self.target[1])/(self.xpos - self.target[0])))))+180

            self.target_angle = self.target_angle % 360
            self.differential = self.target_angle - self.angle
            self.differential = self.differential % 360
            
            if abs(self.differential % 360) > self.turnrate/60:

                  if self.differential % 360 < 180:
                        self.angle += +self.turnrate/60
                  elif self.differential % 360 > 180:
                        self.angle += -self.turnrate/60

            self.sprite.surf = pygame.transform.rotate(self.sprite.surf, self.angle)

            if selectedobjects.count(self) == 1:
                  self.outline = pygame.image.load("outline.png").convert_alpha()
                  self.outline = pygame.transform.rotate(self.outline, timeish)
                  screen.blit(self.outline, (self.xpos - getcenter(self.outline)[0], self.ypos - getcenter(self.outline)[1]))

            self.radcone = pygame.image.load(self.type["radcone"]).convert_alpha()
            self.radcone = self.outline = pygame.transform.rotate(pygame.transform.smoothscale(self.radcone, (500, 150)), self.angle)
            screen.blit(self.radcone, ((self.xpos - getcenter(self.radcone)[0]), (self.ypos - getcenter(self.radcone)[1])))



            #screen.blit 
            
                  
                  

                  