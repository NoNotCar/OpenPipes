import pygame
import sys
pygame.init()
ssize=(480,512)
screen=pygame.display.set_mode(ssize)
import World, Img
clock=pygame.time.Clock()
pdf=pygame.font.get_default_font()
tfont=pygame.font.Font(pdf,32)
bfont=pygame.font.Font(pdf,64)
pygame.display.set_caption("OpenPipes")
pygame.display.set_icon(Img.img32("PipeX"))
lsel=None
try:
    hsfile=open("HS.sav")
    hss=hsfile.readlines()
    hsfile.close()
    maxlevel=len(hss)+1
    hss=[int(h) for h in hss]
except IOError:
    maxlevel=1
    hss=[]
x=1
while True:
    level=(1,x)
    try:
        testlevel=open(Img.np("levels//%s-%s.sav" % tuple(level)))
        testlevel.close()
        x+=1
    except IOError:
        umax=x-1
        break
while True:
    breaking=False
    lset=range(1,(maxlevel if maxlevel<umax else umax)+1)
    while not breaking:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                my=pygame.mouse.get_pos()[1]
                sel=(my-70)//64
                if 0<=sel<len(lset):
                    lsel=lset[sel]
                    breaking=True
        screen.fill((0, 0, 0))
        Img.bcentrex(bfont,"SELECT LEVEL",screen,2,(255,255,255))
        for n,l in enumerate(lset):
            pygame.draw.rect(screen,(200,200,200),pygame.Rect(0,n*64+66,640,64))
            Img.bcentrex(tfont,"WORLD 1-%s" % (str(l)),screen,n*64+70)
            if l!=maxlevel:
                Img.bcentrex(tfont,"HIGH SCORE: "+str(hss[l-1]),screen,n*64+102,(0,200,0))
        pygame.display.flip()
        clock.tick(60)
    level=[1,lsel]
    world=World.World(level,0 if len(hss)<level[1] else hss[level[1]-1])
    Img.musplay("World1")
    while not world.done:
        world.render_update(screen,pygame.event.get())
        pygame.display.flip()
        clock.tick(60)
    if world.done=="success" and world.nhs:
        hsfile=open("HS.sav","w")
        n=-1
        if level[1]>len(hss):
            hss.append(world.score)
            maxlevel+=1
        else:
            hss[level[1]-1]=world.score
        for n,hs in enumerate(hss):
            hsfile.write(str(hs)+("\n" if n+1<len(hss) else ""))
        hsfile.close()
    pygame.mixer.music.stop()
