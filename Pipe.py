import Img
import Direction as D
def rload(fil):
    img=Img.img32(fil)
    return Img.imgrot(img)
def rloadf(fil):
    return rload(fil),rload(fil+"F")
class Pipe(object):
    imgs=None
    ends=[]
    filled=False
    name="Pipe"
    def __init__(self,d):
        self.d=d
        self.get_ends(self.d)
    def get_ends(self,d):
        pass
    def get_other_end(self,ed):
        return self.ends[not self.ends.index(ed)]
    def get_img(self):
        return self.imgs[self.filled][self.d]
    def fill(self,ed):
        self.filled=True
class SPipe(Pipe):
    imgs=rloadf("Pipe")
    def get_ends(self,d):
        self.ends=[D.get_dir(d),D.get_dir(d+2)]
class BPipe(Pipe):
    imgs=rloadf("PipeBend")
    def get_ends(self,d):
        self.ends=[D.get_dir(d),D.get_dir(d+1)]
class XPipe(Pipe):
    imgs=[rload("PipeX"+x) for x in ["","T","B","F"]]
    lfill=None
    name="XPipe"
    ends=D.directions
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
class X2Pipe(Pipe):
    imgs=[rload("PipeX2"+x) for x in ["","T","B","F"]]
    lfill=None
    name="XPipe"
    ends=D.directions
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

class Source(Pipe):
    imgs=rloadf("Source")
    def get_otherend(self,ed):
        return D.get_dir(self.d)
class Drain(Pipe):
    img=Img.img32("Drain")
    name="Drain"
    ends=D.directions
    def get_img(self):
        return self.img
