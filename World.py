import Pipe
import PipeGen
import Img
import pygame
import sys
import Direction as D
import random
pfill=Img.sndget("fill")
exp=Img.sndget("explode")
bexp=Img.sndget("bigexp")
success=Img.sndget("win")
build=Img.sndget("build")
alarm=Img.sndget("alarm")
pdf=pygame.font.get_default_font()
tfont=pygame.font.Font(pdf,32)
bfont=pygame.font.Font(pdf,64)
floor=Img.img32("Floor")
ffloor=Img.img32("FloorFixed")
tt=Img.img("TileTab")
sel=Img.img32("Sel")
editorclasses=[Pipe.Source,Pipe.Drain,Pipe.Block,Pipe.GoldPipe,Pipe.SPipe,Pipe.BPipe,Pipe.XPipe,Pipe.X2Pipe]
class World(object):
    size=(13,13)
    score=0
    ttgo=3660
    ttflow=0
    fx=0
    fy=0
    nd=(0,1)
    done=False
    def __init__(self,level,hs):
        self.objects=[[None]*self.size[1] for _ in range(self.size[0])]
        lfile=open(Img.np("levels//%s-%s.sav" % tuple(level)))
        llines=lfile.readlines()
        for x,row in enumerate(llines):
            for y,n in enumerate(row.split()):
                if n!="0":
                    obj=n.split(":")
                    for c in editorclasses:
                        if c.symb==obj[0]:
                            newobj=c(int(obj[1]))
                            newobj.fixed=True
                            self.objects[x][y]=newobj
                            if obj[0]=="S":
                                self.fx=x
                                self.fy=y
                                self.nd=D.get_dir(int(obj[1]))
        self.hs=hs
        self.new_pipe()
        self.level=level
        self.nhs=None
    def render_update(self,screen,events):
        for e in events:
            if e.type==pygame.QUIT:
                sys.exit()
            elif e.type==pygame.MOUSEBUTTONDOWN:
                if e.button==1:
                    mx,my=pygame.mouse.get_pos()
                    if all([32<=x<14*32 for x in [mx,my]]):
                        mx,my=[x//32-1 for x in [mx,my]]
                        obj=self.objects[mx][my]
                        if obj:
                            if obj.fixed:
                                continue
                            self.score-=100
                            bexp.play()
                        else:
                            build.play()
                        self.objects[mx][my]=self.nextpipe
                        self.new_pipe()
                elif e.button==3:
                    self.score-=25
                    exp.play()
                    self.new_pipe()
        screen.fill((200,200,200))
        keys=pygame.key.get_pressed()
        speed=keys[pygame.K_LSHIFT]
        for x in range(13):
            for y in range(13):
                obj=self.objects[x][y]
                screen.blit(ffloor if obj and obj.fixed else floor,(x*32+32,y*32+32))
                if self.objects[x][y]:
                    screen.blit(self.objects[x][y].get_img(),(x*32+32,y*32+32))
        mx,my=pygame.mouse.get_pos()
        if all([32<=x<14*32 for x in [mx,my]]):
            mx,my=[x//32-1 for x in [mx,my]]
            screen.blit(self.nimg,(mx*32+32,my*32+32))
        if self.ttgo>0:
            self.ttgo-=10 if speed else 1
            Img.bcentrex(tfont,str(self.ttgo//60),screen,464)
            if not self.ttgo:
                self.ttflow=10 if speed else 120
                self.objects[self.fx][self.fy].filled=True
                alarm.play()
        elif self.ttflow>0:
            self.ttflow-=10 if speed else 1
        else:
            self.ttflow=120
            tx=self.fx+self.nd[0]
            ty=self.fy+self.nd[1]
            if not (0<=tx<13 and 0<=ty<13):
                self.fail(screen)
                return None
            np=self.objects[tx][ty]
            self.nd=D.anti(self.nd)
            if np and self.nd in np.ends:
                np.fill(self.nd)
                if np.name=="Drain":
                    for row in self.objects:
                        for obj in row:
                            if obj and not obj.filled and obj.ends and not obj.fixed:
                                self.score-=50
                    self.win(screen)
                    return None
                self.fx=tx
                self.fy=ty
                self.nd=np.get_other_end(self.nd)
                self.score+=100+np.bonus
                if np.name=="XPipe" and np.lfill=="F":
                    self.score+=400
                pfill.play()
            else:
                self.fail(screen)
                return None
        screen.blit(tt,(0,448))
        screen.blit(self.nextpipe.get_img(),(16,464))
        Img.bcentrex(tfont,"SCORE: "+str(self.score),screen,0,(0,0,0) if self.score>=0 else (255,0,0))
    def new_pipe(self):
        self.nextpipe=PipeGen.get_pipe()(random.randint(0,3))
        self.nimg=self.nextpipe.get_img().copy()
        self.nimg.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)
    def fail(self,screen):
        screen.fill((0,0,0))
        Img.bcentre(bfont,"FOOL",screen,col=(255,255,255))
        pygame.display.flip()
        pygame.time.wait(2000)
        self.done="fail"
    def win(self,screen):
        success.play()
        screen.fill((255,255,255))
        Img.bcentre(bfont,"YAY",screen)
        if self.score>self.hs:
            self.nhs=True
            Img.bcentre(tfont,"NEW HIGH SCORE: "+str(self.score),screen,100,(0,255,0))
        else:
            Img.bcentre(tfont,"SCORE: "+str(self.score),screen,100)
            Img.bcentre(tfont,"HIGH SCORE: "+str(self.hs),screen,200)
        pygame.display.flip()
        pygame.time.wait(2000)
        self.done="success"
class EditWorld(object):
    size=(13,13)
    score=0
    ttgo=3660
    ttflow=0
    fx=0
    fy=0
    nd=(0,1)
    def __init__(self):
        self.objects=[[None]*self.size[1] for _ in range(self.size[0])]
        self.sel=0
        self.objlist=[x(0) for x in editorclasses]
    def render_update(self,screen,events):
        keys=pygame.key.get_pressed()
        deleting=keys[pygame.K_LSHIFT]
        for e in events:
            if e.type==pygame.QUIT:
                sys.exit()
            elif e.type==pygame.MOUSEBUTTONDOWN:
                if e.button==1:
                    mx,my=pygame.mouse.get_pos()
                    if all([32<=x<14*32 for x in [mx,my]]):
                        mx,my=[x//32-1 for x in [mx,my]]
                        if deleting:
                            self.objects[mx][my]=None
                        else:
                            self.objects[mx][my]=editorclasses[self.sel](self.objlist[self.sel].d)
                    elif my>=480 and mx<len(self.objlist)*32:
                        self.sel=mx//32
                if e.button==3:
                    self.objlist[self.sel].d=(self.objlist[self.sel].d+1)%4
            elif e.type==pygame.KEYDOWN and e.key==pygame.K_s:
                save=open("levels/save.sav","w")
                for row in self.objects:
                    save.write(" ".join([self.objconv(o) for o in row]) + "\n")
                save.close()
                sys.exit()
        screen.fill((200,200,200))
        for x in range(13):
            for y in range(13):
                screen.blit(floor,(x*32+32,y*32+32))
                if self.objects[x][y]:
                    screen.blit(self.objects[x][y].get_img(),(x*32+32,y*32+32))
        for n,o in enumerate(self.objlist):
            screen.blit(o.get_img(),(n*32,480))
            if n==self.sel:
                screen.blit(sel,(n*32,480))
    def objconv(self,obj):
        if obj is None:
            return "0"
        return obj.symb+":"+str(obj.d)
