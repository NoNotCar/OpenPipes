import Img
import Direction as D
def rload(fil):
    img=Img.img32(fil)
    return Img.imgrot(img)
def rloadf(fil):
    return rload(fil),rload(fil+"F")
class Pipe(object):
    imgs=None
    cimgs=None
    ends=[]
    filled=False
    name="Pipe"
    symb="P"
    bonus=0
    fixed=False
    def __init__(self,d):
        self.d=d
        self.get_ends(self.d)
    def get_ends(self,d):
        pass
    def get_other_end(self,ed):
        return self.ends[not self.ends.index(ed)]
    def get_img(self):
        return self.imgs[self.filled][self.d]
    def get_cimg(self):
        return self.cimgs[self.filled][self.d]
    def fill(self,ed):
        self.filled=True
class SPipe(Pipe):
    imgs=rloadf("Pipe")
    cimgs = rloadf("Cable")
    symb = "SP"
    def get_ends(self,d):
        self.ends=[D.get_dir(d),D.get_dir(d+2)]
class BPipe(Pipe):
    imgs=rloadf("PipeBend")
    cimgs = rloadf("CableBend")
    symb = "BP"
    def get_ends(self,d):
        self.ends=[D.get_dir(d),D.get_dir(d+1)]
class XPipe(Pipe):
    imgs=[rload("PipeX"+x) for x in ["","T","B","F"]]
    cimgs=[rload("CableX"+x) for x in ["","T","B","F"]]
    lfill=None
    name="XPipe"
    ends=D.directions
    symb = "XP"
    def get_other_end(self,ed):
        return D.anti(ed)
    def fill(self,ed):
        self.filled=True
        if self.lfill:
            self.lfill="F"
        else:
            fhoz=ed in D.hoz
            self.ends=D.vert if fhoz else D.hoz
            self.lfill="B" if fhoz!=self.d%2 else "T"
    def get_img(self):
        x=3 if self.lfill=="F" else 2 if self.lfill=="B" else 1 if self.lfill=="T" else 0
        return self.imgs[x][self.d]
    def get_cimg(self):
        x=3 if self.lfill=="F" else 2 if self.lfill=="B" else 1 if self.lfill=="T" else 0
        return self.cimgs[x][self.d]
class X2Pipe(Pipe):
    imgs=[rload("PipeX2"+x) for x in ["","T","B","F"]]
    cimgs=[rload("CableX2"+x) for x in ["","T","B","F"]]
    lfill=None
    name="XPipe"
    ends=D.directions
    symb = "2XP"
    def get_other_end(self,ed):
        return D.rotdir(ed,1 if self.d%2==D.index(ed)%2 else -1)
    def fill(self,ed):
        self.filled=True
        if self.lfill:
            self.lfill="F"
        else:
            self.ends=list(D.directions)
            self.ends.remove(ed)
            self.ends.remove(self.get_other_end(ed))
            self.ends=tuple(self.ends)
            self.lfill="T" if D.index(ed) in [self.d,(self.d+1)%4] else "B"
    def get_img(self):
        x=3 if self.lfill=="F" else 2 if self.lfill=="B" else 1 if self.lfill=="T" else 0
        return self.imgs[x][self.d]
    def get_cimg(self):
        x=3 if self.lfill=="F" else 2 if self.lfill=="B" else 1 if self.lfill=="T" else 0
        return self.cimgs[x][self.d]

class Source(Pipe):
    symb = "S"
    imgs=rloadf("Source")
    cimgs=rloadf("CableSource")
    def get_otherend(self,ed):
        return D.get_dir(self.d)
class Drain(Pipe):
    symb = "D"
    img=Img.img32("Drain")
    cimgs=rloadf("CableDrain")
    name="Drain"
    ends=D.directions
    def get_img(self):
        return self.img
class Block(Pipe):
    img=Img.img32("Block")
    cimg=Img.img32("EBlock")
    symb = "B"
    def get_img(self):
        return self.img
    def get_cimg(self):
        return self.cimg
class GoldPipe(SPipe):
    bonus=900
    symb = "GP"
    imgs=rload("PipeGold")
    cimgs=rload("CableGold")
    def get_img(self):
        return SPipe.imgs[1][self.d] if self.filled else self.imgs[self.d]
    def get_cimg(self):
        return SPipe.cimgs[1][self.d] if self.filled else self.cimgs[self.d]
class OWPipe(Pipe):
    imgs=rloadf("OWPipe")
    cimgs=rloadf("Diode")
    bonus = 200
    symb = "OW"
    def get_ends(self,d):
        self.ends=[D.get_dir(d)]
    def get_other_end(self,ed):
        return D.anti(ed)
class Resevoir(Pipe):
    cimgs=[rload("CableR"+str(n)) for n in range(8)]
    imgs=cimgs
    filllevel=0
    bonus=400
    name="Resevoir"
    symb = "R"
    def get_ends(self,d):
        self.ends=[D.get_dir(d),D.get_dir(d+2)]
    def get_other_end(self,ed):
        if D.get_dir(self.d)!=ed:
            self.d=D.index(ed)
        return D.anti(ed)
    def get_cimg(self):
        return self.cimgs[self.filllevel][self.d]
    def get_img(self):
        return self.imgs[self.filllevel][self.d]
class TeleportB(Pipe):
    cimgs = rloadf("Teleport1")
    imgs=cimgs
    bonus=400
    name="Teleport"
    ttype=0
    symb = "TP1"
    def get_ends(self,d):
        self.ends=[D.get_dir(d)]
class TeleportO(TeleportB):
    cimgs=rloadf("Teleport2")
    imgs=cimgs
    ttype = 1
    symb = "TP2"
class OPipe(Pipe):
    cimgs=rloadf("CableOut")
    imgs=cimgs
    symb = "OP"
    name = "OutPipe"
    def get_ends(self,d):
        self.ends=[D.get_dir(d),D.get_dir(d+2)]

