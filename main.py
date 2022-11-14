#main

#todolist
#rolling
#Make missiles and guns
#stop lag
#gui and polishing such as border around screen

import sys
import time
import pygame

pygame.init()
from pygame.locals import (K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, KEYDOWN,
                           QUIT, RLEACCEL)

from definecraft import *
from extra_libraries import *

pygame.mixer.init()
pygame.init()
clock = pygame.time.Clock()
screen_w = 1900
screen_h = 1000
global selectedobjects
lc = 0
rc = 0
rightclick = False
leftclick = False
# Set up the drawing window
screen = pygame.display.set_mode([screen_w, screen_h])
allcraftsprite = []
bg = pygame.image.load("background.png")
bgmusic1 = pygame.mixer.Sound("aircombattheme1.mp3")
bgmusic2 = pygame.mixer.Sound("aircombattheme2.mp3")
global ticktime
#init craft
global timeish
timeish = 0
foxtrot0 = Craft(Foxtrot, 0, "foxtrot1", 200, 800)
foxtrot1 = Craft(Foxtrot, 1, "foxtrot1", 400, 800)
foxtrot2 = Craft(Foxtrot, 2, "foxtrot1", 600, 800)


allcraft = [foxtrot1, foxtrot2, foxtrot0]
selectedobjects = []
for i in allcraft:
      allcraftsprite.append(i.sprite)
global team1
global team2
global team0
global allteams

team0 = [foxtrot0]
team1 = [foxtrot1]
team2 = [foxtrot2]

allteams = [team0, team1, team2]

for plane in allcraft:
      plane.get_relations(allteams)


def rot_center(image, angle):
    """rotate a Surface, maintaining position."""
    
    loc = image.get_rect().center  #rot_image is not defined 
    rot_sprite = pygame.transform.rotate(image, angle)
    rot_sprite.get_rect().center = loc
    return rot_sprite

# Run until the user asks to quit
chan1 = pygame.mixer.find_channel()
chan1.queue(bgmusic1)
for i in range(3):
      chan1.queue(bgmusic2)


while True:

      # Did the user click the window close button?
      for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                  pygame.quit()
                  sys.exit

      #determine if leftclicking or rightclicking
      mouse_pressed = pygame.mouse.get_pressed()
      if mouse_pressed[0] == True and mouse_pressed[2] == False:
            if lc == 1:
                  lc = 2
                  leftclick = False
            if lc == 2:
                  lc = 2
                  leftclick = False
            if lc == 0:
                  lc = 1
                  leftclick = True

      else:
            lc = 0
            leftclick = False

      if mouse_pressed[2] == True and mouse_pressed[0] == False:  
            if rc == 1:
                  rc = 2
                  rightclick = False
            if rc == 2:
                  lc = 2
                  rightclick = False
            if rc == 0:
                  rc = 1
                  rightclick = True

      else:
            rc = 0 
            rightclick = False   



      if leftclick == True:
            mods = pygame.key.get_mods()
            if selectedobjects == [] or mods & pygame.KMOD_SHIFT:

                  for plane in allcraft:
                        if (sqrt(square(plane.xpos - (pygame.mouse.get_pos()[0])) + square(plane.ypos - (pygame.mouse.get_pos()[1]))) < 35) and selectedobjects.count(plane) == 0:

                              selectedobjects.append(plane)
            else:
                  for plane in selectedobjects:
                        plane.target = pygame.mouse.get_pos()
      if rightclick == True:
            selectedobjects = []

      # clear screen
      screen.fill((0, 0, 0))
      


      screen.blit(bg, (0, 0))  
      #you can edit the screen from here on out
      
      for plane in allcraft:
            plane.sprite.surf = plane.plain.copy()
            plane.sprite.surf = pygame.transform.smoothscale(plane.sprite.surf, (30, 30))
      

      for plane in selectedobjects:
            plane.sprite.surf = plane.highlighted.copy()
            plane.sprite.surf = pygame.transform.smoothscale(plane.sprite.surf, (30, 30))



      for plane in allcraft:
            plane.draw_radcone(screen)
            plane.draw_highlights(selectedobjects, screen, timeish)
            plane.time_turn()

      for plane in allcraft:
            draw_dashed_line(screen, (42, 163, 2), plane.target, (plane.xpos, plane.ypos), 2)



      for plane in allcraft:
            screen.blit(plane.sprite.surf, (plane.xpos - getcenter(plane.sprite.surf)[0], plane.ypos - getcenter(plane.sprite.surf)[1]))

            
            
            #YES I do have a reason for spliting these into two sepperate opperations. It is to control the priority that items are created in to contol what layers they are on
            #The priority of these items is as folows >plane >dashed line >radar thing that goes around and highlits stuff




      pygame.display.flip()
      timeish += 1
      (clock.tick(60))
