#definecraft
import math

import pygame
from numpy import *

from extra_libraries import *

global Foxtrot

Avalanch = {"speed": 10000, "firingangle": 30, "minrange": 250, "immage": "missile.png", "turnrate": 60}
Foxtrot = {"maxspeed": 2750, "turnrate": 20, "acceleration": 600, "image": "foxtrot1.png", "missiles": [Avalanch, Avalanch], "gunhardpoint": 0, "highlighted_image": "foxtrothighlighted1.png", "highlightoverlay" : "outline.png", "radcone" : "radpic2.png", "hitpoints": 600}

class Projectile:

      def __init__(self, team, mother, type=Avalanch):
            self.type = type
            self.xpos = 0
            self.ypos = 0
            self.team = team
            self.mother = mother
            self.speed = type["speed"]
            self.firingangle = type["firingangle"]
            self.range = type["minrange"]
            self.turnrate = type["turnrate"]  #inorder to speed up code I use a diffirent turning system that multiplies the diffirence between the target by the turnrate %
            self.fireable = True
            self.fired = False
            self.angle = 0


      def fireon(self, xpos, ypos, angle, screen, target):
            self.spritesave = pygame.transform.rotate(pygame.image.load(self.type["immage"]).convert_alpha(), 90)
            self.fired = True
            print("missile fired")
            self.xpos = xpos
            self.ypos = ypos
            self.angle = angle
            self.target = target
            self.sprite = pygame.transform.rotate(self.spritesave, self.angle)
            screen.blit(self.sprite, (self.xpos, self.ypos))

      def glide(self, screen):
            radangle = (deg2rad(self.angle))
            pixlespeed = (self.speed/400000)*70

            self.ypos = (sin(radangle))* pixlespeed + self.ypos
            self.xpos = -(cos(radangle))* pixlespeed + self.xpos
            self.sprite = pygame.transform.rotate(self.spritesave, self.angle)
            screen.blit(self.sprite, (self.xpos, self.ypos))
            mda = -(rad2deg(real(math.atan((self.ypos - self.target.ypos)/(self.xpos - self.target.xpos)))))

            if (self.xpos - self.target.xpos) > 0:
                  missiledifangle = mda

            elif (self.xpos - self.target.xpos) < 0:
                  missiledifangle = mda +180
            else:
                  missiledifangle = 270

            missiledifangle = missiledifangle % 360
            self.differential = missiledifangle - self.angle
            self.differential = self.differential % 360

            if self.differential< 180:
                  self.angle += self.turnrate/60
            elif self.differential> 180:
                  self.angle += -self.turnrate/60



            if ((self.target.xpos-self.xpos)**2 + (self.target.ypos-self.ypos)**2)< 400:
                  self.explode()

      def explode(self):
            self.mother.firedmissile.remove(self)

            


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
            self.cooldown = 0

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
            self.turnpertick = self.turnrate/60
            #init craft sprite
            self.sprite = Plane(type)
            self.radconecache = pygame.image.load(self.type["radcone"]).convert_alpha()
            self.highlighted = pygame.image.load(self.type["highlighted_image"]).convert_alpha()
            self.plain = pygame.image.load(self.type["image"]).convert_alpha()
            self.radconecache = pygame.transform.rotate(self.radconecache, self.angle+220)
            self.allstoredmissiles = []
            for misstype in [self.type["missiles"]]:
                  missile = Projectile(self.team, self, misstype[0])
                  self.allstoredmissiles.append(missile)
            self.firedmissile = []


            



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
            radangle = (deg2rad(self.angle))
            pixlespeed = (self.curspeed/400000)*70

            self.ypos = (sin(radangle))* pixlespeed + self.ypos
            self.xpos = -(cos(radangle))* pixlespeed + self.xpos
            if (self.xpos - self.target[0]) > 0:
                  self.target_angle = -(rad2deg(real(math.atan((self.ypos - self.target[1])/(self.xpos - self.target[0])))))

            elif (self.xpos - self.target[0]) < 0:
                  self.target_angle = -(rad2deg(real(math.atan((self.ypos - self.target[1])/(self.xpos - self.target[0])))))+180
            else:
                  self.target_angle = 270

            self.target_angle = self.target_angle % 360
            self.differential = self.target_angle - self.angle
            self.differential = self.differential % 360
            
            if self.differential > self.turnpertick:

                  if self.differential< 180:
                        self.angle += self.turnpertick
                        self.radturn = self.turnpertick
                  elif self.differential> 180:
                        self.angle += -self.turnpertick
                        self.radturn = -self.turnpertick

            self.sprite.surf = pygame.transform.rotate(self.sprite.surf, self.angle)



      def draw_highlights(self, selectedobjects, screen, timeish):
            if selectedobjects.count(self) == 1:
                  self.outline = pygame.image.load("outline.png").convert_alpha()
                  self.outline = pygame.transform.rotate(self.outline, timeish)
                  screen.blit(self.outline, (self.xpos - getcenter(self.outline)[0], self.ypos - getcenter(self.outline)[1]))



      def draw_radcone(self, screen):
            self.radcone = pygame.transform.rotate(self.radconecache, self.angle)
            screen.blit(self.radcone, ((self.xpos - getcenter(self.radcone)[0]), (self.ypos - getcenter(self.radcone)[1])))

#THIS IS A WIP
      




      def inrange(self, screen, selectedobjects):
            missiledifangle = 0
            if self.cooldown > 0:
                  self.cooldown = self.cooldown - 1
            
            for plane in self.enemycraft:
                  entargetx = plane.xpos
                  entargety = plane.ypos
                  
                  for missile in self.allstoredmissiles:
                        if sqrt((self.xpos - entargetx)**2+(self.ypos - entargety)**2) < missile.range:

                              #replace pass with check if within firing angle

                              mda = -(rad2deg(real(math.atan((self.ypos - entargety)/(self.xpos - entargetx)))))

                              if (self.xpos - entargetx) > 0:
                                    missiledifangle = mda

                              elif (self.xpos - entargety) < 0:
                                    missiledifangle = mda +180
                              else:
                                    missiledifangle = 270

                              missiledifangle = missiledifangle % 360
                              self.differential = abs((missiledifangle - self.angle) % 360)
                              
                              if (self.differential < missile.firingangle/2 or abs(self.differential-360)< missile.firingangle/2) and self.cooldown == 0:

                                    missile.fireon(self.xpos, self.ypos, missiledifangle, screen, plane)
                                    self.firedmissile.append(missile)
                                    self.allstoredmissiles.remove(missile)
                                    self.cooldown = 30

      def missilesglide(self, screen):
            for missile in self.firedmissile:
                  missile.glide(screen)
            