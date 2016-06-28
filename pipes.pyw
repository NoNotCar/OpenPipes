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
b1font=pygame.font.Font(pdf,60)
sfont=pygame.font.Font(pdf,16)
pygame.display.set_caption("OpenPipes")
pygame.display.set_icon(Img.img32("PipeX"))
medals={"XS":[1000,2500,4500],"S":[1500,3000,6000],"M":[2000,5000,9000],"H":[4000,10000,14000]}
medalcolours=[(0,0,0),(127,51,0),(240,240,240),(255,255,0)]
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
y=1
medallevels=[]
while True:
    level=(y,x)
    try:
        testlevel=open(Img.np("levels//%s-%s.sav" % tuple(level)))
        medallevels.append(testlevel.readline()[:-1])
        testlevel.close()
        x+=1
        if x==11:
            y+=1
            x=1
    except IOError:
        umax=x-1+(y-1)*10
        break
wsel=1
while True:
    truemax=maxlevel if maxlevel<umax else umax
    wmax=(truemax-1)//10+1
    breaking=False
    scrolly=0
    while not breaking:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    my=pygame.mouse.get_pos()[1]
                    sel=(my-70+scrolly)//64
                    if 0<=sel<wmax:
                        wsel=sel+1
                        breaking=True
                elif event.button in [4,5]:
                    scrolly+=10 if event.button==5 else -10
                    if scrolly>(64+wmax*64)-512:
                        scrolly=(64+wmax*64)-512
                    if scrolly<0:
                        scrolly=0
        screen.fill((0, 0, 0))
        if scrolly<64:
            Img.bcentrex(b1font,"SELECT WORLD",screen,2-scrolly,(255,255,255))
        for n in range(wmax):
            pygame.draw.rect(screen,(200,200,200),pygame.Rect(0,n*64+64-scrolly,640,64))
            Img.bcentrex(bfont,"WORLD %s" % (str(n+1)),screen,n*64+68-scrolly)
        pygame.display.flip()
        clock.tick(60)
    scrolly=0
    while True:
        amedals=[]
        cwsel=wsel-1
        for n,hs in enumerate(hss):
            am=0
            for md in medals[medallevels[n]]:
                if hs>=md:
                    am+=1
            amedals.append(am)
        breaking=False
        lsetmax=(truemax-(wsel-1)*10)+1
        lset=range(1,lsetmax if lsetmax<11 else 11)
        goingout=False
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
                        if scrolly>(64+len(lset)*64)-512:
                            scrolly=(64+len(lset)*64)-512
                        if scrolly<0:
                            scrolly=0
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        breaking=True
                        goingout=True
            screen.fill((0, 0, 0))
            if scrolly<64:
                Img.bcentrex(bfont,"SELECT LEVEL",screen,2-scrolly,(255,255,255))
            for n,l in enumerate(lset):
                pygame.draw.rect(screen,(200,200,200),pygame.Rect(0,n*64+64-scrolly,640,64))
                Img.bcentrex(tfont,"WORLD %s-%s" % (str(wsel),str(l)),screen,n*64+68-scrolly)
                if l+cwsel*10!=maxlevel:
                    Img.bcentrex(tfont,"HIGH SCORE: "+str(hss[l+10*cwsel-1]),screen,n*64+100-scrolly,medalcolours[amedals[n+10*cwsel]])
                    if amedals[n+10*cwsel]!=3:
                        Img.bcentrex(sfont,str(medals[medallevels[n+10*cwsel]][amedals[n+10*cwsel]]),screen,n*64+108-scrolly,medalcolours[amedals[n+10*cwsel]+1],200)
            pygame.display.flip()
            clock.tick(60)
        if goingout:
            break
        level=[wsel,lsel]
        lvl=(level[0]-1)*10 + level[1]
        world=World.World(level,0 if len(hss)<lvl else hss[lvl-1])
        Img.musplay("World2" if world.electric else "World1")
        while not world.done:
            world.render_update(screen,pygame.event.get())
            pygame.display.flip()
            clock.tick(60)
        if world.done=="success" and world.nhs:
            hsfile=open("HS.sav","w")
            n=-1
            if lvl>len(hss):
                hss.append(world.score)
                maxlevel+=1
            else:
                hss[lvl-1]=world.score
            for n,hs in enumerate(hss):
                hsfile.write(str(hs)+("\n" if n+1<len(hss) else ""))
            hsfile.close()
        pygame.mixer.music.stop()
