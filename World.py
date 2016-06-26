import Pipe
import PipeGen
import Img
import pygame
import sys
import Direction as D
import random
pfill=Img.sndget("fill")
exp=Img.sndget("explode")
success=Img.sndget("win")
build=Img.sndget("build")
alarm=Img.sndget("alarm")
pdf=pygame.font.get_default_font()
tfont=pygame.font.Font(pdf,32)
bfont=pygame.font.Font(pdf,64)
floor=Img.img32("Floor")
tt=Img.img("TileTab")
class World(object):
    size=(13,13)
    score=0
    ttgo=3660
    ttflow=0
    fx=0
    fy=0
    nd=(0,1)
    def __init__(self):
        self.objects=[[None]*self.size[1] for _ in range(self.size[0])]
        self.objects[0][0]=Pipe.Source(2)
        self.objects[12][12]=Pipe.Drain(0)
        try:
            hsfile=open("HS.sav")
            self.hs=int(hsfile.readline())
            hsfile.close()
        except IOError:
            self.hs=0
        self.new_pipe()
    def render_update(self,screen,events):
        for e in events:
            if e.type==pygame.QUIT:
                sys.exit()
            elif e.type==pygame.MOUSEBUTTONDOWN:
                if e.button==1:
                    mx,my=pygame.mouse.get_pos()
                    if all([32<=x<14*32 for x in [mx,my]]):
                        mx,my=[x//32-1 for x in [mx,my]]
                        if not self.objects[mx][my]:
                            self.objects[mx][my]=self.nextpipe
                            build.play()
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
                screen.blit(floor,(x*32+32,y*32+32))
                if self.objects[x][y]:
                    screen.blit(self.objects[x][y].get_img(),(x*32+32,y*32+32))
        mx,my=pygame.mouse.get_pos()
        if all([32<=x<14*32 for x in [mx,my]]):
            mx,my=[x//32-1 for x in [mx,my]]
            if not self.objects[mx][my]:
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
            np=self.objects[tx][ty]
            self.nd=D.anti(self.nd)
            if np and self.nd in np.ends:
                np.fill(self.nd)
                if np.name=="Drain":
                    for row in self.objects:
                        for obj in row:
                            if obj and not obj.filled:
                                self.score-=50
                    self.win(screen)
                self.fx=tx
                self.fy=ty
                self.nd=np.get_other_end(self.nd)
                self.score+=100
                if np.name=="XPipe" and np.lfill=="F":
                    self.score+=400
                pfill.play()
            else:
                self.fail(screen)
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
        sys.exit("FOOL")
    def win(self,screen):
        success.play()
        screen.fill((255,255,255))
        Img.bcentre(bfont,"YAY",screen)
        if self.score>self.hs:
            hsfile=open("HS.sav","w")
            hsfile.write(str(self.score))
            hsfile.close()
            Img.bcentre(tfont,"NEW HIGH SCORE: "+str(self.score),screen,100,(0,255,0))
        else:
            Img.bcentre(tfont,"SCORE: "+str(self.score),screen,100)
            Img.bcentre(tfont,"HIGH SCORE: "+str(self.hs),screen,200)
        pygame.display.flip()
        pygame.time.wait(2000)
        sys.exit("success")
