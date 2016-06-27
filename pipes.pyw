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
sfont=pygame.font.Font(pdf,16)
pygame.display.set_caption("OpenPipes")
pygame.display.set_icon(Img.img32("PipeX"))
medals={"S":[1500,3000,6000],"M":[2000,5000,9000],"H":[4000,10000,14000]}
medalcolours=[(0,0,0),(127,51,0),(240,240,240),(219,182,0)]
lsel=None
scrolly=0
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
medallevels=[]
while True:
    level=(1,x)
    try:
        testlevel=open(Img.np("levels//%s-%s.sav" % tuple(level)))
        medallevels.append(testlevel.readline()[:1])
        testlevel.close()
        x+=1
    except IOError:
        umax=x-1
        break
while True:
    amedals=[]
    for n,hs in enumerate(hss):
        am=0
        for md in medals[medallevels[n]]:
            if hs>=md:
                am+=1
        amedals.append(am)
    breaking=False
    lset=range(1,(maxlevel if maxlevel<umax else umax)+1)
    while not breaking:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    my=pygame.mouse.get_pos()[1]
                    sel=(my-70+scrolly)//64
                    if 0<=sel<len(lset):
                        lsel=lset[sel]
                        breaking=True
                elif event.button in [4,5]:
                    scrolly+=10 if event.button==5 else -10
                    if scrolly<0:
                        scrolly=0
                    if scrolly>(64+len(lset)*64)-512:
                        scrolly=(64+len(lset)*64)-512
        screen.fill((0, 0, 0))
        if scrolly<64:
            Img.bcentrex(bfont,"SELECT LEVEL",screen,2-scrolly,(255,255,255))
        for n,l in enumerate(lset):
            pygame.draw.rect(screen,(200,200,200),pygame.Rect(0,n*64+64-scrolly,640,64))
            Img.bcentrex(tfont,"WORLD 1-%s" % (str(l)),screen,n*64+68-scrolly)
            if l!=maxlevel:
                Img.bcentrex(tfont,"HIGH SCORE: "+str(hss[l-1]),screen,n*64+100-scrolly,medalcolours[amedals[n]])
                if amedals[n]!=3:
                    Img.bcentrex(sfont,str(medals[medallevels[n]][amedals[n]]),screen,n*64+108-scrolly,medalcolours[amedals[n]+1],200)
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
