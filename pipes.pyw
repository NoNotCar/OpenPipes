import pygame
import sys
pygame.init()
ssize=(480,512)
screen=pygame.display.set_mode(ssize)
import World, Img
clock=pygame.time.Clock()
world=World.World("1-1.sav")
Img.musplay("World1")
while True:
    world.render_update(screen,pygame.event.get())
    pygame.display.flip()
    clock.tick(60)