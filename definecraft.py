#definecraft
import math

import pygame
from numpy import *

from extra_libraries import *

global Foxtrot
Foxtrot = {"maxspeed": 2750, "turnrate": 30, "acceleration": 600, "image": "foxtrot1.png", "missiles": [1], "smallhardpoint": 0, "gunhardpoint": 0, "highlighted_image": "foxtrothighlighted1.png", "highlightoverlay" : "outline.png", "radcone" : "radpic2.png"}

class Projectile:

      def __init__(self, type, xpos, ypos, target, team, mother):
            self.type = type
            self.xpos = xpos
            self.ypos = ypos
            self.target = target
            self.team = team
            self.mother = mother
            


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
            self.enemycraft = []
            self.friends = []
            self.enemyprojectiles = []
            self.hp = 1000
            self.radturn = 0
            #init craft sprite
            self.sprite = Plane(type)
            self.radcone = pygame.image.load(self.type["radcone"]).convert_alpha()
            self.radcone = self.outline = pygame.transform.rotate(self.radcone, self.angle+90)



      def get_relations(self, allteams):
            #looks at teams and finds friendlys and enemys
            if self.team == 0:
                  self.enemycraft = allteams[1] + allteams[2]
                  self.friends = allteams[0]
            elif self.team == 1:
                  self.enemycraft = allteams[0] + allteams[2]
                  self.friends = allteams[1]
            elif self.team == 2:
                  self.enemycraft = allteams[0] + allteams[1]
                  self.friends = allteams[2]

      def time_turn(self):
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
                        self.angle += self.turnrate/60
                        self.radturn = self.turnrate/60
                  elif self.differential % 360 > 180:
                        self.angle += -self.turnrate/60
                        self.radturn = -self.turnrate/60

            self.sprite.surf = pygame.transform.rotate(self.sprite.surf, self.angle)



      def draw_highlights(self, selectedobjects, screen, timeish):
            if selectedobjects.count(self) == 1:
                  self.outline = pygame.image.load("outline.png").convert_alpha()
                  self.outline = pygame.transform.rotate(self.outline, timeish)
                  screen.blit(self.outline, (self.xpos - getcenter(self.outline)[0], self.ypos - getcenter(self.outline)[1]))



      def draw_radcone(self, screen):
            self.radcone = self.outline = pygame.transform.rotate(self.radcone, self.radturn)
            screen.blit(self.radcone, ((self.xpos - getcenter(self.radcone)[0]), (self.ypos - getcenter(self.radcone)[1])))

            #screen.blit 
            
                  
                  

                  