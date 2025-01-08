import framebuf
from random import randint

#@micropython.viper
def RGB(aR: int, aG: int, aB: int ) -> int :
  return (((aG & 0b00011100) << 3) + ((aB & 0b11111000) >> 3) << 8) + (aR & 0b11111000) + ((aG & 0b11100000) >> 5)

def HSV( h:float, s:float, v:float ) -> int :
    (r, g, b) = hsv_to_rgb(h,s,v)
    return RGB(int(r*255), int(b*255), int(g*255))

def hsv_to_rgb( h:float, s:float, v:float ) -> tuple:
    if s:
        if h == 1.0: h = 0.0
        i = int(h*6.0); f = h*6.0 - i
        
        w = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        
        if i==0: return (v, t, w)
        if i==1: return (q, v, w)
        if i==2: return (w, v, t)
        if i==3: return (w, q, v)
        if i==4: return (t, w, v)
        if i==5: return (v, w, q)
    else: return (v, v, v)
    
DEPTH = {
    8: framebuf.GS8,
    4: framebuf.GS4_HMSB,
    2: framebuf.GS2_HMSB,
    1: framebuf.MONO_HLSB,
}

class Spritle(object):
    
    def __init__(self, size, filename=None):
        self.size = size
        self.buffer = bytearray(size)
        self.bufptr = memoryview(self.buffer)
        self.depth = 0
        self.width = 0
        self.height = 0
        self.frames = 0
        self.framesize = 0
        self.current_frame = 0
        self.palette = None
        self.fb = None
        self.trans = 8184
        if filename is not None:
            self.load_sprite(filename)
            
    def load_sprite(self, filename):
        print ("Loading sprite: "+filename)
        with open(filename, 'rb') as f:
            if f.read(3) == b'SPR':
                self.depth = int.from_bytes(f.read(1),'little')
                self.width = int.from_bytes(f.read(2),'little')
                self.height = int.from_bytes(f.read(2),'little')
                self.dataheight = int.from_bytes(f.read(2),'little')
                self.frames = int.from_bytes(f.read(1),'little')
                self.current_frame = self.frames - 1
                if self.palette is None:
                    self.palette = framebuf.FrameBuffer(bytearray((2 ** self.depth) * 2), 2 ** self.depth, 1, framebuf.RGB565)
                print('- '+str(self.width)+'x'+str(self.height)+'x'+str(self.depth)+'bpp  Frames: '+str(self.frames))
                print("- Palette:")
                for i in range(2 ** self.depth):
                    b = int.from_bytes(f.read(1),'little')
                    g = int.from_bytes(f.read(1),'little')
                    r = int.from_bytes(f.read(1),'little')
                    cc = RGB(r,g,b)
                    print('  - '+str(i)+': '+str(r)+' '+str(g)+' '+str(b)+' = '+str(cc))
                    self.palette.pixel(i, 0, cc)
                self.framesize = int(self.width * self.height / (8 / self.depth))
                f.readinto(self.bufptr, self.frames * self.framesize)
                print("- Loaded "+str(self.frames*self.framesize)+"bytes")
                self.fb = None
        return
    
    def blit_framenext(self, fb, x, y):
        self.current_frame = (self.current_frame + 1) % self.frames
        self.fb = framebuf.FrameBuffer(self.bufptr[self.current_frame*self.framesize:(self.current_frame+1)*self.framesize], self.width, self.height, DEPTH[self.depth])
        fb.blit(self.fb, x, y, self.trans, self.palette)
        return

    def blit_framerand(self, fb, x, y):
        rf = randint(0, self.frames - 1)
        self.fb = framebuf.FrameBuffer(self.bufptr[rf*self.framesize:(rf+1)*self.framesize], self.width, self.height, DEPTH[self.depth])
        fb.blit(self.fb, x, y, self.trans, self.palette)
        return
    
    def blit_frameidx(self, fb, x, y, idx=0):
        self.fb = framebuf.FrameBuffer(self.bufptr[idx*self.framesize:(idx+1)*self.framesize], self.width, self.height, DEPTH[self.depth])
        fb.blit(self.fb, x, y, self.trans, self.palette)
        return
