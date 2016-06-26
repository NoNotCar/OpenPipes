import pygame
import sys
pygame.init()
ssize=(480,512)
screen=pygame.display.set_mode(ssize)
import World
clock=pygame.time.Clock()
world=World.World()
while True:
    world.render_update(screen,pygame.event.get())
    pygame.display.flip()
    clock.tick(60)